# static_checks.py
"""
Ren'Py Static Analysis Checkers:
1. Asset Integrity & Case-Sensitivity Checker
2. Save & Rollback Bug Detector
3. Call Stack Growth & Jump vs Call Flow Checker
4. Label Indentation Checker
5. Init Declarations in Labels Checker
6. Defaulted Variables in Style Definitions Checker
7. Defaulted/Global Variables in Transform Definitions Checker
"""

import os
import re
import sys
from dataclasses import dataclass
from typing import List, Dict, Set, Optional, Tuple


@dataclass
class CheckIssue:
    file: str
    line: int
    checker: str  # "asset-check", "rollback-check", "flow-check", "indentation-check", "label-decl-check", "style-var-check", "transform-var-check"
    issue_type: str
    message: str
    suggestion: str
    code_snippet: str = ""


# Common file extensions for assets in Ren'Py projects
ASSET_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp", ".gif",
    ".ogg", ".mp3", ".wav", ".opus", ".flac",
    ".ttf", ".otf",
    ".webm", ".ogv", ".mp4"
}

# Built-in assets provided directly by the Ren'Py SDK runtime container
RENPY_BUILTIN_ASSETS = {
    "dejavusans.ttf",
    "dejavusans-bold.ttf",
    "dejavusans-oblique.ttf",
}

# Regex to find quoted string literals
STRING_LITERAL_REGEX = re.compile(r'["\']([^"\']+)["\']')

# Keywords/prefixes that indicate safe configuration/library assignments in init python
SAFE_ASSIGNMENT_PREFIXES = (
    "config.", "gui.", "style.", "persistent.", "renpy.", "store.", "_", "bubble."
)

DECLARATION_KEYWORDS = (
    "define", "default", "transform", "style", "image", "screen", "init"
)

# Top-level Ren'Py construct declarations that terminate previous block scopes
TOP_LEVEL_CONSTRUCT_REGEX = re.compile(
    r'^\s*(label|menu|screen|testsuite|init|define|default|transform|style|image|python|translate|layeredimage)\b'
)



def _should_ignore(line_content: str, checker_name: str) -> bool:
    """Checks if a script line contains an inline noqa ignore directive."""
    if "#" not in line_content:
        return False
    comment = line_content.split("#", 1)[1].lower().strip()
    if "noqa" in comment:
        if "noqa" == comment or "noqa:" not in comment:
            return True
        if checker_name in comment:
            return True
    if f"{checker_name}: ignore" in comment or f"{checker_name}:ignore" in comment:
        return True
    return False


def _collect_rpy_files(project_dir: str) -> List[Tuple[str, str]]:
    """Helper to collect all .rpy files under project game/ directory. Returns list of (full_path, rel_path)."""
    if os.path.basename(project_dir).lower() == "game" or os.path.exists(os.path.join(project_dir, "script.rpy")):
        game_dir = project_dir
        base_dir = os.path.dirname(project_dir)
    else:
        game_dir = os.path.join(project_dir, "game") if os.path.exists(os.path.join(project_dir, "game")) else project_dir
        base_dir = project_dir

    if not os.path.exists(game_dir):
        return []
    results = []
    for root, _, files in os.walk(game_dir):
        for file in files:
            if file.endswith(".rpy") and not file.endswith(".rpyc"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir).replace("\\", "/")
                results.append((full_path, rel_path))
    return results


def check_asset_integrity(project_dir: str) -> List[CheckIssue]:
    """
    Scans .rpy script files for image/audio references and verifies that
    referenced files exist on disk with exact case-sensitive matching.
    """
    issues: List[CheckIssue] = []
    game_dir = os.path.join(project_dir, "game")
    if not os.path.exists(game_dir):
        return issues

    exact_files: Set[str] = set()
    lower_files: Dict[str, str] = {}

    for root, _, files in os.walk(game_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, game_dir).replace("\\", "/")
            exact_files.add(rel_path)
            lower_files[rel_path.lower()] = rel_path

    for full_path, rel_script_path in _collect_rpy_files(project_dir):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            continue

        for line_idx, line in enumerate(lines, start=1):
            if _should_ignore(line, "asset-check"):
                continue

            code_part = line.split("#", 1)[0] if "#" in line else line
            matches = STRING_LITERAL_REGEX.findall(code_part)

            for ref in matches:
                ref_str = ref.strip()
                if not ref_str or ref_str.startswith(("http://", "https://", "font/")):
                    continue
                if ref_str.lower() in RENPY_BUILTIN_ASSETS:
                    continue
                if "[" in ref_str or "]" in ref_str or "%" in ref_str or "{" in ref_str:
                    continue

                clean_ref = ref_str.lstrip("/")
                if clean_ref.startswith("game/"):
                    clean_ref = clean_ref[5:]

                _, ext = os.path.splitext(clean_ref)
                ext_lower = ext.lower()

                is_asset_path = (
                    clean_ref.startswith(("images/", "audio/", "gui/", "fonts/", "movies/"))
                    or ext_lower in ASSET_EXTENSIONS
                )

                if not is_asset_path:
                    continue

                candidates = [clean_ref]
                if not clean_ref.startswith(("images/", "audio/", "gui/", "fonts/", "movies/")):
                    if ext_lower in {".ogg", ".mp3", ".wav", ".opus", ".flac"}:
                        candidates.append(f"audio/{clean_ref}")
                    elif ext_lower in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
                        candidates.append(f"images/{clean_ref}")
                        candidates.append(f"gui/{clean_ref}")

                matched_exact = False
                matched_case_mismatch: Optional[Tuple[str, str]] = None

                for cand in candidates:
                    if cand in exact_files:
                        matched_exact = True
                        break
                    elif cand.lower() in lower_files:
                        matched_case_mismatch = (cand, lower_files[cand.lower()])

                if matched_exact:
                    continue

                if matched_case_mismatch:
                    _, actual_on_disk = matched_case_mismatch
                    issues.append(CheckIssue(
                        file=rel_script_path,
                        line=line_idx,
                        checker="asset-check",
                        issue_type="case_mismatch",
                        message=f"Case sensitivity mismatch: '{ref_str}' referenced in script, but file on disk is '{actual_on_disk}'.",
                        suggestion=f"Change script reference to match exact disk casing: '{actual_on_disk}'.",
                        code_snippet=line.strip()
                    ))
                else:
                    issues.append(CheckIssue(
                        file=rel_script_path,
                        line=line_idx,
                        checker="asset-check",
                        issue_type="missing_asset",
                        message=f"Missing asset file: '{ref_str}' does not exist under 'game/'.",
                        suggestion=f"Verify file path or place asset at 'game/{clean_ref}'.",
                        code_snippet=line.strip()
                    ))

    return issues


def check_save_rollback(project_dir: str) -> List[CheckIssue]:
    """
    Scans .rpy files for dynamic state variables initialized inside init python:
    or init: blocks via standard assignment (var = ...) instead of Ren'Py's default keyword.
    """
    issues: List[CheckIssue] = []
    ASSIGNMENT_REGEX = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(=|\+=|-=|\*=|/=)\s*[^=]')

    for full_path, rel_script_path in _collect_rpy_files(project_dir):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            continue

        in_init_python = False
        init_indent = 0
        child_indent: Optional[int] = None

        for line_idx, line in enumerate(lines, start=1):
            if _should_ignore(line, "rollback-check"):
                continue

            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            current_indent = len(line) - len(line.lstrip(" "))

            if re.match(r'^\s*init\s*(\d+)?\s*(python)?:', line):
                in_init_python = True
                init_indent = current_indent
                child_indent = None
                continue

            if in_init_python:
                if current_indent <= init_indent:
                    in_init_python = False
                    child_indent = None
                    continue

                if child_indent is None:
                    child_indent = current_indent

                if current_indent == child_indent:
                    if stripped.startswith((
                        "class ", "def ", "import ", "from ", "pass", "@", "return",
                        "try:", "except", "finally:", "if ", "elif ", "else:", "for ", "while "
                    )):
                        continue

                    match = ASSIGNMENT_REGEX.match(line)
                    if match:
                        var_name = match.group(1)

                        if (
                            var_name.isupper()
                            or var_name.startswith(SAFE_ASSIGNMENT_PREFIXES)
                            or var_name.startswith("__")
                            or var_name in ("__all__", "build", "config", "gui")
                        ):
                            continue

                        issues.append(CheckIssue(
                            file=rel_script_path,
                            line=line_idx,
                            checker="rollback-check",
                            issue_type="rollback_state_assignment",
                            message=f"Dynamic state variable '{var_name}' initialized inside init python block. "
                                    f"Variables declared inside init python are not saved or tracked for rollback.",
                            suggestion=f"Move declaration outside init python and use 'default {var_name} = ...'.",
                            code_snippet=stripped
                        ))

    return issues


def check_call_stack_flow(project_dir: str) -> List[CheckIssue]:
    """
    Detects potential call stack overflow risks and improper call vs jump usage:
    - Calls to labels that end without a return statement or jump away without returning.
    - Labels calling each other in loops without returns.
    """
    issues: List[CheckIssue] = []

    label_info: Dict[str, dict] = {}
    label_def_regex = re.compile(r'^\s*label\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(\([^)]*\))?\s*:')
    call_regex = re.compile(r'\bcall\s+([a-zA-Z_][a-zA-Z0-9_]*)')
    jump_regex = re.compile(r'\bjump\s+([a-zA-Z_][a-zA-Z0-9_]*)')

    for full_path, rel_script_path in _collect_rpy_files(project_dir):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            continue

        current_label: Optional[str] = None
        current_indent = 0

        for line_idx, line in enumerate(lines, start=1):
            if _should_ignore(line, "flow-check"):
                continue

            code_part = line.split("#", 1)[0]
            stripped = code_part.strip()
            if not stripped:
                continue

            indent = len(line) - len(line.lstrip(" "))
            label_match = label_def_regex.match(code_part)

            if label_match:
                current_label = label_match.group(1)
                current_indent = indent
                label_info[current_label] = {
                    "file": rel_script_path,
                    "line": line_idx,
                    "calls": [],
                    "jumps": [],
                    "has_return": False,
                    "snippet": line.strip()
                }
                continue

            if current_label:
                if indent <= current_indent and TOP_LEVEL_CONSTRUCT_REGEX.match(code_part):
                    current_label = None
                    continue

                if "return" in stripped.split():
                    label_info[current_label]["has_return"] = True

                for cm in call_regex.finditer(code_part):
                    label_info[current_label]["calls"].append((cm.group(1), line_idx, line.strip()))

                for jm in jump_regex.finditer(code_part):
                    label_info[current_label]["jumps"].append((jm.group(1), line_idx, line.strip()))

    for caller, data in label_info.items():
        for target, line_num, snippet in data["calls"]:
            if target in label_info:
                target_data = label_info[target]
                if not target_data["has_return"]:
                    jumps_to_caller = any(j[0] == caller for j in target_data["jumps"])
                    if jumps_to_caller or not target_data["has_return"]:
                        issues.append(CheckIssue(
                            file=data["file"],
                            line=line_num,
                            checker="flow-check",
                            issue_type="call_without_return",
                            message=f"Label '{target}' is invoked with 'call', but label '{target}' does not contain a 'return' statement. "
                                    f"This causes call stack accumulation (~200 call limit) until error.",
                            suggestion=f"Use 'jump {target}' instead of 'call {target}', or add a 'return' statement inside label '{target}'.",
                            code_snippet=snippet
                        ))

    return issues


def check_label_indentation(project_dir: str) -> List[CheckIssue]:
    """
    Detects code statements inside label blocks that are unindented (placed at column 0).
    """
    issues: List[CheckIssue] = []
    label_header_regex = re.compile(r'^\s*label\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(\([^)]*\))?\s*:')

    for full_path, rel_script_path in _collect_rpy_files(project_dir):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            continue

        in_label = False
        current_label = ""
        label_indent = 0

        for line_idx, line in enumerate(lines, start=1):
            if _should_ignore(line, "indentation-check"):
                continue

            code_part = line.split("#", 1)[0]
            stripped = code_part.strip()
            if not stripped:
                continue

            indent = len(line) - len(line.lstrip(" "))
            label_match = label_header_regex.match(code_part)

            if label_match:
                lbl_name = label_match.group(1)
                if lbl_name != "_":
                    in_label = True
                    current_label = lbl_name
                    label_indent = indent
                else:
                    in_label = False
                continue

            if in_label:
                if indent <= label_indent:
                    if TOP_LEVEL_CONSTRUCT_REGEX.match(code_part):
                        in_label = False
                        continue
                    if not stripped.startswith("#"):
                        issues.append(CheckIssue(
                            file=rel_script_path,
                            line=line_idx,
                            checker="indentation-check",
                            issue_type="unindented_label_statement",
                            message=f"Statement under label '{current_label}' has no indentation. Statements inside a label must be indented.",
                            suggestion=f"Indent the statement under label '{current_label}'.",
                            code_snippet=stripped
                        ))
                    in_label = False
                    continue

    return issues


def check_label_declarations(project_dir: str) -> List[CheckIssue]:
    """
    Detects init-time declarations (define, default, transform, style, image, screen, init)
    erroneously placed inside label blocks.
    """
    issues: List[CheckIssue] = []
    label_header_regex = re.compile(r'^\s*label\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(\([^)]*\))?\s*:')
    decl_regex = re.compile(r'^\s*(define|default|transform|style|image|screen|init)\b')

    for full_path, rel_script_path in _collect_rpy_files(project_dir):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            continue

        in_label = False
        current_label = ""
        label_indent = 0

        for line_idx, line in enumerate(lines, start=1):
            if _should_ignore(line, "label-decl-check"):
                continue

            code_part = line.split("#", 1)[0]
            stripped = code_part.strip()
            if not stripped:
                continue

            indent = len(line) - len(line.lstrip(" "))
            label_match = label_header_regex.match(code_part)

            if label_match:
                lbl_name = label_match.group(1)
                if lbl_name != "_":
                    in_label = True
                    current_label = lbl_name
                    label_indent = indent
                else:
                    in_label = False
                continue

            if in_label:
                if indent <= label_indent:
                    in_label = False
                    continue

                decl_match = decl_regex.match(code_part)
                if decl_match:
                    kw = decl_match.group(1)
                    issues.append(CheckIssue(
                        file=rel_script_path,
                        line=line_idx,
                        checker="label-decl-check",
                        issue_type="declaration_inside_label",
                        message=f"Init-time declaration '{kw}' placed inside label '{current_label}'. "
                                f"Ren'Py executes '{kw}' only at init time, NOT when label '{current_label}' runs during play.",
                        suggestion=f"Move '{kw}' declaration outside of label '{current_label}' to script top level, or use python assignment ('$ var = val') inside labels.",
                        code_snippet=stripped
                    ))

    return issues


def check_style_variables(project_dir: str) -> List[CheckIssue]:
    """
    Detects defaulted variables referenced inside style definitions.
    Style definitions are only evaluated at init time and won't reflect dynamic variable changes.
    """
    issues: List[CheckIssue] = []

    defaulted_vars: Set[str] = set()
    default_regex = re.compile(r'^\s*default\s+([a-zA-Z_][a-zA-Z0-9_]*)')

    for full_path, _ in _collect_rpy_files(project_dir):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    m = default_regex.match(line)
                    if m:
                        defaulted_vars.add(m.group(1))
        except OSError:
            continue

    if not defaulted_vars:
        return issues

    style_def_regex = re.compile(r'^\s*style\s+([a-zA-Z0-9_]+)')
    style_assign_regex = re.compile(r'^\s*style\.([a-zA-Z0-9_.]+)\.([a-zA-Z0-9_]+)\s*=\s*(.+)')

    for full_path, rel_script_path in _collect_rpy_files(project_dir):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            continue

        in_style_block = False
        style_indent = 0
        style_name = ""

        for line_idx, line in enumerate(lines, start=1):
            if _should_ignore(line, "style-var-check"):
                continue

            code_part = line.split("#", 1)[0]
            stripped = code_part.strip()
            if not stripped:
                continue

            indent = len(line) - len(line.lstrip(" "))
            style_match = style_def_regex.match(code_part)

            if style_match:
                in_style_block = True
                style_name = style_match.group(1)
                style_indent = indent
                continue

            if in_style_block:
                if indent <= style_indent and not stripped.startswith("#"):
                    in_style_block = False
                else:
                    tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code_part)
                    for tok in tokens:
                        if tok in defaulted_vars:
                            issues.append(CheckIssue(
                                file=rel_script_path,
                                line=line_idx,
                                checker="style-var-check",
                                issue_type="defaulted_var_in_style",
                                message=f"Style '{style_name}' references defaulted variable '{tok}'. "
                                        f"Styles are evaluated ONCE at init time and will NOT update when '{tok}' changes at runtime.",
                                suggestion=f"Use static values or dynamic screen properties instead of referencing defaulted variable '{tok}' in style definition.",
                                code_snippet=stripped
                            ))

            assign_match = style_assign_regex.match(code_part)
            if assign_match:
                s_name = assign_match.group(1)
                expr = assign_match.group(3)
                tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expr)
                for tok in tokens:
                    if tok in defaulted_vars:
                        issues.append(CheckIssue(
                            file=rel_script_path,
                            line=line_idx,
                            checker="style-var-check",
                            issue_type="defaulted_var_in_style",
                            message=f"Style property assignment for '{s_name}' references defaulted variable '{tok}'. "
                                    f"Styles are evaluated ONCE at init time and will NOT update when '{tok}' changes at runtime.",
                            suggestion=f"Use static values or dynamic screen properties instead of referencing defaulted variable '{tok}' in style assignment.",
                            code_snippet=stripped
                        ))

    return issues


def check_transform_variables(project_dir: str) -> List[CheckIssue]:
    """
    Detects defaulted or global variables used inside transform definitions
    when not explicitly passed into the transform as parameters.
    """
    issues: List[CheckIssue] = []

    defaulted_vars: Set[str] = set()
    default_regex = re.compile(r'^\s*default\s+([a-zA-Z_][a-zA-Z0-9_]*)')

    for full_path, _ in _collect_rpy_files(project_dir):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    m = default_regex.match(line)
                    if m:
                        defaulted_vars.add(m.group(1))
        except OSError:
            continue

    if not defaulted_vars:
        return issues

    transform_header_regex = re.compile(r'^\s*transform\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(\(([^)]*)\))?\s*:')

    for full_path, rel_script_path in _collect_rpy_files(project_dir):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            continue

        in_transform = False
        transform_name = ""
        transform_indent = 0
        params: Set[str] = set()

        for line_idx, line in enumerate(lines, start=1):
            if _should_ignore(line, "transform-var-check"):
                continue

            code_part = line.split("#", 1)[0]
            stripped = code_part.strip()
            if not stripped:
                continue

            indent = len(line) - len(line.lstrip(" "))
            t_match = transform_header_regex.match(code_part)

            if t_match:
                in_transform = True
                transform_name = t_match.group(1)
                transform_indent = indent
                raw_params = t_match.group(3) or ""
                params = {p.strip().split("=")[0].strip() for p in raw_params.split(",") if p.strip()}
                continue

            if in_transform:
                if indent <= transform_indent and not stripped.startswith("#"):
                    in_transform = False
                else:
                    tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code_part)
                    for tok in tokens:
                        if tok in defaulted_vars and tok not in params:
                            issues.append(CheckIssue(
                                file=rel_script_path,
                                line=line_idx,
                                checker="transform-var-check",
                                issue_type="global_var_in_transform",
                                message=f"Transform '{transform_name}' references defaulted variable '{tok}' without taking it as a parameter. "
                                        f"Transforms evaluate non-parameter variables at init time.",
                                suggestion=f"Pass '{tok}' as a parameter (e.g., 'transform {transform_name}({tok}):') to evaluate its dynamic runtime value.",
                                code_snippet=stripped
                            ))

    return issues


def check_image_paths(project_dir: str) -> List[CheckIssue]:
    """
    Verifies that all image paths referenced in script sources (via image declarations,
    scene/show statements, gui assignments, or image file string literals) exist on disk
    with exact case-sensitive matching.
    """
    issues: List[CheckIssue] = []

    if os.path.basename(project_dir).lower() == "game" or os.path.exists(os.path.join(project_dir, "script.rpy")):
        game_dir = project_dir
    else:
        game_dir = os.path.join(project_dir, "game") if os.path.exists(os.path.join(project_dir, "game")) else project_dir

    if not os.path.exists(game_dir):
        return issues

    exact_files: Set[str] = set()
    lower_files: Dict[str, str] = {}

    for root, _, files in os.walk(game_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, game_dir).replace("\\", "/")
            exact_files.add(rel_path)
            lower_files[rel_path.lower()] = rel_path

    image_exts = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    image_stmt_regex = re.compile(
        r'(?:image\s+.*=\s*|scene\s+|show\s+|show\s+expression\s+|image\s+|gui\.[a-zA-Z0-9_]+\s*=\s*)["\']([^"\']+)["\']',
        re.IGNORECASE
    )

    for full_path, rel_script_path in _collect_rpy_files(project_dir):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            continue

        for line_idx, line in enumerate(lines, start=1):
            if _should_ignore(line, "image-check"):
                continue

            code_part = line.split("#", 1)[0] if "#" in line else line

            candidates_ref: List[str] = []

            for m in image_stmt_regex.finditer(code_part):
                ref = m.group(1).strip()
                if ref:
                    candidates_ref.append(ref)

            for str_match in STRING_LITERAL_REGEX.findall(code_part):
                ref = str_match.strip()
                _, ext = os.path.splitext(ref)
                if ext.lower() in image_exts or ref.startswith(("images/", "gui/")):
                    if ref not in candidates_ref:
                        candidates_ref.append(ref)

            for ref_str in candidates_ref:
                if not ref_str or ref_str.startswith(("http://", "https://", "font/")):
                    continue
                if ref_str.lower() in RENPY_BUILTIN_ASSETS:
                    continue
                if "[" in ref_str or "]" in ref_str or "%" in ref_str or "{" in ref_str:
                    continue

                clean_ref = ref_str.lstrip("/")
                if clean_ref.startswith("game/"):
                    clean_ref = clean_ref[5:]

                _, ext = os.path.splitext(clean_ref)
                ext_lower = ext.lower()

                if not ext_lower and not clean_ref.startswith(("images/", "gui/")):
                    continue

                cands = [clean_ref]
                if not clean_ref.startswith(("images/", "gui/")):
                    cands.append(f"images/{clean_ref}")
                    cands.append(f"gui/{clean_ref}")

                matched_exact = False
                matched_case_mismatch: Optional[Tuple[str, str]] = None

                for cand in cands:
                    if cand in exact_files:
                        matched_exact = True
                        break
                    elif cand.lower() in lower_files:
                        matched_case_mismatch = (cand, lower_files[cand.lower()])

                if matched_exact:
                    continue

                if matched_case_mismatch:
                    _, actual_on_disk = matched_case_mismatch
                    issues.append(CheckIssue(
                        file=rel_script_path,
                        line=line_idx,
                        checker="image-check",
                        issue_type="image_case_mismatch",
                        message=f"Image case sensitivity mismatch: '{ref_str}' referenced in script, but file on disk is '{actual_on_disk}'.",
                        suggestion=f"Change image path reference to match exact disk casing: '{actual_on_disk}'.",
                        code_snippet=line.strip()
                    ))
                else:
                    issues.append(CheckIssue(
                        file=rel_script_path,
                        line=line_idx,
                        checker="image-check",
                        issue_type="missing_image",
                        message=f"Missing image asset file: '{ref_str}' referenced in script does not exist under 'game/'.",
                        suggestion=f"Verify file path or place image asset at 'game/{clean_ref}'.",
                        code_snippet=line.strip()
                    ))

    return issues


def run_all_checks(project_dir: str) -> List[CheckIssue]:
    """Runs all static checks and returns aggregated issue list."""
    issues = []
    issues.extend(check_asset_integrity(project_dir))
    issues.extend(check_image_paths(project_dir))
    issues.extend(check_save_rollback(project_dir))
    issues.extend(check_call_stack_flow(project_dir))
    issues.extend(check_label_indentation(project_dir))
    issues.extend(check_label_declarations(project_dir))
    issues.extend(check_style_variables(project_dir))
    issues.extend(check_transform_variables(project_dir))
    return issues


if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    all_issues = run_all_checks(target_dir)
    print(f"Found {len(all_issues)} issue(s).")
    for issue in all_issues:
        print(f"[{issue.checker}] {issue.file}:{issue.line} - {issue.message}")

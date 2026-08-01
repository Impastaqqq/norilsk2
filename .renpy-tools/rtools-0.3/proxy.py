# .renpy-tools/proxy.py
import datetime
import os
import re
import subprocess
import sys
import time
from env_utils import (
    get_default_timeout,
    get_game_dir,
    get_manage_lib_dir,
    get_sdk_dir,
    get_sdk_paths,
    get_tests_dir,
    load_env,
)

PROXY_DIR = os.path.dirname(os.path.abspath(__file__))

def get_project_dir(provided_dir: str = None) -> str:
    if provided_dir:
        return os.path.abspath(provided_dir)
    # Check if inside a versioned folder .renpy-tools/rtools-<ver> or .renpy-tools
    parent = os.path.abspath(os.path.join(PROXY_DIR, ".."))
    if os.path.basename(parent) == ".renpy-tools":
        return os.path.abspath(os.path.join(parent, ".."))
    elif os.path.basename(PROXY_DIR) == ".renpy-tools":
        return parent
    return PROXY_DIR

def get_help() -> str:
    return """Ren'Py CLI Runner Utility (renpy-build-tools)

Management & Setup Commands:
  python manage.py quickstart [path] [-a|--all] Install renpy-build-tools into a target project
  python manage.py update [-y|--yes]        Check and update tool to the latest release
  python manage.py version                  Display current installed version
  python manage.py setup [--skip-hooks]    Configure git hooks and verify project environment
  python manage.py verify                   Verify paths, .env, and binary dependencies

Execution & Linting Commands:
  python manage.py run                      Launch the game normally
  python manage.py lint                     Run Ren'Py built-in static analysis
  python manage.py check                    Run custom static analysis checkers (asset integrity, rollback)
  python manage.py clean [-v|--verbose]     Clean compiled Ren'Py (*.rpyc) and Python files
  python manage.py warp <scene:line>        Launch the game directly at a script line
  python manage.py bump [part]              Bump version & date stamp in VERSION, README.md, script.rpy (minor|major|patch)

Testing Commands:
  python manage.py test [suite]             Run tests (default suite: global)
                                            Options:
                                              -s, --silent     Suppress output for passing tests
                                              --exclude-e2e    Run all testsuites except E2E UI testsuites
                                              --no-kill        Keep the process alive for manual runs
                                              --timeout <sec>  Set safety timeout in seconds

Asset Encryption & Archiving Commands:
  python manage.py pack <src> <dst> | <alias> Pack folder tree into encrypted archives
  python manage.py unpack <src> <dst> | <alias> Unpack archives and restore folder tree (with backups)
"""

def cmd_verify(project_dir: str) -> None:
    """Checks the validity of paths and environment configuration."""
    print("=== Ren'Py Environment Verification ===")
    print(f"Project Path (Detected): {project_dir}")
    
    env_path = os.path.join(project_dir, ".env")
    if os.path.exists(env_path):
        print(f"[OK] Found local config at: {env_path}")
    else:
        print("[WARNING] Local .env file not found in project root. Will fallback to env vars or default paths.")
        print("          (Run 'python manage.py setup' or copy .env.example to .env)")

    sdk_dir = get_sdk_dir(project_dir)
    print(f"SDK Path: {sdk_dir}")
    if os.path.exists(sdk_dir):
        print("[OK] SDK Directory exists.")
    else:
        print(f"[ERROR] SDK Directory does not exist: '{sdk_dir}'")
        print("Please configure 'RENPY_SDK' in a local '.env' file or set RENPY_SDK in your environment.")
        sys.exit(1)

    game_dir = get_game_dir(project_dir)
    tests_dir = get_tests_dir(project_dir)
    print(f"Game Path: {game_dir}")
    if os.path.exists(game_dir):
        print("[OK] Game Directory exists.")
    else:
        print(f"[WARNING] Game Directory does not exist yet at '{game_dir}'.")

    print(f"Tests Path: {tests_dir}")
    if os.path.exists(tests_dir):
        print("[OK] Tests Directory exists.")
    else:
        print(f"[INFO] Tests Directory not found at '{tests_dir}'.")

    paths = get_sdk_paths(sdk_dir)
    errs = 0
    for name, path in paths.items():
        if os.path.exists(path):
            print(f"[OK] Found {name}: {path}")
        else:
            print(f"[ERROR] Missing {name}: {path}")
            errs += 1
            
    if errs == 0:
        print("\n[SUCCESS] Environment is fully valid and configured correctly!")
    else:
        print(f"\n[ERROR] Found {errs} issues with path resolution.")
        sys.exit(1)

def cmd_setup(args: list[str], project_dir: str) -> None:
    """Configures project settings (e.g., git hooks) and runs verification."""
    print("=== Ren'Py Project Setup ===")
    
    skip_hooks = "--skip-hooks" in args
    if not skip_hooks:
        templates_dir = os.path.join(PROXY_DIR, "templates")
        src_hooks = os.path.join(templates_dir, ".githooks.example")
        dst_hooks = os.path.join(project_dir, ".githooks")
        
        if os.path.exists(src_hooks) and not os.path.exists(dst_hooks):
            import shutil
            os.makedirs(dst_hooks, exist_ok=True)
            for item in os.listdir(src_hooks):
                shutil.copy2(os.path.join(src_hooks, item), os.path.join(dst_hooks, item))
            print(f"[OK] Deployed Git hooks template to: {dst_hooks}")

        if os.path.exists(os.path.join(project_dir, ".git")):
            try:
                subprocess.run(["git", "config", "core.hooksPath", ".githooks"], cwd=project_dir, check=True)
                print("[OK] Configured Git to use '.githooks/' directory for hooks.")
            except (subprocess.CalledProcessError, OSError) as e:
                print(f"[WARNING] Failed to configure Git hooks path: {e}")
        else:
            print("[INFO] Not inside a Git repository. Skipped Git hooks registration.")

    print("\nRunning verification tests...")
    cmd_verify(project_dir)

def cmd_run(project_dir: str) -> None:
    sdk_dir = get_sdk_dir(project_dir)
    paths = get_sdk_paths(sdk_dir)
    cmd = [paths["renpy_exe"], project_dir, "run"]
    print(f"[Runner] Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=False)

def cmd_lint(project_dir: str) -> None:
    sdk_dir = get_sdk_dir(project_dir)
    paths = get_sdk_paths(sdk_dir)
    cmd = [paths["renpy_exe"], project_dir, "lint"]
    print(f"[Runner] Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        sys.exit(result.returncode)
    print(f"[Runner] No lint problems found.")

def cmd_warp(warp_line: str, project_dir: str) -> None:
    sdk_dir = get_sdk_dir(project_dir)
    paths = get_sdk_paths(sdk_dir)
    cmd = [paths["renpy_exe"], project_dir, "warp", warp_line]
    print(f"[Runner] Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=False)

def discover_test_suites(project_dir: str, exclude_e2e: bool = False) -> list[str]:
    tests_dir = get_tests_dir(project_dir)
    suites = []
    if os.path.exists(tests_dir):
        suite_pattern = re.compile(r"testsuite\s+(\w+):")
        for root, _, files in os.walk(tests_dir):
            for file in files:
                if file.endswith(".rpy") and not file.endswith(".rpyc"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            m = suite_pattern.search(line)
                            if m:
                                suite_name = m.group(1)
                                if suite_name not in suites:
                                    suites.append(suite_name)
    if exclude_e2e:
        suites = [s for s in suites if "e2e" not in s.lower()]
    return suites

def cmd_test_single(test_suite: str, project_dir: str, no_kill: bool = False, timeout: float = None, silent: bool = False) -> bool:
    if timeout is None:
        timeout = get_default_timeout(project_dir)

    sdk_dir = get_sdk_dir(project_dir)
    paths = get_sdk_paths(sdk_dir)
    python_exe = paths["python_exe"]
    renpy_py = paths["renpy_py"]
    
    proc_env = os.environ.copy()
    cmd = [python_exe, renpy_py, project_dir, "test", test_suite]

    mode_str = " (no-kill mode)" if no_kill else ""
    silent_str = " (silent mode)" if silent else ""
    if not silent:
        print(f"[Runner] Starting Ren'Py tests for suite: '{test_suite}' (timeout: {timeout}s){mode_str}{silent_str}")
        print(f"[Runner] Command: {' '.join(cmd)}")
        print("-" * 60)
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=proc_env
    )
    
    start_time = time.time()
    current_test = None
    current_test_failed = False
    test_buffer = []
    any_test_failed = False
    clean_termination = False
    
    try:
        for line in iter(process.stdout.readline, ''):
            stripped_line = line.strip()
            
            start_match = re.match(r"^\[rpytest\]\s+\[exc\]\s+-\s+(\w+)\s*$", stripped_line)
            end_match = re.match(r"^\[rpytest\]\s+\[exc\]\s+-\s+(\w+)\s+\((\d+\.\d+)\s*s\)\s*$", stripped_line)
            
            if start_match:
                current_test = start_match.group(1)
                current_test_failed = False
                test_buffer = []
                continue
                
            if current_test:
                if any(
                    marker in stripped_line
                    for marker in ["AssertionError", "Full traceback:", "During testcase execution:", "==="]
                ):
                    current_test_failed = True
                    any_test_failed = True
                
                if end_match and current_test == end_match.group(1):
                    if current_test_failed:
                        status_str = " \033[91m[FAILED]\033[0m"
                        for buf_line in test_buffer:
                            print(buf_line, end='', flush=True)
                        print(line.rstrip('\r\n') + status_str, flush=True)
                    else:
                        status_str = " \033[92m[PASSED]\033[0m"
                        if not silent:
                            for buf_line in test_buffer:
                                print(buf_line, end='', flush=True)
                            print(line.rstrip('\r\n') + status_str, flush=True)
                    current_test = None
                    current_test_failed = False
                    test_buffer = []
                else:
                    test_buffer.append(line)
            else:
                if not silent or any(
                    marker in stripped_line for marker in [
                        "[rpytest] Test outcomes",
                        "[rpytest] Test suites:",
                        "[rpytest] Test cases",
                        "[rpytest] Test hooks",
                        "[rpytest] Assertions",
                        "[rpytest] Time:",
                        "[rpytest] Status:"
                    ]
                ):
                    print(line, end='', flush=True)
            
            if not no_kill:
                if "[rpytest] Status:" in line:
                    if "FAILED" in line or "ERROR" in line:
                        any_test_failed = True
                    if not silent:
                        print("\n[Runner] Test execution completed. Terminating Ren'Py process...")
                    clean_termination = True
                    process.terminate()
                    break
                    
                if time.time() - start_time > timeout:
                    print(f"\n[Runner] Timeout of {timeout}s reached. Terminating Ren'Py process...")
                    process.terminate()
                    any_test_failed = True
                    break
    except KeyboardInterrupt:
        print("\n[Runner] Interrupted by user. Terminating process...")
        process.terminate()
    finally:
        try:
            process.kill()
        except OSError:
            pass
        rc = process.wait()
        if not silent:
            print("-" * 60)
            print("[Runner] Execution finished.")
        if rc != 0 and not clean_termination:
            any_test_failed = True
            
    return not any_test_failed

def cmd_test(args: list[str], project_dir: str) -> None:
    test_suite = "global"
    no_kill = "--no-kill" in args
    exclude_e2e = "--exclude-e2e" in args
    silent = "-s" in args or "--silent" in args
    timeout = get_default_timeout(project_dir)

    skip_next = False
    for i, a in enumerate(args):
        if skip_next:
            skip_next = False
            continue
        if a in ("-t", "--timeout") and i + 1 < len(args):
            try:
                timeout = float(args[i + 1])
                skip_next = True
            except ValueError:
                pass
        elif not a.startswith("-") and a != test_suite and a not in ("global",):
            test_suite = a

    if exclude_e2e:
        suites = discover_test_suites(project_dir, exclude_e2e=True)
        if not silent:
            print(f"[Runner] Excluding E2E test suites. Discovered {len(suites)} non-E2E suite(s): {suites}")
        overall_success = True
        for suite in suites:
            success = cmd_test_single(suite, project_dir, no_kill=no_kill, timeout=timeout, silent=silent)
            if not success:
                overall_success = False
        if not overall_success:
            sys.exit(1)
    else:
        success = cmd_test_single(test_suite, project_dir, no_kill=no_kill, timeout=timeout, silent=silent)
        if not success:
            sys.exit(1)

def cmd_clean(verbose: bool = False, project_dir: str = None) -> None:
    clean_extensions = {".rpyc", ".rpymc", ".rpyb", ".pyc", ".pyo"}
    ignore_dirs = {".git", ".venv", "venv", ".idea", ".vscode"}
    
    print("=== Ren'Py Compiled Files Cleanup ===")
    deleted_count = 0
    total_bytes_freed = 0
    deleted_by_ext: dict[str, int] = {}
    
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            _, ext = os.path.splitext(file)
            ext_lower = ext.lower()
            if ext_lower in clean_extensions:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, project_dir)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_count += 1
                    total_bytes_freed += file_size
                    deleted_by_ext[ext_lower] = deleted_by_ext.get(ext_lower, 0) + 1
                    if verbose:
                        print(f"[Clean] Removed: {rel_path}")
                except OSError as e:
                    print(f"[ERROR] Failed to remove {rel_path}: {e}")

    print("\n=== Cleanup Summary ===")
    print(f"Total files deleted: {deleted_count}")
    if deleted_by_ext:
        ext_summary = ", ".join(f"{ext}: {count}" for ext, count in sorted(deleted_by_ext.items()))
        print(f"Breakdown by extension: {ext_summary}")
    
    if total_bytes_freed >= 1024 * 1024:
        size_str = f"{total_bytes_freed / (1024 * 1024):.2f} MB"
    elif total_bytes_freed >= 1024:
        size_str = f"{total_bytes_freed / 1024:.2f} KB"
    else:
        size_str = f"{total_bytes_freed} Bytes"
    print(f"Total space freed: {size_str}")

def cmd_check(project_dir: str) -> None:
    print("=== Ren'Py Custom Static Analysis Checkers ===")
    
    import static_checks
    target_dir = get_game_dir(project_dir)
    issues = static_checks.run_all_checks(target_dir)
    
    if not issues:
        print("\033[92m[SUCCESS] No static analysis issues found!\033[0m")
        return

    print(f"\033[91m[ERROR] Found {len(issues)} static analysis issue(s):\033[0m\n")
    for issue in issues:
        checker_badge = f"\033[93m[{issue.checker}]\033[0m"
        loc = f"\033[36m{issue.file}:{issue.line}\033[0m"
        print(f"{checker_badge} {loc}: {issue.message}")
        if issue.code_snippet:
            enc = sys.stdout.encoding or "utf-8"
            safe_snippet = issue.code_snippet.encode(enc, errors="replace").decode(enc, errors="replace")
            print(f"   Line: {safe_snippet}")
        print(f"   Fix:  {issue.suggestion}\n")
        
    sys.exit(1)

def find_config_version_file(game_dir: str) -> tuple[str | None, str]:
    """
    Searches game_dir for a file containing 'define config.version', 'label start:', or options.rpy/script.rpy.
    """
    if not os.path.exists(game_dir):
        return None, ""

    label_start_file = None
    options_file = None
    script_file = None

    for root, _, files in os.walk(game_dir):
        for file in sorted(files):
            if file.endswith(".rpy") and not file.endswith(".rpyc"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if re.search(r'define\s+config\.version\s*=', content):
                            return file_path, "config"
                        if not label_start_file and re.search(r'^\s*label\s+start\s*:', content, re.MULTILINE):
                            label_start_file = file_path
                        if file == "options.rpy":
                            options_file = file_path
                        elif file == "script.rpy":
                            script_file = file_path
                except OSError:
                    continue

    if label_start_file:
        return label_start_file, "label_start"
    if options_file:
        return options_file, "options"
    if script_file:
        return script_file, "script"
    return None, ""

def cmd_bump(part_or_ver: str = "minor", project_dir: str = None) -> None:
    version_file = os.path.join(project_dir, "VERSION")
    current_ver = "0.1"
    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            current_ver = f.read().strip() or "0.1"

    target = part_or_ver.lower()
    m = re.match(r'^(\d+)\.(\d+)(?:\.(\d+))?$', current_ver)
    if m:
        major, minor = int(m.group(1)), int(m.group(2))
        patch = int(m.group(3)) if m.group(3) is not None else 0
    else:
        major, minor, patch = 0, 1, 0

    if target == "major":
        new_ver = f"{major + 1}.0"
    elif target == "minor":
        new_ver = f"{major}.{minor + 1}"
    elif target == "patch":
        new_ver = f"{major}.{minor}.{patch + 1}"
    elif re.match(r'^\d+\.\d+(\.\d+)?$', part_or_ver):
        new_ver = part_or_ver
    else:
        new_ver = f"{major}.{minor + 1}"

    today_stamp = datetime.date.today().strftime("%Y%m%d")
    print(f"=== Bumping Version: {current_ver} -> {new_ver} ({today_stamp}) ===")

    with open(version_file, "w", encoding="utf-8") as f:
        f.write(f"{new_ver}\n")
    print(f"[OK] Updated VERSION file to '{new_ver}'")

    readme_path = os.path.join(project_dir, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()

        readme_content = re.sub(r'# Ren\'Py Build Tools v[^\s]+ 🚀', f"# Ren'Py Build Tools v{new_ver} 🚀", readme_content)
        badge_pattern = r'\[!\[Version: [^\]]+\]\(https://img\.shields\.io/badge/version-[^%]+%20%28\d{8}%29-blue\.svg\?style=flat-square\)\]\(README\.md\)'
        new_badge_ver = new_ver.replace('-', '--')
        new_badge = f"[![Version: {new_ver}](https://img.shields.io/badge/version-{new_badge_ver}%20%28{today_stamp}%29-blue.svg?style=flat-square)](README.md)"

        if re.search(badge_pattern, readme_content):
            readme_content = re.sub(badge_pattern, new_badge, readme_content)
        elif "# " in readme_content:
            readme_content = re.sub(r'(# [^\n]+\n)', r'\1\n' + new_badge + '\n', readme_content, count=1)

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"[OK] Updated README.md title and version badge ({new_ver} - {today_stamp})")

    game_dir = get_game_dir(project_dir)
    target_file, match_type = find_config_version_file(game_dir)
    if target_file and os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()

        rel_path = os.path.relpath(target_file, project_dir)
        if re.search(r'define\s+config\.version\s*=', content):
            new_content = re.sub(r'define\s+config\.version\s*=\s*"[^"]*"', f'define config.version = "{new_ver}"', content)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[OK] Updated config.version in '{rel_path}' to '{new_ver}'")
        else:
            new_content = f'define config.version = "{new_ver}"\n' + content
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[OK] Inserted config.version in '{rel_path}' set to '{new_ver}'")

    print(f"\n\033[92m[SUCCESS] Version successfully bumped to {new_ver} ({today_stamp})!\033[0m")

def run_command(command: str, args: list[str], project_dir: str = None) -> None:
    p_dir = get_project_dir(project_dir)
    cmd = command.lower()

    if cmd == "quickstart":
        from quickstart import run_quickstart
        run_quickstart(args, PROXY_DIR)
    elif cmd == "update":
        from updater import run_update
        run_update(args, p_dir)
    elif cmd == "version":
        from updater import run_version
        run_version(p_dir)
    elif cmd == "verify":
        cmd_verify(p_dir)
    elif cmd == "setup":
        cmd_setup(args, p_dir)
    elif cmd == "run":
        cmd_run(p_dir)
    elif cmd == "lint":
        cmd_lint(p_dir)
    elif cmd == "check":
        cmd_check(p_dir)
    elif cmd == "clean":
        verbose = "-v" in args or "--verbose" in args
        cmd_clean(verbose=verbose, project_dir=p_dir)
    elif cmd == "warp":
        if not args:
            print("[Error] Missing warp destination. Format: game/scripts/...:line")
            sys.exit(1)
        cmd_warp(args[0], p_dir)
    elif cmd == "bump":
        part = args[0] if args else "minor"
        cmd_bump(part, p_dir)
    elif cmd == "test":
        cmd_test(args, p_dir)
    elif cmd == "pack":
        from archive_utils import pack_assets
        try:
            pack_assets(p_dir, args)
        except ValueError as e:
            print(e)
            sys.exit(1)
    elif cmd == "unpack":
        from archive_utils import unpack_assets
        try:
            unpack_assets(p_dir, args)
        except ValueError as e:
            print(e)
            sys.exit(1)
    else:
        print(f"[Error] Unknown command: '{command}'\n")
        print(get_help())
        sys.exit(1)

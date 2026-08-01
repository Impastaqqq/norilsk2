# .renpy-tools/env_utils.py
import os
import sys
import glob

def load_env(project_dir: str) -> dict[str, str]:
    """Parses a local .env file in the given project directory."""
    env = {}
    env_path = os.path.join(project_dir, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def get_sdk_dir(project_dir: str) -> str:
    env_vars = load_env(project_dir)
    return env_vars.get("RENPY_SDK") or os.environ.get("RENPY_SDK") or r"C:\renpy\renpy-8.5.3-sdk"

def get_game_dir(project_dir: str) -> str:
    env_vars = load_env(project_dir)
    raw_dir = env_vars.get("RENPY_GAME_DIR") or os.environ.get("RENPY_GAME_DIR") or "game"
    return raw_dir if os.path.isabs(raw_dir) else os.path.join(project_dir, raw_dir)

def get_tests_dir(project_dir: str) -> str:
    env_vars = load_env(project_dir)
    raw_dir = env_vars.get("RENPY_TESTS_DIR") or os.environ.get("RENPY_TESTS_DIR") or os.path.join("game", "scripts", "tests")
    return raw_dir if os.path.isabs(raw_dir) else os.path.join(project_dir, raw_dir)

def get_default_timeout(project_dir: str) -> float:
    env_vars = load_env(project_dir)
    raw_timeout = env_vars.get("RENPY_TEST_TIMEOUT") or os.environ.get("RENPY_TEST_TIMEOUT")
    if raw_timeout:
        try:
            return float(raw_timeout)
        except ValueError:
            pass
    return 30.0

def get_manage_lib_dir(project_dir: str) -> str:
    env_vars = load_env(project_dir)
    raw_dir = env_vars.get("RENPY_MANAGE_LIB_DIR") or os.environ.get("RENPY_MANAGE_LIB_DIR") or os.path.join("game", "libs", "manage")
    return raw_dir if os.path.isabs(raw_dir) else os.path.join(project_dir, raw_dir)

def get_sdk_paths(sdk_dir: str) -> dict[str, str]:
    """Resolves SDK binaries depending on the OS platform."""
    is_windows = sys.platform.startswith("win")
    is_mac = sys.platform == "darwin"
    
    renpy_exe = ""
    python_exe = ""
    renpy_py = os.path.join(sdk_dir, "renpy.py")
    
    if is_windows:
        renpy_exe = os.path.join(sdk_dir, "renpy.exe")
        python_exe = os.path.join(sdk_dir, "lib", "py3-windows-x86_64", "python.exe")
        if not os.path.exists(python_exe):
            lib_dir = os.path.join(sdk_dir, "lib")
            if os.path.exists(lib_dir):
                for sub in os.listdir(lib_dir):
                    candidate = os.path.join(lib_dir, sub, "python.exe")
                    if os.path.exists(candidate):
                        python_exe = candidate
                        break
    elif is_mac:
        renpy_exe = os.path.join(sdk_dir, "Ren'Py.app", "Contents", "MacOS", "Ren'Py")
        lib_dir = os.path.join(sdk_dir, "lib")
        if os.path.exists(lib_dir):
            for sub in os.listdir(lib_dir):
                if "mac-" in sub:
                    candidate = os.path.join(lib_dir, sub, "python")
                    if os.path.exists(candidate):
                        python_exe = candidate
                        break
    else:  # Linux/Unix
        renpy_exe = os.path.join(sdk_dir, "renpy.sh")
        lib_dir = os.path.join(sdk_dir, "lib")
        if os.path.exists(lib_dir):
            for sub in os.listdir(lib_dir):
                if "linux-" in sub:
                    candidate = os.path.join(lib_dir, sub, "python")
                    if os.path.exists(candidate):
                        python_exe = candidate
                        break
                        
    if not renpy_exe or not os.path.exists(renpy_exe):
        renpy_exe = "renpy.exe" if is_windows else "renpy.sh"
    if not python_exe or not os.path.exists(python_exe):
        python_exe = sys.executable
        
    return {
        "renpy_exe": renpy_exe,
        "python_exe": python_exe,
        "renpy_py": renpy_py
    }

def auto_detect_renpy_sdk(project_dir: str = None) -> str | None:
    """Probes environment variables and standard system paths to detect a Ren'Py SDK installation."""
    # 1. Check OS environment variable
    if os.environ.get("RENPY_SDK") and os.path.exists(os.environ["RENPY_SDK"]):
        return os.path.abspath(os.environ["RENPY_SDK"])

    # 2. Check local project .env if provided
    if project_dir:
        env_vars = load_env(project_dir)
        if env_vars.get("RENPY_SDK") and os.path.exists(env_vars["RENPY_SDK"]):
            return os.path.abspath(env_vars["RENPY_SDK"])

    is_win = sys.platform.startswith("win")
    is_mac = sys.platform == "darwin"

    candidates = []
    if is_win:
        # Check current working drive (e.g. H:\)
        current_drive = os.path.splitdrive(os.getcwd())[0]
        if current_drive:
            candidates.extend([
                rf"{current_drive}\renpy\renpy-*-sdk",
                rf"{current_drive}\renpy\renpy-*",
            ])
        candidates.extend([
            r"C:\renpy\renpy-*-sdk",
            r"C:\renpy\renpy-*",
            r"C:\Program Files\renpy\renpy-*-sdk",
            r"D:\renpy\renpy-*-sdk",
            os.path.expanduser(r"~\renpy\renpy-*-sdk"),
        ])
    elif is_mac:
        candidates.extend([
            "/Applications/renpy-*-sdk",
            "/Applications/Ren'Py.app",
            os.path.expanduser("~/Applications/renpy-*-sdk"),
        ])
    else:
        candidates.extend([
            os.path.expanduser("~/renpy/renpy-*-sdk"),
            "/opt/renpy/renpy-*-sdk",
        ])

    for pattern in candidates:
        matches = sorted(glob.glob(pattern), reverse=True)
        for match in matches:
            if os.path.exists(match):
                return os.path.abspath(match)

    return None

def get_encryption_key(project_dir: str) -> str | None:
    """Returns the configured encryption key from local .env or OS environment."""
    env_vars = load_env(project_dir)
    return (
        env_vars.get("RPT_ENCRYPTION_KEY")
        or env_vars.get("NSFW_ENCRYPTION_KEY")
        or os.environ.get("RPT_ENCRYPTION_KEY")
        or os.environ.get("NSFW_ENCRYPTION_KEY")
    )

def get_pack_warn_mb(project_dir: str) -> float:
    """Returns warning threshold in MB for single archive packing."""
    env_vars = load_env(project_dir)
    raw = env_vars.get("RPT_PACK_WARN_MB") or env_vars.get("NSFW_ARCHIVE_WARN_MB") or os.environ.get("RPT_PACK_WARN_MB")
    if raw:
        try:
            return float(raw)
        except ValueError:
            pass
    return 500.0

def get_pack_limit_mb(project_dir: str) -> float:
    """Returns hard limit threshold in MB for single archive packing."""
    env_vars = load_env(project_dir)
    raw = env_vars.get("RPT_PACK_LIMIT_MB") or env_vars.get("NSFW_ARCHIVE_LIMIT_MB") or os.environ.get("RPT_PACK_LIMIT_MB")
    if raw:
        try:
            return float(raw)
        except ValueError:
            pass
    return 1000.0

def get_obfuscate_paths(project_dir: str) -> bool:
    """Returns whether output archive folder paths/filenames should be obfuscated."""
    env_vars = load_env(project_dir)
    raw = env_vars.get("RPT_OBFUSCATE_PATHS") or os.environ.get("RPT_OBFUSCATE_PATHS") or "false"
    return raw.strip().lower() in ("true", "1", "yes")

def get_aliases(project_dir: str) -> dict[str, tuple[str, str]]:
    """Parses alias definitions from local .env (e.g. alias.assets_pack=src dst or RPT_ALIAS_ASSETS=src dst)."""
    env_vars = load_env(project_dir)
    aliases = {}
    for key, val in env_vars.items():
        alias_name = None
        if key.startswith("alias."):
            alias_name = key[len("alias."):]
        elif key.startswith("RPT_ALIAS_"):
            alias_name = key[len("RPT_ALIAS_"):].lower()
        
        if alias_name and val:
            parts = val.split()
            if len(parts) >= 2:
                aliases[alias_name] = (parts[0], parts[1])
    return aliases


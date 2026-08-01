# .renpy-tools/quickstart.py
import os
import shutil
import sys
from env_utils import auto_detect_renpy_sdk, get_sdk_dir, load_env

DEV_WARNING_BANNER = """
================================================================================
[WARNING] Ren'Py Build Tools is currently in active development phase.
[RECOMMENDATION] We strongly advise committing a savepoint before installing:
    git add . && git commit -m "Savepoint before renpy-build-tools quickstart"
================================================================================
"""

def is_renpy_project(target_dir: str) -> bool:
    """Checks whether target_dir looks like a Ren'Py project (has game/ and .rpy files)."""
    game_dir = target_dir if os.path.basename(target_dir) == "game" else os.path.join(target_dir, "game")
    if not os.path.exists(game_dir) or not os.path.isdir(game_dir):
        return False
    
    # Check for any .rpy files inside game/ directory
    for root, _, files in os.walk(game_dir):
        for file in files:
            if file.endswith(".rpy"):
                return True
    return False

def is_valid_renpy_sdk(sdk_path: str) -> bool:
    """Checks whether sdk_path contains renpy.py."""
    if not sdk_path or not os.path.exists(sdk_path):
        return False
    return os.path.exists(os.path.join(sdk_path, "renpy.py"))

def copy_directory_contents(src: str, dst: str, overwrite: bool = True) -> None:
    """Copies all files and subdirectories from src to dst."""
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if os.path.exists(d) and overwrite:
                shutil.rmtree(d)
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

def resolve_sdk_path(repo_root: str, auto_yes: bool = False) -> str:
    """Interactively resolves or prompts for Ren'Py SDK path with renpy.py validation."""
    detected_sdk = auto_detect_renpy_sdk(repo_root)
    
    if auto_yes:
        return detected_sdk or r"C:\renpy\renpy-8.5.3-sdk"
        
    if detected_sdk and is_valid_renpy_sdk(detected_sdk):
        print(f"\n[SDK Config] Auto-detected Ren'Py SDK location: '{detected_sdk}'")
        try:
            user_sdk = input("Enter Ren'Py SDK path [Press Enter to accept auto-detected path]: ").strip()
        except EOFError:
            user_sdk = ""
        if not user_sdk:
            return detected_sdk
        if is_valid_renpy_sdk(user_sdk):
            return user_sdk
        print(f"[WARNING] Provided path '{user_sdk}' does not look like a Ren'Py SDK location (missing 'renpy.py').")

    print("\n[WARNING] Could not auto-detect a valid Ren'Py SDK location.")
    while True:
        try:
            user_sdk = input("Please enter full path to your Ren'Py SDK directory: ").strip()
        except EOFError:
            user_sdk = ""
        
        if is_valid_renpy_sdk(user_sdk):
            return user_sdk
        elif user_sdk:
            print(f"[WARNING] Provided path '{user_sdk}' does not look like a Ren'Py SDK location (missing 'renpy.py').")
            try:
                confirm = input("Use this path anyway? (y/N): ").strip().lower()
            except EOFError:
                confirm = "n"
            if confirm in ("y", "yes"):
                return user_sdk
        else:
            return r"C:\renpy\renpy-8.5.3-sdk"

def run_quickstart(args: list[str], current_tool_dir: str) -> None:
    print(DEV_WARNING_BANNER)
    
    auto_yes = "-a" in args or "--all" in args
    is_standalone = "--standalone" in args or "-s" in args
    
    clean_args = [a for a in args if a not in ("-a", "--all", "--standalone", "-s")]
    
    # Determine target project path
    if clean_args:
        target_path = clean_args[0]
    else:
        try:
            target_path = input("Enter target Ren'Py project path [default: current directory]: ").strip()
        except EOFError:
            target_path = ""
        if not target_path:
            target_path = os.getcwd()
            
    target_dir = os.path.abspath(target_path)
    print(f"\n[Quickstart] Target project path: {target_dir}")
    
    if not auto_yes:
        try:
            confirm = input("Proceed with quickstart setup? (y/N): ").strip().lower()
        except EOFError:
            confirm = "n"
        if confirm not in ("y", "yes"):
            print("[Quickstart] Setup aborted by user.")
            return

    # Validate if target looks like a Ren'Py project
    if not is_renpy_project(target_dir):
        print(f"\n[WARNING] Target directory does not appear to be a Ren'Py project.")
        print("          (Missing 'game/' directory or .rpy script files)")
        if not auto_yes:
            try:
                confirm = input("Do you want to proceed with quickstart anyway? (y/N): ").strip().lower()
            except EOFError:
                confirm = "n"
            if confirm not in ("y", "yes"):
                print("[Quickstart] Aborted due to non-Ren'Py project directory.")
                return

    repo_root = os.path.abspath(os.path.join(current_tool_dir, ".."))

    # If --standalone or -s flag was specified
    if is_standalone:
        print(f"\n[Quickstart] Setting up Standalone Usage mode...")
        game_dir = target_dir if os.path.basename(target_dir) == "game" else os.path.join(target_dir, "game")
        
        tool_env = os.path.join(repo_root, ".env")
        detected_sdk = resolve_sdk_path(repo_root, auto_yes=auto_yes)
        
        with open(tool_env, "w", encoding="utf-8") as f:
            f.write(f"RENPY_SDK={detected_sdk}\n")
            f.write(f"RENPY_GAME_DIR={game_dir}\n")
            f.write("RENPY_TESTS_DIR=game/scripts/tests\n")
            f.write("RENPY_TEST_TIMEOUT=30.0\n")
            
        print(f"[OK] Configured central .env file: {tool_env}")
        print(f"[OK] RENPY_GAME_DIR set to: {game_dir}")
        print(f"\n[Quickstart] Running standalone verification...")
        import proxy
        proxy.run_command("verify", [], project_dir=repo_root)
        print(f"\n[SUCCESS] Standalone configuration completed for: {target_dir}")
        return

    # Standard Direct Project Installation
    version_file = os.path.join(repo_root, "VERSION")
    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            version_str = f.read().strip()
    else:
        version_str = "0.1"

    print(f"\n[Quickstart] Installing Ren'Py Build Tools v{version_str} into project...")

    # 1. Copy manage.py launcher to project root
    src_manage = os.path.join(repo_root, "manage.py")
    dst_manage = os.path.join(target_dir, "manage.py")
    if os.path.exists(src_manage):
        shutil.copy2(src_manage, dst_manage)
        print(f"[OK] Installed launcher: {dst_manage}")

    # 2. Copy .renpy-tools/ to target project .renpy-tools/rtools-<version>/
    target_tools_dir = os.path.join(target_dir, ".renpy-tools")
    version_dest_dir = os.path.join(target_tools_dir, f"rtools-{version_str}")
    os.makedirs(version_dest_dir, exist_ok=True)
    
    # Copy .renpy-tools source files into version_dest_dir
    src_renpy_tools = os.path.join(repo_root, ".renpy-tools")
    copy_directory_contents(src_renpy_tools, version_dest_dir)
    print(f"[OK] Installed core tools to: {version_dest_dir}")

    # 3. Create / update CURRENT_VERSION
    current_ver_file = os.path.join(target_tools_dir, "CURRENT_VERSION")
    with open(current_ver_file, "w", encoding="utf-8") as f:
        f.write(f"{version_str}\n")
    print(f"[OK] Created version marker: {current_ver_file}")

    # Locate component templates directory
    templates_dir = os.path.join(version_dest_dir, "templates")

    # 4. Handle optional component: .agents
    install_agents = auto_yes
    if not auto_yes:
        try:
            ans = input("\nInstall AI Agent guidelines (.agents)? [Y/n]: ").strip().lower()
            install_agents = ans in ("", "y", "yes")
        except EOFError:
            install_agents = True
            
    if install_agents:
        src_agents = os.path.join(templates_dir, ".agents.example")
        dst_agents = os.path.join(target_dir, ".agents")
        if os.path.exists(src_agents):
            copy_directory_contents(src_agents, dst_agents)
            print(f"[OK] Installed .agents guidelines to: {dst_agents}")

    # 5. Handle optional component: .github (CI)
    install_ci = auto_yes
    if not auto_yes:
        try:
            ans = input("Install CI Workflows (.github)? [Y/n]: ").strip().lower()
            install_ci = ans in ("", "y", "yes")
        except EOFError:
            install_ci = True

    if install_ci:
        src_ci = os.path.join(templates_dir, ".github.example")
        dst_ci = os.path.join(target_dir, ".github")
        if os.path.exists(src_ci):
            copy_directory_contents(src_ci, dst_ci)
            print(f"[OK] Installed CI workflows to: {dst_ci}")

    # 6. Handle optional component: .githooks
    install_hooks = auto_yes
    if not auto_yes:
        try:
            ans = input("Install Git Hooks (.githooks)? [Y/n]: ").strip().lower()
            install_hooks = ans in ("", "y", "yes")
        except EOFError:
            install_hooks = True

    if install_hooks:
        src_hooks = os.path.join(templates_dir, ".githooks.example")
        dst_hooks = os.path.join(target_dir, ".githooks")
        if os.path.exists(src_hooks):
            copy_directory_contents(src_hooks, dst_hooks)
            print(f"[OK] Installed Git hooks to: {dst_hooks}")

    # 7. Configure .env file inside target project
    dst_env = os.path.join(target_dir, ".env")
    if not os.path.exists(dst_env):
        sdk_path = resolve_sdk_path(repo_root, auto_yes=auto_yes)
        with open(dst_env, "w", encoding="utf-8") as f:
            f.write(f"RENPY_SDK={sdk_path}\n")
            f.write("RENPY_GAME_DIR=game\n")
            f.write("RENPY_TESTS_DIR=game/scripts/tests\n")
            f.write("RENPY_TEST_TIMEOUT=30.0\n")
        print(f"[OK] Configured project environment: {dst_env}")

    # 8. Post-installation setup execution
    print("\n[Quickstart] Running project setup...")
    import proxy
    setup_args = []
    if not install_hooks:
        setup_args.append("--skip-hooks")
    proxy.run_command("setup", setup_args, project_dir=target_dir)

    print(f"\n[SUCCESS] Ren'Py Build Tools quickstart completed successfully for: {target_dir}")

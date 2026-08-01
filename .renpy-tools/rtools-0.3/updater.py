# .renpy-tools/updater.py
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from quickstart import DEV_WARNING_BANNER, copy_directory_contents

REMOTE_VERSION_URL = "https://raw.githubusercontent.com/DocDVZ/renpy-build-tools/main/VERSION"
REMOTE_ZIP_URL = "https://github.com/DocDVZ/renpy-build-tools/archive/refs/heads/main.zip"

def get_current_version(project_dir: str) -> tuple[str, str]:
    """Returns (version_string, source_directory)."""
    tools_dir = os.path.join(project_dir, ".renpy-tools")
    version_file = os.path.join(tools_dir, "CURRENT_VERSION")
    
    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            ver = f.read().strip()
        source_dir = os.path.join(tools_dir, f"rtools-{ver}")
        return ver, source_dir
    
    # Fallback to tool repo VERSION file (standalone mode)
    repo_version_file = os.path.join(project_dir, "VERSION")
    if os.path.exists(repo_version_file):
        with open(repo_version_file, "r", encoding="utf-8") as f:
            ver = f.read().strip()
        return ver, tools_dir
        
    return "0.1", tools_dir

def run_version(project_dir: str) -> None:
    ver, src_dir = get_current_version(project_dir)
    print(f"Ren'Py Build Tools version: {ver}")
    print(f"Active source directory: {src_dir}")

def fetch_remote_version() -> str | None:
    """Downloads the version string from the remote repository."""
    try:
        req = urllib.request.Request(
            REMOTE_VERSION_URL,
            headers={"User-Agent": "RenPy-Build-Tools-Updater"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8").strip()
    except Exception as e:
        print(f"[Warning] Failed to check remote version: {e}")
        return None

def parse_version_tuple(ver_str: str) -> tuple[int, ...]:
    parts = []
    for part in ver_str.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(0)
    return tuple(parts)

def run_update(args: list[str], project_dir: str) -> None:
    print(DEV_WARNING_BANNER)

    auto_yes = "-y" in args or "--yes" in args or "-a" in args or "--all" in args

    if not auto_yes:
        try:
            confirm = input("Proceed with update check? (y/N): ").strip().lower()
        except EOFError:
            confirm = "n"
        if confirm not in ("y", "yes"):
            print("[Update] Operation cancelled by user.")
            return

    current_ver, current_src = get_current_version(project_dir)
    print(f"[Update] Checking for updates... (Current local version: {current_ver})")
    
    remote_ver = fetch_remote_version()
    if not remote_ver:
        print("[Update] Unable to determine remote version. Aborting update.")
        return

    print(f"[Update] Remote version available: {remote_ver}")

    local_tuple = parse_version_tuple(current_ver)
    remote_tuple = parse_version_tuple(remote_ver)

    if local_tuple > remote_tuple:
        print(f"\n[WARNING] Your local version ({current_ver}) is newer than remote branch ({remote_ver}).")
        print("          You may be using a custom or development version.")
        if not auto_yes:
            try:
                ans = input("Force re-install remote version anyway? (y/N): ").strip().lower()
            except EOFError:
                ans = "n"
            if ans not in ("y", "yes"):
                print("[Update] Update skipped.")
                return

    elif local_tuple == remote_tuple:
        print(f"\n[INFO] You are already using the latest version of Ren'Py Build Tools ({current_ver}).")
        
        # Check if user wants to setup or re-install optional components
        if not auto_yes:
            try:
                ans = input("\nWould you like to re-configure optional components (.agents, CI, git hooks)? (y/N): ").strip().lower()
            except EOFError:
                ans = "n"
            if ans in ("y", "yes"):
                import proxy
                proxy.run_command("setup", [], project_dir=project_dir)
        return

    print(f"\n[Update] Upgrading Ren'Py Build Tools: {current_ver} -> {remote_ver}...")

    # Download archive to temporary directory
    temp_dir = tempfile.mkdtemp(prefix="renpy_tools_update_")
    zip_path = os.path.join(temp_dir, "repo.zip")

    try:
        print(f"[Update] Downloading release package from repository...")
        req = urllib.request.Request(
            REMOTE_ZIP_URL,
            headers={"User-Agent": "RenPy-Build-Tools-Updater"}
        )
        with urllib.request.urlopen(req, timeout=30) as response, open(zip_path, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
            
        print(f"[Update] Extracting update archive...")
        extract_dir = os.path.join(temp_dir, "extracted")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        # Locate extracted root folder (e.g. renpy-build-tools-main)
        subfolders = [os.path.join(extract_dir, d) for d in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, d))]
        if not subfolders:
            print("[Update Error] Invalid zip archive structure.")
            return
        downloaded_root = subfolders[0]

        target_tools_dir = os.path.join(project_dir, ".renpy-tools")
        current_ver_file = os.path.join(target_tools_dir, "CURRENT_VERSION")
        src_renpy_tools = os.path.join(downloaded_root, ".renpy-tools")

        if os.path.exists(current_ver_file):
            # Target Project Installed Mode
            new_version_dir = os.path.join(target_tools_dir, f"rtools-{remote_ver}")
            if os.path.exists(src_renpy_tools):
                copy_directory_contents(src_renpy_tools, new_version_dir)
                print(f"[OK] Extracted new tools version to: {new_version_dir}")
            with open(current_ver_file, "w", encoding="utf-8") as f:
                f.write(f"{remote_ver}\n")
            print(f"[OK] Updated CURRENT_VERSION to {remote_ver}")
        else:
            # Standalone / Tool Repository Mode
            if os.path.exists(src_renpy_tools):
                copy_directory_contents(src_renpy_tools, target_tools_dir)
                print(f"[OK] Extracted new tools version to: {target_tools_dir}")
            repo_version_file = os.path.join(project_dir, "VERSION")
            with open(repo_version_file, "w", encoding="utf-8") as f:
                f.write(f"{remote_ver}\n")
            print(f"[OK] Updated VERSION file to {remote_ver}")

        # Update root manage.py launcher safely
        new_manage = os.path.join(downloaded_root, "manage.py")
        local_manage = os.path.join(project_dir, "manage.py")
        if os.path.exists(new_manage):
            shutil.copy2(new_manage, local_manage)
            print(f"[OK] Updated manage.py launcher.")

        # Re-run setup
        print("\n[Update] Running post-update setup...")
        import proxy
        proxy.run_command("setup", [], project_dir=project_dir)

        print(f"\n[SUCCESS] Ren'Py Build Tools successfully updated to v{remote_ver}!")

    except Exception as e:
        print(f"[Update Error] Update failed: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

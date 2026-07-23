# manage.py
import os
import sys
import subprocess
import time
import re
import urllib.request
import json

# Resolve project root path dynamically based on script location
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_env() -> dict[str, str]:
    """Parses a local .env file in the project directory."""
    env = {}
    env_path = os.path.join(PROJECT_DIR, ".env")
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

# Resolve SDK root path from local env file, system environment, or hardcoded default fallback
env_vars = load_env()
SDK_DIR = env_vars.get("RENPY_SDK") or os.environ.get("RENPY_SDK") or r"h:\renpy\renpy-8.5.3-sdk"

def get_sdk_paths() -> dict[str, str]:
    """Resolves SDK binaries depending on the platform."""
    is_windows = sys.platform.startswith("win")
    is_mac = sys.platform == "darwin"
    
    renpy_exe = ""
    python_exe = ""
    renpy_py = os.path.join(SDK_DIR, "renpy.py")
    
    if is_windows:
        renpy_exe = os.path.join(SDK_DIR, "renpy.exe")
        # Try to locate Python directory in windows folder
        python_exe = os.path.join(SDK_DIR, "lib", "py3-windows-x86_64", "python.exe")
        if not os.path.exists(python_exe):
            # Fallback scanning
            lib_dir = os.path.join(SDK_DIR, "lib")
            if os.path.exists(lib_dir):
                for sub in os.listdir(lib_dir):
                    candidate = os.path.join(lib_dir, sub, "python.exe")
                    if os.path.exists(candidate):
                        python_exe = candidate
                        break
    elif is_mac:
        renpy_exe = os.path.join(SDK_DIR, "Ren'Py.app", "Contents", "MacOS", "Ren'Py")
        lib_dir = os.path.join(SDK_DIR, "lib")
        if os.path.exists(lib_dir):
            for sub in os.listdir(lib_dir):
                if "mac-" in sub:
                    candidate = os.path.join(lib_dir, sub, "python")
                    if os.path.exists(candidate):
                        python_exe = candidate
                        break
    else:  # Linux/Unix
        renpy_exe = os.path.join(SDK_DIR, "renpy.sh")
        lib_dir = os.path.join(SDK_DIR, "lib")
        if os.path.exists(lib_dir):
            for sub in os.listdir(lib_dir):
                if "linux-" in sub:
                    candidate = os.path.join(lib_dir, sub, "python")
                    if os.path.exists(candidate):
                        python_exe = candidate
                        break
                        
    # Fallbacks if not found
    if not renpy_exe or not os.path.exists(renpy_exe):
        renpy_exe = "renpy.exe" if is_windows else "renpy.sh"
    if not python_exe or not os.path.exists(python_exe):
        python_exe = sys.executable  # Fallback to current python interpreter
        
    return {
        "renpy_exe": renpy_exe,
        "python_exe": python_exe,
        "renpy_py": renpy_py
    }

def cmd_verify() -> None:
    """Checks the validity of Paths and Environment Configuration."""
    print("=== Ren'Py Environment Verification ===")
    print(f"Project Path (Detected): {PROJECT_DIR}")
    
    # Check .env
    env_path = os.path.join(PROJECT_DIR, ".env")
    if os.path.exists(env_path):
        print(f"[OK] Found local config at: {env_path}")
    else:
        print("[WARNING] Local .env file not found in project root. Will fallback to env vars or defaults.")
        
    # Check SDK Dir
    print(f"SDK Path: {SDK_DIR}")
    if os.path.exists(SDK_DIR):
        print("[OK] SDK Directory exists.")
    else:
        print(f"[ERROR] SDK Directory does not exist: '{SDK_DIR}'")
        print("Please configure 'RENPY_SDK' in a local '.env' file.")
        sys.exit(1)
        
    paths = get_sdk_paths()
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

def cmd_run() -> None:
    """Launches the Ren'Py project."""
    paths = get_sdk_paths()
    cmd = [paths["renpy_exe"], PROJECT_DIR, "run"]
    print(f"[Runner] Executing: {' '.join(cmd)}")
    subprocess.run(cmd)

def cmd_lint() -> None:
    """Lints the Ren'Py project."""
    paths = get_sdk_paths()
    cmd = [paths["renpy_exe"], PROJECT_DIR, "lint"]
    print(f"[Runner] Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

def cmd_warp(warp_line: str) -> None:
    """Warps the Ren'Py project to a specific file and line."""
    paths = get_sdk_paths()
    cmd = [paths["renpy_exe"], PROJECT_DIR, "warp", warp_line]
    print(f"[Runner] Executing: {' '.join(cmd)}")
    subprocess.run(cmd)

def discover_test_suites(exclude_e2e: bool = False) -> list[str]:
    """Scans game/scripts/tests/ for defined testsuites."""
    tests_dir = os.path.join(PROJECT_DIR, "game", "scripts", "tests")
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




def cmd_test_single(test_suite: str, no_kill: bool = False, timeout: float = 30.0) -> bool:
    """Executes a single test suite with timeout and auto-termination. Returns True if passed."""
    paths = get_sdk_paths()
    python_exe = paths["python_exe"]
    renpy_py = paths["renpy_py"]
    
    cmd = [python_exe, renpy_py, PROJECT_DIR, "test", test_suite]
    mode_str = " (no-kill mode)" if no_kill else ""
    print(f"[Runner] Starting Ren'Py tests for suite: '{test_suite}' (timeout: {timeout}s){mode_str}")
    print(f"[Runner] Command: {' '.join(cmd)}")
    print("-" * 60)
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    start_time = time.time()
    
    current_test = None
    current_test_failed = False
    any_test_failed = False
    clean_termination = False
    
    try:
        # Read stdout line by line
        for line in iter(process.stdout.readline, ''):
            stripped_line = line.strip()
            
            # Detect test start
            start_match = re.match(r"^\[rpytest\]\s+\[exc\]\s+-\s+(\w+)\s*$", stripped_line)
            if start_match:
                current_test = start_match.group(1)
                current_test_failed = False
                
            # Detect failure markers during active testcase
            if current_test:
                if any(marker in stripped_line for marker in ["AssertionError", "Full traceback:", "During testcase execution:", "==="]):
                    current_test_failed = True
                    any_test_failed = True
                    
            # Detect test end and append status
            end_match = re.match(r"^\[rpytest\]\s+\[exc\]\s+-\s+(\w+)\s+\((\d+\.\d+)\s*s\)\s*$", stripped_line)
            if end_match and current_test == end_match.group(1):
                if current_test_failed:
                    status_str = " \033[91m[FAILED]\033[0m"
                else:
                    status_str = " \033[92m[PASSED]\033[0m"
                print(line.rstrip('\r\n') + status_str, flush=True)
                current_test = None
                current_test_failed = False
            else:
                print(line, end='', flush=True)
            
            if not no_kill:
                # Watch for completion status signals in stdout
                if "[rpytest] Status:" in line:
                    if "FAILED" in line or "ERROR" in line:
                        any_test_failed = True
                    print("\n[Runner] Test execution completed. Terminating Ren'Py process...")
                    clean_termination = True
                    process.terminate()
                    break
                    
                # Enforce safety timeout
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
        print("-" * 60)
        print("[Runner] Execution finished.")
        if rc != 0 and not clean_termination:
            any_test_failed = True
            
        if any_test_failed:
            print("\n[Runner] --- FAILURE DIAGNOSTICS (errors.txt / traceback.txt) ---")
            for filename in ["errors.txt", "traceback.txt"]:
                filepath = os.path.join(PROJECT_DIR, filename)
                if os.path.exists(filepath):
                    print(f"=== {filename} ===")
                    try:
                        with open(filepath, "r", encoding="utf-8-sig", errors="ignore") as f:
                            content = f.read().strip()
                            if content:
                                try:
                                    print(content)
                                except UnicodeEncodeError:
                                    print(content.encode("ascii", "backslashreplace").decode("ascii"))
                            else:
                                print("(empty)")
                    except Exception as e:
                        print(f"Failed to read {filename}: {e}")
            
    return not any_test_failed

def cmd_test(test_suite: str = "global", no_kill: bool = False, exclude_e2e: bool = False, timeout: float = 30.0) -> None:
    """Executes test suite(s). If exclude_e2e is True, discovers and runs all non-E2E testsuites."""
    if exclude_e2e:
        suites = discover_test_suites(exclude_e2e=True)
        print(f"[Runner] Excluding E2E test suites. Discovered {len(suites)} non-E2E suite(s): {suites}")
        overall_success = True
        for suite in suites:
            success = cmd_test_single(suite, no_kill=no_kill, timeout=timeout)
            if not success:
                overall_success = False
        if not overall_success:
            sys.exit(1)
    else:
        success = cmd_test_single(test_suite, no_kill=no_kill, timeout=timeout)
        if not success:
            sys.exit(1)

def cmd_clean(verbose: bool = False) -> None:
    """Removes compiled Ren'Py and Python files from the project directory."""
    clean_extensions = {".rpyc", ".rpymc", ".rpyb", ".pyc", ".pyo"}
    ignore_dirs = {".git", ".venv", "venv", ".idea", ".vscode"}
    
    print("=== Ren'Py Compiled Files Cleanup ===")
    deleted_count = 0
    total_bytes_freed = 0
    deleted_by_ext: dict[str, int] = {}
    
    for root, dirs, files in os.walk(PROJECT_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            _, ext = os.path.splitext(file)
            ext_lower = ext.lower()
            if ext_lower in clean_extensions:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, PROJECT_DIR)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_count += 1
                    total_bytes_freed += file_size
                    deleted_by_ext[ext_lower] = deleted_by_ext.get(ext_lower, 0) + 1
                    if verbose:
                        print(f"[Clean] Removed: {rel_path}")
                except Exception as e:
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

def cmd_setup() -> None:
    """Configures project settings (e.g., git hooks) and runs verification."""
    print("=== Ren'Py Project Setup ===")
    try:
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], check=True)
        print("[OK] Configured Git to use '.githooks/' directory for hooks.")
    except Exception as e:
        print(f"[ERROR] Failed to configure Git hooks path: {e}")
        print("Please ensure Git is installed and you are inside the Git repository.")
        sys.exit(1)
        
    print("\nRunning verification tests...")
    cmd_verify()

class _NoAuthRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
        new_req.remove_header("Authorization")
        return new_req

def get_git_token() -> str:
    try:
        p = subprocess.Popen(["git", "credential", "fill"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        out, _ = p.communicate("url=https://github.com\n")
        for line in out.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return ""

def fetch_ci_logs(run_id: int) -> None:
    token = get_git_token()
    if not token:
        return
    try:
        import json
        jobs_url = f"https://api.github.com/repos/Impastaqqq/norilsk2/actions/runs/{run_id}/jobs"
        req = urllib.request.Request(jobs_url, headers={"User-Agent": "Mozilla/5.0", "Authorization": f"token {token}"})
        with urllib.request.urlopen(req) as resp:
            jobs_data = json.loads(resp.read().decode("utf-8"))
            jobs = jobs_data.get("jobs", [])
            if not jobs:
                return
            job_id = jobs[0]["id"]
            
        logs_url = f"https://api.github.com/repos/Impastaqqq/norilsk2/actions/jobs/{job_id}/logs"
        log_req = urllib.request.Request(logs_url, headers={"User-Agent": "Mozilla/5.0", "Authorization": f"Bearer {token}"})
        opener = urllib.request.build_opener(_NoAuthRedirectHandler())
        with opener.open(log_req) as log_resp:
            content = log_resp.read().decode("utf-8", errors="ignore")
            print(f"\n=== CI Log Stream Output (Run #{run_id}, Job #{job_id}) ===")
            matching_lines = [line for line in content.splitlines() if any(k in line for k in ["[rpytest]", "DIAGNOSTIC", "RenpyTestTimeoutError", "ERRORS", "TRACEBACK", "FAILED", "PASSED"])]
            if matching_lines:
                print("\n".join(matching_lines[-60:]))
            else:
                print("\n".join(content.splitlines()[-40:]))
    except Exception as e:
        print(f"[CI Log Fetcher Warning] Could not fetch log stream: {e}")

def cmd_ci_status(watch: bool = False) -> None:
    """Queries GitHub Actions REST API for recent workflow runs."""
    token = get_git_token()
    headers = {"User-Agent": "Mozilla/5.0"}
    if token:
        headers["Authorization"] = f"token {token}"
        
    url = "https://api.github.com/repos/Impastaqqq/norilsk2/actions/runs"
    print("=== GitHub Actions CI Status ===")
    
    while True:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                runs = data.get("workflow_runs", [])
                if not runs:
                    print("No workflow runs found.")
                    return
                
                latest = runs[0]
                run_id = latest.get("id")
                status = latest.get("status")
                conclusion = latest.get("conclusion")
                branch = latest.get("head_branch")
                commit_msg = latest.get("head_commit", {}).get("message", "").split("\n")[0]
                
                print(f"[CI] Latest Run #{run_id} (Branch: '{branch}')")
                print(f"     Commit: '{commit_msg}'")
                print(f"     Status: {status} | Conclusion: {conclusion}")
                
                if not watch or status == "completed":
                    if conclusion == "failure":
                        fetch_ci_logs(run_id)
                    break
                
                print("     [Watching] Waiting 10s for workflow run to complete...")
                time.sleep(10)
        except Exception as e:
            print(f"[ERROR] Failed to query GitHub Actions API: {e}")
            break

def print_help() -> None:
    print("""Ren'Py CLI Runner Utility

Usage:
  python manage.py run                 Launch the game normally
  python manage.py lint                Run Ren'Py built-in static analysis
  python manage.py clean [-v|--verbose] Clean compiled Ren'Py (*.rpyc) and Python files
  python manage.py warp <scene:line>   Launch the game directly at a script line
  python manage.py test [suite]        Run tests (default suite: global)
                                       Options:
                                         --exclude-e2e    Run all testsuites except E2E UI testsuites
                                         --no-kill        Keep the process alive for manual runs/validation
                                         --timeout <sec>  Set safety timeout in seconds (default: 30.0)
  python manage.py verify              Verify paths, .env, and binary dependencies
  python manage.py setup               Configure shared git hooks and verify the project environment
  python manage.py ci-status [--watch] Query status of GitHub Actions workflow runs
""")

def main() -> None:
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    
    if cmd == "verify":
        cmd_verify()
    elif cmd == "setup":
        cmd_setup()
    elif cmd == "run":
        cmd_run()
    elif cmd == "clean":
        args = sys.argv[2:]
        verbose = "-v" in args or "--verbose" in args
        cmd_clean(verbose=verbose)
    elif cmd == "lint":
        cmd_lint()
    elif cmd == "warp":
        if len(sys.argv) < 3:
            print("[Error] Missing warp destination. Format: game/scripts/...:line")
            sys.exit(1)
        cmd_warp(sys.argv[2])
    elif cmd == "test":
        args = sys.argv[2:]
        no_kill = False
        exclude_e2e = False
        timeout = 30.0
        
        if "--no-kill" in args:
            no_kill = True
            args.remove("--no-kill")
        if "--exclude-e2e" in args:
            exclude_e2e = True
            args.remove("--exclude-e2e")
            
        # Parse --timeout option
        for arg in list(args):
            if arg.startswith("--timeout="):
                try:
                    timeout = float(arg.split("=", 1)[1])
                    args.remove(arg)
                except ValueError:
                    pass
            elif arg == "--timeout" and args.index(arg) + 1 < len(args):
                idx = args.index(arg)
                try:
                    timeout = float(args[idx + 1])
                    args.pop(idx + 1)
                    args.pop(idx)
                except ValueError:
                    pass
                    
        suite = args[0] if args else "global"
        cmd_test(suite, no_kill=no_kill, exclude_e2e=exclude_e2e, timeout=timeout)
    elif cmd == "ci-status":
        args = sys.argv[2:]
        watch = "--watch" in args or "-w" in args
        cmd_ci_status(watch=watch)
    else:
        print(f"[Error] Unknown command: '{cmd}'\n")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()


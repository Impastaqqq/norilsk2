# manage.py
"""
Ultra-thin launcher for Ren'Py Build Tools.
Resolves active version source directory and proxies commands into .renpy-tools/proxy.py.
"""
import os
import sys

def main() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    tools_dir = os.path.join(root, ".renpy-tools")
    version_file = os.path.join(tools_dir, "CURRENT_VERSION")

    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            ver = f.read().strip()
        source_dir = os.path.join(tools_dir, f"rtools-{ver}")
    else:
        source_dir = tools_dir

    if not os.path.exists(source_dir):
        print(f"[Error] Ren'Py build tools source directory not found: {source_dir}")
        sys.exit(1)

    if source_dir not in sys.path:
        sys.path.insert(0, source_dir)

    try:
        import proxy
    except ImportError as e:
        print(f"[Error] Failed to load tool proxy from '{source_dir}': {e}")
        sys.exit(1)

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(proxy.get_help())
        sys.exit(0)

    proxy.run_command(sys.argv[1], sys.argv[2:])

if __name__ == "__main__":
    main()

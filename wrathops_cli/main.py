import sys
from wrathops_cli.install import install_hook
from wrathops_cli.scanner import scan_repo

def main():
    if len(sys.argv) < 2:
        print("Usage: wrathops [install | scan]")
        sys.exit(1)   # 🔥 ensure proper exit

    cmd = sys.argv[1]

    if cmd == "install":
        install_hook()

    elif cmd == "scan":
        result = scan_repo()
        if not result:
            sys.exit(1)   # 🔥 required for commit blocking
        else:
            print("✅ No secrets found")
            sys.exit(0)   # 🔥 explicit success

    else:
        print("Unknown command")
        sys.exit(1)   # 🔥 fail for invalid command
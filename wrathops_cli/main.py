import sys
from wrathops_cli.install import install_hook
from wrathops_cli.scanner import scan_repo

def main():
    if len(sys.argv) < 2:
        print("Usage: wrathops [install | scan]")
        return

    cmd = sys.argv[1]

    if cmd == "install":
        install_hook()

    elif cmd == "scan":
        result = scan_repo()
        if not result:
            sys.exit(1)
        print("✅ No secrets found")

    else:
        print("Unknown command")
import sys

from .tui import run


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    run()


if __name__ == "__main__":
    main()

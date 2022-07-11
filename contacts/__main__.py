"""Contacts entry point script."""
# contacts/__main__.py

from contacts import cli, __app_name__

def main():
  cli.app(prog_name=__app_name__)

if __name__ == '__main__':
  main()
"""This module provides the contacts CLI."""
# contacts/cli.py

from pathlib import Path
from typing import List, Optional
import typer
from contacts import ERRORS, __app_name__, __version__, config, database, contacts

app = typer.Typer()

@app.command()
def init(
  db_path: str = typer.Option(
    str(database.DEFAULT_DB_FILE_PATH),
    "--db-path",
    "-db",
    prompt="contacts database location?"
  ),
) -> None:
  """Initialize the contacts database"""
  app_init_error = config.init_app(db_path)
  if app_init_error:
    typer.secho(
      f'Creating config file failed with "{ERRORS[app_init_error]}"',
      fg=typer.colors.RED
    )
    raise typer.Exit(1)
  db_init_error = database.init_database(Path(db_path))
  if db_init_error:
    typer.secho(
      f'Creating database failed with "{ERRORS[db_init_error]}"',
      fg=typer.colors.RED
    )
    raise typer.Exit(1)
  else:
    typer.secho(f"The contacts database is {db_path}", fg=typer.colors.GREEN)

def get_contact_maker() -> contacts.ContactMaker:
  if config.CONFIG_FILE_PATH.exists():
    db_path = database.get_database_path(config.CONFIG_FILE_PATH)
  else:
    typer.secho(
      'Config file not found. Please run "contacts init"',
      fg=typer.colors.RED
    )
    raise typer.Exit(1)
  if db_path.exists():
    return contacts.ContactMaker(db_path)
  else:
    typer.secho(
      'Database not found. Please run "contacts init"',
      fg=typer.colors.RED
    )
    raise typer.Exit(1)
 
@app.command(name='add')
def add(
  first: str,
  last: str = typer.Option(..., prompt=True),
  mobile: str = typer.Option(..., prompt=True),
  email: str = typer.Option(..., prompt=True)
) -> None:
  """Add a new contact"""
  contact_maker = get_contact_maker()
  contact, error = contact_maker.add(first, last, mobile, email)
  if error:
    typer.secho(
      f'Adding contact failed with {ERRORS[error]}',
      fg=typer.colors.RED
    )
    raise typer.Exit(1)
  else:
    typer.secho(
      f'Contact: "{contact["First"]} {contact["Last"]}" was added ' 
      f'with mobile #: {contact["Mobile"]} and email: {contact["email"]}',
      fg=typer.colors.GREEN
    )

@app.command(name='list')
def list_all() -> None:
  """List all contacts."""
  contact_maker = get_contact_maker()
  contact_list = contact_maker.get_contact_list()
  if len(contact_list) == 0:
    typer.secho(
      'There are no contacts in the database yet.', fg=typer.colors.RED
    )
    raise typer.Exit()
  typer.secho('\ncontact list:\n', fg=typer.colors.BLUE, bold=True)
  columns = (
    "ID.  ",
    "First Name  ",
    "Last Name   ",
    "Mobile #    ",
    "email       "
  )
  headers = "".join(columns)
  typer.secho(headers, fg=typer.colors.BLUE, bold=True)
  typer.secho("-" * (len(headers) + 10), fg=typer.colors.BLUE)
  for id, contact in enumerate(contact_list, 1):
    first, last, mobile, email = contact.values()
    typer.secho(
      f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
      f"| {first}{(len(columns[1]) - len(str(first)) - 4) * ' '}"
      f"| {last}{(len(columns[2]) - len(str(last)) - 4) * ' '}"
      f"| {mobile}{(len(columns[3]) - len(str(mobile)) - 4) * ' '}"
      f"| {email}{(len(columns[4]) - len(str(email)) - 4) * ' '}",
      fg=typer.colors.BLUE
    )
  typer.secho("-" * (len(headers) + 10) + "\n", fg=typer.colors.BLUE)

def _version_callback(value: bool) -> None:
  if value:
    typer.echo(f'{__app_name__} v{__version__}')
    raise typer.Exit()

@app.callback()
def main(
  version: Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show application's version and exit",
    callback=_version_callback,
    is_eager=True
  )
) -> None:
  return
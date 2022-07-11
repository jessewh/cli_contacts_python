"""This module provides the contacts model-controller."""
# contacts/contacts.py

from typing import Any, Dict, List, NamedTuple
import re
import typer
from pathlib import Path
from contacts import DB_READ_ERROR
from contacts.database import DatabaseHandler

class CurrentContact(NamedTuple):
  contact: Dict[str, Any]
  error: int
  
class ContactMaker:
  def __init__(self, db_path: Path) -> None:
    self._db_handler = DatabaseHandler(db_path)
    
  def add(self, first: str, last: str, mobile: str, email: str) -> CurrentContact:
    """Add new contact to database."""
    email_re = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if not re.fullmatch(email_re, email):
      return typer.secho(f'{email} is invalid. Please check.')
    else: 
      contact = {
        "First": first,
        "Last": last,
        "Mobile": mobile,
        "email": email
      }
      read = self._db_handler.read_contacts()
      if read.error == DB_READ_ERROR:
        return CurrentContact(contact, read.error)
      read.contact_list.append(contact)
      write = self._db_handler.write_contacts(read.contact_list)
      return CurrentContact(contact, write.error)
    
    
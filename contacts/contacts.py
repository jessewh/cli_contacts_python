"""This module provides the contacts model-controller."""
# contacts/contacts.py

from typing import Any, Dict, List, NamedTuple
import re
import typer
from pathlib import Path
from contacts import DB_READ_ERROR, ID_ERROR
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
      typer.secho(f'{email} is invalid. Please check.')
      raise typer.Exit(1)
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
    
  def get_contact_list(self) -> List[Dict[str, Any]]:
    """Return the current contact list"""
    read = self._db_handler.read_contacts()
    # read = sorted(read, key=lambda contact: contact['First'])
    return read.contact_list
  
  # def edit_mobile(self, contact_id: int):
  #   """Change a mobile number"""
  #   read = self._db_handler.read_contacts()
  #   if read.error:
  #     return CurrentContact({}, read.error)
  #   try:
  #     contact = read.contact_list[contact_id - 1]
  #   except IndexError:
  #     return CurrentContact({}, read.error)
    
    
    
    
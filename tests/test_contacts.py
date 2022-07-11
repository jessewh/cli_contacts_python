# tests/test_contacts.py
import json
import pytest
from typer.testing import CliRunner
from contacts import (
  DB_READ_ERROR,
  SUCCESS,
  __app_name__,
  __version__,
  cli,
  contacts
)

runner = CliRunner()

def test_version():
  result = runner.invoke(cli.app, ["--version"])
  assert result.exit_code == 0
  assert f"{__app_name__} v{__version__}\n" in result.stdout
  
@pytest.fixture
def mock_json_file(tmp_path):
  contact = [{"first": "Jesse", "last": "Hardage", "mobile": "+447728387541", "email": "jesse.hardage1@gmail.com"}]
  db_file = tmp_path / "contacts.json"
  with db_file.open("w") as db:
    json.dump(contact, db, indent=4)
  return db_file

test_data1 = {
  "First": "Jesse",
  "Last": "Hardage",
  "Mobile": "+447728387541",
  "email": "jesse.hardage1@gmail.com",
  "contact": {
    "First": "Jesse",
    "Last": "Hardage",
    "Mobile": "+447728387541",
    "email": "jesse.hardage1@gmail.com"
  }
}

test_data2 = {
  "First": "Jimbo",
  "Last": "Jones",
  "Mobile": "+449989987651",
  "email": "jimmy.jones@gmail.com",
  "contact": {
    "First": "Jimbo",
    "Last": "Jones",
    "Mobile": "+449989987651",
    "email": "jimmy.jones@gmail.com"
  }
}

@pytest.mark.parametrize(
  "first, last, mobile, email, expected",
  [
    pytest.param(
      test_data1["First"],
      test_data1["Last"],
      test_data1["Mobile"],
      test_data1["email"],
      (test_data1["contact"], SUCCESS),
    ),
    pytest.param(
      test_data2["First"],
      test_data2["Last"],
      test_data2["Mobile"],
      test_data2["email"],
      (test_data2["contact"], SUCCESS),
    ),
  ],
)

def test_add(mock_json_file, first, last, mobile, email, expected):
  contact_maker = contacts.ContactMaker(mock_json_file)
  assert contact_maker.add(first, last, mobile, email) == expected
  read = contact_maker._db_handler.read_contacts()
  assert len(read.contact_list) == 2

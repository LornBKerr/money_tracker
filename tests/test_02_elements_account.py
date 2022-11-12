import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal, Element

from elements import Account

database = "test.db"


def close_database(dbref):
    dbref.sql_close()


@pytest.fixture
def open_database(tmpdir):
    path = tmpdir.join(database)
    dbref = Dbal()
    dbref.sql_connect(path)
    return dbref


@pytest.fixture
def create_accounts_table(open_database):
    dbref = open_database
    dbref.sql_query("DROP TABLE IF EXISTS 'accounts'")
    create_table = (
        'CREATE TABLE IF NOT EXISTS "accounts"'
        + '("record_id" INTEGER NOT NULL,'
        + '"name" TEXT NOT NULL,'
        + '"description" TEXT,'
        + '"company" TEXT,'
        + '"account_number" TEXT,'
        + '"check_writing_avail", '
        + '"account_separate" BOOLEAN,'
        + '"hide_in_transaction_list" BOOLEAN,'
        + '"hide_in_account_lists" TEXT,'
        + '"remarks" TEXT,'
        + 'PRIMARY KEY("record_id" AUTOINCREMENT)'
        + ")"
    )
    result = dbref.sql_query(create_table)
    return dbref


# set account values for tests
account_values = {
    "record_id": 10,
    "name": "Cash",
    "description": "a description",
    "company": "SlimyBank",
    "account_number": "124356987",
    "check_writing_avail": False,
    "account_separate": False,
    "hide_in_transaction_list": False,
    "hide_in_account_lists": False,
    "remarks": "a bank account",
}

sparse_values = {"record_id": 10, "name": "Cash"}

string_too_long = (
    "ShortTermCapitalGainsShortTermCapitalGains"
    + "ShortTermCapitalGainsShortTermCapitalGains"
    + "ShortTermCapitalGainsShortTermCapitalGains"
    + "ShortTermCapitalGainsShortTermCapitalGains"
)


def test_0201_constr(open_database):
    dbref = open_database
    account = Account(dbref)
    assert type(account) == Account
    assert isinstance(account, Element)
    close_database(dbref)


def test_0202_get_table(open_database):
    dbref = open_database
    account = Account(dbref)
    assert account.get_table() == "accounts"
    close_database(dbref)


def test_0203_get_dbref(open_database):
    dbref = open_database
    account = Account(dbref)
    assert account.get_dbref() == dbref
    close_database(dbref)


def test_0204_set_get_name(open_database):
    dbref = open_database
    account = Account(dbref)
    defaults = account.get_initial_values()
    account._set_property("name", account_values["name"])
    assert account_values["name"] == account.get_name()
    account._set_property("name", None)
    assert account.defaults["name"] == account.get_name()

    result = account.set_name(None)
    assert not result["valid"]
    assert result["entry"] == None
    assert len(result["msg"]) > 0

    result = account.set_name(account.defaults["name"])
    assert result["entry"] == account.defaults["name"]
    assert not result["valid"]  # valid name is required
    assert len(result["msg"]) > 0
    name = account.get_name()
    assert name == account.defaults["name"]

    result = account.set_name(account_values["name"])
    assert result["valid"]  # good name
    assert result["entry"] == account_values["name"]
    assert len(result["msg"]) == 0
    stored_name = account._get_property("name")
    assert stored_name == account_values["name"]
    name = account.get_name()
    assert name == account_values["name"]

    result = account.set_name(string_too_long)
    assert result["entry"] == string_too_long
    assert not result["valid"]  # bad name too long
    assert len(result["msg"]) > 0
    close_database(dbref)


def test_0205_set_get_description(open_database):
    dbref = open_database
    account = Account(dbref)
    defaults = account.get_initial_values()
    account._set_property("description", account_values["description"])
    assert account_values["description"] == account.get_description()
    account._set_property("description", None)
    assert account.defaults["description"] == account.get_description()

    result = account.set_description(None)
    assert not result["valid"]
    assert result["entry"] == None
    assert len(result["msg"]) > 0

    result = account.set_description(account.defaults["description"])
    assert result["entry"] == account.defaults["description"]
    assert result["valid"]  # optional so no description is valid
    assert len(result["msg"]) == 0
    description = account.get_description()
    assert description == account.defaults["description"]

    result = account.set_description(account_values["description"])
    assert result["valid"]  # good description
    assert result["entry"] == account_values["description"]
    assert len(result["msg"]) == 0
    stored_description = account._get_property("description")
    assert stored_description == account_values["description"]
    description = account.get_description()
    assert description == account_values["description"]

    extra_long_string = string_too_long + string_too_long
    result = account.set_description(extra_long_string)
    assert result["entry"] == extra_long_string
    assert not result["valid"]  # bad description too long
    assert len(result["msg"]) > 0
    close_database(dbref)


def test_0206_set_get_company(open_database):
    dbref = open_database
    account = Account(dbref)
    defaults = account.get_initial_values()
    account._set_property("company", account_values["company"])
    assert account_values["company"] == account.get_company()
    account._set_property("company", None)
    assert account.defaults["company"] == account.get_company()

    result = account.set_company(None)
    assert not result["valid"]
    assert result["entry"] == None
    assert len(result["msg"]) > 0

    result = account.set_company(account.defaults["company"])
    assert result["entry"] == account.defaults["company"]
    assert not result["valid"]  # required so empty string not valid
    assert len(result["msg"]) >= 0
    company = account.get_company()
    assert company == account.defaults["company"]

    result = account.set_company(account_values["company"])
    assert result["valid"]  # good company
    assert result["entry"] == account_values["company"]
    assert len(result["msg"]) == 0
    stored_company = account._get_property("company")
    assert stored_company == account_values["company"]
    company = account.get_company()
    assert company == account_values["company"]

    result = account.set_company(string_too_long)
    assert result["entry"] == string_too_long
    assert not result["valid"]  # bad company too long
    assert len(result["msg"]) > 0
    close_database(dbref)


def test_0207_set_get_account_number(open_database):
    dbref = open_database
    account = Account(dbref)
    defaults = account.get_initial_values()
    account._set_property("account_number", account_values["account_number"])
    assert account_values["account_number"] == account.get_account_number()
    account._set_property("account_number", None)
    assert account.defaults["account_number"] == account.get_account_number()

    result = account.set_account_number(None)
    assert not result["valid"]
    assert result["entry"] == None
    assert len(result["msg"]) > 0

    result = account.set_account_number(account.defaults["account_number"])
    assert result["entry"] == account.defaults["account_number"]
    assert result["valid"]  # optional so empty string is valid
    assert len(result["msg"]) >= 0
    account_number = account.get_account_number()
    assert account_number == account.defaults["account_number"]

    result = account.set_account_number(account_values["account_number"])
    assert result["valid"]  # good account_number
    assert result["entry"] == account_values["account_number"]
    assert len(result["msg"]) == 0
    stored_account_number = account._get_property("account_number")
    assert stored_account_number == account_values["account_number"]
    account_number = account.get_account_number()
    assert account_number == account_values["account_number"]

    result = account.set_account_number(string_too_long)
    assert result["entry"] == string_too_long
    assert not result["valid"]  # bad account_number too long
    assert len(result["msg"]) > 0
    close_database(dbref)


def test_0208_get_set_check_writing_avail(open_database):
    dbref = open_database
    account = Account(dbref)
    defaults = account.get_initial_values()
    account._set_property("check_writing_avail", account_values["check_writing_avail"])
    assert account_values["check_writing_avail"] == account.get_check_writing_avail()
    account._set_property("check_writing_avail", None)
    assert defaults["check_writing_avail"] == account.get_check_writing_avail()
    result = account.set_check_writing_avail(None)
    assert not result["valid"]
    assert result["entry"] == 0
    result = account.set_check_writing_avail(3)
    assert not result["valid"]
    assert result["entry"] == 0
    result = account.set_check_writing_avail(account_values["check_writing_avail"])
    assert result["valid"]
    assert result["entry"] == account_values["check_writing_avail"]
    assert result["entry"] == account.get_check_writing_avail()
    close_database(dbref)


def test_0209_get_set_account_separate(open_database):
    dbref = open_database
    account = Account(dbref)
    defaults = account.get_initial_values()
    account._set_property("account_separate", account_values["account_separate"])
    assert account_values["account_separate"] == account.get_account_separate()
    account._set_property("account_separate", None)
    assert defaults["account_separate"] == account.get_account_separate()
    result = account.set_account_separate(None)
    assert not result["valid"]
    assert result["entry"] == 0
    result = account.set_account_separate(3)
    assert not result["valid"]
    assert result["entry"] == 0
    result = account.set_account_separate(account_values["account_separate"])
    assert result["valid"]
    assert result["entry"] == account_values["account_separate"]
    assert result["entry"] == account.get_account_separate()
    close_database(dbref)


def test_0210_get_set_hide_in_transaction_list(open_database):
    dbref = open_database
    account = Account(dbref)
    defaults = account.get_initial_values()
    account._set_property(
        "hide_in_transaction_list", account_values["hide_in_transaction_list"]
    )
    assert (
        account_values["hide_in_transaction_list"]
        == account.get_hide_in_transaction_list()
    )
    account._set_property("hide_in_transaction_list", None)
    assert (
        defaults["hide_in_transaction_list"] == account.get_hide_in_transaction_list()
    )
    result = account.set_account_separate(None)
    assert not result["valid"]
    assert result["entry"] == 0
    result = account.set_hide_in_transaction_list(3)
    assert not result["valid"]
    assert result["entry"] == 0
    result = account.set_hide_in_transaction_list(
        account_values["hide_in_transaction_list"]
    )
    assert result["valid"]
    assert result["entry"] == account_values["hide_in_transaction_list"]
    assert result["entry"] == account.get_hide_in_transaction_list()
    close_database(dbref)


def test_0211_get_set_hide_in_account_lists(open_database):
    dbref = open_database
    account = Account(dbref)
    defaults = account.get_initial_values()
    account._set_property(
        "hide_in_account_lists", account_values["hide_in_account_lists"]
    )
    assert (
        account_values["hide_in_account_lists"] == account.get_hide_in_account_lists()
    )
    account._set_property("hide_in_account_lists", None)
    assert defaults["hide_in_account_lists"] == account.get_hide_in_account_lists()
    result = account.set_account_separate(None)
    assert not result["valid"]
    assert result["entry"] == 0
    result = account.set_hide_in_account_lists(3)
    assert not result["valid"]
    assert result["entry"] == 0
    result = account.set_hide_in_account_lists(account_values["hide_in_account_lists"])
    assert result["valid"]
    assert result["entry"] == account_values["hide_in_account_lists"]
    assert result["entry"] == account.get_hide_in_account_lists()
    close_database(dbref)


def test_0212_get_default_property_values(open_database):
    dbref = open_database
    account = Account(dbref)
    assert isinstance(account.get_properties(), dict)
    assert account.get_record_id() == account.defaults["record_id"]
    assert account.get_name() == account.defaults["name"]
    assert account.get_description() == account.defaults["description"]
    assert account.get_company() == account.defaults["company"]
    assert account.get_account_number() == account.defaults["account_number"]
    assert account.get_account_separate() == account.defaults["account_separate"]
    assert (
        account.get_hide_in_transaction_list()
        == account.defaults["hide_in_transaction_list"]
    )
    assert (
        account.get_hide_in_account_lists() == account.defaults["hide_in_account_lists"]
    )
    assert account.get_remarks() == account.defaults["remarks"]
    close_database(dbref)


def test_0213_set_properties_from_dict(open_database):
    # set Account from array
    dbref = open_database
    account = Account(dbref)
    account.set_properties(account_values)
    assert len(account.get_properties()) == len(account_values)
    assert account.get_record_id() == account_values["record_id"]
    assert account.get_name() == account_values["name"]
    assert account.get_description() == account_values["description"]
    assert account.get_company() == account_values["company"]
    assert account.get_account_number() == account_values["account_number"]
    assert account.get_check_writing_avail() == account_values["check_writing_avail"]
    assert account.get_account_separate() == account_values["account_separate"]
    assert (
        account.get_hide_in_transaction_list()
        == account_values["hide_in_transaction_list"]
    )
    assert (
        account.get_hide_in_account_lists() == account_values["hide_in_account_lists"]
    )
    assert account.get_remarks() == account_values["remarks"]
    close_database(dbref)


def test_0214_initial_partial_account_values(open_database):
    dbref = open_database
    account = Account(dbref, sparse_values)
    assert len(account.get_properties()) == len(account_values)
    assert account.get_record_id() == sparse_values["record_id"]
    assert account.get_name() == sparse_values["name"]
    assert account.get_description() == account.defaults["description"]
    assert account.get_company() == account.defaults["company"]
    assert account.get_account_number() == account.defaults["account_number"]
    assert account.get_check_writing_avail() == account.defaults["check_writing_avail"]
    assert account.get_account_separate() == account.defaults["account_separate"]
    assert (
        account.get_hide_in_transaction_list()
        == account.defaults["hide_in_transaction_list"]
    )
    assert (
        account.get_hide_in_account_lists() == account.defaults["hide_in_account_lists"]
    )
    assert account.get_remarks() == account.defaults["remarks"]
    close_database(dbref)


def test_0215_bad_column_name(open_database):
    dbref = open_database
    account = Account(dbref, None, "a_column")
    assert len(account.get_properties()) == len(account_values)
    assert account.get_record_id() == account.defaults["record_id"]
    assert account.get_name() == account.defaults["name"]
    assert account.get_description() == account.defaults["description"]
    assert account.get_company() == account.defaults["company"]
    assert account.get_account_number() == account.defaults["account_number"]
    assert account.get_check_writing_avail() == account.defaults["check_writing_avail"]
    assert account.get_account_separate() == account.defaults["account_separate"]
    assert (
        account.get_hide_in_transaction_list()
        == account.defaults["hide_in_transaction_list"]
    )
    assert (
        account.get_hide_in_account_lists() == account.defaults["hide_in_account_lists"]
    )
    assert account.get_remarks() == account.defaults["remarks"]
    close_database(dbref)


def test_0216_account_add(create_accounts_table):
    dbref = create_accounts_table
    account = Account(dbref, account_values)
    record_id = account.add()
    assert len(account.get_properties()) == len(account_values)
    assert account.get_record_id() == record_id
    assert account.get_name() == account_values["name"]
    assert account.get_description() == account_values["description"]
    assert account.get_company() == account_values["company"]
    assert account.get_account_number() == account_values["account_number"]
    assert account.get_check_writing_avail() == account_values["check_writing_avail"]
    assert account.get_account_separate() == account_values["account_separate"]
    assert (
        account.get_hide_in_transaction_list()
        == account_values["hide_in_transaction_list"]
    )
    assert (
        account.get_hide_in_account_lists() == account_values["hide_in_account_lists"]
    )
    assert account.get_remarks() == account_values["remarks"]
    close_database(dbref)


def test_0217_account_read_db(create_accounts_table):
    dbref = create_accounts_table
    account = Account(dbref)
    account.set_properties(account_values)
    record_id = account.add()
    assert record_id == 1
    # read db for existing account
    account2 = Account(dbref, 1)
    assert account2 is not None
    assert not account2.get_properties() is None
    assert record_id == account2.get_record_id()
    assert account2.get_name() == account_values["name"]
    assert account2.get_description() == account_values["description"]
    assert account2.get_company() == account_values["company"]
    assert account2.get_account_number() == account_values["account_number"]
    assert account2.get_check_writing_avail() == account_values["check_writing_avail"]
    assert account2.get_account_separate() == account_values["account_separate"]
    assert (
        account2.get_hide_in_transaction_list()
        == account_values["hide_in_transaction_list"]
    )
    assert (
        account2.get_hide_in_account_lists() == account_values["hide_in_account_lists"]
    )
    assert account2.get_remarks() == account_values["remarks"]
    # read db for non-existing account
    record_id = 5
    account3 = Account(dbref, record_id)
    assert len(account3.get_properties()) == len(account_values)
    assert not account3.get_record_id == record_id
    assert account3.get_record_id() == account.defaults["record_id"]
    close_database(dbref)


def test_0218_account_update(create_accounts_table):
    dbref = create_accounts_table
    account = Account(dbref)
    account.set_properties(account_values)
    record_id = account.add()
    assert record_id == 1
    assert account_values["account_number"] == account.get_account_number()
    assert account_values["check_writing_avail"] == account.get_check_writing_avail()
    assert account_values["account_separate"] == account.get_account_separate()
    # update acount_number and account_separate
    account.set_account_number("5431")
    account.set_account_separate(True)
    result = account.update()
    assert result
    account2 = Account(dbref, 1)
    assert account2.get_properties() is not None
    assert account2.get_record_id() == 1
    assert account2.get_name() == account_values["name"]
    assert account2.get_description() == account_values["description"]
    assert account2.get_company() == account_values["company"]
    assert account2.get_account_number() == "5431"
    assert account2.get_check_writing_avail() == account_values["check_writing_avail"]
    assert account2.get_account_separate()
    assert (
        account2.get_hide_in_transaction_list()
        == account_values["hide_in_transaction_list"]
    )
    assert (
        account2.get_hide_in_account_lists() == account_values["hide_in_account_lists"]
    )
    assert account2.get_remarks() == account_values["remarks"]
    close_database(dbref)


def test_0219_item_delete(create_accounts_table):
    dbref = create_accounts_table
    account = Account(dbref, account_values)
    account.add()
    # delete account
    result = account.delete()
    assert result
    # make sure it is really gone
    account = Account(dbref, 1)
    assert isinstance(account.get_properties(), dict)
    assert len(account.get_properties()) == len(account_values)
    assert account.get_record_id() == 0
    assert account.get_name() == ""
    close_database(dbref)


# end test_02_elements_account.py

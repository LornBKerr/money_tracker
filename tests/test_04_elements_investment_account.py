import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal

from constants import AccountType, BankAccountType, InvestmentAccountType
from elements import Account, InvestmentAccount

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
        'CREATE TABLE IF NOT EXISTS "accounts" '
        + '("record_id" INTEGER NOT NULL, '
        + '"name" TEXT NOT NULL, '
        + '"description" TEXT, '
        + '"company" TEXT, '
        + '"account_number" TEXT, '
        + '"account_separate" BOOLEAN, '
        + '"hide_in_transaction_list" BOOLEAN, '
        + '"hide_in_account_lists" BOOLEAN, '
        + '"check_writing_avail" BOOLEAN, '
        + '"account_type" INTEGER, '
        + '"subtype" INTEGER, '
        + '"tax_deferred" BOOLEAN, '
        + '"remarks" TEXT,'
        + 'PRIMARY KEY("record_id" AUTOINCREMENT)'
        + ")"
    )
    result = dbref.sql_query(create_table)
    return dbref


# set account values for tests
account_values = {
    "record_id": 10,
    "name": "My Account",
    "description": "a description",
    "company": "SlimyBank",
    "account_number": "124356987",
    "account_separate": False,
    "hide_in_transaction_list": False,
    "hide_in_account_lists": False,
    "check_writing_avail": True,
    "tax_deferred": False,
    "account_type": AccountType.INVESTMENT,
    "subtype": InvestmentAccountType.NO_TYPE,
    "remarks": "a bank account",
}

sparse_values = {
    "record_id": 10,
    "name": "Cash",
    "account_type": AccountType.INVESTMENT,
}


def test_0501_constr(open_database):
    dbref = open_database
    account = InvestmentAccount(dbref)
    assert type(account) is InvestmentAccount
    assert isinstance(account, Account)
    close_database(dbref)


def test_0502_get_table(open_database):
    dbref = open_database
    account = InvestmentAccount(dbref)
    assert account.get_table() == "accounts"
    close_database(dbref)


def test_0503_get_dbref(open_database):
    dbref = open_database
    account = InvestmentAccount(dbref)
    assert account.get_dbref() == dbref
    close_database(dbref)


def test_0504_set_get_type(open_database):
    dbref = open_database
    account = InvestmentAccount(dbref)
    account._set_property("account_type", account_values["account_type"])
    assert account_values["account_type"] == account.get_account_type()
    account._set_property("account_type", None)
    assert account.defaults["account_type"] == account.get_account_type()
    result = account.set_account_type(None)
    assert not result["valid"]
    assert result["entry"] == AccountType.NO_TYPE
    assert len(result["msg"]) > 0
    result = account.set_account_type(AccountType.NO_TYPE)
    assert not result["valid"]
    assert result["entry"] == AccountType.NO_TYPE
    assert len(result["msg"]) > 0
    result = account.set_account_type(AccountType.BANK)
    assert not result["valid"]
    assert result["entry"] == AccountType.NO_TYPE
    assert len(result["msg"]) > 0
    result = account.set_account_type(AccountType.INVESTMENT)
    assert result["valid"]
    assert result["entry"] == AccountType.INVESTMENT
    assert len(result["msg"]) == 0
    account_type = account._get_property("account_type")
    assert account_type == account_values["account_type"]
    assert account.get_account_type() == account_values["account_type"]
    close_database(dbref)


def test_0505_set_get_subtype(open_database):
    dbref = open_database
    account = InvestmentAccount(dbref)
    account._set_property("subtype", account_values["subtype"])
    assert account_values["subtype"] == account.get_subtype()
    account._set_property("subtype", None)
    assert account.defaults["subtype"] == account.get_subtype()
    result = account.set_subtype(None)
    assert not result["valid"]
    assert result["entry"] == InvestmentAccountType.NO_TYPE
    assert len(result["msg"]) > 0
    result = account.set_subtype(InvestmentAccountType.NO_TYPE)
    assert not result["valid"]
    assert result["entry"] == InvestmentAccountType.NO_TYPE
    assert len(result["msg"]) > 0
    result = account.set_subtype(InvestmentAccountType.BROKERAGE)
    assert result["valid"]
    assert result["entry"] == InvestmentAccountType.BROKERAGE
    assert len(result["msg"]) == 0
    assert account.get_subtype() == InvestmentAccountType.BROKERAGE
    result = account.set_subtype(InvestmentAccountType.SINGLE_FUND)
    assert result["valid"]
    assert result["entry"] == InvestmentAccountType.SINGLE_FUND
    assert len(result["msg"]) == 0
    assert account.get_subtype() == InvestmentAccountType.SINGLE_FUND
    result = account.set_subtype(BankAccountType.CD)
    assert not result["valid"]
    assert result["entry"] == InvestmentAccountType.NO_TYPE
    assert len(result["msg"]) > 0
    assert account.get_subtype() == InvestmentAccountType.NO_TYPE
    close_database(dbref)


def test_0506_get_set_tax_deferred(open_database):
    dbref = open_database
    account = InvestmentAccount(dbref)
    defaults = account.get_initial_values()
    account._set_property("tax_deferred", account_values["tax_deferred"])
    assert account_values["tax_deferred"] == account.get_tax_deferred()
    account._set_property("tax_deferred", None)
    assert defaults["tax_deferred"] == account.get_tax_deferred()
    result = account.set_tax_deferred(None)
    assert not result["valid"]
    assert result["entry"] == 0
    result = account.set_tax_deferred(3)
    assert not result["valid"]
    assert result["entry"] == 0
    result = account.set_tax_deferred(account_values["tax_deferred"])
    assert result["valid"]
    assert result["entry"] == account_values["tax_deferred"]
    assert result["entry"] == account.get_tax_deferred()
    close_database(dbref)


def test_0507_get_default_property_values(open_database):
    dbref = open_database
    account = InvestmentAccount(dbref)
    assert isinstance(account.get_properties(), dict)
    assert account.get_account_type() == account.defaults["account_type"]
    assert account.get_subtype() == account.defaults["subtype"]
    assert account.get_tax_deferred() == account.defaults["tax_deferred"]
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
    assert account.get_check_writing_avail() == account.defaults["check_writing_avail"]
    assert account.get_remarks() == account.defaults["remarks"]
    close_database(dbref)


def test_0507_set_properties_from_dict(open_database):
    # set InvestmentAccount from array
    dbref = open_database
    account = InvestmentAccount(dbref)
    account.set_properties(account_values)
    assert len(account.get_properties()) == len(account_values)
    assert account.get_account_type() == account_values["account_type"]
    assert account.get_subtype() == account_values["subtype"]
    assert account.get_tax_deferred() == account_values["tax_deferred"]
    assert account.get_record_id() == account_values["record_id"]
    assert account.get_name() == account_values["name"]
    assert account.get_description() == account_values["description"]
    assert account.get_company() == account_values["company"]
    assert account.get_account_number() == account_values["account_number"]
    assert account.get_account_separate() == account_values["account_separate"]
    assert (
        account.get_hide_in_transaction_list()
        == account_values["hide_in_transaction_list"]
    )
    assert (
        account.get_hide_in_account_lists() == account_values["hide_in_account_lists"]
    )
    assert account.get_check_writing_avail() == account_values["check_writing_avail"]
    assert account.get_remarks() == account_values["remarks"]
    close_database(dbref)


def test_0508_initial_partial_account_values(open_database):
    dbref = open_database
    account = InvestmentAccount(dbref, sparse_values)
    assert len(account.get_properties()) == len(account_values)
    assert account.get_record_id() == sparse_values["record_id"]
    assert account.get_name() == sparse_values["name"]
    assert account.get_account_type() == sparse_values["account_type"]
    assert account.get_subtype() == account.defaults["subtype"]
    assert account.get_tax_deferred() == account.defaults["tax_deferred"]
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
    assert account.get_check_writing_avail() == account.defaults["check_writing_avail"]
    assert account.get_remarks() == account.defaults["remarks"]
    close_database(dbref)


def test_0509_bad_column_name(open_database):
    dbref = open_database
    account = InvestmentAccount(dbref, None, "a_column")
    assert isinstance(account.get_properties(), dict)
    assert len(account.get_properties()) == len(account_values)
    assert account.get_account_type() == account.defaults["account_type"]
    assert account.get_subtype() == account.defaults["subtype"]
    assert account.get_tax_deferred() == account.defaults["tax_deferred"]
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
    assert account.get_check_writing_avail() == account.defaults["check_writing_avail"]
    assert account.get_remarks() == account.defaults["remarks"]
    close_database(dbref)


def test_0510_account_add(create_accounts_table):
    dbref = create_accounts_table
    account = InvestmentAccount(dbref, account_values)
    record_id = account.add()
    assert account.get_record_id() == record_id
    assert record_id == 1
    close_database(dbref)


def test_0511_account_read_db(create_accounts_table):
    dbref = create_accounts_table
    account = InvestmentAccount(dbref)
    account.set_properties(account_values)
    record_id = account.add()
    assert record_id == 1
    # read db for existing account
    assert account.get_account_type() == account_values["account_type"]
    assert account.get_subtype() == account_values["subtype"]
    assert account.get_tax_deferred() == account_values["tax_deferred"]
    assert account.get_record_id() == record_id
    assert account.get_name() == account_values["name"]
    assert account.get_description() == account_values["description"]
    assert account.get_company() == account_values["company"]
    assert account.get_account_number() == account_values["account_number"]
    assert account.get_account_separate() == account_values["account_separate"]
    assert (
        account.get_hide_in_transaction_list()
        == account_values["hide_in_transaction_list"]
    )
    assert (
        account.get_hide_in_account_lists() == account_values["hide_in_account_lists"]
    )
    assert account.get_check_writing_avail() == account_values["check_writing_avail"]
    assert account.get_remarks() == account_values["remarks"]
    # read db for non-existing account
    record_id = 5
    account3 = InvestmentAccount(dbref, record_id)
    assert len(account3.get_properties()) == len(account_values)
    assert not account3.get_record_id == record_id
    assert account3.get_account_type() == account.defaults["account_type"]
    assert account3.get_subtype() == account.defaults["subtype"]
    assert account3.get_record_id() == account.defaults["record_id"]
    assert account3.get_name() == account.defaults["name"]
    assert account3.get_description() == account.defaults["description"]
    assert account3.get_company() == account.defaults["company"]
    assert account3.get_account_number() == account.defaults["account_number"]
    assert account3.get_account_separate() == account.defaults["account_separate"]
    assert (
        account3.get_hide_in_transaction_list()
        == account.defaults["hide_in_transaction_list"]
    )
    assert (
        account3.get_hide_in_account_lists()
        == account.defaults["hide_in_account_lists"]
    )
    assert account3.get_check_writing_avail() == account.defaults["check_writing_avail"]
    assert account3.get_remarks() == account.defaults["remarks"]
    close_database(dbref)


def test_0512_account_update(create_accounts_table):
    dbref = create_accounts_table
    account = InvestmentAccount(dbref)
    account.set_properties(account_values)
    record_id = account.add()
    assert record_id == 1
    assert account_values["account_number"] == account.get_account_number()
    assert account_values["account_separate"] == account.get_account_separate()
    # update acount_number and account_separate
    account.set_account_number("5431")
    account.set_account_separate(True)
    result = account.update()
    assert result
    account2 = InvestmentAccount(dbref, 1)
    assert account2.get_properties() is not None
    assert account2.get_account_type() == account_values["account_type"]
    assert account2.get_subtype() == account_values["subtype"]
    assert account2.get_tax_deferred() == account_values["tax_deferred"]
    assert account2.get_record_id() == 1
    assert account2.get_name() == account_values["name"]
    assert account2.get_description() == account_values["description"]
    assert account2.get_company() == account_values["company"]
    assert account2.get_account_number() == "5431"
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


def test_0513_item_delete(create_accounts_table):
    dbref = create_accounts_table
    account = InvestmentAccount(dbref, account_values)
    account.add()
    # delete account
    result = account.delete()
    assert result
    # make sure it is really gone
    account = InvestmentAccount(dbref, 1)
    assert isinstance(account.get_properties(), dict)
    assert len(account.get_properties()) == len(account_values)
    assert account.get_record_id() == 0
    assert account.get_name() == ""
    close_database(dbref)


# end test_05_elements_investment_account

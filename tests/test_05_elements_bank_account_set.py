import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)
from lbk_library import Dbal, ElementSet

from constants.account_types import AccountType, BankAccountType
from elements.bank_account import BankAccount
from elements.bank_account_set import BankAccountSet

from db_support import (
    close_database,
    create_accounts_table,
    database,
    load_accounts_table,
    open_database,
)


def test_0501_constructor(create_accounts_table):
    dbref = create_accounts_table
    account_set = BankAccountSet(dbref)
    assert isinstance(account_set, BankAccountSet)
    assert isinstance(account_set, ElementSet)
    close_database(dbref)

def test_0502_get_dbref(create_accounts_table):
    dbref = create_accounts_table
    account_set = BankAccountSet(dbref)
    assert account_set.get_dbref() == dbref
    close_database(dbref)


def test_0503_get_table(create_accounts_table):
    dbref = create_accounts_table
    account_set = BankAccountSet(dbref)
    assert account_set.get_table() == "accounts"
    close_database(dbref)

def test_0504_all_rows_empty(create_accounts_table):
    dbref = create_accounts_table
    account_set = BankAccountSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + account_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(account_set.get_property_set())
    assert count == account_set.get_number_elements()
    close_database(dbref)

def test_0505_all_rows(create_accounts_table):
    dbref = create_accounts_table
    load_accounts_table(dbref)
    account_set = BankAccountSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + account_set.get_table() + " WHERE account_type = " + str(AccountType.BANK))
    count = dbref.sql_fetchrow(count_result)['COUNT(*)']
    assert count == len(account_set.get_property_set())
    close_database(dbref)

def test_0506_selected_rows(create_accounts_table):
    dbref = create_accounts_table
    load_accounts_table(dbref)
    account_set = BankAccountSet(dbref,'account_subtype', BankAccountType.CD)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + account_set.get_table() + " WHERE account_subtype = " + str(BankAccountType.CD))
    count = dbref.sql_fetchrow(count_result)['COUNT(*)']
    assert count == len(account_set.get_property_set())
    close_database(dbref)

def test_0507_ordered_selected_rows(create_accounts_table):
    dbref = create_accounts_table
    load_accounts_table(dbref)
    account_set = BankAccountSet(dbref,'account_subtype', BankAccountType.CD, 'name')
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + account_set.get_table() + " WHERE account_subtype = " + str(BankAccountType.CD))
    count = dbref.sql_fetchrow(count_result)['COUNT(*)']
    selected_set = account_set.get_property_set()
    assert count == len(selected_set)
    for counter in range(0, count - 2):
        account1 = selected_set[counter]
        account2 = selected_set[counter + 1]
        assert account1.get_name() < account2.get_name()
    close_database(dbref)
## end test_05_elements_account_set.py

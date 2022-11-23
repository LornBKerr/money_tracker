import pytest
import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal

from constants.account_types import AccountType, InvestmentAccountType
from elements.investment_account_set import InvestmentAccountSet

from db_support import (
    close_database,
    create_accounts_table,
    database,
    load_accounts_table,
    open_database,
)

def test_0601_constructor(create_accounts_table):
    dbref = create_accounts_table
    account_set = InvestmentAccountSet(dbref)
    assert isinstance(account_set,InvestmentAccountSet)
    close_database(dbref)
    
def test_0602_get_dbref(create_accounts_table):
    dbref = create_accounts_table
    account_set = InvestmentAccountSet(dbref)
    assert account_set.get_dbref() == dbref
    close_database(dbref)

def test_0603_get_table(create_accounts_table):
    dbref = create_accounts_table
    account_set = InvestmentAccountSet(dbref)
    assert account_set.get_table() == "accounts"
    close_database(dbref)

def test_0604_all_rows_empty(create_accounts_table):
    dbref = create_accounts_table
    account_set = InvestmentAccountSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + account_set.get_table())
    count = dbref.sql_fetchrow(count_result)['COUNT(*)']
    assert count == len(account_set.get_property_set())
    assert count == account_set.get_number_elements()
    close_database(dbref)

def test_0605_all_rows(create_accounts_table):
    dbref = create_accounts_table
    load_accounts_table(dbref)
    account_set = InvestmentAccountSet(dbref)
    print(account_set.get_property_set())
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + account_set.get_table() + " WHERE account_type = " + str(AccountType.INVESTMENT))
    count = dbref.sql_fetchrow(count_result)['COUNT(*)']
    assert count == len(account_set.get_property_set())
    close_database(dbref)

def test_0606_selected_rows(create_accounts_table):
    dbref = create_accounts_table
    load_accounts_table(dbref)
    account_set = InvestmentAccountSet(dbref,'account_subtype', InvestmentAccountType.SINGLE_FUND)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + account_set.get_table() + " WHERE account_subtype = " + str(InvestmentAccountType.SINGLE_FUND))
    count = dbref.sql_fetchrow(count_result)['COUNT(*)']
    assert count == len(account_set.get_property_set())
    close_database(dbref)

def test_0607_ordered_selected_rows(create_accounts_table):
    dbref = create_accounts_table
    load_accounts_table(dbref)
    account_set = InvestmentAccountSet(dbref,'account_subtype', InvestmentAccountType.BROKERAGE, 'name')
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + account_set.get_table() + " WHERE account_subtype = " + str(InvestmentAccountType.BROKERAGE))
    count = dbref.sql_fetchrow(count_result)['COUNT(*)']
    selected_set = account_set.get_property_set()
    assert count == len(selected_set)
    for counter in range(0, count - 2):
        account1 = selected_set[counter]
        account2 = selected_set[counter + 1]
        assert account1.get_name() < account2.get_name()
    close_database(dbref)
# end test_06_elements_account_set.py

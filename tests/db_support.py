import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal

from constants.account_types import AccountType, BankAccountType

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
        + '("record_id" INTEGER NOT NULL,'
        + '"account_type" INTEGER, '
        + '"account_subtype" INTEGER, '
        + '"name" TEXT NOT NULL, '
        + '"description" TEXT, '
        + '"company" TEXT, '
        + '"account_number" TEXT, '
        + '"account_separate" BOOLEAN, '
        + '"hide_in_transaction_list" BOOLEAN, '
        + '"hide_in_account_lists" BOOLEAN, '
        + '"check_writing_avail" BOOLEAN, '
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
    "account_type": AccountType.NO_TYPE,
    "account_subtype": AccountType.NO_TYPE,
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

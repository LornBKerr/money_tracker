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


string_too_long = (
    "ShortTermCapitalGainsShortTermCapitalGains"
    + "ShortTermCapitalGainsShortTermCapitalGains"
    + "ShortTermCapitalGainsShortTermCapitalGains"
    + "ShortTermCapitalGainsShortTermCapitalGains"
)


def load_accounts_table(dbref):
    columns = [
        "record_id",
        "account_type",
        "account_subtype",
        "name",
        "description",
        "company",
        "account_number",
        "account_separate",
        "hide_in_transaction_list",
        "hide_in_account_lists",
        "check_writing_avail",
        "tax_deferred",
        "remarks",
    ]
    value_set = [
        ["1", "18V672", "A", "1", "Rebuild", "1", "", ""],
        ["2", "BTB1108", "B", "1", "Usable", "0", "", ""],
        ["3", "X036", "D", "1", "Usable", "0", "", ""],
        ["4", "BTB1108", "CA", "1", "Usable", "0", "", ""],
        ["5", "22H1053", "BB", "1", "Usable", "0", "", ""],
        ["6", "268-090", "BC", "1", "Usable", "1", "", ""],
        ["8", "BTB1108", "BD", "1", "Usable", "1", "", ""],
        ["9", "X055", "EB", "1", "Usable", "1", "", ""],
        ["56", "BULB-1895", "JCIB", "2", "Replace", "1", "", "License Plate Lamp"],
        ["59", "158-520", "JCIA", "2", "Replace", "1", "", ""],
        ["70", "BTB1108", "CX", "1", "Usable", "1", "", ""],
    ]
    sql_query = {"type": "INSERT", "table": "accounts"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)

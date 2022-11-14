import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from constants import AccountType, BankAccountType, InvestmentAccountType


def test_0101_AccountType():
    assert AccountType.NO_TYPE == 0
    assert AccountType.BANK
    assert AccountType.INVESTMENT
    assert AccountType.TAX
    assert AccountType.NO_TYPE in AccountType.list()
    assert AccountType.BANK in AccountType.list()
    assert AccountType.INVESTMENT in AccountType.list()
    assert AccountType.TAX in AccountType.list()


def test_0102_BankAccountType():
    assert BankAccountType.NO_TYPE == 0
    assert BankAccountType.CHECKING
    assert BankAccountType.SAVINGS
    assert BankAccountType.CD
    assert BankAccountType.NO_TYPE in BankAccountType.list()
    assert BankAccountType.CHECKING in BankAccountType.list()
    assert BankAccountType.SAVINGS in BankAccountType.list()
    assert BankAccountType.CD in BankAccountType.list()


def test_0103_InvestmentAccountType():
    assert InvestmentAccountType.NO_TYPE == 0
    assert InvestmentAccountType.BROKERAGE
    assert InvestmentAccountType.SINGLE_FUND
    assert InvestmentAccountType.NO_TYPE in InvestmentAccountType.list()
    assert InvestmentAccountType.BROKERAGE in InvestmentAccountType.list()
    assert InvestmentAccountType.SINGLE_FUND in InvestmentAccountType.list()
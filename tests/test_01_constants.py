import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from constants.account_types import AccountType, BankAccountType, InvestmentAccountType
from constants.element_types import ElementType


def test_0101_ElementType():
    assert ElementType.NO_TYPE == 0
    assert ElementType.ACCOUNT
    #    assert ElementType.SECURITY
    #    assert ElementType.TRANSACTION
    #    assert ElementType.CATEGORY
    assert ElementType.NO_TYPE in ElementType.list()
    assert ElementType.ACCOUNT in ElementType.list()
    #    assert ElementType.SECURITY in ElementType.list()
    #    assert ElementType.TRANSACTION in ElementType.list()
    #    assert ElementType.CATEGORY in ElementType.list()


def test_0102_AccountType():
    assert AccountType.NO_TYPE
    assert AccountType.BANK
    assert AccountType.INVESTMENT
    assert AccountType.TAX
    assert AccountType.NO_TYPE in AccountType.list()
    assert AccountType.BANK in AccountType.list()
    assert AccountType.INVESTMENT in AccountType.list()
    assert AccountType.TAX in AccountType.list()


def test_0103_BankAccountType():
    assert BankAccountType.NO_TYPE
    assert BankAccountType.CHECKING
    assert BankAccountType.SAVINGS
    assert BankAccountType.CD
    assert BankAccountType.NO_TYPE in BankAccountType.list()
    assert BankAccountType.CHECKING in BankAccountType.list()
    assert BankAccountType.SAVINGS in BankAccountType.list()
    assert BankAccountType.CD in BankAccountType.list()


def test_0104_InvestmentAccountType():
    assert InvestmentAccountType.NO_TYPE
    assert InvestmentAccountType.BROKERAGE
    assert InvestmentAccountType.SINGLE_FUND
    assert InvestmentAccountType.NO_TYPE in InvestmentAccountType.list()
    assert InvestmentAccountType.BROKERAGE in InvestmentAccountType.list()
    assert InvestmentAccountType.SINGLE_FUND in InvestmentAccountType.list()

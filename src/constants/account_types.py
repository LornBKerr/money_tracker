"""
The account database elements used throughout the MoneyTrack program.

File:       account_types.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

from constants.element_types import ElementType


class AccountType:
    """
    Available account types.

    The defined account types for general use are 'Bank'
    accounts and  'Investment' accounts. A 'Tax' account is defined for
    internal use to support generating simplified income tax estimates.
    The NO_TYPE type is used to indicate no account type has been assigned.
    """

    ACCOUNT_TYPE_NASK = ElementType.ELEMENT_TYPE_MASK | 0x000F0
    NO_TYPE = ElementType.ACCOUNT | 0x00000
    BANK = ElementType.ACCOUNT | 0x00010
    INVESTMENT = ElementType.ACCOUNT | 0x00020
    TAX = ElementType.ACCOUNT | 0x00030

    @staticmethod
    def list() -> []:
        """
        Return a list of the defined AccountTypes.

        Returns:
            (list) a list of the available AccountTypes
        """
        return [
            AccountType.NO_TYPE,
            AccountType.BANK,
            AccountType.INVESTMENT,
            AccountType.TAX,
        ]

    # end list()


# end class AccountType


class BankAccountType:
    """
    Available bank account types.

    The defined Bank account types are standard 'Checking', 'Savings',
    'CD' accounts. The NO_TYPE type is used to indicate no account type has
    been assigned.
    """

    BANK_ACCOUNT_TYPE_NASK = ElementType.ELEMENT_TYPE_MASK | AccountType.BANK | 0x0000F

    NO_TYPE = AccountType.BANK | 0x0
    CHECKING = AccountType.BANK | 0x1
    SAVINGS = AccountType.BANK | 0x2
    CD = AccountType.BANK | 0x3

    @staticmethod
    def list() -> []:
        """
        Return a list of the defined BankAccountTypes.

        Returns:
            (list) a list of the available BankAccountTypes
        """
        return [
            BankAccountType.NO_TYPE,
            BankAccountType.CHECKING,
            BankAccountType.SAVINGS,
            BankAccountType.CD,
        ]

    # end list()


# end class BankAccountType


class InvestmentAccountType:
    """
    Available investment account types.

    The NO_TYPE type is used to indicate no account type has been assigned.
    """

    INVESTMENT_ACCOUNT_TYPE_MASK = (
        ElementType.ELEMENT_TYPE_MASK | AccountType.INVESTMENT | 0x0000F
    )
    NO_TYPE = AccountType.INVESTMENT | 0x0
    BROKERAGE = AccountType.INVESTMENT | 0x1
    SINGLE_FUND = AccountType.INVESTMENT | 0x2

    @staticmethod
    def list() -> []:
        """
        Return a list of the defined InvestmentAccountTypes.

        Returns:
            (list) a list of the available InvestmentAccountTypes
        """
        return [
            InvestmentAccountType.NO_TYPE,
            InvestmentAccountType.BROKERAGE,
            InvestmentAccountType.SINGLE_FUND,
        ]

    # end list()


# end class InvestmentAccountType

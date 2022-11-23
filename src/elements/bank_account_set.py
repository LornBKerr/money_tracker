"""
This is a set of BankAccounts in the database.

File:       bank_account_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

from lbk_library import Dbal, ElementSet

from constants.account_types import AccountType, BankAccountType
from elements.bank_account import BankAccount


class BankAccountSet(ElementSet):
    """
    Provides a set of BankAccounts from the database table 'accounts'.
    """

    def __init__(
        self,
        dbref: Dbal,
        where_column: str = None,
        where_value: int = BankAccountType.NO_TYPE,
        order_by_column: str = "name",
        limit: int = None,  # No limit
        offset: int = None,
    ) -> None:
        """
        Builds a set of BankAccounts from the database table 'accounts'.

        Parameters:
            dbref (Dbal): the dababase instance to use.
            where_column (int): column of the 'accounts' table to select
                the specific subset of bank accounts; default is no
                subset.
            where_value (int): Value of the specific subset requested;
                limited to the set of values in BankAccountTypes;
                default is BankAccountTypoes.NONE indicating no subset.
            order_by_column (str): column of the 'accounts' table to set
                the order of the bank_account_set. Default order is by
                the account name.
            limit (int): number of rows to retrieve, defaults to all.
            offset (int): row number to start retrieval, 0 based,
                defaults to row 0.
        """
        table_name = "accounts"  # The database table for this element
        element_type = BankAccount
        bank_account_column = "account_type"
        account_type = AccountType.BANK

        super().__init__(
            dbref,
            table_name,
            element_type,
            bank_account_column,
            account_type,
            order_by_column,
            limit,
            offset,
        )
        
        # Build the subset from the total bank account set
        subset = []
        if where_column != None and where_value in BankAccountType.list() and where_value != BankAccountType.NO_TYPE:
            for account in self.get_property_set():
                if account._get_property(where_column) == where_value:
                    subset.append(account)
            self.set_property_set(subset)
        # end __init__()

# end Class BankAccountSet

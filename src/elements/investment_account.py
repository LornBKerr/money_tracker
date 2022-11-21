"""
AInvestment account for the MoneyTrack program.

File:       investment_account.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

from copy import deepcopy
from typing import Any, Union

from lbk_library import Dbal

from constants.account_types import AccountType, InvestmentAccountType
from elements.account import Account


class InvestmentAccount(Account):
    """
    Implement an Investment Account in the database.

    This extends the basic Account and add state and functionality
    specific to investment accounts such as brokerage and mutual fund
    accounts.
    """

    def __init__(
        self, dbref: Dbal, account_key: Union[int, str] = None, column: str = None
    ) -> None:
        """
        Define an Investment Account.

        An Investment Account will always be type 'AccountType.INVESTMENT'.
         The account_subtype must be one of InvestmentAccountType.BROKERAGE or
        InvestmentAccountType.SINGLE_FUND.

        The 'column' can be set to None, "record_id", or "account_name".
        If not one of these three choices, both 'account_key' and 'column'
        are set to "None" and an Account with default values is constructed.
        The general defaults are: string values are set to
        empty string, numeric values are set to 0, and logical values
        are set to False.

        If account_key' is not given, the 'column' is ignored and an empty
        Account is constructed with all properties set to default values.

        If account_key is a dict{} object, the properties of this Account
        are set from the dict object.

        If 'account_key' is given as a single value, it must be either
        an 'record_id' or an 'account name' as indicated by 'column'.
        If 'column' is not given, 'record_id' is the default. The
        account will be constructed from the database for the specific
        value given by 'column' and 'account_key'

        Parameters:
            dbref (Dbal): reference to the database holding the element
            account_key (Mixed): - the specific key of the Account being
                constructed or a dict object of the values for an Account
                for direct insertion into the properties array. If a
                specific key, must be either an account name or
                record_id value and must be consistent with the type
                given by the column name.
            column(string): Either 'account_key' or 'name', default is
                None. Column name and account_key must be consistent,
        """
        super().__init__(dbref)

        # Default values for the Account
        self.defaults: dict[str, Any] = {
            "record_id": 0,
            "name": "",
            "description": "",
            "company": "",
            "account_number": "",
            "account_separate": False,
            "hide_in_transaction_list": False,
            "hide_in_account_lists": False,
            "check_writing_avail": False,
            "tax_deferred": False,
            "account_type": AccountType.INVESTMENT,
            "account_subtype": InvestmentAccountType.NO_TYPE,
            "remarks": "",
        }
        self.set_initial_values(deepcopy(self.defaults))
        self.clear_value_valid_flags()

        if isinstance(account_key, dict):
            # make sure there are no missing keys
            for key in self.defaults:
                if key not in account_key:
                    account_key[key] = deepcopy(self.defaults[key])

        if column is None:
            column = "record_id"

        if column not in ("record_id", "name"):
            account_key = None
            column = None

        if isinstance(account_key, (int, str)):
            account_key = self.get_properties_from_db(column, account_key)

        if not account_key:
            account_key = deepcopy(self.defaults)

        self.set_properties(account_key)
        self.set_initial_values(self.get_properties())
        self.clear_value_changed_flags()
        # end __init__()

    def set_properties(self, properties: dict[str, Any]) -> None:
        """
        Set the values of the Account properties array.

        Each property is validated for type and value within an acceptable
        range, with unacceptable values set to None. Properties not part
        of the element are discarded.

        Parameters:
            properties (dict): holding the element values. Keys must
                match the required keys of the element being modified,
                properties may be sparse.
        """
        if properties is not None and isinstance(properties, dict):
            super().set_properties(properties)

            for key in properties.keys():
                if key == "account_type":
                    self.__set_account_type(properties[key])
                elif key == "account_subtype":
                    self.set_account_subtype(properties[key])
                elif key == "tax_deferred":
                    self.set_tax_deferred(properties[key])
        # end set_properties()

    def get_account_type(self) -> int:
        """
        Get the Account type.

        This will always be the constant AccountType.INVESTMENT.

        Return:
            (str) The constant AccountType.INVESTMENT.
        """
        # always return the AccountType.INVESTMENT type
        return AccountType.INVESTMENT
        # end get_account_type()

    def __set_account_type(
        self, account_type: AccountType = AccountType.INVESTMENT
    ) -> dict[str, Any]:
        """
        Set the Account's type.

        This account type must be constant AccountType.INVESTMENT. If
        the supplied account_type is not AccountType.INVESTMENT, set the
        result to AccountType.INVESTMENT and return a valid result.

        Parameters:
            account_type (int): the type of this Account. The account
            type is optional and must be the constant
            AccountType.INVESTMENT. If the supplied account_type is not
            valid, the account type is set to the constant
            AccountType.INVESTMENT and the result will be valid.

        Returns:
            (dict): ['entry'] - (str) the updated account_type
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = {}

        if account_type != AccountType.INVESTMENT:
            account_type = AccountType.INVESTMENT

        result["entry"] = account_type
        result["valid"] = True
        result["msg"] = ""

        self._set_property("account_type", result["entry"])
        self.update_property_flags("account_type", result["entry"], result["valid"])
        return result
        # end set_account_type()

    def get_account_subtype(self) -> int:
        """
        Get the specific Investment Account type. This will be one of the types
        defined in the constants InvestmentAccountType. These type
        include 'BROKERAGE' and 'SINGLE_FUND'. The account_subtype
        InvestmentAccountType.NO_TYPE is returned for invalid account_subtypes.

        Return:
            (str) One of the constant InvestmentAccountType members
        """
        account_subtype = self._get_property("account_subtype")
        if (
            account_subtype not in InvestmentAccountType.list()
            or account_subtype is None
        ):
            account_subtype = InvestmentAccountType.NO_TYPE
        return account_subtype
        # end get_account_subtype()

    def set_account_subtype(
        self, account_subtype: InvestmentAccountType
    ) -> dict[str, Any]:
        """
        Set the Investment Account's specific type.

        This account_subtype must be one of the members of InvestmentAccountType.
        This includes 'BROKERAGE' or 'SINGLE_FUND'. The 'NO_TYPE'
        account_subtype indicates the account_subtype has not been assigned or the
        assigned type is invalid.

        If the account_subtype is not valid, return an invalid result.

        Parameters:
            account_subtype (Enum): the specific type of this Account. The
                account_subtype is required and must be one of the members of
                InvestmentAccountType If the supplied account_subtype is not
                valid, the account type is set to the constant
                InvestmentAccountType.NO_TYPE and the result will be
                invalid.

        Returns:
            (dict): ['entry'] - (str) the updated account_subtype
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = {}
        if (
            account_subtype is not None
            and account_subtype in InvestmentAccountType.list()
            and account_subtype != InvestmentAccountType.NO_TYPE
        ):
            result["entry"] = account_subtype
            result["valid"] = True
            result["msg"] = ""
        else:
            result["entry"] = InvestmentAccountType.NO_TYPE
            result["valid"] = False
            result["msg"] = "Invalid bankaccount type ('" + str(account_subtype) + "')."
        self._set_property("account_subtype", result["entry"])

        self.update_property_flags("account_subtype", result["entry"], result["valid"])

        return result
        # end set_account_subtype()

    def get_tax_deferred(self) -> bool:
        """
        Is an investment account to tax deferred?

        These accounts are IRA, 401K, 403B, and 529 type accounts.

        Returns:
            (bool) True if account is to be tax deferred, False if not.
        """
        tax_deferred = self._get_property("tax_deferred")
        if tax_deferred is None:
            tax_deferred = self.defaults["tax_deferred"]
        return tax_deferred
        # end get_tax_deferred()

    def set_tax_deferred(self, tax_deferred: bool) -> dict[str, Any]:
        """Set the account to be tax deferred.

        Parameters:
            tax_deferred (bool): True if the account is tax deferred,
                False if not
        Returns:
            (dict): ['entry'] - (str) the updated tax_deferred value
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = self.validate.boolean(tax_deferred)
        if result["valid"]:
            self._set_property("tax_deferred", result["entry"])
        else:
            self._set_property("tax_deferred", False)
        return result
        self.update_property_flags("tax_deferred", result["entry"], result["valid"])
        # end set_tax_deferred()


# end class Investment Account

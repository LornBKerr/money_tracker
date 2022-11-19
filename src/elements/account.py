"""
A basic account for the MoneyTrack program

File:       elements/account.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

from copy import deepcopy
from typing import Any

from lbk_library import Element


class Account(Element):
    """
    Implement a basic Account in the database.

    This provides the common functions of all MoneyTrack Accounts. It is
    to be extended with added functionality for usable accounts such as
    Bank and Investment accounts.
    """

    def __init__(self, dbref, account_key=None, column=None):
        """
        Define a basic Account.

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
        super().__init__(dbref, "accounts")

        # Default values for the Account
        self.defaults: dict[str, Any] = {
            "record_id": 0,
            "name": "",
            "description": "",
            "company": "",
            "account_number": "",
            "check_writing_avail": False,
            "account_separate": False,
            "hide_in_transaction_list": False,
            "hide_in_account_lists": False,
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

    def set_properties(self, properties):
        """Set the values of the Account properties array.

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
                if key == "name":
                    self.set_name(properties[key])
                elif key == "description":
                    self.set_description(properties[key])
                elif key == "company":
                    self.set_company(properties[key])
                elif key == "account_number":
                    self.set_account_number(properties[key])
                elif key == "check_writing_avail":
                    self.set_check_writing_avail(properties[key])
                elif key == "account_separate":
                    self.set_account_separate(properties[key])
                elif key == "hide_in_transaction_list":
                    self.set_hide_in_transaction_list(properties[key])
                elif key == "hide_in_account_lists":
                    self.set_hide_in_account_lists(properties[key])
        # end set_properties()

    def get_name(self):
        """Get the Account's name.

        Return:
            (str) The Account's name or, if None, the default value.
        """
        name = self._get_property("name")
        if name is None:
            name = self.defaults["name"]
        return name
        # end get_name()

    def set_name(self, name):
        """
        Set the Account's name.

        The account name is required and can contain from 1 to 127
        characters.

        Parameters:
            name (str):the new account name for the Account. The account
                name is required and can be between 1 and 127 characters
                in length. If the supplied account name is not valid,
                the account name is set to the empty string.

        Returns:
            (dict): ['entry'] - (str) the updated name
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = self.validate.text_field(name, self.validate.REQUIRED, 1, 127)
        if result["valid"]:
            self._set_property("name", result["entry"])
        else:
            self._set_property("name", "")

        self.update_property_flags("name", result["entry"], result["valid"])
        return result
        # end set_name()

    def get_description(self):
        """
        Get the description of the account.

        Returns:
            (str) the description of the account.
        """
        description = self._get_property("description")
        if description is None:
            description = self.defaults["description"]
        return description
        # end get_description()

    def set_description(self, description):
        """Set the description of the account.

        Parameter:
            description (str): A brief description of the account. This
                is optional and is limited to no more than 255
                characters. If the description is not present, itis set
                to the empty string.
        Returns:
            (dict): ['entry'] - (str) the updated name
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = self.validate.text_field(description, self.validate.OPTIONAL, 0, 255)
        if result["valid"]:
            self._set_property("description", result["entry"])
        else:
            self._set_property("description", "")

        self.update_property_flags("description", result["entry"], result["valid"])
        return result
        # end set_description()

    def get_company(self):
        """
        Get the financial company holding this account.

        Returns:
            (str) the finanacial company hosting the account.
        """
        company = self._get_property("company")
        if company is None:
            company = self.defaults["company"]
        return company
        # end get_company()

    def set_company(self, company):
        """Set the company holding the account.

        Parameters:
            company (str): The name of the Financial Company holding
                the account. This is required and is between 1 and 127
                characters long. If the company is not present, it
                is set to the empty string.
        Returns:
            (dict): ['entry'] - (str) the updated name of the company
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = self.validate.text_field(company, self.validate.REQUIRED, 0, 127)
        if result["valid"]:
            self._set_property("company", result["entry"])
        else:
            self._set_property("company", "")
        self.update_property_flags("company", result["entry"], result["valid"])
        return result
        # end set_company()

    def get_account_number(self):
        """
        Get the account_number of the account.

        Returns:
            (str) the account_number of the account.
        """
        account_number = self._get_property("account_number")
        if account_number is None:
            account_number = self.defaults["account_number"]
        return account_number
        # end get_account_number()

    def set_account_number(self, account_number: str) -> dict[str, Any]:
        """Set the account_number of the account.

        Parameter:
            account_number (str): The account_number of the account.
                This is optional and is limited to no more than 63
                characters. If the account_number is not present, it is
                set to the empty string.
        Returns:
            (dict): ['entry'] - (str) the updated account_number
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = self.validate.text_field(account_number, self.validate.OPTIONAL, 0, 63)
        if result["valid"]:
            self._set_property("account_number", result["entry"])
        else:
            self._set_property("account_number", "")
        self.update_property_flags("account_number", result["entry"], result["valid"])
        return result
        # end set_account_number()

    def get_check_writing_avail(self) -> bool:
        """
        Does an account have check writing available. All checking
        accounts and many savings account will have check writing enabled.
        Some brokerage accounts will also have check writing available.
        Generally, CD bank accounts and retirement investment accounts
        will not.

        Returns:
            (bool) True if account has checking, False if not.
        """
        check_writing_avail = self._get_property("check_writing_avail")
        if check_writing_avail is None:
            check_writing_avail = self.defaults["check_writing_avail"]
        return check_writing_avail
        # end get_check_writing_avail()

    def set_check_writing_avail(self, check_writing_avail: bool) -> dict[str, Any]:
        """
        Set the check_writing_avail value of the account.

        Parameters:
            check_writing_avail (bool): True if the account has checking
            available, False if not
        Returns:
            (dict): ['entry'] - (str) the updated check_writing_avail value
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = self.validate.boolean(check_writing_avail)
        if result["valid"]:
            self._set_property("check_writing_avail", result["entry"])
        else:
            self._set_property("check_writing_avail", False)
        return result
        self.update_property_flags("account_separate", result["entry"], result["valid"])
        # end set_check_writing_avail()

    def get_account_separate(self) -> bool:
        """
        Is an account kept separate from various calculations such as
        net worth, overview, budgets, accounts summary, reports, and
        graphs by default.

        Returns:
            (bool) True if account is to be kept separate, False if not.
        """
        account_separate = self._get_property("account_separate")
        if account_separate is None:
            account_separate = self.defaults["account_separate"]
        return account_separate
        # end get_account_separate()

    def set_account_separate(self, account_separate: bool) -> dict[str, Any]:
        """
        Set the account_separate value of the account.

        Parameters:
            account_separate (bool): True if the account is to be kept
                separate, False if not

        Returns:
            (dict): ['entry'] - (str) the updated account_separate value
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = self.validate.boolean(account_separate)
        if result["valid"]:
            self._set_property("account_separate", result["entry"])
        else:
            self._set_property("account_separate", False)
        return result
        self.update_property_flags("account_separate", result["entry"], result["valid"])
        # end set_account_separate()

    def get_hide_in_transaction_list(self) -> bool:
        """
        Is an account to be hidden in the Transactions Lists?

        Returns:
            (bool) True if account is to be kept hidden, False if not.
        """
        hide_in_transaction_list = self._get_property("hide_in_transaction_list")
        if hide_in_transaction_list is None:
            hide_in_transaction_list = self.defaults["hide_in_transaction_list"]
        return hide_in_transaction_list
        # end get_hide_in_transaction_list()

    def set_hide_in_transaction_list(
        self, hide_in_transaction_list: bool
    ) -> dict[str, Any]:
        """
        Set the account to be hiiden in transaction lists..

        Parameters:
            hide_in_transaction_list (bool): True if the account is to be kept
                hidden in Transaction Lists, False if not
        Returns:
            (dict): ['entry'] - (str) the updated hide_in_transaction_list value
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = self.validate.boolean(hide_in_transaction_list)
        if result["valid"]:
            self._set_property("hide_in_transaction_list", result["entry"])
        else:
            self._set_property("hide_in_transaction_list", False)
        return result
        self.update_property_flags(
            "hide_in_transaction_list", result["entry"], result["valid"]
        )
        # end set_hide_in_transaction_list()

    def get_hide_in_account_lists(self) -> bool:
        """
        Is an account to be hidden in sidebar and account lists?

        Returns:
            (bool) True if account is to be kept hidden, False if not.
        """
        hide_in_account_lists = self._get_property("hide_in_account_lists")
        if hide_in_account_lists is None:
            hide_in_account_lists = self.defaults["hide_in_account_lists"]
        return hide_in_account_lists
        # end get_hide_in_account_lists()

    def set_hide_in_account_lists(self, hide_in_account_lists: bool) -> dict[str, Any]:
        """
        Set the account to be hiiden in transaction lists..

        Parameters:
            hide_in_account_lists (bool): True if the account is to be
                kept hidden in sidebar and account lists, False if not
        Returns:
            (dict): ['entry'] - (str) the updated hide_in_account_lists value
                    ['valid'] - (bool) True if the operation suceeded,
                        False otherwise
                    ['msg'] - (str) Error message if not valid
        """
        result = self.validate.boolean(hide_in_account_lists)
        if result["valid"]:
            self._set_property("hide_in_account_lists", result["entry"])
        else:
            self._set_property("hide_in_account_lists", False)
        return result
        self.update_property_flags(
            "hide_in_account_lists", result["entry"], result["valid"]
        )
        # end set_hide_in_account_lists()


# end class Account

"""
General Flags used throughout the MoneyTrack program

File:       flags.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""


class AccountType:
    """
    Available top level account types.
    
    The defined Top level account types for general use are 'Bank'
    accounts and  'Investment' accounts. A 'Tax' account is defined for
    internal use to support generating simplified income tax estimates.
    The NO_TYPE type is used to indicate no account type has been assigned.
    """
    NO_TYPE = 0
    BANK = 1
    INVESTMENT = 2
    TAX = 3
    
    @staticmethod
    def list() -> []:
        """
        Return a list of the defined AccountTypes.
        
        Returns:
            (list) a list of the available AccountTypes
        """
        return [AccountType.NO_TYPE, AccountType.BANK, AccountType.INVESTMENT, AccountType.TAX]

    # end list()

# end class AccountType


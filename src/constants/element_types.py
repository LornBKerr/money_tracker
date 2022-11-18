"""
The top level database elements used throughout the MoneyTrack program

File:       element_types.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""


class ElementType:
    """
    Define the basic kinds of database elements.

    These relate directly to the set of tables in the database. These
    include the various kinds of accounts, securities, transactions, and
    categories used in transactions.
    """

    ELEMENT_TYPE_MASK = 0xF0000

    NO_TYPE = 0x00000
    ACCOUNT = 0x10000
    #    SECURITY = 0x20000
    #    TRANSACTION = 0x30000
    #    CATEGORY = 0x40000

    @staticmethod
    def list() -> []:
        """
        Return a list of the defined ElementTypes.

        Returns:
            (list) a list of the available ElementTypes
        """
        return [
            ElementType.NO_TYPE,
            ElementType.ACCOUNT,
            #            ElementType.SECURITY,
            #            ElementType.TRANSACTION,
            #            ElementType.CATEGORY,
        ]

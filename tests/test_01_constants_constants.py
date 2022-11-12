import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from constants import AccountType

def test_0101_AccountType():
    assert AccountType.NO_TYPE == 0
    assert AccountType.BANK
    assert AccountType.INVESTMENT
    assert AccountType.TAX
    assert AccountType.NO_TYPE in AccountType.list()
    assert AccountType.BANK in AccountType.list()
    assert AccountType.INVESTMENT in AccountType.list()
    assert AccountType.TAX in AccountType.list()


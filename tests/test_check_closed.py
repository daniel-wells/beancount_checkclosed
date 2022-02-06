__copyright__ = "Copyright (C) 2018  Martin Blais, Daniel Wells 2022"
__license__ = "GNU GPLv2"

import unittest

from beancount.parser import cmptest
from beancount import loader

from beancount_checkclosed.check_closed import check_closed

class TestCheckClosing(cmptest.TestCase):

    @loader.load_doc(expect_errors=True)
    def test_check_closed_unbalanced(self, entries, _, options_map):
        """
        2020-01-01 open Equity:Opening-Balances GBP, USD
        2020-01-01 open Assets:BankA GBP, USD
        2020-01-01 open Expenses:Food GBP, USD

        2020-01-15 txn "Example"
           Assets:BankA 100 GBP
           Assets:BankA 10 USD
           Equity:Opening-Balances 100 GBP
           Equity:Opening-Balances 10 USD

        2020-01-15 txn "Example"
           Expenses:Food 50 GBP
           Expenses:Food 5 USD
           Assets:BankA -50 GBP
           Assets:BankA -5 USD

        2020-02-01 close Assets:BankA
        """
        new_entries, _ = check_closed(entries, options_map)

        self.assertEqualEntries("""
        2020-01-01 open Equity:Opening-Balances GBP, USD
        2020-01-01 open Assets:BankA GBP, USD
        2020-01-01 open Expenses:Food GBP, USD

        2020-01-15 txn "Example"
           Assets:BankA 100 GBP
           Assets:BankA 10 USD
           Equity:Opening-Balances 100 GBP
           Equity:Opening-Balances 10 USD

        2020-01-15 txn "Example"
           Expenses:Food 50 GBP
           Expenses:Food 5 USD
           Assets:BankA -50 GBP
           Assets:BankA -5 USD

        2020-02-01 close Assets:BankA

        2020-02-02 balance Assets:BankA 0 GBP
        2020-02-02 balance Assets:BankA 0 USD
        """, new_entries)


if __name__ == '__main__':
    unittest.main()

"""A plugin that automatically inserts a 0 balance check for closed accounts.

A closing directive e.g.

2015-04-23 close Assets:Checking

Will ensure transactions can not involve this account after that date.
However it will not check that the balance is 0 after closing.
This is what this plugin does.

There is a similarly named plugin within beancount 'check_closing' but that
plugin requires you to add metadata to the specific closing transaction.

"""
__copyright__ = "Copyright (C) 2018  Martin Blais, Daniel Wells 2022"
__license__ = "GNU GPLv2"

import datetime
import collections

from beancount.core.number import ZERO
from beancount.core import data
from beancount.core import amount
from beancount.core import account_types

__plugins__ = ('check_closed',)


def check_closed(entries, options_map):
    """Add a zero balance check to closed accounts.

    Args:
      entries: A list of directives.
      unused_options_map: An options map.
    Returns:
      A list of new errors, if any were found.
    """
    new_entries = []
    units_map = collections.defaultdict(set)
    for entry in entries:
        if isinstance(entry, data.Open):
            if entry.currencies is not None:
                for currency in entry.currencies:
                    units_map[entry.account].add(currency)
        if isinstance(entry, data.Transaction):
            for posting in entry.postings:
                units_map[posting.account].add(posting.units.currency)
        if isinstance(entry, data.Close):
            if account_types.is_balance_sheet_account(entry.account, account_types.DEFAULT_ACCOUNT_TYPES):
                date = entry.date + datetime.timedelta(days=1)
                for currency in units_map[entry.account]:
                    balance = data.Balance(data.new_metadata("<check_closed>", 0),
                                           date, entry.account,
                                           amount.Amount(ZERO, currency),
                                           None, None)
                    new_entries.append(balance)
        new_entries.append(entry)
    return new_entries, []


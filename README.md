A beancount plugin that automatically inserts a 0 balance check for closed accounts.

A closing directive e.g.
```
2015-04-23 close Assets:Checking
```
will ensure transactions can not involve this account after that date.
However it will not check that the balance is 0 after closing.
This is what this plugin does.

There is a similarly named plugin within beancount 'check_closing' but that
plugin requires you to add metadata to the specific closing transaction.

Installation:
```
pip install git+https://github.com/daniel-wells/beancount_checkclosed.git
```

Usage:
Add the following line to your ledger file:
```
plugin "beancount_checkclosed.check_closed"
```

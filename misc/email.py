import imaplib
import email
import getpass

_EMAIL = 'dhruvlaad@gmail.com'
_IMAP = 'imap.gmail.com'

def sort_emails_by_author(k: int):
"""
sorts inbox by authors, and returns `k` senders with most mails
"""
    passwd = getpass.getpass(prompt='Password: ')


def 
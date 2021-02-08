# this code is from: https://github.com/sadovnychyi/alfred-chrome-passwords

import argparse
import base64
import codecs
# import fuzzywuzzy.process
from pyfzf.pyfzf import FzfPrompt
from debug import DEBUG
import json
import os
import sqlite3
import sys
import tempfile
try:
  from urlparse import urlparse
except ImportError:
  from urllib.parse import urlparse
opj = os.path.join

HOME = os.path.expanduser('~')
CHROME = 'Library/Application Support/Google/Chrome'
PROFILE = 'Default'
LOGIN_DATA = 'Login Data'

CHROME_PASS_J=opj(
  HOME, CHROME, PROFILE, LOGIN_DATA
)

def get_site(passwords:list):
  fzf = FzfPrompt()
  if DEBUG:
    print("--- passwords")
    for p in passwords:
      print(p)
    print("--- END ---")

  new_list_with_mail = []
  for p in passwords:
    username = p["subtitle"]
    if len(username) == 0:
      username = "NOUSER"
    new_list_with_mail.append({"title": p["title"], "username": username})
  map_passwords_site_with_name = list(
    map(
      lambda x: x["title"] + "\t" + x["username"],
      new_list_with_mail
    )
  )
  if DEBUG:
    for i in map_passwords_site_with_name:
      print(i)

  return map_passwords_site_with_name



def select_site_and_get_encrypted_password(query, profile):
  with tempfile.NamedTemporaryFile() as tmp:
    with open(os.path.join(HOME, CHROME, profile, LOGIN_DATA), 'rb') as f:
      tmp.write(f.read())
    cursor = sqlite3.connect(tmp.name).cursor()
    cursor.execute('''SELECT origin_url, username_value, password_value
                      FROM logins ORDER BY times_used desc''')
    passwords = []
    for origin_url, account, password in cursor.fetchall():
      password = base64.b64encode(password[3:]).decode('utf8')
      url = urlparse(origin_url)
      title = codecs.decode(url.netloc.encode('utf8'), 'idna')
      if title.lower().startswith('www.'):
        title = title[4:]
      if url.scheme == 'android':
        title = '%s://%s' % (url.scheme, title.split('@')[1])
      passwords.append({
        'type': 'default',
        'title': title,
        'subtitle': account,
        'arg': password,
        'valid': 'true' if len(password) > 0 else 'false',
        'autocomplete': title,
      })
    sites = get_site(passwords)
    fzf = FzfPrompt()
    selected_site = fzf.prompt(sites)
    assert len(selected_site) > 0
    assert selected_site[0].split("\t")

    sitename, username = selected_site[0].split("\t")
    target = None
    for p in passwords:
      new_sub = "NOUSER" if len(p["subtitle"]) == 0 else p["subtitle"]
      if (sitename == p["title"] and username == new_sub):
        target = p
        break
    if DEBUG:
      print("target: ", target)
    password_encrypted = target["arg"]

    return password_encrypted

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--query', default='')
  parser.add_argument('--profile', default=PROFILE)
  args = parser.parse_args()
  select_site_and_get_encrypted_password(args.query, args.profile)

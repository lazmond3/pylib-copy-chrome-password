import argparse
from .passwords import select_site_and_get_encrypted_password
from .decrypt import decrypt
from clipboard import clipboard_write_to_clipboard

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--query', default='')
  parser.add_argument('--profile', default="Default")
  args = parser.parse_args()
  password_encrypted = select_site_and_get_encrypted_password(args.query, args.profile)
  password = decrypt(password_encrypted)
  clipboard_write_to_clipboard(password)
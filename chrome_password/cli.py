import argparse
from .passwords import select_site_and_get_encrypted_password

def main():
    # select_site_and_get_encrypted_password()
  print("name: ", __name__)
  parser = argparse.ArgumentParser()
  parser.add_argument('--query', default='')
  parser.add_argument('--profile', default="Default")
  args = parser.parse_args()
  password_encrypted = select_site_and_get_encrypted_password(args.query, args.profile)
# if __name__ == "__main__":
#     print()
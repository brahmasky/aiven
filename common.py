# common functions used for this excercise

import os, os.path, json, bcrypt

from mylogger import logger

# file path check, and force user to re-input the file
def check_file_exist(filename):
  while not os.path.isfile(filename):
    # print('os.path.isfile({}) == {}'.format(filename, os.path.isfile(filename)))
    filename = input('File does not exist, please provide a valid path to the file: ')
  return filename

# check special char for login details such as username and password
def check_special_char(str):
  special_char='"!@#$%^&*()-+?_=,<>/'
  while any(c in special_char for c in str):
    str = input('special character used, please provide another value: ')
  return str

### https://dev.to/kmistele/how-to-securely-hash-and-store-passwords-in-your-next-application-4e2f
# this will create the hash that you need to store in your database
def create_bcrypt_hash(password):
    # convert the string to bytes
    password_bytes = password.encode()      
    # generate a salt
    salt = bcrypt.gensalt(14)               
    # calculate a hash as bytes
    password_hash_bytes = bcrypt.hashpw(password_bytes, salt)   
    # decode bytes to a string
    password_hash_str = password_hash_bytes.decode()            

    # the password hash string should similar to:
    # $2b$10$//DXiVVE59p7G5k/4Klx/ezF7BI42QZKmoOD0NDvUuqxRE5bFFBLy
    return password_hash_str        

# this will return true if the user supplied a valid password and 
# should be logged in, otherwise false
def verify_password(password, hash_from_database):
    password_bytes = password.encode()
    hash_bytes = hash_from_database.encode()

    # this will automatically retrieve the salt from the hash, 
    # then combine it with the password (parameter 1)
    # and then hash that, and compare it to the user's hash
    does_match = bcrypt.checkpw(password_bytes, hash_bytes)

    return does_match

def read_settings(service):
  settings_file='settings.json'
  try:
    with open(settings_file, "r") as f:
      settings = json.loads(f.read())
      logger.info('{} content: {}'.format(settings_file, settings))
  except Exception as e:
      logger.exception("{} not found in local directory:\n {}".format(settings_file, e))

  return settings[service]
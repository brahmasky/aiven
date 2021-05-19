#! /usr/bin/python3
"""
This script to init the settings for the tasks given in the Aiven homework
and running the two script sequentially assuming no other user intervention is required
"""

import time, sys, subprocess, json, bcrypt
from myaiven import common
from myaiven.mylogger import logger

# create settings json with user input, with some level of verification
# could do more with integration with other systems such as database/vault management

def user_input():
  logger.info('=== Please provide details for the Kafka server/service ===')
  kafka_server = input('Kafka server [EG: localhost or demo-kafka.aivencloud.com]: ')
  kafka_port = input('Kafka server port [EG: 9092]: ')
  kafka_ca_file = input('Access key filename [EG: ./ca.pem]: ')
  kafka_ca_file = common.check_file_exist(kafka_ca_file)
  kafka_cert_file = input('Access certificate filename [EG: ./service.cert]: ')
  kafka_cert_file = common.check_file_exist(kafka_cert_file)
  kafka_key_file = input('Access key filename [EG: ./service.key]: ')
  kafka_key_file = common.check_file_exist(kafka_key_file)
  kafka_client_id = input('Client ID [EG: my_client]: ')
  kafka_group_id = input('Group ID [EG: my_group]: ')
  kafka_topic = input('Kafka topic [EG: my_topic]: ')

  kafka_settings = {
    'KAFKA_SERVER': kafka_server,
    'KAFKA_PORT': kafka_port,
    'KAFKA_PROTOCOL': 'SSL',
    'KAFKA_CA_FILE': kafka_ca_file,
    'KAFKA_CERT_FILE': kafka_cert_file,
    'KAFKA_KEY_FILE': kafka_key_file,
    'KAFKA_TOPIC': kafka_topic,
    'KAFKA_CLIENT_ID': kafka_client_id,
    'KAFKA_GROUP_ID': kafka_group_id,
  }

  logger.info('\n\n=== Please provide details for the PostgreSQL server/service ===')
  db_host = input('PostgreSQL Server [EG: localhost or demo-postgre.aivencloud.com]: ')
  db_port = input('PostgreSQL Server port [EG: 5432]: ')
  
  db_user = input('PostgreSQL username [EG: myuser]: ')
  # do not allow special character in username and password in consideration of SQL injection
  db_user = common.check_special_char(db_user)

  db_password = input('PostgreSQL password [EG: mypassword]: ')
  # do not allow special character in username and password in consideration of SQL injection
  db_password = common.check_special_char(db_password)
  # encrypt the password given we are using local json, with modern Vault such as Hashicorp one or AWS Secrets Manager it can be implement otherwise
  hash_pwd = common.create_bcrypt_hash(db_password)
  
  db_name = input('PostgreSQL database name [EG: mydb]: ')
  db_table = input('PostgreSQL databse table nname [EG: mytable]: ')

  db_settings = {
    'DB_HOST': db_host,
    'DB_PORT': db_port,
    'DB_USER': db_user,
    'DB_PASSWORD': db_password,
    'DB_HASH_PASSWORD': hash_pwd,
    'DB_NAME': db_name,
    'DB_TABLE': db_table,
  }

  settings = {}
  settings['kafka'] = kafka_settings
  settings['db'] = db_settings

  with open('settings.json', 'w') as f:
    json.dump(settings, f, indent=2)  

def main():
  # Step 1: capture kafka and db settings from user input
  logger.info('=== STEP 1: initialise the kafka and postgre server/service ===')
  user_input()

  logger.info('=== STEP 2: checking website and send the result to pre-defined kafka topic ===')
  # could do some futher check with user input, skip for now...
  web_process = subprocess.Popen([sys.executable, 'web_to_kafka.py'],
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.STDOUT)

  if web_process is not None:
    logger.info('The web_to_kafka.py script is now runing, pid == {}'.format(web_process.pid))

  logger.info('=== STEP 3: wait for 1 minute, poll the message from kafka topic and dump the result into an existing table in PostgreSQL Database server ===')
   # could do some futher check with user input, skip for now...
  time.sleep(60)
  db_process = subprocess.Popen([sys.executable, 'kafka_to_db.py'],
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.STDOUT)
  if db_process is not None:
    logger.info('The kafka_to_db.py script is now runing, pid == {}'.format(db_process.pid))

if __name__ == "__main__":
    main()
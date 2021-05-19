
#! /usr/bin/python3
"""
This script polls the message from a kafka topic and dump it to an existing table of a PostgreSQL database
"""
import sys, psycopg2

from myaiven import common
from myaiven.mylogger import logger
from myaiven.mykafka import MyKafkaConsumer
from myaiven.mypostgredb import MyPostgreDB


def main():
  # init kafka consumer
  try:
    kafka_consumer_settings = common.read_settings('kafka')
    kafka_consumer = MyKafkaConsumer(kafka_consumer_settings)
  except Exception as e:
    logger.exception('Cannot create kafka consumer...', e)

  # init postgre db
  try:
    db_settings = common.read_settings('db')
    #check if passowrd has been compromised
    if common.verify_password(db_settings["DB_PASSWORD"], db_settings["DB_HASH_PASSWORD"]):
      my_db = MyPostgreDB(db_settings)
    else:
      print('password has been compromised, exiting...')
      logger.critical('password has been compromised, exiting...')
      sys.exit(1)
  except Exception as e:
    logger.exception('Cannot connect to database...', e)

  # dump messages from kafka topic to database
  if kafka_consumer is not None and my_db is not None:
    msgs=kafka_consumer.receive()
    for msg in msgs:
      my_db.write(msg)

  my_db.close()    

if __name__ == "__main__":
    main()
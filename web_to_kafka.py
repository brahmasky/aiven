#! /usr/bin/python3
"""
This script periodically scans a webpage and sends the result to a kafka topic.
"""

import re, json, time, requests
from datetime import datetime

import common
from mylogger import logger
from mykafka import MyKafkaProducer


# check githut events site with keyword check
def http_check(regex='DeleteEvent'):
  URL = 'https://api.github.com/events'
  results={}

  results["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  try:
    logger.info('Checking URL'.format(URL))
    r = requests.get(URL, timeout=1)
    results["error"] = ""
    results["status"] = r.status_code
    results["elapsed"] = r.elapsed.total_seconds()
    results["regex_found"] = bool(re.search(regex, r.text))

  except Exception as e:
    results["error"] = str(e)
    results["status"] = -1
    results["elapsed"] = -1
    results["regex_found"] = False

  return results

def main():
  # creat kafka producer from kafka_settings.json
  try:
    kafka_producer_settings = common.read_settings('kafka')
    kafka_producer = MyKafkaProducer(kafka_producer_settings)
  except Exception as e:
    logger.exception('Cannot create kafka producer', e)

  # periodically checking a public website untill terminated manually
  try:
    while True:
      CHECK_INTERVAL = 30 # in seconds
      time.sleep(CHECK_INTERVAL)
      
      http_result = http_check()

      if kafka_producer is not None and http_result is not None:
        logger.info('Sending result to kafka: {}'.format(http_result))
        try:
          kafka_producer.send(json.dumps(http_result))
        except Exception as e:
          logger.exception('Cannot send message to broker', e)
  
  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
    main()
# A class to implement Kafka Producer and Consumer on Aiven.io from json settings
from kafka import KafkaProducer,KafkaConsumer
import json
from mylogger import logger

# a customised procuder from json settings
class MyKafkaProducer:
  def __init__(self, settings):
    self.topic = settings["KAFKA_TOPIC"]
    self.bootstrap_servers = f'{settings["KAFKA_SERVER"]}:{settings["KAFKA_PORT"]}'
    self.security_protocol = settings["KAFKA_PROTOCOL"]
    self.ssl_cafile = settings["KAFKA_CA_FILE"]
    self.ssl_certfile = settings["KAFKA_CERT_FILE"]
    self.ssl_keyfile = settings["KAFKA_KEY_FILE"]
    self.producer=''

    try:
      logger.info('Creating Kafka producer from settings... on {}'.format(self.bootstrap_servers))
      self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                          security_protocol=self.security_protocol,
                          ssl_cafile=self.ssl_cafile,
                          ssl_certfile=self.ssl_certfile,
                          ssl_keyfile=self.ssl_keyfile,
                          )
    except Exception as e:
      logger.exception("Unable to create producer", e)

  # sends messages to the topic
  def send(self, message):
    try:
      self.producer.send(self.topic, message.encode("utf-8"))
      self.producer.flush()
    except Exception as e:
      logger.exception("Unable to send data to Kafka", e)

# a customised consumer from json settings
class MyKafkaConsumer:
  def __init__(self, settings):
    self.topic = settings["KAFKA_TOPIC"]
    self.bootstrap_servers = f'{settings["KAFKA_SERVER"]}:{settings["KAFKA_PORT"]}'
    self.security_protocol = settings["KAFKA_PROTOCOL"]
    self.ssl_cafile = settings["KAFKA_CA_FILE"]
    self.ssl_certfile = settings["KAFKA_CERT_FILE"]
    self.ssl_keyfile = settings["KAFKA_KEY_FILE"]

    self.client_id = settings["KAFKA_CLIENT_ID"]
    self.group_id = settings["KAFKA_GROUP_ID"]
    self.consumer =''

    try:
      logger.info('Creating Kafka consumer from settings... on {}'.format(self.bootstrap_servers))
      self.consumer = KafkaConsumer(self.topic,
                          auto_offset_reset="earliest",
                          bootstrap_servers=self.bootstrap_servers,
                          security_protocol=self.security_protocol,
                          ssl_cafile=self.ssl_cafile,
                          ssl_certfile=self.ssl_certfile,
                          ssl_keyfile=self.ssl_keyfile,
                          client_id=self.client_id,
                          group_id=self.group_id,
                          consumer_timeout_ms=1000,
                          )

    except Exception as e:
      logger.exception("Unable to create consumer", e)

  # poll messages from a topic and return a list 
  def receive(self):
    data = []
    try:
      for _ in range(2):
        raw_msgs = self.consumer.poll(timeout_ms=1000)
        for tp, msgs in raw_msgs.items():
          for msg in msgs:
            logger.info("Received: {}".format(msg.value))
            data.append(json.loads(msg.value))
      self.consumer.commit()

    except Exception as e:
      logger.exception("Unable to poll data from Kafka", e)
      
    return data

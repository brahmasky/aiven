
from kafka import KafkaProducer,KafkaConsumer
import json

consumer = KafkaConsumer('github_event',
  bootstrap_servers='kafka-homework-epicon-55ed.aivencloud.com:22118',
  auto_offset_reset='earliest',
  security_protocol='SSL',
  ssl_cafile='ca.pem',
  ssl_certfile='service.cert',
  ssl_keyfile='service.key',
  client_id='my_client',
  group_id='my_group',
  consumer_timeout_ms=1000,
)

for _ in range(2):
  raw_msgs = consumer.poll()
  for tp, msgs in raw_msgs.items():
    print("tp: {}".format(tp))
    for msg in msgs:
      print("Received: {}".format(msg.value))

consumer.commit()

data=[]
for _ in range(2):
  raw_msgs = consumer.poll()
  for tp, msgs in raw_msgs.items():
    for msg in msgs:
      print("Received: {}".format(msg.value))
      data.append(json.loads(msg.value))
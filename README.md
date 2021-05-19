# Aiven Exercise
A system to  monitors website, produces metrics and passes these events through an Aiven Kafka instance into an Aiven PostgreSQL database

## Overview
1. `init.py` -- an 'automatic' script to guide the user through
    - initialise the settings for Aiven Kafka and PosgreSQL services
    - run the `web_to_kafka.py` script to periodically check a website on the background, and send the metrics to kafka topic
    - run the `kafka_to_db.py` script to poll the messages from kafka topic and save it into a table in PostgreSQL database
2. `web_to_kafka.py` -- the main script to periodically check a website on the background, and send the metrics to kafka topic
3. `kafka_to_db.py` -- the main script to poll the messages from kafka topic and save it into a table in PostgreSQL database
4. `mykafka.py` -- a custom class to wrap Kafka Producer and Consumer on Aiven.io
5. `mypostgredb.py` -- a custom class to connect and write to a PostegreSQL database on Aiven.io
6. `common.py` -- a support module for common used functions to manage settings, encryptions etc.
7. `mylogger.py` -- a support module for logging across the entire application

### Requirements
The module requies the following libraries to be able to run successfully in your Python virtual environment.
- requests
- kafka-python
- psycopg2-binary
- bcrypt

## Usage
There are two ways to execute the application after cloning the repo. The _assumption_ is that the kafka topic and database has been setup.

### Automatic
Run the `init.py` script (`python init.py`) which will guide you through setting up the kafka and postgre DB details, following by running the two main scripts to complete the tasks
- check a website for a number of metics such as download time
- send the metrics to a kafka topic
- poll the kafka topic and save the metics to a table in PostgreDB database

### Manual
1. Create a settings file (**`settings.json`**) with all relevant details following the configuraion in `sample_settings.json`. As an example, execute `cp sample_settings.json settings.json` and update the setting with any editor
2. Execute `web_to_kafka.py` script to check a website and send metrics to kafka topic: `python web_to_kafka.py` or `python web_to_kafka.py &` to leave the script running in the background
3. Leave the above script running for a while, in the background or open a new command console, and execute `kafka_to_db.py`: `python kafka_to_db.py`.
4. Check the results in the database to see if the table has been populate with latest 

### sample_settings.json
With the `init.py` script, you can create a dedicated `settings.json` file to be used with your kafka and postgredb configurations. Below is an explanation of the parameters used in the file in case you are going to manually configure the service details and run the two main scripts.
|Key|Description|Sample Value|
|-|-|-|
|**Kafka Settings**|
|KAFKA_SERVER|kafka server hostname|localhost|
|KAFKA_PORT |kafka server port |9092|
|KAFKA_PROTOCOL | kafka connection protocol, `SSL` recommended |SSL|
|KAFKA_CA_FILE|file path for CA file|ca.pem or ~/ca.pem|
|KAFKA_CERT_FILE|file path Certificate|service.cert or ~/service.cert|
|KAFKA_KEY_FILE|file path for Key file|service.key or ~/service.key|
|KAFKA_TOPIC|kafka topic name| my_topic|
|KAFKA_CLIENT_ID | kafka consumer client id | my_client|
|KAFKA_GROUP_ID| kafka consumer group id | my_group |
|**PostgreSQL DB Settings**|
| DB_HOST| DB server name| localhost |
| DB_PORT| DB server port| 5432 |
| DB_USER | username| myuser |
| DB_PASSWORD |password| mypassword |
| DB_HASH_PASSWORD |encrypted password|  |
| DB_NAME |Database Name| mydb |
| DB_TABLE |Table name| mytable |

## Attributions
- https://github.com/VishnuUnnikrishnan/aiven_assignment -- a similar repo on Aiven assignment which I referenced a lot
- https://help.aiven.io/en/ -- sample code for Kafka connection
- https://github.com/raosaif/sample_postgresql_database/ -- reference for PostgreSQL sample code




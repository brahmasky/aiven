# A class to implement PostgreSQL DB service on Aiven.io from json settings

from logging import exception
import psycopg2
from mylogger import logger
from datetime import datetime

# class for DB connection and cursor
class MyPostgreDB:
  def __init__(self, settings):
    user = settings["DB_USER"]
    pwd = settings["DB_PASSWORD"]
    host = settings["DB_HOST"]
    port = settings["DB_PORT"]
    dbname = settings["DB_NAME"]

    self.table = settings["DB_TABLE"]
    self.uri = f'postgres://{user}:{pwd}@{host}:{port}/{dbname}?sslmode=require'
    self.conn = ''
    self.cur = ''

    try:
      self.conn = psycopg2.connect(self.uri)
      self.cur = self.conn.cursor()
    except exception as e:
      logger.exception("Unable to connect to database...", e)

  # method to create the table for Aiven homework
  def create_table(self):
    try:
      self.cur.execute('''CREATE TABLE {} (
        event_id serial PRIMARY KEY,
        event_time timestamp,
        event_elapsed float,
        event_status varchar(50),
        event_error varchar(250),
        event_regex_found boolean);'''.format(self.table))
      self.conn.commit()
    except exception as e:
      logger.exception("Unable to create table...", e)      

  # verify the table counts
  def verify(self):
    try:
      sql = f'select count(*) from {self.table}'
      self.cur.execute(sql)
      result = self.cur.fetchone()
      logger.info('The execution result is {}'.format(result))
    except exception as e:
      logger.exception("Unable to execute query...", e)
    
    return result

  # insert msg values into table 
  def write(self, msg):
      date = datetime.strptime(msg["datetime"], "%Y-%m-%d %H:%M:%S")
      status = int(msg["status"])
      elapsed = float(msg["elapsed"])

      sql = 'INSERT INTO '+self.table+'(event_time, event_status, event_elapsed, event_regex_found, event_error) VALUES(%s,%s, %s, %s, %s);'
      data = (date, status, elapsed, msg["regex_found"], msg["error"], )
      
      try:
          self.cur.execute(sql, data)
          logger.info('write status: {}'.format(self.cur.statusmessage))      
          self.conn.commit()
      except Exception as e:
          logger.exception("Unable to execute query",e)

  # close connection
  def close(self):
    self.cur.close()
    self.conn.close()





from imgurpython import ImgurClient
import os
import configparser
from datetime import datetime
from datetime import timedelta

config = configparser.ConfigParser()
config.read("config.ini")

class Create_Album():

  def __init__(self):
    self.client_id = os.environ.get('Client_ID')
    self.client_secret = os.environ.get('Client_Secret')
    self.access_token = os.environ.get('access_token')
    self.refresh_token = os.environ.get('refresh_token')
    # self.client_id = config['imgur_api']['Client_ID']
    # self.client_secret = config['imgur_api']['Client_Secret']
    # self.access_token = config['imgur_api']['access_token']
    # self.refresh_token = config['imgur_api']['refresh_token']
    self.client = ImgurClient(self.client_id, self.client_secret, self.access_token, self.refresh_token)
    self.logger = None

  def exelogging(self, msg):
    if self.logger:
      self.logger.debug(msg)
    else:
      print(msg)

  def create(self, title, description):

    fields = {
      'title': title,
      'description': description,
    }
    self.exelogging(fields)
    self.exelogging("create album... ")
    try:  
      reply = self.client.create_album(fields=fields)
    except Exception as e:
      self.exelogging(e)
      return False, dict()

    self.exelogging("Done")

    return True, reply

if __name__ == "__main__":
    # for test
    creator = Create_Album()
    today = datetime.now()
    IsSucess, reply = creator.create("PTT_Beauty_" + str(today.year) + str(today.month) + str(today.day), "Test_Create_Album")
    print(type(reply))
    print(reply['id'])

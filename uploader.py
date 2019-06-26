from imgurpython import ImgurClient
import os


class uploader():

  def __init__(self):
    self.client_id = os.environ.get('Client_ID')
    self.client_secret = os.environ.get('Client_Secret')
    self.access_token = os.environ.get('access_token')
    self.refresh_token = os.environ.get('refresh_token')
    self.album_id = os.environ.get('Album_ID')
    self.client = ImgurClient(self.client_id, self.client_secret, self.access_token, self.refresh_token)
    self.logger = None

  def exelogging(self, msg):
    if self.logger:
      self.logger.debug(msg)
    else:
      print(msg)

  def upload_photo(self, image_url, album, name):

    config = {
      'album': album,
      'name': name,
    }
    self.exelogging(config)
    self.exelogging("Uploading image... ")
    try:  
      self.client.upload_from_url(image_url, config=config, anon=False)
    except Exception as e:
      self.exelogging(e)
      return True

    self.exelogging("Done")

    return False

if __name__ == "__main__":
  print("refresh_token={}".format(os.environ.get('refresh_token')))
  uploader = uploader()
  uploader.upload_photo("http://i.imgur.com/c0DTmUW.jpg",uploader.album_id, "Test1234")
  # uploader = uploader()
  # uploader.upload_photo("http://images.performgroup.com/di/library/omnisport/d/49/rose-derrick-usnews-getty-ftr_g3codycqfuf91veyq2qtvdma1.jpg?t=-1980713401&w=960&quality=70",'P8Kuvtc')


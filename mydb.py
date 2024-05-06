from country import Country
from user import User
from post import Post
from reponse import Reponse
from validate import Validate
class Mydb():
  def __init__(self):
    print("hello")
    self.Country=Country()
    self.Validate=Validate()
    self.Validerreponse=Validate()
    self.User=User()
    self.Post=Post()
    self.Reponse=Reponse()

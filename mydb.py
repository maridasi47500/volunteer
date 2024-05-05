from country import Country
from user import User
from post import Post
class Mydb():
  def __init__(self):
    print("hello")
    self.Country=Country()
    self.User=User()
    self.Post=Post()

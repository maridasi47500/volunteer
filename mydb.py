from country import Country
from user import User
from post import Post
from member import Member
from relationship import Relationship
from userfamily import Userfamily
class Mydb():
  def __init__(self):
    print("hello")
    self.Country=Country()
    self.User=User()
    self.Post=Post()
    self.Member=Member()
    self.Userfamily=Userfamily()
    self.Relationship=Relationship()

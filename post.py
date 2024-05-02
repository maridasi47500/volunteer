# coding=utf-8
import sqlite3
import sys
import re
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


from model import Model
class Post(Model):
    def get_text(self,hey):
        return BeautifulSoup(hey).get_text()
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.con.create_function("GET_TEXT",1,self.get_text)
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists post(
        id integer primary key autoincrement,
        title text,
            content text
                    );""")
        self.con.commit()
        #self.con.close()
    def search(self,search):
        s="%"+search.replace(" ","%")+"%"
        t=search.split(" ")[0]
        self.cur.execute("select *, GET_TEXT(content) as mycontent, INSTR(lower(GET_TEXT(content)), ?) position1, INSTR(lower(GET_TEXT(title)),?) position2 from post where lower(GET_TEXT(title)) like ? or lower(GET_TEXT(content)) like ?", (t,t,s,s))
        row=self.cur.fetchall()
        return row
    def download(self):
        URL = "https://www.whatismyip.com/sitemap/"
        req = Request(URL , headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        results = soup.find(id="content")
        python_jobs = results.find_all("a")
        for link in python_jobs:
            try:
                URL = "https://www.whatismyip.com"+link["href"]
                print(URL)
                req = Request(URL , headers={'User-Agent': 'Mozilla/5.0'})
                webpage = urlopen(req).read()
                soup = BeautifulSoup(webpage, "html.parser")
                title = soup.find("h1")
                content = soup.find(id="the-article")
                self.create({"title":title,"content":content})
            except:
                print("wow error with this link")
        self.cur.execute("select count(post.id) as mycount from post")
        row=dict(self.cur.fetchone())
        row["notice"]=str(row["mycount"])+" posts ont été téléchargé"
        return row
    def getall(self):
        self.cur.execute("select * from post")
        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):

        self.cur.execute("delete from post where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyid(self,myid):
        self.cur.execute("select * from post where id = ?",(myid,))
        row=dict(self.cur.fetchone())
        print(row["id"], "row id")
        job=self.cur.fetchall()
        return row
    def create(self,params):
        print("ok")
        myhash={}
        for x in params:
            if 'confirmation' in x:
                continue
            if 'envoyer' in x:
                continue
            if '[' not in x and x not in ['routeparams']:
                #print("my params",x,params[x])
                try:
                  myhash[x]=str(params[x].decode())
                except:
                  myhash[x]=str(params[x])
        print("M Y H A S H")
        print(myhash,myhash.keys())
        myid=None
        try:
          self.cur.execute("insert into post (title,content) values (:title,:content)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["post_id"]=myid
        azerty["notice"]="votre post a été ajouté"
        return azerty





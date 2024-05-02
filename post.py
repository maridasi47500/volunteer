# coding=utf-8
import sqlite3
import sys
import re
import requests
from bs4 import BeautifulSoup

from model import Model
class Post(Model):
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists post(
        id integer primary key autoincrement,
        title text,
            content text
                    );""")
        self.con.commit()
        #self.con.close()
    def download(self):
        URL = "https://www.whatismyip.com/sitemap/"
        page = requests.get(URL)
        
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="content")
        python_jobs = results.find_all("a")
        for link in python_jobs:
            page = requests.get(link["href"])
            soup = BeautifulSoup(page.content, "html.parser")
            title = soup.find("h1")
            content = soup.find(id="the-article")
            self.create({"title":title,"content":content})
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





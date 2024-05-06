# coding=utf-8
import sqlite3
import sys
import re
from model import Model
class Rdv(Model):
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists rdv(
        id integer primary key autoincrement,
        volunteer1_id text,
            volunteer2_id text,
            heure text,
            date text,
            lat text,
            lon text,
            content text
    , MyTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP                );""")
        self.con.commit()
        #self.con.close()
    def getallbyuserid(self,userid1, userid2):
        self.cur.execute("select * from rdv where (volunteer1_id = ? and volunteer2_id = ?)  or (volunteer2_id = ? and volunteer1_id = ?)",(userid1,userid2,userid1,userid2,))

        row=self.cur.fetchall()
        return row
    def getall(self):
        self.cur.execute("select * from rdv")

        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):

        self.cur.execute("delete from rdv where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyid(self,myid):
        self.cur.execute("select * from rdv where id = ?",(myid,))
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
        del myhash["reponseid"]
        myid=None
        try:
          self.cur.execute("insert into rdv (heure,date,volunteer1_id,volunteer2_id,lat,lon,content) values (:heure,:date,:volunteer1_id,:volunteer2_id,:lat,:lon,:content)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["rdv_id"]=myid
        azerty["notice"]="votre rdv a été ajouté"
        return azerty





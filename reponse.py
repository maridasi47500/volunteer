# coding=utf-8
import sqlite3
from validate import Validate
import sys
import re
from model import Model
class Reponse(Model):
    def __init__(self):
        self.dbValidate=Validate()
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists reponse(
        id integer primary key autoincrement,
        post_id text,
            user_id text,
            content text
    , MyTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP                );""")
        self.con.commit()
        #self.con.close()
    def someoneonone(self,userid,reponseid):
        self.cur.execute("select reponse.user_id as reponseuser_id, post.volunteer_id,u.username,userr.username as otrusername, post.title as reponsetext, reponse.*,post.id as postid  from reponse left join user u on reponse.user_id = u.id left join post on post.id = reponse.post_id left join user userr on userr.id = post.volunteer_id left outer join validate on validate.reponse_id = reponse.id group by post.id having count(distinct validate.id) > 0 and reponse.id = ? and (post.volunteer_id = ? or reponseuser_id = ?) ",(reponseid, userid,userid))

        row=self.cur.fetchone()
        return row
    def oneonone(self,userid):
        self.cur.execute("select reponse.user_id as reponseuser_id, post.volunteer_id,u.username,post.title as reponsetext, reponse.*,post.id as postid  from reponse left join user u on reponse.user_id = u.id left join post on post.id = reponse.post_id left outer join validate on validate.reponse_id = reponse.id group by post.id having count(distinct validate.id) > 0 and (post.volunteer_id = ? or reponseuser_id = ?)",(userid,userid))

        row=self.cur.fetchall()
        return row
    def reponses(self,userid):
        self.cur.execute("select post.volunteer_id,u.username,post.title as reponsetext, reponse.*,post.id as postid  from reponse left join user u on reponse.user_id = u.id left join post on post.id = reponse.post_id left outer join validate on validate.reponse_id = reponse.id group by post.id having post.volunteer_id = ? and count(distinct validate.id) = 0",(userid,))

        row=self.cur.fetchall()
        return row
    def getall(self):
        self.cur.execute("select * from reponse")

        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):

        self.cur.execute("delete from reponse where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyid(self,myid):
        self.cur.execute("select * from reponse where id = ?",(myid,))
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
          self.cur.execute("insert into reponse (post_id,user_id,content) values (:post_id,:user_id,:content)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["reponse_id"]=myid
        azerty["notice"]="votre reponse a été ajouté"
        return azerty





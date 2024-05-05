# coding=utf-8
import sqlite3
import sys
from photohasjob import Photohasjob
import re
from model import Model
class Photo(Model):
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.photohasjob=Photohasjob()
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists photo(
        id integer primary key autoincrement,
        userfamily_id text,
            filename text,
            description text,
            lat text,
            lon text
                    );""")
        self.con.commit()
        #self.con.close()
    def getjobfromphoto(self,photoid):
        self.cur.execute("select job.name, photohasjob.* from photohasjob left join job on job.id = photohasjob.job_id where photohasjob.photo_id = ?",(photoid,))

        row=self.cur.fetchone()
        return row
    def getall(self):
        self.cur.execute("select photo.*,user.username from photo left join userfamily a on photo.userfamily_id = a.id left join member m on m.id = a.member_id left join user on user.id = a.user_id left join relationship r on r.id = a.relationship_id")

        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):

        self.cur.execute("delete from photo where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyid(self,myid):
        self.cur.execute("select m.name as membername,photo.*,user.username from photo left join userfamily a on photo.userfamily_id = a.id left join member m on m.id = a.member_id left join user on user.id = a.user_id left join relationship r on r.id = a.relationship_id where photo.id = ?",(myid,))
        row=dict(self.cur.fetchone())
        print(row["id"], "row id")
        return row
    def createphotojob(self,params):
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
        del myhash["job_id"]
        print("M Y H A S H")
        print(myhash,myhash.keys())
        myid=None
        try:
          self.cur.execute("insert into photo (description,userfamily_id,filename,lat,lon) values (:description,:userfamily_id,:filename,:lat,:lon)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
          self.cur.execute("insert into photohasjob (photo_id,job_id) values (:photo_id, :job_id)",{"photo_id": myid, "job_id":params["job_id"]})
          self.con.commit()
          #myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["photo_id"]=myid
        azerty["notice"]="votre photo a été ajouté"
        print(azerty)
        return azerty
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
          self.cur.execute("insert into photo (description,userfamily_id,filename,lat,lon) values (:description,:userfamily_id,:filename,:lat,:lon)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["photo_id"]=myid
        azerty["notice"]="votre photo a été ajouté"
        print(azerty)
        return azerty





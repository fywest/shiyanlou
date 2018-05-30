#!/usr/bin/env python3
from flask import Flask, render_template,redirect,url_for,make_response,request,abort

import json
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime



app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shiyanlou'
db=SQLAlchemy(app)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, id,name):
        self.id=id
        self.name = name

    def __repr__(self):
        return '%s' % self.id


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time=db.Column(db.DateTime)
    category_id=db.Column(db.Integer, ForeignKey('category.id'))
    content = db.Column(db.Text)

    def __init__(self, id,title,datetime1,category_id,content):
        self.id=id
        self.title = title
        self.created_time = datetime1
        self.category_id = category_id
        self.content = content

    def __repr__(self):
        return "<File(title=%s)>" % self.title

infoList=db.session.query(File.id,File.title,File.created_time,File.content,Category.name).filter(File.category_id==Category.id).all()
infoList1=infoList[0]
infoList2=infoList[1]

list1=[]
for item in infoList1:
    list1.append(item)
info_dict1={}
info_dict1['id']=list1[0]
info_dict1['title']=list1[1]
info_dict1['datetime']=datetime.strftime(list1[2],'%Y-%m-%d %H:%M:%S')
info_dict1['content']=list1[3]
info_dict1['category']=list1[4]
print('****info_dict1*****')
print(info_dict1)

list2=[]
for item in infoList2:
    list2.append(item)

info_dict2={}
info_dict2['id']=list2[0]
info_dict2['title']=list2[1]
info_dict2['datetime']=datetime.strftime(list2[2],'%Y-%m-%d %H:%M:%S')
info_dict2['content']=list2[3]
info_dict2['category']=list2[4]
print('****info_dict2*****')
print(info_dict2)

id_dict={}
id_dict[1]='http://localhost:3000/files/'+str(info_dict1['id'])
id_dict[2]='http://localhost:3000/files/'+str(info_dict2['id'])
print('****id_dict*****')
print(id_dict)

title_dict={}
title_dict[1]=str(info_dict1['title'])
title_dict[2]=str(info_dict2['title'])
print('****title_dict*****')
print(title_dict)

@app.route('/')
def index():
    return render_template('index.html',title_dict=title_dict,id_dict=id_dict)


@app.route('/files/<fileId>')
def file(fileId):
    if(int(fileId)==int(info_dict1['id'])):
        return render_template('file.html',hello=info_dict1)
    elif (int(fileId)==int(info_dict2['id'])):
        return render_template('file.html', hello=info_dict2)
    else:
        return render_template('404.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run()

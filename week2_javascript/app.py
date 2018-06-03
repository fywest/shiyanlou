#!/usr/bin/env python3
from flask import Flask, render_template,redirect,url_for,make_response,request,abort

import json
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime

from pymongo import MongoClient


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://fywest:990113@localhost/shiyanlou'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shiyanlou'
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
    # tag=[]

    def __init__(self, id,title,datetime1,category_id,content):
        self.id=id
        self.title = title
        self.created_time = datetime1
        self.category_id = category_id
        self.content = content
        # self.tag=[]

    # def add_tags(self,tag_name):
    #     if tag_name not in self.tag:
    #         self.tag.append(tag_name)
    #
    # def remove_tags(self,tag_name):
    #     if tag_name in self.tag:
    #         self.tag.remove(tag_name)


    def __repr__(self):
        return "<File(title=%s)>" % self.title


db.create_all()
# java = Category(1,'Java')
# python = Category(2,'Python')
# file1 = File(1,'Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
# file2 = File(2,'Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
# db.session.add(java)
# db.session.add(python)
# db.session.add(file1)
# db.session.add(file2)
# db.session.commit()

# sql = Category(3,'SQL')
# linux = Category(4,'Linux')
# file3 = File(3,'Hello SQL', datetime.utcnow(), sql, 'File Content - SQL is cool!')
# file4 = File(4,'Hello linux', datetime.utcnow(), linux, 'File Content - linux is cool!')
# db.session.add(sql)
# db.session.add(linux)
# db.session.add(file3)
# db.session.add(file4)
# db.session.commit()


# file1.add_tag('tech')
# file1.add_tag('java')
# file1.add_tag('linux')
# file2.add_tag('tech')
# file2.add_tag('python')



infoList=db.session.query(File.id,File.title,File.created_time,File.content,Category.name).filter(File.category_id==Category.id).all()

list=[]
title_data=[]

for list in infoList:
    title_data_dict = {}
    title_data_dict['id'] = str(list[0])
    title_data_dict['link'] = 'http://localhost:3000/files/' + str(list[0])
    title_data_dict['title'] = str(list[1])
    title_data_dict['datetime'] = str(datetime.strftime(list[2],'%Y-%m-%d %H:%M:%S'))
    title_data_dict['content'] = str(list[3])
    title_data_dict['category'] = str(list[4])

    client = MongoClient('127.0.0.1', 27017)
    db = client.shiyanlou
    for x in db.tag.find():
        if x['id'] == title_data_dict['id']:
            title_data_dict['tag']=x['tag']
        elif x['id'] == title_data_dict['id']:
            title_data_dict['tag']=x['tag']

    title_data.append(title_data_dict)

print('****title_data*****')
print(title_data)


@app.route('/')
def index():
    return render_template('index.html',title_data=title_data)



@app.route('/files/<fileId>')
def file(fileId):
    for i in range(len(title_data)):
        if (int(fileId) == int(title_data[i]['id'])):
            return render_template('file.html', hello=title_data[i])
    return render_template('404.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run()
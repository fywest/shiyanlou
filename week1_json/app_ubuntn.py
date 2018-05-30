#!/usr/bin/env python3
from flask import Flask, render_template,redirect,url_for,make_response,request,abort

import json
import os


filetitle={}
helloworld={}
helloshiyanlou={}

d=os.getcwd()
parent_path=os.path.dirname(d)
filepath=os.path.join(parent_path,"files")
helloworld_path=os.path.join(filepath,"helloworld.json")
helloshiyanlou_path=os.path.join(filepath,"helloshiyanlou.json")
with open(helloworld_path,'r') as file:
    helloworld=json.loads(file.read())
    filetitle['helloworld']=helloworld['title']



with open(helloshiyanlou_path,'r') as file:
    helloshiyanlou=json.loads(file.read())
    filetitle['helloshiyanlou'] = helloshiyanlou['title']


app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config.update({'SECRET_KEY':'a random string'})

@app.route('/')
def index():
    return render_template('index.html',filetitle=filetitle)


@app.route('/files/<filename>')
def file(filename):
    if(filename=='helloworld'):
        return render_template('file.html',hello=helloworld)
    elif (filename=='helloshiyanlou'):
        return render_template('file.html', hello=helloshiyanlou)
    else:
        return render_template('404.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run()
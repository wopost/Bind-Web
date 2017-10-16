#!/usr/bin/env python
# -*-coding:utf-8 -*-

from flask import request,render_template, redirect,session
from utils import  getone,check,_update,_delete,insert_sql,list
from . import app
from sessions import sessionmsg
import json

field  = ["id","zone","host","type","data","ttl"]
fields  = ["zone","host","type","data","ttl"]

# 域名列表
@app.route('/namedlist/',methods=['GET', 'POST'])
def namedlist():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    result = list('dns_records',field)
    return  render_template('named.html',msg=msg,result=result['msg'])


# 添加域名解析
@app.route('/namedadd/',methods=['GET', 'POST'])
def namedadd():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    if request.method=='POST':
        data= {k:v[0] for k,v in dict(request.form).items()}
        result = insert_sql('dns_records',fields,data)
        if  result['code'] == 0:
            result ={'code':0, 'msg':"Add Zone Successful"}
            return  json.dumps(result)

#修改域名信息
@app.route('/namedupdate/',methods=['GET', 'POST'])
def namedupdate():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    if request.method=='GET':
        named_id = request.args.get('id')
        data={'id':named_id}
        result = getone('dns_records',data,field)
        return json.dumps(result['msg'])
    if request.method=='POST':
        data= {k:v[0] for k,v in dict(request.form).items()}
        result = _update('dns_records',field,data)
        return json.dumps(result)

#删除域名信息
@app.route('/nameddelete/',methods=['GET', 'POST'])
def nameddelete():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    if request.method=='GET':
        dataid = request.args.get('id')
        data  =  {'id':dataid}
        if _delete('dns_records',data):
            result ={'code':0, 'msg':"delete user success"}
        return  json.dumps(result)

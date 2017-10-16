#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask import Flask,request,render_template,redirect,session
import json
import hashlib
import paramiko
from utils  import    insert_sql,list,_delete,getone,_update

salt='98b85629951ad584feaf87e28c073088'

app = Flask(__name__)
app.secret_key = "98b85629951ad584feaf87e28c0730881"

import login
import user
import userlist
import named

#!/usr/bin/env python
# -*-coding:utf-8 -*-
from flask import session
def sessionmsg():

    msg = {'username':session['username'],'role':session['role']}
    return msg


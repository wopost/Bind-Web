#!/usr/bin/env  python
#_*_ coding:utf-8 _*_
__author__ = 'Eagle'
import MySQLdb as mysql
import config

connect_db = mysql.connect(
                           user   =  config.db_user,
                           passwd =  config.db_passwd,
                           db     =  config.db_name ,
                           host   =  config.db_host,
                           charset=  "utf8" )
cur = connect_db.cursor()



# 获得注册信息，并写入数据库
def insert_sql(table_name,field,data):
    sql = "INSERT INTO %s (%s) VALUES (%s);" % (table_name, ','.join(field), ','.join(['"%s"' % data[x] for x in field]))
    print sql
    res = cur.execute(sql)
    connect_db.commit()
    if  res:
        result = {'code':0,'msg':'insert ok'}
    else:
        result = {'code':1,'msg':'insert fail'}
    return result

# 获得数据列表  
def list(table_name,field):
    sql = "select  *  from %s ;" % table_name
    cur.execute(sql)
    res = cur.fetchall()
    if res:
        user = [dict((k,row[i]) for i,k in enumerate(field))for row in res]
        result = {'code':0,'msg':user}
    else:
        result = {'code':1,'errmsg':'data is null'}

    return  result
# 获取一条数据
def getone(table,data,field):
    if data.has_key('username'):
        sql = 'select * from %s where username="%s";' % (table,data['username'])
    else:
        sql = 'select %s  from %s where id="%s";' % (','.join(field),table,data['id'])
    print sql
    cur.execute(sql)
    res = cur.fetchone()
    if res:
        user = {k:res[i] for i,k in enumerate(field)}
        result  = {'code':0,'msg':user}
    else:
        result ={'code':1, 'msg':"data is null"}
    return result 

# 数据更新
def _update(table,field,data): 
    conditions = ["%s='%s'" % (k,data[k]) for k in data]
    sql = "update %s set %s where id=%s ;" %(table,','.join(conditions),data['id'])
    print sql 
    res = cur.execute(sql)
    if res :
        connect_db.commit()
        result = {'code':0,'msg':'update ok'}
    else:
        result = {'code':1,'errmsg':'Update fail'}
    return result 


# 数据删除
def _delete(table_name,data):
    tag=False
    try:
        sql = 'DELETE FROM %s where id="%s" ;' % (table_name,data['id'])
        if  cur.execute(sql):
            connect_db.commit()
            tag=True
    except Exception, e:
        print 'Error %s' % (sql)
    return   tag

# 用户是否存在监测
def check(table,field,where):
    if isinstance(where, dict) and where:
        conditions = []
        for k,v in where.items():
            conditions.append("%s='%s'" % (k, v))
    sql = "select %s from %s where %s ;" % (','.join(field),table,' AND '.join(conditions))
    print sql
    try:
        if  cur.execute(sql):
            res = cur.fetchone()
            print res
            user =  {k:res[i] for i,k in enumerate(field)}
            print user
            result  = {'code':0,'msg':user}
        else:
            result ={'code':1, 'msg':"data is null"}
    except Exception, e:
        result ={'code':1, 'msg':"SQL Error "}

    return  result



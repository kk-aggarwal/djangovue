
from django import forms

from djangovue.connections import open_db_connection,dictfetchall



def suppcodechoices():
    #cursor = conInStr.cursor()
    
    
    sql = "SELECT code,name FROM suppliers "
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)
    options=[(d['code'],str(d['code'])+": "+d["name"]) for d in c1]
    options.insert(0,('', '----'))
    return options

def despatchchoices():
    #cursor = conInStr.cursor()
    
    
    sql = "SELECT code,des FROM despatchmode "
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)

    return [(d['code'],str(d['code'])+": "+d["des"]) for d in c1]
def currencychoices():
    #cursor = conInStr.cursor()
    
    
    sql = "SELECT code,des FROM currencycodes "
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)

    return [(d['code'],str(d['code'])+": "+d["des"]) for d in c1]

def pricechoices():
    #cursor = conInStr.cursor()
    
    
    sql = "SELECT code,des FROM pricing "
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)
    
    choices=[(d['code'],str(d['code'])+": "+d["des"]) for d in c1]
    
    
    return choices





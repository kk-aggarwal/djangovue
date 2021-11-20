from contextlib import contextmanager
import pyodbc
import sys
from collections import OrderedDict


connection_string={}
connection_string['edssql']='DRIVER={SQL Server};SERVER=laptop-kk\sqlexpress;DATABASE=edssql;Integrated Security=False;Trusted_Connection=False'
#connection_string['opllayout']='DRIVER={SQL Server};SERVER=dc;DATABASE=opllayouts;Integrated Security=False;Trusted_Connection=False'
connection_string['incomingstore']='DRIVER={SQL Server};SERVER=laptop-kk\sqlexpress;DATABASE=incomingstore;Integrated Security=False;Trusted_Connection=False'
#connection_string['accounts']='DRIVER={SQL Server};SERVER=dc;DATABASE=accounts;Integrated Security=False;Trusted_Connection=False'
#connection_string['general']='DRIVER={SQL Server};SERVER=dc;DATABASE=general;Integrated Security=False;Trusted_Connection=False'

#connection_string['pyrl']='DSN=dpc1;UID=pyrl;PWD=pyrl'
#connection_string['mcst']='DSN=dpc1;UID=m_cst;PWD=m_cst'
#connection_string['taxpro']='DRIVER={SQL Server Native Client 10.0};SERVER=192.100.200.49;DATABASE=SmartOffice;UID=sa;PWD=taxpro1234'

@contextmanager
def open_db_connection(database,commit=False):
    connection = pyodbc.connect(connection_string[database])
    cursor = connection.cursor()
    try:
        yield cursor
    except pyodbc.DatabaseError as err:
        error, = err.args
        sys.stderr.write(error.message)
        cursor.execute("ROLLBACK")
        raise err
    else:
        if commit:
            cursor.execute("COMMIT")
        else:
            cursor.execute("ROLLBACK")
    finally:
        connection.close()





def dictfetchall(cursor):
    desc=cursor.description
    #print (desc)
    return[OrderedDict(zip([col[0].lower() for col in desc],row)) for row in cursor.fetchall()]
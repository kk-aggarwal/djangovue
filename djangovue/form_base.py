from django import  forms

from djangovue.connections import open_db_connection,dictfetchall
import pyodbc

class baseform(forms.Form):
    def update_values_of_query(self,request):
    

        set = ''
        for f in self.changed_data:
            if set == '':
                if isinstance(self.cleaned_data[f], str):
                    set = set + f + "='%s'" % self.cleaned_data[f]
                elif isinstance(self.cleaned_data[f], bool):
                    set = set + f + "=%d" % self.cleaned_data[f]
                else:
                    set = set + f + '=%r' % self.cleaned_data[f]
            else:
                if isinstance(self.cleaned_data[f], str):
                    set = set + ',' + f + "='%s'" % self.cleaned_data[f]
                elif isinstance(self.cleaned_data[f], bool):
                    set = set + ',' + f + "=%d" % self.cleaned_data[f]
                else:
                    set = set + ',' + f + '=%r' % self.cleaned_data[f]
        set=set+",username='%s'"%request.user.username
        return set
    def insert_values_of_query(self,request):
        
        print(self.fields)
        selffields=self.fields.copy()
        fields = ','.join(self.fields)
        print(fields)
        v = ''
        for f in self.fields:
            # print(f)
            if self.cleaned_data[f]!=None:
                if v == '':
                    if isinstance(self.cleaned_data[f], str):
                        v = v + "'%s'" % self.cleaned_data[f]
                    elif isinstance(self.cleaned_data[f], bool):
                        v = v + "%d" % self.cleaned_data[f]
                    else:
                        v = v + "%r" % self.cleaned_data[f]
                else:
                    if isinstance(self.cleaned_data[f], str):
                        v = v + ",'%s'" % self.cleaned_data[f]
                    elif isinstance(self.cleaned_data[f], bool):
                        v = v + ",%d" % self.cleaned_data[f]
                    else:
                        v = v + ",%r" % self.cleaned_data[f]
            else:
                selffields.pop(f)
        fields= ','.join(selffields)
        fields=fields+',username'
        v=v+",'%s'"%request.user.username
        return fields,v
    @staticmethod
    def runQuery(database,sql):
        data={}
        #databases={'edssql':settings.CON,'incomingstore':settings.CONINSTR}
        #con=databases[database]
        #cursor = con.cursor()
        try:
            print(sql)

            with open_db_connection(database,True) as cursor:
                rowcount=cursor.execute(sql).rowcount
                if cursor.description==None:
                    c1=None
                else:
                    c1 = dictfetchall(cursor)
            #cursor.execute(sql)
            #con.commit()

            data['success']=True
            data['exception']=''
            data['cursor']=c1
            return data
        except pyodbc.DatabaseError as e:
            print(e)
            data['success'] = False
            data['exception'] = e.__str__()
            return data
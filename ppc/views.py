from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth import authenticate,logout,login
from django.http import HttpResponse, Http404, HttpResponseRedirect,JsonResponse,HttpResponseNotFound
from ppc.models import Operation,OlItemStatus
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from datetime import datetime

from djangovue.connections import open_db_connection,dictfetchall

# Create your views here.

#@login_required
def Index(request):
    template = "ppc/index_d.html"
    return render(request,template,context={'a':'kk'})

def ajax_workordernos(request):
    urls = {}
    tableparticulars = {}

    documentnos=[163,165,173,175,179,180,181,182,183,184,186,187,188,212,216,217]
    sql="select dno,des,won,warrant,dated from ProdPapers_Hom where dno in"+ str(tuple(documentnos))
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = [ 'dno', 'des','won','warrant']
        for item in c1:
            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
        tableFields_verbose={ 'dno':'dno', 'des':'des','won':'won','warrant':'warrant'}

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success}, safe=False)


def ajax_parentsec(request):
    urls = {}
    tableparticulars = {}
    dno = int(request.GET.get('dno', ''))

    c1 = [{'parentsec':1224,'dno':dno},{'parentsec':1251,'dno':dno},{'parentsec':1252,'dno':dno},{'parentsec':1255,'dno':dno},{'parentsec':1256,'dno':dno},{'parentsec':1257,'dno':dno},{'parentsec':1259,'dno':dno}]
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = [ 'parentsec']
        for item in c1:
            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                if f=='qty':
                    color='blue'
                item['fieldcolor']={f:color}
        tableFields_verbose={ 'parentsec':'parentsec'}

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success}, safe=False)


def operation_completion(drwgno, dno, parentsec):
    itemno = 0
    #sql = "select isnull(altindex,'') as altindex from mainitems where itemcodesuffix+itemcodeno='%s'" % drwgno
    sql="select drwgno from ProdPapersItems_homView where dno=%s and drwgnoa='%s'"%(dno,drwgno)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #drwgnoa = drwgno + c1[0]['altindex']
    drwgnoa =  c1[0]['drwgno'].lower()

    sql = "select opllayouts.[dbo].[GetCommaSeparatedOpList]('%s', %s)  as OpList,dno=%s,drwgno='%s',parentsec=%s" % (
    drwgnoa, itemno, dno, drwgno, parentsec)
    #print(sql)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #print(c1)
    pdc=''
    if len(c1) > 0:

        for item in c1:
            try:
                olitemstatus=OlItemStatus.objects.get(dno=dno, drwgno=drwgno, itemno=itemno)
            except ObjectDoesNotExist:
                olitemstatus=None
            if olitemstatus==None:
                pdc=''
            else:
                pdc=olitemstatus.PDC

            opstatus = []
            for op in item['oplist'].split(','):
                try:
                    operation = Operation.objects.get(dno=dno, drwgno=drwgno, itemno=itemno, opno=op)
                except ObjectDoesNotExist:
                    operation = None
                if operation == None:
                    opstatus.append(0)

                else:
                    opstatus.append(operation.status)

        cou = -1
        for i,v in enumerate(opstatus):

            if v:
                cou=i
        #print(cou)
        complete=str(int((cou+1)/len(opstatus)*100))
        if complete=="100":
            pdc='C'
        completion = (complete + "%", len(opstatus),pdc)
    else:
        completion = "unknown", 0,pdc
    return completion


def ajax_orderlist(request):
    urls = {}
    tableparticulars = {}
    tableFields_width={}
    dno = int(request.GET.get('dno', ''))
    psec=int(request.GET.get('parentsec', ''))
    field=request.GET.get('field', '')
    #print(field)
    sql="select drwgnoa,itemdesig,isnull(rawmat,'not specified') as rawmat,qty,dno,workorderno,dno,parentsec from ProdPapersItems_homView where itemno=0 and dno =%s and parentsec=%s order by drwgnoa"%(dno,psec)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = [ 'drwgno','drwgnoa','itemdesig','controlnos','rawmat', 'qty','completion','PDC']

        for item in c1:
            sql = "select controlno,itemno,qtyme from smallpartscontrolregister where drwgno='" + item['drwgnoa'] +"' and won='"+ item['workorderno']+"' order by controlno"
            with open_db_connection('edssql') as cursor:
                cursor.execute(sql)
                c2 = dictfetchall(cursor)
            if len(c2)>0:
                controlnos="; ".join(['cno:'+str(item['controlno'])+',ino:'+str(item['itemno'])+',qty:'+str(item['qtyme']) for item in c2])
            else:
                controlnos=''
            item['controlnos']=controlnos
            item['completion'], item['operations'], item['PDC'] = operation_completion(item['drwgnoa'], item['dno'],
                                                                          item['parentsec'])
            href = "http://192.100.200.45/mtpinfoshare/homstockposition/?drwgno=" + item['drwgnoa']
            item['drwgno'] = "<a target='_blank' href='%s' style='color:blue;text-decoration: underline;'>" % (href) + item['drwgnoa'] + "</a>"

            color='default'
            item['rowcolor']=color
            item['fieldcolor']={}
            for f in formFields:
                color='default'
                if f=='completion' and item['completion']!='100%':
                    color='red'
                    item['fieldcolor'].update({f: color})
                #if f=='drwgnoa':
                    #href="http://192.100.200.45/mtpinfoshare/homstockposition/?drwgno="+ item[f]
                    #item['drwgno']="<a target='_blank' href='%s'>"%href +item[f]+"</a>"
        tableFields_verbose={ 'drwgno':'drwgno','drwgnoa':'drwgnoa' ,'itemdesig':'itemdesig','controlnos':'controlnos','rawmat':'rawmat','qty':'qty','completion':'completion','PDC':'PDC'}
        tableFields_width['drwgnoa']='0%'
        tableparticulars['completion']=str(round(sum([int(c['completion'][0:-1]) for c in c1])/len(c1),2))+'%'
        tableparticulars['Total parts'] =len(c1)

        tableparticulars['100% complete']=sum([1 for k in c1 if k['completion']=='100%'])
        tableparticulars['>50% complete'] = sum([1 for k in c1 if k['completion'] > '50%'])
        tableparticulars['0% complete'] = sum([1 for k in c1 if k['completion']== '0%'])

        for k in formFields[::-1]:
            #print(k)
            if k=='completion':
                sortedc1=sorted(c1,key=lambda i:(int(i['completion'][0:-1]),-i['operations']))
            elif k=='PDC':
                print(item['PDC'])
                sortedc1 = sorted(c1, key=lambda i: ('' if i['PDC']==None else str(i['PDC']),int(i['completion'][0:-1])),reverse=False)
            else:
                sortedc1 = sorted(c1, key=lambda c: float(str(c[k]).strip().lower()) if str(
                    c[k]).strip().lower().replace('.', '', 1).isdigit() else str(c[k]).strip().lower())

            n = 0
            for c in sortedc1:
                c['sortkey_' + k] = n
                n += 1

        """sorted(c1,key=lambda i:(int(i['completion'][0:-1]),-i['operations']))"""

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,'tableFields_width':tableFields_width,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success}, safe=False)

def ajax_smallparts_running(request):
    urls = {}
    tableparticulars = {}
    won = (request.GET.get('workorderno', ''))
    drwgno=(request.GET.get('drwgno', ''))
    sql="select controlno,paper,drwgno,itemno,won,qtyru,replace(convert(varchar(11),dateru,106),' ','-') as dateru from smallpartscontrolregisterview where won='%s' and drwgno ='%s' and qtyru>0"%(won,drwgno)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = [ 'controlno', 'paper','itemno','dateru','qtyru']
        for item in c1:

            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                if f=='qtyru':
                    color="blue"
                item['fieldcolor']={f:color}
        tableFields_verbose={ 'controlno':'controlno', 'paper':'paper','itemno':'itemno','dateru':'date','qtyru':'qty'}

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success}, safe=False)

def ajax_hom_transac(request):
    urls = {}
    tableparticulars = {}
    won = (request.GET.get('won', ''))
    drwgno=(request.GET.get('drwgno', ''))
    sql="select drwgno,won,rec as qty,replace(convert(varchar(11),transacdate,106),' ','-') as dated from homtransacview where won='%s' and drwgno ='%s' and rec>0"%(won,drwgno)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = ['dated','qty']
        for item in c1:
            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                if f=='qty':
                    color="red"
                item['fieldcolor']={f:color}
        tableFields_verbose={ 'dated':'dated', 'qty':'qty'}

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success}, safe=False)
        
def ajax_operations(request):
    urls = {}
    tableparticulars = {}
    dno = (request.GET.get('dno', ''))
    drwgno = (request.GET.get('drwgno', ''))
    parentsec = (request.GET.get('parentsec', ''))
    itemno=0
    fields = {'oplist': {'verbose': 'oplist', 'align': 'center','width':'35%', 'summary': '', 'summaryinfo': ''},
              'remarks':{'verbose': 'remarks', 'align': 'center','width':'40%', 'summary': '', 'summaryinfo': ''},
              'pdc': {'verbose': 'pdc', 'align': 'center', 'width': '25%', 'summary': '', 'summaryinfo': ''},

              }
    formFields = list(fields.keys())
    tableFields_verbose = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('verbose', k) for k in fields])}
    tableFields_align = {i: j for (i, j) in
                         zip(list(fields.keys()), [fields[k].get('align', 'center') for k in fields])}
    tableFields_width = {i: j for (i, j) in
                         zip(list(fields.keys()), [fields[k].get('width', '10%') for k in fields])}
    tableFields_summary = {i: j for (i, j) in
                           zip(list(fields.keys()), [fields[k].get('summary', 'center') for k in fields])}
    tableFields_summaryinfo = {i: j for (i, j) in
                               zip(list(fields.keys()), [fields[k].get('summaryunfo', 'center') for k in fields])}

    # sql = "select isnull(altindex,'') as altindex from mainitems where itemcodesuffix+itemcodeno='%s'" % drwgno
    sql = "select drwgno from ProdPapersItems_homView where dno=%s and drwgnoa='%s'" % (dno, drwgno)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #drwgnoa=drwgno+c1[0]['altindex']
    drwgnoa = c1[0]['drwgno']
    """select item,opllayouts.[dbo].[GetCommaSeparatedOpList](oplmain.suffix+oplmain.itemcode, oplmain.item)  as OpList from oplmain where suffix+itemcode='f1176013'"""

    sql="select opllayouts.[dbo].[GetCommaSeparatedOpList]('%s', %s)  as OpList,dno=%s,drwgno='%s',parentsec=%s,remarks=''"%(drwgnoa,itemno,dno,drwgno,parentsec)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        #formFields = ['oplist','remarks','pdc']
        for item in c1:
            opstatus=[]
            datestatus=[]
            for op in item['oplist'].split(','):
                try:
                    operation=Operation.objects.get(dno=dno,drwgno=drwgno,itemno=itemno,opno=op)
                except ObjectDoesNotExist:
                    operation=None
                if operation==None:
                    opstatus.append(0)
                    datestatus.append('')
                else:
                    opstatus.append(operation.status)
                    datestatus.append(operation.dated)
            try:
                olitemstatus=OlItemStatus.objects.get(dno=dno,drwgno=drwgno,itemno=itemno)
            except ObjectDoesNotExist:
                olitemstatus = None
            if olitemstatus==None:
                item['PDC'] =''
                item['remarks'] = ''
            else:
                item['PDC']=olitemstatus.PDC
                item['remarks']=olitemstatus.remarks
            item['opstatus']=opstatus
            item['datestatus']=datestatus
            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                if f=='qty':
                    color="red"
                item['fieldcolor']={f:color}
        #tableFields_verbose={ 'oplist':'oplist','remarks':'remarks','pdc':'PDC'}
        #print(c1)
        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'tableFields_align': tableFields_align,'tableFields_width': tableFields_width,'tableFields_summary': tableFields_summary,'tableFields_summaryinfo': tableFields_summaryinfo,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success}, safe=False)

@login_required
def operationcreate(request):

    username = str(request.user.get_username())
    user=(request.POST.get('user', ''))
    
    if request.user.is_authenticated and (request.user.groups.filter(name='ppc-smallparts').exists()):
        success=True
    else:
        success=False
        #return HttpResponseRedirect("/accounts/login/")
    dno = int(request.POST.get('dno', ''))
    drwgno = (request.POST.get('drwgno', ''))
    itemno=int(request.POST.get('itemno', ''))
    opno=(request.POST.get('opno', ''))
    status=(request.POST.get('status', ''))
    status=True if status=='true' else False
    #operation=Operation(dno=dno,drwgno=drwgno,itemno=itemno,status=status,opno=opno)
    operation,created=Operation.objects.update_or_create(dno=dno,drwgno=drwgno,itemno=itemno,opno=opno,defaults={'status':status})
    

    return JsonResponse({'success': success}, safe=False)

def olitempdcupdate(request):
    pass
def olitemremarksupdate(request):
    username = str(request.user.get_username())
    print(username)
    if request.user.is_authenticated and (request.user.groups.filter(name='ppc-smallparts').exists()):
        success = True
    else:
        success = False
        # return HttpResponseRedirect("/accounts/login/")
    dno = int(request.POST.get('dno', ''))
    drwgno = (request.POST.get('drwgno', ''))
    itemno = int(request.POST.get('itemno', ''))
    remarks = (request.POST.get('remarks', ''))

    # operation=Operation(dno=dno,drwgno=drwgno,itemno=itemno,status=status,opno=opno)
    olitem, created = OlItemStatus.objects.update_or_create(dno=dno, drwgno=drwgno, itemno=itemno,
                                                            defaults={'remarks': remarks})

    return JsonResponse({'success': success}, safe=False)

def olitempdcupdate(request):
    username = str(request.user.get_username())
    print(username)
    if request.user.is_authenticated and (request.user.groups.filter(name='ppc-smallparts').exists()):
        success = True
    else:
        success = False
        # return HttpResponseRedirect("/accounts/login/")
    dno = int(request.POST.get('dno', ''))
    drwgno = (request.POST.get('drwgno', ''))
    itemno = int(request.POST.get('itemno', ''))
    pdc = (request.POST.get('pdc', ''))
    print(pdc)
    #pdc=datetime.strptime(pdc, '%Y-%m-%d').strftime("%d-%b-%Y")
    print(pdc)
    # operation=Operation(dno=dno,drwgno=drwgno,itemno=itemno,status=status,opno=opno)
    olitem, created = OlItemStatus.objects.update_or_create(dno=dno, drwgno=drwgno, itemno=itemno,
                                                            defaults={'PDC': pdc})
    #print(list(olitem),created)
    return JsonResponse({'success': success}, safe=False)

def ajax_shortagelists(request):
    urls = {}
    tableparticulars = {}

    documentnos=[2660,2661,2662]
    sql="select dno,des,won,warrant,dated from ProdPapers_Hom_issue where dno in"+ str(tuple(documentnos))
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = [ 'dno', 'des','won','warrant']
        for item in c1:
            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
        tableFields_verbose={ 'dno':'dno', 'des':'des','won':'won','warrant':'warrant'}

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success}, safe=False)


def ajax_shortagelist(request):
    urls = {}
    tableparticulars = {}
    tableFields_width={}
    dno = int(request.GET.get('dno', ''))
    psec=int(request.GET.get('parentsec', ''))
    field=request.GET.get('field', '')
    #print(field)
    sql="select (drwgno+isnull(suffix,'')) as drwgno,drwgno as drwgnoa,itemdesig,qty,dno,won as workorderno,dno,parentsec from ProdPapers_homItems_issueView where  dno =%s and parentsec=%s order by drwgnoa"%(dno,psec)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = [ 'drwgno','drwgnoa','itemdesig', 'qty','controlnos',]

        for item in c1:
            sql = "select controlno,itemno,qtyme from smallpartscontrolregister where drwgno='" + item['drwgnoa'] +"' and won='"+ item['workorderno']+"' order by controlno"
            with open_db_connection('edssql') as cursor:
                cursor.execute(sql)
                c2 = dictfetchall(cursor)
            if len(c2)>0:
                controlnos="; ".join(['cno:'+str(item['controlno'])+',ino:'+str(item['itemno'])+',qty:'+str(item['qtyme']) for item in c2])
            else:
                controlnos=''
            item['controlnos']=controlnos
            #item['completion'], item['operations'], item['PDC'] = operation_completion(item['drwgnoa'], item['dno'],
             #                                                             item['parentsec'])
            href = "http://192.100.200.45:8090/mtpinfoshare/homstockposition/?drwgno=" + item['drwgnoa']
            item['drwgno'] = "<a target='_blank' href='%s' style='color:blue;text-decoration: underline;'>" % (href) + item['drwgnoa'] + "</a>"

            color='default'
            item['rowcolor']=color
            item['fieldcolor']={}
            for f in formFields:
                color='default'
                if f=='completion' and item['completion']!='100%':
                    color='red'
                    item['fieldcolor'].update({f: color})
                #if f=='drwgnoa':
                    #href="http://192.100.200.45/mtpinfoshare/homstockposition/?drwgno="+ item[f]
                    #item['drwgno']="<a target='_blank' href='%s'>"%href +item[f]+"</a>"
        tableFields_verbose={ 'drwgno':'drwgno','drwgnoa':'drwgnoa' ,'itemdesig':'itemdesig','controlnos':'controlnos','rawmat':'rawmat','qty':'qty','completion':'completion','PDC':'PDC'}
        #tableFields_width['drwgnoa']='0%'
        #tableparticulars['completion']=str(round(sum([int(c['completion'][0:-1]) for c in c1])/len(c1),2))+'%'
        #tableparticulars['Total parts'] =len(c1)

        #tableparticulars['100% complete']=sum([1 for k in c1 if k['completion']=='100%'])
        #tableparticulars['>50% complete'] = sum([1 for k in c1 if k['completion'] > '50%'])
        #tableparticulars['0% complete'] = sum([1 for k in c1 if k['completion']== '0%'])

        for k in formFields[::-1]:
            #print(k)
            if k=='completion':
                sortedc1=sorted(c1,key=lambda i:(int(i['completion'][0:-1]),-i['operations']))
            elif k=='PDC':
                print(item['PDC'])
                sortedc1 = sorted(c1, key=lambda i: ('' if i['PDC']==None else str(i['PDC']),int(i['completion'][0:-1])),reverse=False)
            else:
                sortedc1 = sorted(c1, key=lambda c: float(str(c[k]).strip().lower()) if str(
                    c[k]).strip().lower().replace('.', '', 1).isdigit() else str(c[k]).strip().lower())

            n = 0
            for c in sortedc1:
                c['sortkey_' + k] = n
                n += 1

        """sorted(c1,key=lambda i:(int(i['completion'][0:-1]),-i['operations']))"""

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,'tableFields_width':tableFields_width,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success}, safe=False)












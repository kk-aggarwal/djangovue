from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect,JsonResponse,HttpResponseNotFound
from django.urls import reverse
import json
from django.template.loader import render_to_string
from pyodbc import Error

from djangovue.connections import open_db_connection,dictfetchall
from .forms import poeditForm,poitemeditForm,poauthForm
import pyodbc
import adodbapi
import win32com.client as win32
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.contrib.auth import authenticate
# Create your views here.


def getcurrentyear(request):
    sql = "select yearid from stcurrentyear"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    stCurrentYear = c1[0]['yearid']
    #stCurrentYear='2020-2021'
    return JsonResponse({'stcurrentyear': stCurrentYear,})

def pos(request):
    finyear=request.GET.get('finyear', '')
    group=request.GET.get('group','')
   
    urls = {}
    tableData = []
    tableFields = []
    fields = {}
    formFields = []
    tableFields_verbose = {}
    tableparticulars = {}
    tableFields_align={}
    tableFields_width={}
    tableFields_summary={}
    tableFields_summaryinfo = {}

    
    

    fields = {'authstatus': {'verbose': 'Status', 'align': 'center'},'poid': {'verbose': 'PO ref ', 'align': 'center','summary':'','summaryinfo':''},
    'pono': {'verbose': 'Po no', 'align': 'center'},
    'amendno': {'verbose': 'Amend', 'align': 'center'},
    'dated': {'verbose': 'PO Date', 'align': 'right'},
    'suppcode': {'verbose': 'Supplier', 'align': 'right'},
    'mprs': {'verbose': 'MPRs', 'align': 'right'},
    'items': {'verbose': 'Items', 'align': 'center'},
    'amendments': {'verbose': 'amendments', 'align': 'center'},
    
    }
    formFields = list(fields.keys())
    tableFields_verbose = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('verbose',k) for k in fields])}
    tableFields_align = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('align','center') for k in fields])}
    tableFields_width = {i: j for (i, j) in
                         zip(list(fields.keys()), [fields[k].get('width', '10%') for k in fields])}
   
    tableFields_summary = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summary','center') for k in fields])}
    tableFields_summaryinfo = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summaryunfo','center') for k in fields])}

    sql= "select * from poview as t where (poid in (select max(poid) from poview where authstatus=1 group by pono) or authstatus=0) and [year]='" + finyear + "' order by [year],pono asc,poid asc"


    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    try:
        urls['urlcreate'] = request.build_absolute_uri(reverse('pocreate', kwargs={'finyear':finyear,'poid': 0, }))
    except:
        urls['urlcreate'] = ''

    success = "true"
    # print(c1)
    if len(c1) > 0:
        tableData = c1

        
        # print(tableFields)
        
        for item in c1:
            sql="SELECT * From poview WHERE (pono =" + str(item["pono"]) + " and authstatus=0) "
            with open_db_connection('edssql') as cursor:
                cursor.execute(sql)
                c2 = dictfetchall(cursor)
            if len(c2)>0:
                item['pendingamendment']=1
            else:
                item['pendingamendment']=0
            item['urledit'] = request.build_absolute_uri(reverse('poedit', kwargs={'finyear':finyear,'poid': item['poid'], }))
            
            item['urlprint'] = request.build_absolute_uri(reverse('poprint', kwargs={'poid': item['poid'], }))
          
            item['mprs']=po_mprs(item['poid'])
            item['items']=po_items(item['poid'])
            item['amendments']=NoAmendments(item['poid'])
            item['potype']="" if item['potype']==None else item['potype']
            color = 'default'
            item['rowcolor'] = color
            item['fieldcolor'] = {}
            for f in tableFields:
                color = 'default'
                if f == 'potype' and item['potype']==2:
                    color = 'red'
                item['fieldcolor'].update({f: color})
            item['mprs']=po_mprs(item['poid'])
            item['items']=po_items(item['poid'])
        tableFields = list(c1[0].keys()) 
               # print(item['fieldcolor'])
        # for k in formFields[::-1]:
        
        #     sortedc1 = sorted(c1, key=lambda c: float(str(c[k]).strip().lower()) if str(
        #     c[k]).strip().lower().replace('.', '', 1).isdigit() else str(c[k]).strip().lower())
        #     n = 0
        #     for c in sortedc1:
        #         c['sortkey_' + k] = n
        #         n += 1
        # tableData=sortedc1
        
    else:
        tableData = []
        tableFields = formFields

    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,
                         'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars,'tableFields_align': tableFields_align,'tableFields_width':tableFields_width,'tableFields_summary': tableFields_summary,'tableFields_summaryinfo': tableFields_summaryinfo}, safe=False)

def poedit(request,poid,finyear):
    submitbuttondisabled="false"
    html_form=''
    #print(request.method)
    sql = "SELECT * from po where poid=%s"%(poid)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #print(c1[0])
    success = "True"
    if len(c1)>0:

        if request.method == 'GET':
            form = poeditForm(initial=c1[0])
            #form.fields['stockno'].widget.attrs['readonly'] = True



            context = {'form': form,'save':'saveMe_edit','poid':poid,'finyear':finyear,'formaction':'poedit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('purchase/poedit.html', context, request=request)
            #print(html_form)
            success='True'
        if request.method == 'POST':
            #print('save form')
            #print(dict(request.POST))
            #print(c1[0])
            #a={k:v[0] if len(v)==1 else v for k,v in request.POST.lists()}
            form=poeditForm(request.POST,initial=c1[0])
            #form.fields['stockno'].widget.attrs['readonly'] = True
            #print(form.changed_data)
            if form.is_valid():
                print('edit po')
                data=form.save_update(request)
                if not data['success']:
                    form.add_error(field=None, error=str(data['exception']))
                    success='False'
                else:
                    success = 'True'
            else:
                pass

            context = {'form': form, 'save': 'saveMe_edit', 'poid':poid,'finyear':finyear,'formaction':'poedit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('purchase/poedit.html', context, request=request)
    return JsonResponse({'html_form': html_form,'success':success})

def pocreate(request,poid,finyear):
    submitbuttondisabled = "false"

    success = 'False'
    if request.method == 'GET':
        # print('d')
        form = poeditForm(initial={'year':finyear,})
        # form.fields['mrrdate'].widget.attrs['readonly'] = True

        context = {'form': form, 'save': 'saveMe_add',
                   'formaction': 'pocreate','poid':poid,'finyear':finyear, 'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('purchase/poedit.html', context, request=request)
        # print(html_form)

    if request.method == 'POST':
        # print('dffgg')
        form = poeditForm(request.POST)
        # form.fields['mrrno'].widget.attrs['readonly'] = False
        # print(request.POST)
        if form.is_valid():
            # print('create new mislip')
            data = form.save_create(request)
            if not data['success']:
                form.add_error(field=None, error=str(data['exception']))
                success = 'False'
            else:
                success = 'True'
        else:
            pass
        context = {'form': form, 'save': 'saveMe_add',
                   'formaction': 'pocreate','poid':poid,'finyear':finyear, 'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('purchase/poedit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})

def podel(request,poid):
    pass
def poprint(request,poid):
    pass

def po_mprs(poid):
    sql = "select mprno from po_Mprview where poid=" + str(poid) + " order by mprno"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        return ",".join([item['mprno'] for item in c1 ])
    else:
        return ""
def po_items(poid):
    sql="select count(*) as items from poitems where poid=" + str(poid) + ""
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        return c1[0]['items']
    else:
        return "NIL"

def PendingAmendment(pono):
    sql = "SELECT * From poview WHERE (pono ="+ str(pono) + " and authstatus=0) "
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1) > 0:
        return True
    else:
        return False

def NoAmendments(poid): 
    sql = "SELECT count(*) as no From poamendments WHERE poid =" +str(poid)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1) > 0:
        return c1[0]['no']
    else:
        return 0
    
def poitems(request):
    poid=request.GET.get('poid', '')
    

    urls = {}
    tableData = []
    tableFields = []
    fields = {}
    formFields = []
    tableFields_verbose = {}
    tableparticulars = {}
    tableFields_align={}
    tableFields_width={}
    tableFields_summary={}
    tableFields_summaryinfo = {}

    
    

    fields = {'stockno': {'verbose': 'Stock no', 'align': 'center'},'poid': {'verbose': 'PO ref ', 'align': 'center','summary':'','summaryinfo':''},
    'drwgno': {'verbose': 'Drawing', 'align': 'center'},
    'des': {'verbose': 'Description', 'align': 'center'},
    'unit': {'verbose': 'Unit', 'align': 'right'},
    'qty': {'verbose': 'Qty', 'align': 'right'},
    'rate': {'verbose': 'Rate', 'align': 'right'},
    'discount': {'verbose': 'Discount', 'align': 'center'},
    'doscountbase': {'verbose': 'doscountbase', 'align': 'center'},
    
    }
    formFields = list(fields.keys())
    tableFields_verbose = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('verbose',k) for k in fields])}
    tableFields_align = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('align','center') for k in fields])}
    tableFields_width = {i: j for (i, j) in
                         zip(list(fields.keys()), [fields[k].get('width', '10%') for k in fields])}
   
    tableFields_summary = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summary','center') for k in fields])}
    tableFields_summaryinfo = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summaryunfo','center') for k in fields])}

    sql = "select * from poitemsview where poid=" + poid + ""

    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    try:
        urls['urlcreate'] = request.build_absolute_uri(reverse('poitemcreate', kwargs={'poid': poid,'stockno':'0' }))
    except:
        urls['urlcreate'] = ''

    success = "true"
    # print(c1)
    if len(c1) > 0:
        tableData = c1

        tableFields = list(c1[0].keys())
        # print(tableFields)
        
        for item in c1:

            item['urledit'] = request.build_absolute_uri(reverse('poitemedit', kwargs={'poid': item['poid'],'stockno': item['stockno'],  }))
            item['urldel'] = request.build_absolute_uri(reverse('poitemdel', kwargs={'poid': item['poid'],'stockno': item['stockno'],  }))
            
            color = 'default'
            item['rowcolor'] = color
            item['fieldcolor'] = {}
            for f in tableFields:
                color = 'default'
                if f == 'potype' and item['potype']==2:
                    color = 'red'
                item['fieldcolor'].update({f: color})
            
               # print(item['fieldcolor'])
        # for k in formFields[::-1]:
        
        #     sortedc1 = sorted(c1, key=lambda c: float(str(c[k]).strip().lower()) if str(
        #     c[k]).strip().lower().replace('.', '', 1).isdigit() else str(c[k]).strip().lower())
        #     n = 0
        #     for c in sortedc1:
        #         c['sortkey_' + k] = n
        #         n += 1
        # tableData=sortedc1
        
    else:
        tableData = []
        tableFields = formFields

    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,
                         'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars,'tableFields_align': tableFields_align,'tableFields_width':tableFields_width,'tableFields_summary': tableFields_summary,'tableFields_summaryinfo': tableFields_summaryinfo}, safe=False)

def mpr_items(request):
    mprno=request.GET.get('mprno','')
    print(mprno)
    sql= "select * from latestMprDetail where mprno='" + mprno +"' ORDER BY STOCKNO"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    
    urls = {}
    tableData = []
    tableFields = []
    fields = {}
    formFields = []
    tableFields_verbose = {}
    tableparticulars = {}
    tableFields_align={}
    tableFields_width={}
    tableFields_summary={}
    tableFields_summaryinfo = {}

    
    

    fields = {'stockno': {},
    #'amend': {},
    #'drwgno': {},
    #'itemdesig': {'verbose': 'Amend', 'align': 'center'},
    #'qty': {},
    #'unit': {},
    }
    formFields = list(fields.keys())
    tableFields_verbose = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('verbose',k) for k in fields])}
    tableFields_align = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('align','center') for k in fields])}
    tableFields_width = {i: j for (i, j) in
                         zip(list(fields.keys()), [fields[k].get('width', '10%') for k in fields])}
    success = "true"
    print(c1)
    if len(c1) > 0:
        tableData = c1
        for item in c1:
            item["drwgno"]=('' if item['itemcodesuffix']==None else item['itemcodesuffix'])+('' if item['itemcodeno']==None else str(item['itemcodeno']))
            item['fieldcolor'] = {}
            for f in formFields:
                color = 'default'
                
                item['fieldcolor'].update({f: color})
        tableFields = list(c1[0].keys())
    else:
        tableData = []
        tableFields = formFields 
    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                            'tableFields_verbose': tableFields_verbose,
                            'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars,'tableFields_align': tableFields_align,'tableFields_width':tableFields_width,'tableFields_summary': tableFields_summary,'tableFields_summaryinfo': tableFields_summaryinfo}, safe=False)

def poitemedit(request,poid,stockno):
    submitbuttondisabled="false"
    html_form=''
    #print(request.method)
    sql = "SELECT * from poitems where poid=%s and stockno='%s'"%(poid,stockno)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #print(c1[0])
    success = 'False'
    if len(c1)>0:

        if request.method == 'GET':
            form = poitemeditForm(initial=c1[0])
            #form.fields['stockno'].widget.attrs['readonly'] = True



            context = {'form': form,'save':'saveMe_edit','poid':poid,'stockno':stockno,'formaction':'poitemedit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('purchase/poitemedit.html', context, request=request)
            #print(html_form)
            success='True'
        if request.method == 'POST':
            #print('save form')
            #print(dict(request.POST))
            #print(c1[0])
            #a={k:v[0] if len(v)==1 else v for k,v in request.POST.lists()}
            form=poeditForm(request.POST,initial=c1[0])
            #form.fields['stockno'].widget.attrs['readonly'] = True
            #print(form.changed_data)
            if form.is_valid():
                print('edit po item')
                data=form.save_update(request)
                if not data['success']:
                    form.add_error(field=None, error=str(data['exception']))
                    success='False'
                else:
                    success = 'True'
            else:
                pass

            context = {'form': form, 'save': 'saveMe_edit', 'poid':poid,'stockno':stockno,'formaction':'poitemedit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('purchase/poitemedit.html', context, request=request)
    return JsonResponse({'html_form': html_form,'success':success})

def poitemcreate(request,poid,stockno):
    submitbuttondisabled = "false"
    sql = "SELECT mprno FROM po_mpr where poid= "+str(poid)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    mprnos=[(d['mprno'],d['mprno']) for d in c1]
    print(mprnos)
    success = 'False'
    if request.method == 'GET':
        
        # print('d')
        form = poitemeditForm(initial={'poid':poid})
        # form.fields['mrrdate'].widget.attrs['readonly'] = True

        context = {'form': form, 'save': 'saveMe_add',
                   'formaction': 'poitemcreate','poid':poid,'stockno':stockno,'mprnos':mprnos, 'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('purchase/poitemedit.html', context, request=request)
        # print(html_form)

    if request.method == 'POST':
        # print('dffgg')
        form = poitemeditForm(request.POST)
        # form.fields['mrrno'].widget.attrs['readonly'] = False
        # print(request.POST)
        if form.is_valid():
            # print('create new mislip')
            data = form.save_create(request)
            if not data['success']:
                form.add_error(field=None, error=str(data['exception']))
                success = 'False'
            else:
                success = 'True'
        else:
            pass
        context = {'form': form, 'save': 'saveMe_add',
                   'formaction': 'pocreate','poid':poid,'stockno':stockno,'mprnos':mprnos, 'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('purchase/poitemedit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})

def poitemdel(request,poid,stockno):
    pass

def poamendments(request):
    poid=request.GET.get('poid', '')
    

    urls = {}
    tableData = []
    tableFields = []
    fields = {}
    formFields = []
    tableFields_verbose = {}
    tableparticulars = {}
    tableFields_align={}
    tableFields_width={}
    tableFields_summary={}
    tableFields_summaryinfo = {}

    
    

    fields = {
        'poid': {'verbose': 'PO ref ', 'align': 'center','summary':'','summaryinfo':''},
        'stockno': {'verbose': 'Stock no', 'align': 'center'},
    
    'des': {'verbose': 'Description', 'align': 'center'},
    'fieldname': {'verbose': 'fieldname', 'align': 'right'},
    'tablename': {'verbose': 'tablename', 'align': 'right'},
    'whereclause': {'verbose': 'whereclause', 'align': 'right'},
    'amendid': {'verbose': 'amendid', 'align': 'center'},
    'type': {'Base': 'amendments', 'align': 'center'},
    
    }
    formFields = list(fields.keys())
    tableFields_verbose = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('verbose',k) for k in fields])}
    tableFields_align = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('align','center') for k in fields])}
    tableFields_width = {i: j for (i, j) in
                         zip(list(fields.keys()), [fields[k].get('width', '10%') for k in fields])}
   
    tableFields_summary = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summary','center') for k in fields])}
    tableFields_summaryinfo = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summaryunfo','center') for k in fields])}

    sql = "select * from poamendmentsview  where poid=" + poid + "  order by amendid"

    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    try:
        urls['urlcreate'] = reverse('poamendmentscreate', kwargs={'poid': poid,'stockno': '0', })
    except:
        urls['urlcreate'] = ''

    success = "true"
    # print(c1)
    if len(c1) > 0:
        tableData = c1

        tableFields = list(c1[0].keys())
        # print(tableFields)
        
        for item in c1:

            item['urledit'] = reverse('poamendmentsedit', kwargs={'poid': item['poid'],'stockno': item['stockno'],  })
            item['urldel'] = reverse('poamendmentsdel', kwargs={'poid': item['poid'],'stockno': item['stockno'],  })
            
            color = 'default'
            item['rowcolor'] = color
            item['fieldcolor'] = {}
            for f in tableFields:
                color = 'default'
                if f == 'potype' and item['potype']==2:
                    color = 'red'
                item['fieldcolor'].update({f: color})
            
               # print(item['fieldcolor'])
        # for k in formFields[::-1]:
        
        #     sortedc1 = sorted(c1, key=lambda c: float(str(c[k]).strip().lower()) if str(
        #     c[k]).strip().lower().replace('.', '', 1).isdigit() else str(c[k]).strip().lower())
        #     n = 0
        #     for c in sortedc1:
        #         c['sortkey_' + k] = n
        #         n += 1
        # tableData=sortedc1
        
    else:
        tableData = []
        tableFields = formFields

    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,
                         'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars,'tableFields_align': tableFields_align,'tableFields_width':tableFields_width,'tableFields_summary': tableFields_summary,'tableFields_summaryinfo': tableFields_summaryinfo}, safe=False)

def poamendmentsedit(request,poid,stockno):
    pass
def poamendmentscreate(request,poid):
    pass
def poamendmentsdel(request,poid,stockno):
    pass

def pomprs(request):
    poid=request.GET.get('poid', '')
    

    urls = {}
    tableData = []
    tableFields = []
    fields = {}
    formFields = []
    tableFields_verbose = {}
    tableparticulars = {}
    tableFields_align={}
    tableFields_width={}
    tableFields_summary={}
    tableFields_summaryinfo = {}

    
    

    fields = {
        'poid': {'verbose': 'PO ref ', 'align': 'center','summary':'','summaryinfo':''},
        'mprno': {'verbose': 'MPR', 'align': 'center'},
    
    'amend': {'verbose': 'Amend No', 'align': 'center'},
    'des': {'verbose': 'Description', 'align': 'right'},
    'gpname': {'verbose': 'Category', 'align': 'right'},
    
    
    }
    formFields = list(fields.keys())
    tableFields_verbose = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('verbose',k) for k in fields])}
    tableFields_align = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('align','center') for k in fields])}
    tableFields_width = {i: j for (i, j) in
                         zip(list(fields.keys()), [fields[k].get('width', '10%') for k in fields])}
   
    tableFields_summary = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summary','center') for k in fields])}
    tableFields_summaryinfo = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summaryunfo','center') for k in fields])}

    sql = "select * from po_Mprview where poid=" + poid + ""

    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    try:
        urls['urlcreate'] = reverse('pomprcreate', kwargs={'poid': poid,'mprno': '0', })
    except:
        urls['urlcreate'] = ''

    success = "true"
    #print(c1)
    if len(c1) > 0:
        tableData = c1

        tableFields = list(c1[0].keys())
        # print(tableFields)
        
        for item in c1:

            item['urledit'] = reverse('pompredit', kwargs={'poid': item['poid'],'mprno': item['mprno'],  })
            item['urldel'] = reverse('pomprdel', kwargs={'poid': item['poid'],'mprno': item['mprno'],  })
            
            color = 'default'
            item['rowcolor'] = color
            item['fieldcolor'] = {}
            for f in tableFields:
                color = 'default'
                if f == 'potype' and item['potype']==2:
                    color = 'red'
                item['fieldcolor'].update({f: color})
            
               # print(item['fieldcolor'])
        # for k in formFields[::-1]:
        
        #     sortedc1 = sorted(c1, key=lambda c: float(str(c[k]).strip().lower()) if str(
        #     c[k]).strip().lower().replace('.', '', 1).isdigit() else str(c[k]).strip().lower())
        #     n = 0
        #     for c in sortedc1:
        #         c['sortkey_' + k] = n
        #         n += 1
        # tableData=sortedc1
        
    else:
        tableData = []
        tableFields = formFields

    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,
                         'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars,'tableFields_align': tableFields_align,'tableFields_width':tableFields_width,'tableFields_summary': tableFields_summary,'tableFields_summaryinfo': tableFields_summaryinfo}, safe=False)

def pompredit(request,poid,stockno):
    pass
def pomprcreate(request,poid):
    pass
def pomprdel(request,poid,stockno):
    pass

def amend_po(request):
    poid=request.GET.get('poid','')
    sql = r'exec copy_po @poid = ' + "" + poid + ""
    print(sql)
    success=''
    try:
        with open_db_connection('edssql',True) as cursor:
            cursor.execute(sql)
        success='success'
    except  pyodbc.DatabaseError as e:
        print(e)
        success=''
    return JsonResponse({'success':success})

def ifNull(data,r):
    return r if data is None else data

def transferPO(poid):
    sql = "SELECT * From poview WHERE (poid =" + str(poid) + ")"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        item = dictfetchall(cursor)

    poDate = item[0].get("podate",'')
    poNo = item[0].get("pono",'')
    suppRef = item[0].get("supprefno","")
    Payterms = item[0].get("payterms", "")
    SuppCode = str(item[0].get("suppcode", ""))
    agentCode = str(item[0].get("agentcode", ""))
    POReason = item[0].get("poreason","")
    PFCharges = "" if item[0].get("pfcharges", "")=="" else str(item[0].get("pfcharges", ""))+"%"
    ILN = item[0].get("iln", "")
    insp = item[0].get("insp", "")
    Interest = item[0].get("interest", "")
    intPeriod = item[0].get("intper", "")
    catCode = item[0].get("catcode", "")
    poprefix = item[0].get("refprefix", "")

    Reason = item[0].get("areason", "")
    amendNo = item[0].get("amendno", "")
    ANote = item[0].get("abottomnote", "")
    ArefNo = item[0].get("arefno", "")
    Adate = item[0].get("adate", "")

    GSTIC = item[0].get("gstic", "")
    HSNCode = item[0].get("hsncode", "")
    RevCharge = item[0].get("revcharge", "")
    SGST = "" if item[0].get("sgst",'') == 0 else "SGST: " + str(item[0]["sgst"]) + "%"
    CGST = "" if item[0].get("cgst",'') == 0 else "CGST: " + str(item[0]["cgst"]) + "%"
    IGST = "" if item[0].get("igst",'') == 0 else "IGST: " + str(item[0]["igst"]) + "%"

    ExDuty = str(item[0]["sgst"]) + str(item[0]["cgst"]) + str(item[0]["igst"]) + "% (" + SGST + "  " + CGST + "  " + IGST + ")"

    sql = "select des,code from salestax where code=" + str(item[0]["cst"])
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    cst=c1[0]['des'] if item[0]['cst']==4 else c1[0]["des"] + " " + str(item[0]["cstvalue"]) + "%"
    
    Price = item[0].get("pricedes", "")
    Insurance = item[0].get("insurance", "")
    bottomNote = item[0].get("bottomnote", "")
    DeliveryNote = item[0].get("deliverynote", "")
    desMode="" if item[0]['despatchdes']==None else item[0]['despatchdes'] if item[0]["despatch"]==1 else item[0]["desmodedes"] + " " + "" if item[0]['despatchdes']==None or item[0]['despatchdes']=="" else ": " +item[0]['despatchdes']
    discountApp = item[0]["discountapp"]
    discountVal = item[0]["discountval"]
    sql = "select * from po_Mprview where poid=" + str(poid) + " order by mprno"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    
    if len(c1)>0:
        Mprstr=",".join([x['mprno'] for x in c1])
    else:
        Mprstr=""
    poref=poprefix + Mprstr + "/" + poNo if item[0]['authstatus'] else  poprefix + Mprstr +"/POID: " + str(poid)
    sql = "select * from currencycodes where code=" + str(item[0]["cc"])
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    Cur = c1[0]["des"]
    sql = "select * from suppliers where code=" + SuppCode + ""
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        NAME = c1[0]["name"]
        ADD1 = "" if c1[0]['add1']==None else  c1[0]['add1']
        ADD2 = "" if c1[0]['add2']==None else  c1[0]['add2']
        ADD3 = "" if c1[0]['add3']==None else  c1[0]['add3']
        CITY = "" if c1[0]['city']==None else  c1[0]['city']
        PIN = "" if c1[0]['pincode']==None else  c1[0]['pincode']

        VendorGSTNo = "" if c1[0]['gstregno']==None else  c1[0]['gstregno']

        suppADD = NAME + "" if ADD1=="" else "\n" + ADD1 +"" if ADD2=="" else "\n" + ADD2+"" if ADD3=="" else "\n" + ADD3+"" if CITY=="" else "\n" + CITY + "-" + PIN
        if item[0]["potype"]==2:
            suppADD=suppADD+"" if c1[0]['country']=="" else "\n" + c1[0]['country']
    sql = "select * from suppliers where code=" + agentCode + ""
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if agentCode ==0:
        agentAdd = ""
    else:
        NAME = c1[0]["name"]
        ADD1 = "" if c1[0]['add1']==None else  c1[0]['add1']
        ADD2 = "" if c1[0]['add2']==None else  c1[0]['add2']
        ADD3 = "" if c1[0]['add3']==None else  c1[0]['add3']
        CITY = "" if c1[0]['city']==None else  c1[0]['city']
        PIN = "" if c1[0]['pincode']==None else  c1[0]['pincode']
        agentAdd = NAME + "" if ADD1=="" else "\n" + ADD1 +"" if ADD2=="" else "\n" + ADD2+"" if ADD3=="" else "\n" + ADD3+"" if CITY=="" else "\n" + CITY + "-" + PIN
    sql = "select * from poitemsview where poid=" + str(poid) + " order by stockno"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        database = "C:\My Documents\purchase_New_GST.mdb"
        constr = 'Provider=Microsoft.Jet.OLEDB.4.0; Data Source=%s' % database
        tablename = "poprint"
        
        # connect to the database
        conn = adodbapi.connect(constr)
        cursor = conn.cursor()
        sql = "delete * from poprint"
        cursor.execute(sql)
        conn.commit()
        for item in c1:
            des = item["des"]
            DrwgNo ="" if item['drwgno']==None or item['drwgno']=="" else "\n" +item['drwgno']
            des = des + DrwgNo
            if discountApp == True:
                discountedRate = item["rate"]
                TotalVal = (discountedRate * item["qty"] )/ item["ratebase"]
            elif (item["discountbase"] == 1):

                discountVal = 0
                discountedRate = item["rate"] - ((item["rate"] * item["discount"]) / 100)
                TotalVal = round(discountedRate * item["qty"], 2)
            else:
                discountVal = 0
                discountedRate = item["rate"] - item["discount"]
                TotalVal = round(discountedRate * item["qty"], 2)
            if Interest > 0:
                intval = ((TotalVal * Interest) * round(intPeriod / 30)) / 1200
                intPer = "PLUS " +Interest + "% " + " INTEREST PER ANNUM FOR " + intPeriod & " DAYS"
            else:
                intval = 0
                intPer = ""
            totalamt=''
            sql = "INSERT INTO poPrint ( poRef, podate, suppcode, suppref, payterms, suppadd, exduty, cst, price, insurance, bottomnote, deliverynote, totalamt, stockno, Des, unit, qty ,drwgno,rate,totalval,discountval,itemdelivery,desmode,poreason,PFcharges,ILN,insp,agentadd,intval,catcode,INTPER,cur,arefno,anote,adate,reason,amendno,gstic,hsncode,revcharge,vendorgstno)"
            sql = sql + " values ('" + poref + "','" + str(poDate) + "','" + str(SuppCode) + "','" + suppRef + "','" + ifNull(Payterms,'') + "','" + suppADD +"','" + str(ExDuty) + "','" + str(cst) + "','" + str(Price) + "','" + str(Insurance) + "','" + ifNull(bottomNote,'') + "','" + ifNull(DeliveryNote,'') + "','" + totalamt +"','" + item["stockno"] + "','" + des + "','" +  (item["unit"] if item["ratebase"] == 1 else (str(item["ratebase"])) + " " + item["unit"]) + "','" + str(item["qty"]) + "','" + ifNull(item["drwgno"],"") + "','"+ str(ifNull(discountedRate,"")) + "','" + str(TotalVal) + "','" + str(ifNull(discountVal,"")) + "','" + ifNull(item["itemdelivery"],"") + "','" + str(ifNull(desMode,"")) + "',"
            print(sql)
            sql = sql +"'"+ ifNull(POReason,"") +"','" + ifNull(PFCharges,"") + "','" + ifNull(ILN,"") + "','"+ ifNull(insp,'') + "','" + ifNull(agentAdd,"") + "','" + str(intval) + "','" + ifNull(catCode,"") + "','"+ str(intPer) + "','" + str(Cur) + "','" + str(ifNull(ArefNo,"")) + "','" + ifNull(ANote,"") + "','" + ifNull(str(Adate),"") + "','" + ifNull(Reason,"") + "','" + str(amendNo) + "','" + str(GSTIC) + "','" + str(HSNCode) + "','" + ifNull(RevCharge,'') + "','" + ifNull(VendorGSTNo,'')+ "')"
            print(sql)
            cursor.execute(sql)
            conn.commit()
        return True
    else:
        return False

def transferAmendments(poid):
    sql = "SELECT * From poview WHERE poid =" + str(poid) 
    with open_db_connection('edssql',True) as cursor:
        cursor.execute(sql)
        item=dictfetchall(cursor)
    poDate = str(item[0].get("podate",''))
    Adate = str(item[0].get("adate", ""))
    poNo = str(item[0].get("pono",''))
    #suppRef = item[0].get("supprefno","")
    #Payterms = item[0].get("payterms", "")
    SuppCode = str(item[0].get("suppcode", ""))
    agentCode = str(item[0].get("agentcode", ""))
    Reason = item[0].get("areason", "")
    amendNo = str(item[0].get("amendno", ""))
    #POReason = item[0].get("poreason","")
    #PFCharges = "" if item[0].get("pfcharges", "")=="" else str(item[0].get("pfcharges", ""))+"%"
    bottomNote = item[0].get("abottomnote", "")
    ArefNo = item[0].get("arefno", "")
    discountApp = item[0]["discountapp"]
    discountVal = item[0]["discountval"]
    sql = "select * from po_Mprview where poid=" + str(poid) + " order by mprno"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    
    if len(c1)>0:
        Mprstr=",".join([x['mprno'] for x in c1])
    else:
        Mprstr=""
    if item[0]["authstatus"] == True:
        if len(poNo) == 4:
            poref = "Pinj/IMP/" + Mprstr + "/" + poNo + " Amendment: " + amendNo
        else:
            poref = "Pinj/4.2/" + Mprstr + "/" + poNo + " Amendment: " + amendNo
    else:
        if len(poNo) == 4:
            poref = "Pinj/IMP/" + Mprstr + "/" & poNo + " Amendment: " +amendNo + " POID: " + str(poid)
        else:
            poref = "Pinj/4.2/" + Mprstr+ "/" & poNo + " Amendment: " + amendNo + " POID: " + str(poid)
    
    sql = "select * from suppliers where code=" + SuppCode + ""
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        NAME = c1[0]["name"]
        ADD1 = "" if c1[0]['add1']==None else  c1[0]['add1']
        ADD2 = "" if c1[0]['add2']==None else  c1[0]['add2']
        ADD3 = "" if c1[0]['add3']==None else  c1[0]['add3']
        CITY = "" if c1[0]['city']==None else  c1[0]['city']
        PIN = "" if c1[0]['pincode']==None else  c1[0]['pincode']

        VendorGSTNo = "" if c1[0]['gstregno']==None else  c1[0]['gstregno']

        suppADD = NAME + "" if ADD1=="" else "\n" + ADD1 +"" if ADD2=="" else "\n" + ADD2+"" if ADD3=="" else "\n" + ADD3+"" if CITY=="" else "\n" + CITY + "-" + PIN
        if item[0]["potype"]==2:
            suppADD=suppADD+"" if c1[0]['country']=="" else "\n" + c1[0]['country']
    sql = "select * from suppliers where code=" + agentCode + ""
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if agentCode ==0:
        agentAdd = ""
    else:
        NAME = c1[0]["name"]
        ADD1 = "" if c1[0]['add1']==None else  c1[0]['add1']
        ADD2 = "" if c1[0]['add2']==None else  c1[0]['add2']
        ADD3 = "" if c1[0]['add3']==None else  c1[0]['add3']
        CITY = "" if c1[0]['city']==None else  c1[0]['city']
        PIN = "" if c1[0]['pincode']==None else  c1[0]['pincode']
        agentAdd = NAME + "" if ADD1=="" else "\n" + ADD1 +"" if ADD2=="" else "\n" + ADD2+"" if ADD3=="" else "\n" + ADD3+"" if CITY=="" else "\n" + CITY + "-" + PIN
    #Price = item[0].get("pricedes", "")
    #Insurance = item[0].get("insurance", "")
    #bottomNote = item[0].get("bottomnote", "")
    #DeliveryNote = item[0].get("deliverynote", "")
    #desMode="" if item[0]['despatchdes']==None else item[0]['despatchdes'] if item[0]["despatch"]==1 else item[0]["desmodedes"] + " " + "" if item[0]['despatchdes']==None or item[0]['despatchdes']=="" else ": " +item[0]['despatchdes']
    
    sql = "SELECT * From poamendmentsview WHERE poid =" + str(poid) + " order by type, tablename desc,stockno"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)


    if len(c1) > 0:
        database = "C:\My Documents\purchase_New_GST.mdb"
        constr = 'Provider=Microsoft.Jet.OLEDB.4.0; Data Source=%s' % database
        tablename = "poprint"
        
        # connect to the database
        conn = adodbapi.connect(constr)
        cursor1 = conn.cursor()
        sql = "delete from amendmentsprint"
        cursor1.execute(sql)
        conn.commit()
        
        
        for item in c1:
            fldName = item["fieldname"]
            tblName = item["tablename"]
            if item["type"]== 1:
                if fldName == "qty" or fldName == "rate":
                    des = item["des"]
                    sql = "select * from poitemsview where poid=" + str(poid) + " and stockno='" +item["stockno"] + "' order by stockno"
                    with open_db_connection('edssql') as cursor:
                        cursor.execute(sql)
                        c2 = dictfetchall(cursor)
                    itemDelivery = c2[0]["itemdelivery"]
                    if len(c2) > 0:
                        if discountApp == True:
                            #discountedRate = rs.Fields("rate").Value - ((rs.Fields("rate").Value * discountVal) / 100)
                            discountedRate = c2[0]["rate"]
                            nTotalVal = (discountedRate * c2[0]["qty"]) / c2[0]["ratebase"]
                        elif c2[0]["discountbase"] ==1 :
                            discountVal = 0
                            discountedRate = c2[0]["rate"] - ((c2[0]["rate"] * c2[0]["discount"]) / 100)
                            nTotalVal = round(discountedRate * c2[0]["qty"], 2)
                        else:
                            discountVal = 0
                            discountedRate = c2[0]["rate"] - c2[0]["discount"]
                            nTotalVal = round(discountedRate * c2[0]["qty"], 2)
                        
                        NewQty =c2[0]["qty"]
                        NewRate = str(discountedRate)
                        Unit = c2[0]["unit"]
                    
                    sql = "select * from poitemsview " + item["whereclause"]
                    with open_db_connection('edssql') as cursor:
                        cursor.execute(sql)
                        c2 = dictfetchall(cursor)
                    if len(c2) > 0:
                        if discountApp == True:
                            #discountedRate = rs.Fields("rate").Value - ((rs.Fields("rate").Value * discountVal) / 100)
                            discountedRate = c2[0]["rate"]
                            oTotalVal = (discountedRate * c2[0]["qty"]) / c2[0]["ratebase"]
                        elif c2[0]["discountbase"] == 1:
                            discountVal = 0
                            discountedRate = c2[0]["rate"] - ((c2[0]["rate"] * c2[0]["discount"]) / 100)
                            oTotalVal = round(discountedRate * c2[0]["qty"], 2)
                        else:
                            discountVal = 0
                            discountedRate = c2[0]["rate"] - c2[0]["discount"]
                            oTotalVal = round(discountedRate * c2[0]["qty"], 2)
                            
                        OldQty = c2[0]["qty"]
                        OldRate = str(discountedRate)
                        
                    sql = "select * from poitemsview where poid=" + str(poid) + " and stockno='" + item["stockno"] + "' order by stockno"
                    with open_db_connection('edssql') as cursor:
                        cursor.execute(sql)
                        c2 = dictfetchall(cursor)
                        
                    itemDelivery = ifNull(c2[0]["itemdelivery"], "")
                    des = c2[0]["des"]
                    des = des + "--" + item["des"] + "--"
                    diffValue = nTotalVal - oTotalVal
                    StockNo = ifNull(c2[0]["stockno"],'')
                else:
                    if tblName == "PoItems":
                        sql = "select * from poitemsview where poid=" + str(poid) + " and stockno='" + item["stockno"] + "' order by stockno"
                        with open_db_connection('edssql') as cursor:
                            cursor.execute(sql)
                            c2 = dictfetchall(cursor)
                        itemDelivery = ifNull(c2[0]["itemdelivery"],'')
                        des = item["des"]+  "\n"
                        des = des + "--" + c2[0]["des"] + "--"
                    else:
                        des = item["des"]
                        
                    
                    if fldName == "discountval":
                        sql= "SELECT  sum(qty * case discountapp when 1 then rate /ratebase when 0 then (rate-((rate *discount)/100))/ratebase end) FROM dbo.PO INNER JOIN dbo.POItems ON dbo.PO.POID = dbo.POItems.POID Where po.poid ="+ str(poid)
                        with open_db_connection('edssql') as cursor:
                            cursor.execute(sql)
                            c2 = dictfetchall(cursor)
                        diffValue = 0
                    else:
                        diffValue = 0
                    
            
                    StockNo = ifNull(item["stockno"],'')
                    OldQty = ""
                    NewQty = ""
                    OldRate = ""
                    NewRate = ""
                    Unit = ""
                
            else:
                sql = "select * from poitemsview where poid=" + str(poid) + " and stockno='" + item["stockno"] + "' order by stockno"
                with open_db_connection('edssql') as cursor:
                        cursor.execute(sql)
                        c2 = dictfetchall(cursor)
                itemDelivery = ifNull(c2[0]["itemdelivery"],'')
                des = c2[0]["des"] + "\n" + " Qty: " + c2[0]["qty"]
                des = des +" unit: " + c2[0]["unit"] + " Rate: " + c2[0]["rate"] + " Delivery: " + itemDelivery
                
                
                StockNo = "Added: " + ifNull(item["stockno"])
                
                if discountApp == True:
                    
                    discountedRate = c2[0]["rate"]
                    TotalVal = (discountedRate * c2[0]["qty"]) / c2[0]["ratebase"]
                elif c2[0]["discountbase"] == 1:
                    discountVal = 0
                    discountedRate = c2[0]["rate"] - ((c2[0]["rate"] * c2[0]["discount"]) / 100)
                    TotalVal = round(discountedRate * c2[0]["qty"], 2)
                else:
                    discountVal = 0
                    discountedRate = c2[0]["rate"] - c2[0]["discount"]
                    TotalVal = round(discountedRate * c2[0]["qty"], 2)

                
                diffValue = TotalVal
                OldQty = "0"
                NewQty = c2[0]["qty"]
                OldRate = "0"
                NewRate = str(discountedRate)
                Unit = c2[0]["unit"]
                    

            sql = "INSERT INTO amendmentsPrint (stockno, poRef, Adate, suppcode, AREFNO, suppadd,  ANOTE, Des, DIFF,discountval,itemdelivery,reason,podate,oldqty,oldrate,newqty,newrate,unit,agentadd) \
            values ('" + StockNo + "','" + poref + "','" + Adate + "','" + str(SuppCode) + "','" + ArefNo + "','" + suppADD + "','" + bottomNote + "','" + des + "','" + str(diffValue) + "','" + str(discountVal) + "','" + itemDelivery + "','" + Reason + "','" + poDate + "','" + str(OldQty) + "','" + str(OldRate) + "','" + str(NewQty) + "','" + str(NewRate) + "','" + Unit + "','" + agentAdd + "')" 
            cursor1.execute(sql)
            conn.commit()
        return True
    else:
        return False

            
      
def getReportfromAccess(rptname):
    #print (len(d))
    try:
        ac=win32.gencache.EnsureDispatch('Access.Application')
    except AttributeError:
        f_loc = r'C:\Users\kkaggarwal2\AppData\Local\Temp\gen_py'
        for f in Path(f_loc):
            Path.unlink(f)
        Path.rmdir(f_loc)
        ac = win32.gencache.EnsureDispatch('Access.Application')
    
    #ac.Visible=False
    print('p')
    strdb = "c:\my documents\purchase_new_GST.mdb"
    ac.OpenCurrentDatabase (strdb)
    db=ac.CurrentDb()
    #strReportName = "MiSlipPrintQuery1"
    strReportName=rptname
    #ac.DoCmd.OpenReport (strReportName)
    #rpt = ac.Reports(strReportName)
    #ac.DoCmd.OpenReport(strReportName, 1)
    #ac.Visible = True
    x=ac.Run ('ConvertReportToPDF',strReportName, "", strReportName + ".PDF")
    ac.Application.Quit()

def poprint(request,poid):

    if transferPO(poid):
        sql= "select * from poview as t where (poid in (select max(poid) from poview where authstatus=1 group by pono) or authstatus=0) and poid=" + str(poid) 
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
        strdb = "c:\my documents\purchase_new_GST.mdb"
    
    
        if c1[0]['authstatus']== True:
            if c1[0]['potype'] == 1:
                strReportName = "poprint"
            else:
                strReportName = "poprinti"
            
        else:
            if c1[0]['potype'] == 1:
                strReportName = "poconcur"
            else:
                strReportName = "poconcuri"
            
        
        getReportfromAccess(strReportName)
        fs=FileSystemStorage(r"C:\users\kkaggarwal2\documents")
        filename=strReportName+".pdf"
        if fs.exists(filename):
            with fs.open(filename) as pdf:
                response=HttpResponse(pdf,content_type='application/pdf')
                response['Content-Disposition']='attachment;filename="mypdf.pdf"'
                return response
        else:
            return HttpResponseNotFound('the rquested pdf not found')
    else:
        return HttpResponse('PO cannot be transferred')

def poamendmentprint(request):
    poid=int(request.GET.get('poid',''))
    if transferAmendments(poid):
        sql= "select * from poview as t where (poid in (select max(poid) from poview where authstatus=1 group by pono) or authstatus=0) and poid=" + str(poid) 
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
        strdb = "c:\my documents\purchase_new_GST.mdb"
    
    
        if c1[0]['authstatus']== True:
            
            strReportName = "aprint"
        else:
            strReportName = "aconcur"
            
        
            
        
        getReportfromAccess(strReportName)
        fs=FileSystemStorage(r"C:\users\kkaggarwal2\documents")
        filename=strReportName+".pdf"
        if fs.exists(filename):
            with fs.open(filename) as pdf:
                response=HttpResponse(pdf,content_type='application/pdf')
                response['Content-Disposition']='attachment;filename="mypdf.pdf"'
                return response
        else:
            return HttpResponseNotFound('the rquested pdf not found')
    else:
        return HttpResponse('PO cannot be transferred')

def poauth(request,poid):
    submitbuttondisabled="false"
    html_form=''
    sql="select * from poauth where poid="+str(poid)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    success='False'
    if len(c1)>0:
        if request.method == 'GET':
            form = poauthForm(initial=c1[0])
            #form.fields['stockno'].widget.attrs['readonly'] = True
            context = {'form': form,'save':'saveMe','poid':poid,'formaction':'poauth','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('purchase/poauth.html', context, request=request)
            #print(html_form)
            success='True'
        if request.method == 'POST':
            pass
    else:
        if request.method == 'GET':
            form = poauthForm(initial={'poid':poid})
            #form.fields['stockno'].widget.attrs['readonly'] = True
            context = {'form': form,'save':'saveMe','poid':poid,'formaction':'poauth','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('purchase/poauth.html', context, request=request)
            #print(html_form)
            success='True'
        if request.method == 'POST':
            form = poauthForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['name'], password=form.cleaned_data['password'])
                if user is not None:
                    sql = 'insert into poauth (poid,authstatus) values(%s,%s)' %(form.cleaned_data['poid'],1)
                    print(sql)
                    data = form.runQuery('edssql',sql)
                    if not data['success']:
                        form.add_error(field=None, error=str(data['exception']))
                        success = 'False'
                    else:
                        success = 'True'
                else:
                    form.add_error(field=None,error='User not Valid!')
                    success="False"
            else:
                success='False'
            context = {'form': form,'save':'saveMe','poid':poid,'formaction':'poauth','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('purchase/poauth.html', context, request=request)
            
    return JsonResponse({'html_form': html_form,'success':success})







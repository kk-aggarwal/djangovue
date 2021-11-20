from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect,JsonResponse,HttpResponseNotFound
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlquote,urlunquote
from datetime import datetime
import json
import adodbapi
import win32com.client as win32
from django.core.files.storage import FileSystemStorage

from djangovue.connections import open_db_connection,dictfetchall
from .forms import mislipeditForm,mislipitemeditForm,mislipmrreditForm,mislipbilleditForm,mrreditForm,mrrvalueeditForm,ledgereditForm,stdocregistereditForm,stmislipitemeditForm,ststockmastereditForm

from django.contrib.auth.decorators import login_required
# Create your views here.

def test(request):
    hellotemplate = render_to_string('mi_website/hello.html', {'finyear': '2021-2022'})
    return JsonResponse({'template':hellotemplate,'mounted':"(function(){console.log('sddfff');})", 'click1': "<button  style='padding-to:20px' class='btn btn-primary btn-sm' @click='click1'> add</button>"})

@login_required
def Index(request):
    template = "mi_website/index_d.html"
    return render(request,template,context={'a':'kk'})

def get_all_fields_from_form(instance):
    """return names of all avialable foelds from given form instance"""
    fields=list(instance().base_fields)
    for field in list(instance().declared_fields):
        if fields not in fields:
            fields.append(field)
    return fields


def mihome(request):
    mislipviewtemplate=render_to_string('mi_website/mislipview.html',{'finyear':'2021-2022'})
    mrrviewtemplate = render_to_string('mi_website/mrrview.html', {'finyear': '2021-2022'})
    return render(request,'mi_website/stMainStoreView.html',{'mislipviewtemplate':mislipviewtemplate,'mrrviewtemplate':mrrviewtemplate})

@login_required
def mainstorehome(request):
    sql = "select yearid from stcurrentyear"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    stCurrenyYear = c1[0]['yearid']
    # stCurrenyYear='2020-2021'
    sql = "select groupid  as value,cast(groupid as varchar(2)) as text from stvalidgroups order by groupid"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c2 = dictfetchall(cursor)
    ledgertemplate=render_to_string('mi_website/ledgerview.html',{'finyear':stCurrenyYear})
    stdocregisterviewtemplate = render_to_string('mi_website/stdocregisterview.html', {'finyear': stCurrenyYear,'options':c2})
    stmislipsviewtemplate = render_to_string('mi_website/stmislipsview.html', {'finyear': stCurrenyYear})
    ststockmasterviewtemplate = render_to_string('mi_website/ststockmasterview.html', {'finyear': stCurrenyYear})

    return render(request,'mi_website/stMainStoreView.html',{'ledgertemplate':ledgertemplate,'stdocregisterviewtemplate':stdocregisterviewtemplate,'stmislipsviewtemplate':stmislipsviewtemplate,'ststockmasterviewtemplate':ststockmasterviewtemplate})

@login_required
def mislipview(request):

    sql="select yearid from stcurrentyear"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    stCurrenyYear=c1[0]['yearid']
    #stCurrenyYear='2020-2021'
    print(request.user.username)
    return render(request,'mi_website/mislipview.html',{'finyear':stCurrenyYear})

def ajax_mislips(request):

    #request.headers['Origin']=' http://192.100.200.23:8033/'
    urls = {}
    tableData=[]
    tableFields=[]
    tableFields_verbose={}
    formFields=[]
    tableparticulars={}

    finyear = (request.GET.get('finyear', ''))
    mislipdate=(request.GET.get('dated', ''))
    mislipno = (request.GET.get('mislipno', ''))
    matgrp = (request.GET.get('matgrp', ''))
    field=(request.GET.get('field', ''))

    formFields = ['mislipno', 'matgrp', 'mislipdate', 'pono', 'recdby', 'note', 'st_auth', 'ins_auth', 'me_auth',
                  'mst_auth']
    tableFields_verbose = {'mislipno': 'No', 'matgrp': "Grp", 'mislipdate': "Dated", 'pono': 'PO', 'recdby': 'Recd',
                           'note': "note", 'st_auth': 'ST', 'ins_auth': "INS", 'me_auth': "ME", 'mst_auth': "MST"}

    if mislipdate!='':
        mislipdate = datetime.strptime(mislipdate, '%m-%d-%Y').strftime("%d-%b-%Y")
    print(matgrp)
    whereclause=" finyear='%s'"%finyear
    if mislipdate :
         whereclause=whereclause+" and mislipdate='%s'"%str(mislipdate)
    if mislipno:
        whereclause=whereclause+" and mislipno=%s"%mislipno
    if matgrp:
        whereclause=whereclause+" and matgrp=%s"%matgrp
    sql = "SELECT FinYear, replace(convert(varchar(11),mislipdate,106),' ','-') as MiSlipDate, MiSlipNo, MatGrp, RecDBy, Note, St_Auth, Ins_Auth, Pono, Mprno, MSt_auth, ME_auth FROM MiSlip WHERE %s"%whereclause
    #print(sql)
    if field=='':
        sql=sql+ " order by mislipno"
        #sql = "SELECT FinYear, MiSlipDate, MiSlipNo, MatGrp, RecDBy, Note, St_Auth, Ins_Auth, Pono, Mprno, MSt_auth, ME_auth FROM MiSlip WHERE (FinYear ='" + finyear + "') AND (MiSlipDate ='" + str(
          #  mislipdate) + "') ORDER BY MiSlipNo"
    else:
        sql=sql+" order by %s"%field
        #sql = "SELECT FinYear, MiSlipDate, MiSlipNo, MatGrp, RecDBy, Note, St_Auth, Ins_Auth, Pono, Mprno, MSt_auth, ME_auth FROM MiSlip WHERE (FinYear ='" + finyear + "') AND (MiSlipDate ='" + str(
          #  mislipdate) + "') ORDER BY %s"%field
    with open_db_connection('incomingstore') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
    if len(c1)==1:
        mislipdate=c1[0]['mislipdate']

    try:
        urls['urlcreate'] = request.build_absolute_uri(reverse('mislipcreate', kwargs={'finyear': finyear,'mislipno': 0,'matgrp': 0,'mislipdate':mislipdate}))
    except:
        urls['urlcreate'] =''

    success="true"
    if len(c1) > 0:
        tableData=c1

        tableFields = list(c1[0].keys())
        #print(tableFields)

        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('mislipedit', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp'],'mislipdate':item['mislipdate']}))
            #print(item['urledit'])
            #item['urledit']="http://192.100.200.23:8033/mi/ajax/mislipedit/2021-2022/1/6/20-apr-2021"
            item['urldel'] = request.build_absolute_uri(reverse('mislipdel', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp']}))
            item['urlprint'] = request.build_absolute_uri(reverse('mislipprint', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp']}))

            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
    else:
        tableData = []
        tableFields = formFields
        #tableFields_verbose = {f: f for f in tableFields }

    return JsonResponse({'success':success,'tableData': tableData, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)


def mislipedit(request,finyear,mislipno,matgrp,mislipdate):
    submitbuttondisabled="false"
    html_form=''
    #print(request.method)
    sql = "SELECT FinYear, replace(convert(varchar(11),mislipDate,106),' ','-') as mislipdate, MiSlipNo, MatGrp, RecDBy, isnull(Note,'') AS NOTE,suppname, St_Auth, isnull(Ins_Auth,0) as ins_auth, Pono, Mprno, MSt_auth, ME_auth, replace(convert(varchar(11),mst_auth_date,23),' ','-') as mst_auth_date FROM MiSlip WHERE (FinYear ='%s') AND (Matgrp =%s) AND (MiSlipno =%s) ORDER BY MiSlipNo" % (
    finyear, matgrp, mislipno)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    print(c1[0])
    success = 'False'
    if len(c1)>0:
        submitbuttondisabled= "true" if c1[0]['ins_auth'] else "false"
        #print(submitbuttondisabled)
        if request.method == 'GET':
            form = mislipeditForm(initial=c1[0])

            form.fields['st_auth'].widget.attrs['onclick'] = 'return  false' if c1[0]['ins_auth'] else 'return  true'

            context = {'form': form,'save':'saveMe_edit','finyear':finyear,'mislipno':mislipno,'matgrp':matgrp,'mislipdate':mislipdate,'formaction':'mislipedit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('mi_website/mislipedit.html', context, request=request)
            #print(html_form)
            success='True'
        if request.method == 'POST':
            #print('save form')
            #print(dict(request.POST))
            #print(c1[0])
            #a={k:v[0] if len(v)==1 else v for k,v in request.POST.lists()}
            form=mislipeditForm(request.POST,initial=c1[0])
            form.fields['st_auth'].widget.attrs['onclick'] = 'return  false' if c1[0]['ins_auth'] else 'return  true'

            #print(form.changed_data)
            if form.is_valid():
                print('edit new mislip')
                data=form.save_update(request)
                if not data['success']:
                    form.add_error(field=None, error=str(data['exception']))
                    success='False'
                else:
                    success = 'True'
            else:
                pass

            context = {'form': form, 'save': 'saveMe_edit', 'finyear':finyear,'mislipno':mislipno,'matgrp':matgrp,'mislipdate':mislipdate,'formaction':'mislipedit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('mi_website/mislipedit.html', context, request=request)
    return JsonResponse({'html_form': html_form,'success':success})

def mislipdel(request,finyear,mislipno,matgrp):
    pass

def mislipcreate(request,finyear,mislipno,matgrp,mislipdate):
    submitbuttondisabled = "false"
    mislipno=0
    matgrp=0
    success = 'False'
    #mislipdate=datetime.strptime(mislipdate,'%m-%d-%Y').strftime("%d-%b-%Y")
    if request.method == 'GET':
        print('d')
        form = mislipeditForm(initial={'finyear':finyear,'mislipdate':mislipdate})
        form.fields['matgrp'].widget.attrs['readonly'] = False
        form.fields['mislipno'].widget.attrs['readonly'] = False
        form.fields['st_auth'].widget.attrs['disabled'] =True
        context = {'form': form, 'save': 'saveMe_add', 'finyear':finyear,'mislipno':mislipno,'matgrp':matgrp,'mislipdate':mislipdate,'formaction':'mislipcreate','submitbuttondisabled':submitbuttondisabled}
        html_form = render_to_string('mi_website/mislipedit.html', context, request=request)
        #print(html_form)

    if request.method == 'POST':
        #print(request.POST)
        form = mislipeditForm(request.POST)
        form.fields['matgrp'].widget.attrs['readonly'] = False
        form.fields['mislipno'].widget.attrs['readonly'] = False
        form.fields['st_auth'].widget.attrs['disabled'] = True
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
        context = {'form': form, 'save': 'saveMe_add', 'finyear':finyear,'mislipno':mislipno,'matgrp':matgrp,'mislipdate':mislipdate,'formaction':'mislipcreate','submitbuttondisabled':submitbuttondisabled}
        html_form = render_to_string('mi_website/mislipedit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})




def getsuppaddfrompono(request):
    data={}
    vSuppAdd=''
    print(request)
    pono=request.GET.get('pono')
    print(pono)
    sql = "SELECT  suppcode,potype from validpoview where pono=%s"%pono
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor = con.cursor()
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)
    if len(c1)>0:
        sql = "SELECT  * from suppliers where code='%s'" % c1[0]['suppcode']
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c2 = dictfetchall(cursor)


        if len(c2)>0:
            for item in c2:
                Nme = item["name"]
                Add1 = '' if item["add1"] is None else item["add1"]
                Add2 = '' if item["add2"]is None else item["add2"]
                Add3 = '' if item["add3"]is None else item["add3"]
                CITY = '' if item["city"] is None else item["city"]
                vCity = '-' if (item["city"] is None or item["city"] == "")  else  item["city"]
                Pin = '' if  item["pincode"] is None else str(item["pincode"])
                VendorGstNo = '' if item["gstregno"] is None else item["gstregno"]

                vSuppAdd = Nme + ("" if Add1== "" else '\r\n'+Add1) + ( "" if Add2== "" else '\r\n'+Add2) +  ("" if Add3== "" else '\r\n'+Add3) +  ("" if CITY== "" else ''+CITY) + "-" + Pin +  ("" if VendorGstNo== "" else '\r\n'+VendorGstNo)

                if  c1[0]["potype"] == 2:
                    vSuppAdd = vSuppAdd + ('' if item["country"]is None else ('' + item["country"]))
        else:
            vSuppAdd = ''
    else:
        vSuppAdd=''
    data['suppadd']=(vSuppAdd)
    return JsonResponse(data,safe=False)

def ajax_mislipitems(request):
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    formFields = []
    tableparticulars={}

    finyear = (request.GET.get('finyear', ''))
    mislipno = int(request.GET.get('mislipno', ''))
    matgrp = int(request.GET.get('matgrp', ''))
    field = (request.GET.get('field', ''))
    urls={}
    try:
        urls['urlcreate'] = request.build_absolute_uri(reverse('mislipitemcreate', kwargs={'finyear': finyear, 'mislipno': mislipno,'matgrp': matgrp,'stockno':'0'}))
    except:
        urls['urlcreate']=''

    if field=='':
        sql = "SELECT FinYear, MiSlipNo, StocKNo, Des, Unit,round(qtyrecd,3) as qtyrecd,round(qtyaccepted,3) as qtyaccepted, MatGrp FROM MislipDet WHERE (FinYear = '%s') AND (MiSlipNo = %s) AND (MatGrp = %s) ORDER BY StocKNo" % (
    finyear, mislipno, matgrp)
    else:
        sql = "SELECT FinYear, MiSlipNo, StocKNo, Des, Unit,round(qtyrecd,3) as qtyrecd,round(qtyaccepted,3) as qtyaccepted, MatGrp FROM MislipDet WHERE (FinYear = '%s') AND (MiSlipNo = %s) AND (MatGrp = %s) ORDER BY %s" % (
            finyear, mislipno, matgrp,field)

    formFields = ['stockno', 'des', 'unit', 'qtyrecd', ]
    tableFields_verbose = {'stockno':'stock No', 'des':'Description', 'unit':'Unit', 'qtyrecd':'Recd Qty', }

    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)


    success = 'true'
    if len(c1) > 0:
        tableData=c1

        tableFields = list(c1[0].keys())
        #print(tableFields)

        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('mislipitemedit', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp'],'stockno': item['stockno']}))
            item['urldel'] = request.build_absolute_uri(reverse('mislipitemdel', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp'],'stockno': item['stockno']}))

            #item['urlprint'] = reverse('mislipprint', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp']})

            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
    else:
        tableData=[]
        tableFields=formFields
    #print(formFields)
    return JsonResponse({'success':success,'tableData': tableData, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)


def mislipitemedit(request,finyear, matgrp, mislipno, stockno):
    submitbuttondisabled = "false"
    html_form = ''
    # print(request.method)
    sql = "SELECT FinYear, MiSlipNo, MatGrp,stockno,des, qtyrecd, unit,stdwt,scalewt,billedwt,'edit' as addedit FROM MiSlipdet WHERE (FinYear ='%s') AND (Matgrp =%s) AND (MiSlipno =%s) AND (stockno ='%s') ORDER BY MiSlipNo" % (
    finyear, matgrp, mislipno, stockno)

    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    # print(c1[0]['ins_auth'])
    success = 'False'
    if len(c1) > 0:
        #submitbuttondisabled = "true" if c1[0]['st_auth'] else "false"
        # print(submitbuttondisabled)
        if request.method == 'GET':
            form = mislipitemeditForm(initial=c1[0])

            #form.fields['st_auth'].widget.attrs['disabled'] = c1[0]['ins_auth']
            context = {'form': form, 'save': 'saveMe_edit','formaction':'mislipitemedit', 'finyear': finyear, 'mislipno': mislipno, 'matgrp': matgrp, 'stockno': stockno,
                       'submitbuttondisabled': submitbuttondisabled}
            html_form = render_to_string('mi_website/mislipitemedit.html', context, request=request)
            # print(html_form)
            success = 'True'
        if request.method == 'POST':
            print('save form')
            # print(dict(request.POST))
            # print(c1[0])
            # a={k:v[0] if len(v)==1 else v for k,v in request.POST.lists()}
            form = mislipitemeditForm(request.POST, initial=c1[0])

            if form.is_valid():
                print('edit new mislip item')
                data = form.save_update(request)
                if not data['success']:
                    form.add_error(field=None, error=str(data['exception']))
                    success = 'False'
                else:
                    success = 'True'
            else:
                pass

            context = {'form': form, 'save': 'saveMe_edit','formaction':'mislipitemedit', 'finyear': finyear, 'mislipno': mislipno, 'matgrp': matgrp, 'stockno': stockno,
                       'submitbuttondisabled': submitbuttondisabled}
            html_form = render_to_string('mi_website/mislipitemedit.html', context, request=request)

    return JsonResponse({'html_form': html_form, 'success': success})


def mislipitemdel(request):
    pass

def mislipitemcreate(request,finyear,mislipno,matgrp,stockno):
    submitbuttondisabled = "false"
    stockno="0"
    success = 'False'
    if request.method == 'GET':
        print('d')
        form = mislipitemeditForm(initial={'finyear': finyear, 'mislipno': mislipno, 'matgrp': matgrp})
        #form.fields['matgrp'].widget.attrs['readonly'] = False
        #form.fields['mislipno'].widget.attrs['readonly'] = False
        #form.fields['st_auth'].widget.attrs['disabled'] = True
        context = {'form': form, 'save': 'saveMe_add','formaction':'mislipitemcreate', 'finyear': finyear, 'mislipno': mislipno, 'matgrp': matgrp,'stockno':stockno,
                   'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/mislipitemedit.html', context, request=request)
        # print(html_form)

    if request.method == 'POST':
        print(request.POST)
        form = mislipitemeditForm(request.POST)
        #form.fields['matgrp'].widget.attrs['readonly'] = False
        #form.fields['mislipno'].widget.attrs['readonly'] = False
        #form.fields['st_auth'].widget.attrs['disabled'] = True
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
        context = {'form': form, 'save': 'saveMe_add','formaction':'mislipitemcreate', 'finyear': finyear, 'mislipno': mislipno, 'matgrp': matgrp,'stockno':stockno,
                   'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/mislipitemedit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})

def getdesfromstockno(request):
    data = {}
    print(request)
    stockno = request.GET.get('stockno')
    #print(pono)
    sql = "SELECT  des from stmaster where stockno='%s'" % stockno
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor = con.cursor()
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)
    if len(c1)>0:
        data['stockdes'] = c1[0]['des']
    else:
        data['stockdes']='<stock no not  in stock master>'
    return JsonResponse(data)

def ajax_mislipmrrs(request):
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    formFields = []
    tableparticulars={}

    finyear = (request.GET.get('finyear', ''))
    mislipno = int(request.GET.get('mislipno', ''))
    matgrp = int(request.GET.get('matgrp', ''))
    field = (request.GET.get('field', ''))
    urls = {}
    urls['urlcreate'] = request.build_absolute_uri(reverse('mislipmrrcreate',
                                kwargs={'finyear': finyear, 'mislipno': mislipno, 'matgrp': matgrp, 'mrrno': '0'}))

    if field == '':
        sql = "select finyear,matgrp,mislipno,mrrno,type,billno,value,cgst,sgst,igst,cenventno from mislipmrr_invoiceview WHERE (FinYear = '%s') AND (MiSlipNo = %s) AND (MatGrp = %s) " % (
            finyear, mislipno, matgrp)
    else:
        sql = "SELECT finyear,matgrp,mislipno,mrrno,type,billno,value,cgst,sgst,igst,cenventno from mislipmrr_invoiceview WHERE (FinYear = '%s') AND (MiSlipNo = %s) AND (MatGrp = %s) ORDER BY %s" % (
            finyear, mislipno, matgrp, field)

    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    success="true"
    if len(c1) > 0:
        tableData=c1

        tableFields = list(c1[0].keys())
        print(tableFields)
        formFields = ['mrrno','type','billno', ]
        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('mislipbillcreate',
                                      kwargs={'finyear': item['finyear'], 'mislipno': item['mislipno'],
                                              'matgrp': item['matgrp'], 'billno':  urlquote(item['billno'],''),'billtype': item['type']}))
            item['urldel'] = request.build_absolute_uri(reverse('mislipmrrdel', kwargs={'finyear': item['finyear'], 'mislipno': item['mislipno'],
                                                              'matgrp': item['matgrp'], 'mrrno': item['mrrno']}))

            # item['urlprint'] = reverse('mislipprint', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp']})

            color = 'default'
            item['rowcolor'] = color
            for f in formFields:
                color = 'default'
                item['fieldcolor'] = {f: color}
        tableFields_verbose = {f: f for f in tableFields}

    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                             'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields, 'urls': urls,'tableparticulars':tableparticulars}, safe=False)


def mislipmrredit(request,finyear, matgrp, mislipno, mrrno):
    pass
    sql = "select finyear,matgrp,mislipno,mrrno,type,billno,value,cgst,sgst,igst,cenventno from mislipmrr_invoiceview WHERE (FinYear = '%s') AND (MiSlipNo = %s) AND (MatGrp = %s) " % (
    finyear, mislipno, matgrp)


def mislipmrrcreate(request,finyear, matgrp, mislipno, mrrno):
    submitbuttondisabled = "false"
    mrrno = "0"
    success = 'False'
    if request.method == 'GET':
        print('d')
        form = mislipmrreditForm(initial={'finyear': finyear, 'mislipno': mislipno, 'matgrp': matgrp})
        # form.fields['matgrp'].widget.attrs['readonly'] = False
        # form.fields['mislipno'].widget.attrs['readonly'] = False
        # form.fields['st_auth'].widget.attrs['disabled'] = True
        context = {'form': form, 'save': 'saveMe_add', 'formaction': 'mislipmrrcreate', 'finyear': finyear,
                   'mislipno': mislipno, 'matgrp': matgrp, 'mrrno': mrrno,
                   'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/mislipmrredit.html', context, request=request)
        # print(html_form)

    if request.method == 'POST':

        form = mislipmrreditForm(request.POST,initial={'finyear': finyear, 'mislipno': mislipno, 'matgrp': matgrp})
        # form.fields['matgrp'].widget.attrs['readonly'] = False
        # form.fields['mislipno'].widget.attrs['readonly'] = False
        # form.fields['st_auth'].widget.attrs['disabled'] = True
        if form.is_valid():
            # print('create new mislip')
            data = form.save_create(request)
            if not data['success']:
                print('sssss'+data['exception'])
                form.add_error(field=None,error=str(data['exception']))
                success = 'False'
            else:
                success = 'True'
        else:
            pass
        context = {'form': form, 'save': 'saveMe_add', 'formaction': 'mislipmrrcreate', 'finyear': finyear,
                   'mislipno': mislipno, 'matgrp': matgrp, 'mrrno': mrrno,
                   'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/mislipmrredit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})

def mislipmrrdel(request,finyear, matgrp, mislipno, mrrno):
    pass

def ajax_mislipbills(request):
    urls={}
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    formFields = []
    tableparticulars = {}

    finyear = (request.GET.get('finyear', ''))
    mislipno = int(request.GET.get('mislipno', ''))
    matgrp = int(request.GET.get('matgrp', ''))
    field = (request.GET.get('field', ''))

    #urls['urlcreate'] = reverse('mislipbillcreate',kwargs={'finyear': finyear, 'mislipno': mislipno, 'matgrp': matgrp, 'billno': '0','billtype': '0'})
    urls['urlcreate']=''
    if field == '':
        sql = "SELECT FinYear, MatGrp, MislipNo, BillNo, cast(Value as decimal(10,2)) as value, BillType, MrrNo, CenventNo, CenventDate, EdAmount, EduCess, dated, cast(sgst as decimal(10,2)) as SGST, cast(cgst as decimal(10,2)) as CGST,cast(igst as decimal(10,2)) as IGST FROM MIslipBills WHERE (FinYear = '%s') AND (MatGrp = %s) AND (MislipNo = %s)" % (
            finyear, matgrp, mislipno)
    else:
        sql = "SELECT FinYear, MatGrp, MislipNo, BillNo, cast(Value as decimal(10,2)) as value, BillType, MrrNo, CenventNo, CenventDate, EdAmount, EduCess, dated, cast(sgst as decimal(10,2)) as SGST, cast(cgst as decimal(10,2)) as CGST,cast(igst as decimal(10,2)) as IGST FROM MIslipBills WHERE (FinYear = '%s') AND (MiSlipNo = %s) AND (MatGrp = %s) ORDER BY %s" % (
            finyear, mislipno, matgrp, field)

    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    success="true"
    if len(c1) > 0:
        tableData=c1
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = ['billtype','billno','sgst','cgst','igst','value' ]
        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('mislipbilledit',
                                      kwargs={'finyear': item['finyear'], 'mislipno': item['mislipno'],
                                              'matgrp': item['matgrp'], 'billno': urlquote(item['billno'],''), 'billtype': item['billtype']}))
            item['urldel'] = request.build_absolute_uri(reverse('mislipbilldel', kwargs={'finyear': item['finyear'], 'mislipno': item['mislipno'],
                                                             'matgrp': item['matgrp'],  'billno': urlquote(item['billno'],''), 'billtype': item['billtype']}))

            # item['urlprint'] = reverse('mislipprint', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp']})

            color = 'default'
            item['rowcolor'] = color
            for f in formFields:
                color = 'default'
                item['fieldcolor'] = {f: color}
        tableFields_verbose = {f: f for f in tableFields}

    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                             'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields, 'urls': urls,'tableparticulars':tableparticulars}, safe=False)


def mislipbilledit(request,finyear, matgrp, mislipno, billno,billtype):
    submitbuttondisabled = "false"
    html_form = ''
    # print(request.method)
    #sql = "select finyear,matgrp,mislipno,mrrno,type as billtype,billno,value,cgst,sgst,igst,cenventno,cenventdate,replace(convert(varchar(11),dated,106),' ','-') as dated from mislipmrr_invoiceview WHERE (FinYear = '%s') AND (MiSlipNo = %s) AND (MatGrp = %s) AND (type = '%s') AND (billno = '%s') " % (
    #finyear, mislipno, matgrp, billtype, billno)
    sql = "select finyear,matgrp,mislipno,mrrno,billtype,billno,value,cgst,sgst,igst,cenventno,cenventdate,replace(convert(varchar(11),dated,106),' ','-') as dated from mislipbills WHERE (FinYear = '%s') AND (MiSlipNo = %s) AND (MatGrp = %s) AND (billtype = '%s') AND (billno = '%s') " % (
    finyear, mislipno, matgrp, billtype, urlunquote(billno))

    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    # print(c1[0]['ins_auth'])
    success = 'False'
    if len(c1) > 0:
        # submitbuttondisabled = "true" if c1[0]['st_auth'] else "false"
        # print(submitbuttondisabled)
        if request.method == 'GET':
            form = mislipbilleditForm(initial=c1[0])

            # form.fields['st_auth'].widget.attrs['disabled'] = c1[0]['ins_auth']
            context = {'form': form, 'save': 'saveMe_edit', 'formaction': 'mislipbilledit', 'finyear': finyear,
                       'mislipno': mislipno, 'matgrp': matgrp, 'billno': urlunquote(billno),'billtype': billtype,
                       'submitbuttondisabled': submitbuttondisabled}
            print(context)
            html_form = render_to_string('mi_website/mislipbilledit.html', context, request=request)
            # print(html_form)
            success = 'True'
        if request.method == 'POST':
            print('save form')
            # print(dict(request.POST))
            # print(c1[0])
            # a={k:v[0] if len(v)==1 else v for k,v in request.POST.lists()}
            form = mislipbilleditForm(request.POST, initial=c1[0])

            if form.is_valid():
                print('edit new mislip bill')
                data = form.save_update(request)
                if not data['success']:
                    form.add_error(field=None,error=data['exception'])
                    success = 'False'
                else:
                    success = 'True'
            else:
                pass

            context = {'form': form, 'save': 'saveMe_edit', 'formaction': 'mislipbilledit', 'finyear': finyear,
                       'mislipno': mislipno, 'matgrp': matgrp, 'billno': billno,'billtype': billtype,
                       'submitbuttondisabled': submitbuttondisabled}
            html_form = render_to_string('mi_website/mislipbilledit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})

def mislipbillcreate(request,finyear, matgrp, mislipno, billno,billtype):
    submitbuttondisabled = "false"
    #billno = "0"
    #billtype="0"
    sql = "select finyear,matgrp,mislipno,mrrno,type as billtype,billno,replace(convert(varchar(11),dated,106),' ','-') as dated,value,cgst,sgst,igst,cenventno from mislipmrr_invoiceview WHERE (FinYear = '%s') AND (MiSlipNo = %s) AND (MatGrp = %s)AND (billno = '%s')AND (type = '%s') " % (
        finyear, mislipno, matgrp,urlunquote(billno),billtype)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    success = 'False'
    if request.method == 'GET':
        #print('d')
        form = mislipbilleditForm(initial=c1[0])
                                  #{'finyear': finyear, 'mislipno': mislipno, 'matgrp': matgrp, 'mrrno': mrrno, 'billno': billno, 'billtype': billtype})
        # form.fields['matgrp'].widget.attrs['readonly'] = False
        # form.fields['mislipno'].widget.attrs['readonly'] = False
        # form.fields['st_auth'].widget.attrs['disabled'] = True
        context = {'form': form, 'save': 'saveMe_add', 'formaction': 'mislipbillcreate', 'finyear': finyear,
                   'mislipno': mislipno, 'matgrp': matgrp, 'billno': urlquote(billno,''),'billtype': billtype,
                   'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/mislipbilledit.html', context, request=request)
        # print(html_form)

    if request.method == 'POST':

        form = mislipbilleditForm(request.POST)
        # form.fields['matgrp'].widget.attrs['readonly'] = False
        # form.fields['mislipno'].widget.attrs['readonly'] = False
        # form.fields['st_auth'].widget.attrs['disabled'] = True
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
        context = {'form': form, 'save': 'saveMe_add', 'formaction': 'mislipbillcreate', 'finyear': finyear,
                   'mislipno': mislipno, 'matgrp': matgrp,'billno': urlquote(billno,""),'billtype': billtype,
                   'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/mislipbilledit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})


def mislipbilldel(request):
    pass

def mrrview(request):
    sql="select yearid from stcurrentyear"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    stCurrenyYear=c1[0]['yearid']
    #stCurrenyYear='2020-2021'
    return render(request,'mi_website/mrrview.html',{'finyear':stCurrenyYear})

def ajax_mrrs(request):
    urls = {}
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    formFields = []
    tableparticulars={}

    finyear = (request.GET.get('finyear', ''))
    mrrdate=(request.GET.get('dated', ''))
    field=(request.GET.get('field', ''))
    if mrrdate != '':
        mrrdate = datetime.strptime(mrrdate, '%m-%d-%Y').strftime("%d-%b-%Y")

    if field=='':
        sql = "SELECT Mrr.FinYear, MatCat.MatCat, Mrr.MrrNo, Mrr.MrrDate, Mrr.GrcNo, Mrr.PoNo, Mrr.SuppName, Mrr.Des, Mrr.ActQty, Mrr.BilledQty, Mrr.Unit, Mrr.WtAct, Mrr.WtCharged, Mrr.WtUnit, Mrr.CenventCopy, Mrr.CenventNo, Mrr.CenventDate, Mrr.EdAmount, Mrr.CollectedBy, Mrr.TypeOfSupp, Mrr.ECCNo, Mrr.SuppCity, ISNULL(InspAuthMislip_mrr.Ins_Auth, 0) AS InspAuth FROM MatCat INNER JOIN Mrr ON MatCat.MatCatID = Mrr.MatCatID LEFT OUTER JOIN InspAuthMislip_mrr ON Mrr.MrrNo = InspAuthMislip_mrr.Mrrno  AND Mrr.FinYear = InspAuthMislip_mrr.FinYear  WHERE (mrr.FinYear ='" + finyear + "') AND (MrrDate ='" + str(
            mrrdate) + "') ORDER BY mrr.MrrNo"


    else:
        sql = "SELECT Mrr.FinYear, MatCat.MatCat, Mrr.MrrNo, Mrr.MrrDate, Mrr.GrcNo, Mrr.PoNo, Mrr.SuppName, Mrr.Des, Mrr.ActQty, Mrr.BilledQty, Mrr.Unit, Mrr.WtAct, Mrr.WtCharged, Mrr.WtUnit, Mrr.CenventCopy, Mrr.CenventNo, Mrr.CenventDate, Mrr.EdAmount, Mrr.CollectedBy, Mrr.TypeOfSupp, Mrr.ECCNo, Mrr.SuppCity, ISNULL(InspAuthMislip_mrr.Ins_Auth, 0) AS InspAuth FROM MatCat INNER JOIN Mrr ON MatCat.MatCatID = Mrr.MatCatID LEFT OUTER JOIN InspAuthMislip_mrr ON Mrr.MrrNo = InspAuthMislip_mrr.Mrrno  AND Mrr.FinYear = InspAuthMislip_mrr.FinYear  WHERE (mrr.FinYear ='" + finyear + "') AND (MrrDate ='" + str(
            mrrdate) + "') ORDER BY %s"%field
    urls['urlcreate'] = request.build_absolute_uri(reverse('mrrcreate', kwargs={'finyear': finyear,'mrrno':0,'mrrdate':mrrdate}))

    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    success="true"
    if len(c1) > 0:
        tableData=c1
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = ['mrrno', 'matcat','inspauth',]
        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('mrredit', kwargs={'finyear': item['finyear'],'mrrno': item['mrrno'],'mrrdate':mrrdate}))
            item['urldel'] = request.build_absolute_uri(reverse('mrrdel', kwargs={'finyear': item['finyear'],'mrrno': item['mrrno']}))
            #item['urlprint'] = reverse('mislipprint', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp']})

            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
        tableFields_verbose = {f: f for f in tableFields }

    return JsonResponse({'success':success,'tableData': tableData, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)


def mrredit(request,finyear,mrrno,mrrdate):
    submitbuttondisabled="false"
    html_form=''
    #print(request.method)
    sql = "SELECT Mrr.FinYear,mrr.matcatid, Mrr.MrrNo, replace(convert(varchar(11),Mrr.MrrDate,106),' ','-') as mrrdate, Mrr.GrcNo, Mrr.PoNo, Mrr.SuppName, Mrr.Des, Mrr.ActQty, Mrr.BilledQty, Mrr.Unit, Mrr.WtAct, Mrr.WtCharged, Mrr.WtUnit, Mrr.CenventCopy, Mrr.CenventNo, Mrr.CenventDate, Mrr.EdAmount, Mrr.CollectedBy, Mrr.TypeOfSupp, Mrr.ECCNo, Mrr.SuppCity, ISNULL(InspAuthMislip_mrr.Ins_Auth, 0) AS InspAuth,'edit' as addedit,cash_po=case mrr.cash_po when  1 then 1 else 0 end ,imp_ind=case mrr.imp_ind when  1 then 1 else 0 end   ,mrr.reg_unreg_comp,rcm=case mrr.rcm when  1 then 1 else 0 end  FROM MatCat INNER JOIN Mrr ON MatCat.MatCatID = Mrr.MatCatID LEFT OUTER JOIN InspAuthMislip_mrr ON Mrr.MrrNo = InspAuthMislip_mrr.Mrrno  AND Mrr.FinYear = InspAuthMislip_mrr.FinYear  WHERE (mrr.FinYear ='%s') AND (mrr.Mrrno =%s) ORDER BY mrr.MrrNo" % (
    finyear, mrrno)

    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #print(c1[0]['ins_auth'])
    success = 'False'
    if len(c1)>0:
        submitbuttondisabled= "true" if c1[0]['inspauth'] else "false"
        #print(submitbuttondisabled)
        if request.method == 'GET':
            form = mrreditForm(initial=c1[0])

            form.fields['mrrno'].widget.attrs['readonly'] = True
            context = {'form': form,'save':'saveMe_edit','finyear':finyear,'mrrno':mrrno,'mrrdate':mrrdate,'formaction':'mrredit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('mi_website/mrredit.html', context, request=request)
            #print(html_form)
            success='True'
        if request.method == 'POST':
            #print('save form')
            #print(dict(request.POST))
            #print(c1[0])
            #a={k:v[0] if len(v)==1 else v for k,v in request.POST.lists()}
            form=mrreditForm(request.POST,initial=c1[0])
            #if c1[0]['ins_auth']==1:
            #    form.fields['st_auth'].widget.attrs['readonly'] = True
            #print(form.changed_data)
            if form.is_valid():
                print('edit new mrr')
                data=form.save_update(request)
                if not data['success']:
                    form.add_error(field=None, error=str(data['exception']))
                    success='False'
                else:
                    success = 'True'
            else:
                pass

            context = {'form': form, 'save': 'saveMe_edit', 'finyear':finyear,'mrrno':mrrno,'mrrdate':mrrdate,'formaction':'mrredit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('mi_website/mrredit.html', context, request=request)
    return JsonResponse({'html_form': html_form,'success':success})

def mrrdel(request,finyear,mislipno,matgrp):
    pass

def mrrcreate(request,finyear,mrrno,mrrdate):
    submitbuttondisabled = "false"
    mrrno=0

    success = 'False'
    if request.method == 'GET':
        #print('d')
        form = mrreditForm(initial={'finyear':finyear,'mrrdate':mrrdate})
        form.fields['mrrdate'].widget.attrs['readonly'] = True

        context = {'form': form, 'save': 'saveMe_add', 'finyear':finyear,'mrrno':mrrno,'mrrdate':mrrdate,'formaction':'mrrcreate','submitbuttondisabled':submitbuttondisabled}
        html_form = render_to_string('mi_website/mrredit.html', context, request=request)
        # print(html_form)

    if request.method == 'POST':
        #print('mrrpost')
        form = mrreditForm(request.POST)
        form.fields['mrrdate'].widget.attrs['readonly'] = False

        if form.is_valid():
            #print('create new mrr')
            data = form.save_create(request)
            if not data['success']:
                form.add_error(field=None, error=str(data['exception']))
                success = 'False'
            else:
                success = 'True'
        else:
            pass
        context = {'form': form, 'save': 'saveMe_add', 'finyear':finyear,'mrrno':mrrno,'mrrdate':mrrdate,'formaction':'mrrcreate','submitbuttondisabled':submitbuttondisabled}
        html_form = render_to_string('mi_website/mrredit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})



def ajax_mrrvalues(request):
    urls = {}
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    formFields = []
    tableparticulars={}

    finyear = (request.GET.get('finyear', ''))
    mrrno=(request.GET.get('mrrno', ''))
    field=(request.GET.get('field', ''))
    if field=='':
        sql = "SELECT FinYear, MrrNo, type, replace(convert(varchar(11),dated,106),' ','-') as Dated, BillNo, cast(Value as decimal(10,2)) as value, CenventNo, CenventDate, EdAmount, EduCess, HeduCess, EValue, CVD, TarrifNo, Qty, CenventType, DocNo, AddDuty, cast(sgst as decimal(10,2)) as SGST, cast(cgst as decimal(10,2)) as CGST,cast(igst as decimal(10,2)) as IGST FROM Invoice WHERE (FinYear ='%s') AND (MrrNo = %s) ORDER BY BillNo" % (
                finyear, mrrno)


    else:
        sql = "SELECT FinYear, MrrNo, type, replace(convert(varchar(11),dated,106),' ','-') as Dated, BillNo, cast(Value as decimal(10,2)) as value, CenventNo, CenventDate, EdAmount, EduCess, HeduCess, EValue, CVD, TarrifNo, Qty, CenventType, DocNo, AddDuty, cast(sgst as decimal(10,2)) as SGST, cast(cgst as decimal(10,2)) as CGST,cast(igst as decimal(10,2)) as IGST FROM Invoice WHERE (FinYear ='%s') AND (MrrNo = %s) ORDER BY %s" % (
                finyear, mrrno,field)
    urls['urlcreate'] = request.build_absolute_uri(reverse('mrrvaluecreate', kwargs={'finyear': finyear,'mrrno':mrrno,'billno':0}))

    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    success="true"
    if len(c1) > 0:
        tableData=c1
        tableFields = list(c1[0].keys())
        print(tableFields)
        formFields = ['type','dated','billno','value',]
        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('mrrvalueedit', kwargs={'finyear': item['finyear'],'mrrno': item['mrrno'],'billno': urlquote(item['billno'],'')}))
            item['urldel'] = request.build_absolute_uri(reverse('mrrvaluedel', kwargs={'finyear': item['finyear'],'mrrno': item['mrrno'],'billno': urlquote(item['billno'],'')}))
            #item['urlprint'] = reverse('mislipprint', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp']})

            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
        tableFields_verbose = {f: f for f in tableFields }

    return JsonResponse({'success':success,'tableData': tableData, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields,'urls':urls,'tableparticulars':tableparticulars}, safe=False)


def mrrvalueedit(request,finyear,mrrno,billno):
    print("yy")
    submitbuttondisabled="false"
    html_form=''
    #print(request.method)
    sql = "SELECT     FinYear, MrrNo, BillNo, replace(convert(varchar(11),dated,23),' ','-') as dated, type, CenventNo, CenventDate, TarrifNo, EValue, cast(sgst as decimal(10,2)) as SGST, cast(cgst as decimal(10,2)) as CGST,cast(igst as decimal(10,2)) as IGST, cast([Value] as decimal(10,2)) as value  FROM         dbo.Invoice  WHERE (invoice.FinYear ='%s') AND (invoice.Mrrno =%s)  AND (invoice.billno ='%s') " % (
    finyear, mrrno, urlunquote(billno))
    print(sql)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #print(c1[0]['ins_auth'])
    success = 'False'
    if len(c1)>0:
        #submitbuttondisabled= "true" if c1[0]['st_auth'] else "false"
        #print(submitbuttondisabled)
        if request.method == 'GET':
            form = mrrvalueeditForm(initial=c1[0])

            form.fields['mrrno'].widget.attrs['readonly'] = True
            form.fields['billno'].widget.attrs['readonly'] = True
            context = {'form': form,'save':'saveMe_edit','finyear':finyear,'mrrno':mrrno,'billno':billno,'formaction':'mrrvalueedit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('mi_website/mrrvalueedit.html', context, request=request)
            #print(html_form)
            success='True'
        if request.method == 'POST':
            #print('save form')
            #print(dict(request.POST))
            #print(c1[0])
            #a={k:v[0] if len(v)==1 else v for k,v in request.POST.lists()}
            form=mrrvalueeditForm(request.POST,initial=c1[0])
            #if c1[0]['ins_auth']==1:
            #    form.fields['st_auth'].widget.attrs['readonly'] = True
            #print(form.changed_data)
            if form.is_valid():
                print('edit new mrr')
                data=form.save_update(request)
                if not data['success']:
                    form.add_error(field=None, error=str(data['exception']))
                    success='False'
                else:
                    success = 'True'
            else:
                pass

            context = {'form': form, 'save': 'saveMe_edit', 'finyear':finyear,'mrrno':mrrno,'billno':billno,'formaction':'mrrvalueedit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('mi_website/mrrvalueedit.html', context, request=request)
    return JsonResponse({'html_form': html_form,'success':success})

def mrrvaluedel(request,finyear,mislipno,matgrp):
    pass

def mrrvaluecreate(request,finyear,mrrno,billno):
    submitbuttondisabled = "false"
    billno=0

    success = 'False'
    if request.method == 'GET':
        #print('d')
        form = mrrvalueeditForm(initial={'finyear':finyear,'mrrno':mrrno,})
        #form.fields['mrrdate'].widget.attrs['readonly'] = True

        context = {'form': form, 'save': 'saveMe_add', 'finyear':finyear,'mrrno':mrrno,'billno':billno,'formaction':'mrrvaluecreate','submitbuttondisabled':submitbuttondisabled}
        html_form = render_to_string('mi_website/mrrvalueedit.html', context, request=request)
        # print(html_form)

    if request.method == 'POST':

        form = mrrvalueeditForm(request.POST)
        #form.fields['mrrno'].widget.attrs['readonly'] = False

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
        context = {'form': form, 'save': 'saveMe_add', 'finyear':finyear,'mrrno':mrrno,'billno':billno,'formaction':'mrrvaluecreate','submitbuttondisabled':submitbuttondisabled}
        html_form = render_to_string('mi_website/mrrvalueedit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})

def getcurrentyear(request):
    sql = "select yearid from stcurrentyear"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    stCurrentYear = c1[0]['yearid']
    #stCurrentYear='2020-2021'
    return JsonResponse({'stcurrentyear': stCurrentYear,})

def getmatgroups(request):
    sql = "select groupid  as value,cast(groupid as varchar(2)) as text from stvalidgroups order by groupid"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c2 = dictfetchall(cursor)
    matgroups= [{'value':c['value'], 'text': c['text']}  for c in c2 ]
    return JsonResponse({'matgroups': matgroups,})

@login_required
def ledgerview(request):
    username = str(request.user.get_username())
    print(username)
    if request.user.is_authenticated and (request.user.groups.filter(name='mainstore').exists()):
        pass
    else:
        return
    sql="select yearid from stcurrentyear"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    stCurrenyYear=c1[0]['yearid']
    #stCurrenyYear='2020-2021'
    return render(request,'mi_website/ledgerview.html',{'finyear':stCurrenyYear})

def ajax_ledger(request):
    urls = {}
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    tableFields_width={}
    formFields = []
    #tableparticulars={}
    formFields = ['docparticular', 'trdate', 'qtyin', 'qtyout', ]
    tableFields_verbose = {'docparticular': 'particulars', 'trdate': 'dated', 'qtyin': 'recept', 'qtyout': 'issue', }
    finyear = (request.GET.get('finyear', ''))
    stockno = (request.GET.get('stockno', ''))
    mattype = (request.GET.get('mattype', ''))
    field = (request.GET.get('field', ''))
    if mattype=='stock':
        if field == '' :
            sql = "select docparticular=case t.doctype when 3 then 'MN/' + t.yearid+'/'+cast(t.groupid as varchar(50))+'-'+cast (t.docno as varchar(100)) when 1 then 'DN:' + cast (t.docno as varchar(100)) when 2 then 'RN:'+ cast (t.docno as varchar(100)) when 4 then 'RV:' + cast (t.docno as varchar(100)) when 5 then 'VA NO:'+cast (t.docno as varchar(100)) when 6 then 'SAV NO:'+ cast (t.docno as varchar(100)) End ," \
                  "t.docno,t.qtyin,t.qtyout,t.transid,replace(convert(varchar(11),t.trdate,106),' ','-') as trdate,t.stockno, (select round(sum(sttransactions.qtyin),3)-round(sum(sttransactions.qtyout),3)  from sttransactions where sttransactions.trdate <= t.trdate  and sttransactions.status !='d' and yearid='" + finyear + "' and sttransactions.stockno='" + stockno + "' )as Datebal  from sttransactions as t where t.stockno='" + stockno + "' and yearid='" + finyear + "' and t.status !='d' order by trdate desc"
        else:
            sql = "select docparticular=case t.doctype when 3 then 'MN/' + t.yearid+'/'+cast(t.groupid as varchar(50))+'-'+cast (t.docno as varchar(100)) when 1 then 'DN:' + cast (t.docno as varchar(100)) when 2 then 'RN:'+ cast (t.docno as varchar(100)) when 4 then 'RV:' + cast (t.docno as varchar(100)) when 5 then 'VA NO:'+cast (t.docno as varchar(100)) when 6 then 'SAV NO:'+ cast (t.docno as varchar(100)) End ," \
                  "t.docno,t.qtyin,t.qtyout,t.transid,replace(convert(varchar(11),t.trdate,106),' ','-') as trdate,t.stockno, (select round(sum(sttransactions.qtyin),3)-round(sum(sttransactions.qtyout),3)  from sttransactions where sttransactions.trdate <= t.trdate  and sttransactions.status !='d' and yearid='" + finyear + "' and sttransactions.stockno='" + stockno + "' )as Datebal  from sttransactions as t where t.stockno='" + stockno + "' and yearid='" + finyear + "' and t.status !='d' order by %s desc"%field
    if mattype == 'raw':
        if field == '':
            sql = "select docparticular=case t.doctype when 3 then 'MN/' + t.yearid+'/'+cast(t.groupid as varchar(50))+'-'+cast (t.docno as varchar(100)) when 1 then 'DN:' + cast (t.docno as varchar(100)) when 2 then 'RN:'+ cast (t.docno as varchar(100)) when 4 then 'RV:' + cast (t.docno as varchar(100)) when 5 then 'VA NO:'+cast (t.docno as varchar(100)) when 6 then 'SAV NO:'+ cast (t.docno as varchar(100)) End ,t.docno,t.qtyin,t.qtyout,t.transid,replace(convert(varchar(11),t.trdate,106),' ','-') as trdate,t.stockno, (select round(sum(sttransactions.qtyin),3)-round(sum(sttransactions.qtyout),3)  from sttransactions where sttransactions.trdate <= t.trdate  and sttransactions.status !='d' and yearid='" + finyear + "' and sttransactions.stockno='" + stockno + "' )as Datebal  from sttransactions as t where t.stockno='" + stockno + "' and yearid='" + finyear + "' and t.status !='d' order by trdate desc"
        else:
            sql = "select docparticular=case t.doctype when 3 then 'MN/' + t.yearid+'/'+cast(t.groupid as varchar(50))+'-'+cast (t.docno as varchar(100)) when 1 then 'DN:' + cast (t.docno as varchar(100)) when 2 then 'RN:'+ cast (t.docno as varchar(100)) when 4 then 'RV:' + cast (t.docno as varchar(100)) when 5 then 'VA NO:'+cast (t.docno as varchar(100)) when 6 then 'SAV NO:'+ cast (t.docno as varchar(100)) End ,t.docno,t.qtyin,t.qtyout,replace(convert(varchar(11),t.trdate,106),' ','-') as transid,t.trdate,t.stockno, (select round(sum(sttransactions.qtyin),3)-round(sum(sttransactions.qtyout),3)  from sttransactions where sttransactions.trdate <= t.trdate  and sttransactions.status !='d' and yearid='" + finyear + "' and sttransactions.stockno='" + stockno + "' )as Datebal  from sttransactions as t where t.stockno='" + stockno + "' and yearid='" + finyear + "' and t.status !='d' order by %s desc" % field

    tableparticulars=stockinfo(finyear,stockno,mattype)

    #print(tableparticulars)
    urls['urlcreate'] = request.build_absolute_uri(reverse('ledgercreate', kwargs={'finyear': finyear,'stockno': stockno,'matgroup':tableparticulars['matgroup'], 'transid': 0}))
    print(urls['urlcreate'])
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    print(c1)
    success = "true"
    if len(c1) > 0:
        tableData = c1
        tableFields = list(c1[0].keys())
        #print(tableFields)

        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('ledgeredit', kwargs={'finyear': finyear, 'stockno': item['stockno'],'matgroup':tableparticulars['matgroup'],'transid': item['transid']}))
            item['urldel'] = request.build_absolute_uri(reverse('ledgerdel', kwargs={'transid': item['transid']}))
            # item['urlprint'] = reverse('mislipprint', kwargs={'finyear': item['finyear'],'mislipno': item['mislipno'],'matgrp': item['matgrp']})

            color = 'default'
            item['rowcolor'] = color
            for f in formFields:
                color = 'default'
                item['fieldcolor'] = {f: color}

    tableFields_width['docparticular']='10%'
    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,'tableFields_width': tableFields_width,
                         'formFields': formFields, 'urls': urls,'tableparticulars':tableparticulars}, safe=False)


def ledgeredit(request,finyear,stockno,matgroup,transid):
    pass

def ledgercreate(request,finyear,stockno,matgroup,transid):
    submitbuttondisabled = "false"
    transid = 0

    success = 'False'
    if request.method == 'GET':
        #print('d')
        form = ledgereditForm(initial={'yearid': finyear, 'stockno': stockno,'docyearid': finyear,'groupid':matgroup })
        # form.fields['mrrdate'].widget.attrs['readonly'] = True

        context = {'form': form, 'save': 'saveMe_add', 'finyear': finyear, 'stockno': stockno,'matgroup':matgroup, 'transid': transid,
                   'formaction': 'ledgercreate', 'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/ledgeredit.html', context, request=request)
        #print(html_form)

    if request.method == 'POST':
        #print('dffgg')
        form = ledgereditForm(request.POST)
        # form.fields['mrrno'].widget.attrs['readonly'] = False
        #print(request.POST)
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
        context = {'form': form, 'save': 'saveMe_add', 'finyear': finyear, 'stockno': stockno,'matgroup':matgroup, 'transid': transid,
                   'formaction': 'ledgercreate', 'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/ledgeredit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})

def ledgerdel(request,transid):
    pass

def stockinfo(finyear,stockno,mattype):
    tableparticulars={}
    if mattype=='stock':
        sql = "select stockno,des,catcode='',matgroup,[unit] from stmaster where stockno='" + stockno + "'"
    elif mattype=='raw':
        sql = "select stockno,mattype as des,catcode,matgroup=0,[unit] from rawmatdes where stockno='" + stockno + "'"
    else:
        pass
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        tableparticulars['des']=c1[0]['des']
        tableparticulars['matgroup'] = c1[0]['matgroup']

    sql = "select isnull((sum(qtyin)-sum(qtyout)),0)+ isnull((select isnull(qty,0) from stopeningbal where yearid='" + finyear + "' and stockno='" + stockno + "' and status=1),0) as balance from sttransactions where yearid='" + finyear + "' and stockno='" + stockno + "' and status !='d'"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        st_balance=round(c1[0]['balance'],3)
    else:
        st_balance=0
    sql="select isnull(qty, 0)as openingBal from stopeningbal where yearid = '" + finyear + "' and stockno = '" + stockno + "' and status = 1"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1) > 0:
        openingbalance=round(c1[0]['openingbal'],3)
    else:
        openingbalance=0
    tableparticulars['Balance']=st_balance
    tableparticulars['Open_bal'] = openingbalance
    #print(tableparticulars)
    return tableparticulars

def updateWON(request):
    rec_issue=request.GET.get('rec_issue','')
    stockno=request.GET.get('stockno','')
    finyear=request.GET.get('finyear','')
    matgroup=(request.GET.get('matgroup',''))
    doctype=(request.GET.get('doctype',''))
    docno=(request.GET.get('docno',''))
    qtyin=0
    qtyout=0
    alarm=""
    if doctype == 5:
        #txtIssue.Enabled = False
        #txtRec.Enabled = False
        sql = "select * from vaview where yearid='" + finyear + "' and matgroup=" + matgroup + " and vano=" + docno + " and doctype=" + doctype + " and stockno='" + stockno + "'"

        with open_db_connection('incomingstore') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)

        if len(c1) > 0:
            if c1[0]['accept']==0 and rec_issue=='receipt':
                alarm="wrong data!"

            if c1[0]['reject']==0 and rec_issue=='issue':
                alarm="wrong data!"

            if c1[0]['accept'] == 0:
                qtyout=c1[0]['reject']
            if c1[0]['reject'] == 0:
                qtyin=c1[0]['accept']
            docref=c1[0]["vadetrefid"]
        else:
            docref=""
    else:
        sql = "select * from stdocregister where yearid='" + finyear + "' and groupid=" + matgroup + " and docno=" + docno + " and doctype=" + doctype + ""

        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)

        if len(c1) > 0:
            won= c1[0]["won"]
            warrant ="" if c1[0]["warrant"]==0 else  c1[0]["warrant"]
            docref=c1[0]['refid']
        else:
            won=""
            warrant=""
            docref=""
    if doctype==3:
        sql = "select * from mislipdetailview where finyear='" + finyear + "' and matgrp=" + matgroup + " and mislipno=" + docno + " and ins_auth=1 and stockno='" + stockno + "'"
        with open_db_connection('incomingstore') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
        if len(c1) > 0:
            docref = c1[0]['misref']
        else:
            alarm="Wrong Mislip No"
    print('warrant',warrant)
    return JsonResponse({'alert': alarm, 'qtyin': qtyin,'qtyout': qtyout,'docref': docref,'won': won,'warrant': warrant})
@login_required
def stdocregisterview(request):
    username = str(request.user.get_username())
    #print(username)
    if request.user.is_authenticated and (request.user.groups.filter(name='mainstore').exists()):
        pass
    else:
        login_url = None

        from django.contrib.auth.views import redirect_to_login
        from django.contrib.auth import REDIRECT_FIELD_NAME
        from django.shortcuts import resolve_url
        from django.conf import settings
        resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
        path = request.get_full_path()
        redirect_field_name = REDIRECT_FIELD_NAME
        return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
    sql = "select yearid from stcurrentyear"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    stCurrenyYear = c1[0]['yearid']
    #stCurrenyYear = '2020-2021'
    sql="select groupid  as value,cast(groupid as varchar(2)) as text from stvalidgroups order by groupid"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c2 = dictfetchall(cursor)
    return render(request, 'mi_website/stdocregisterview.html', {'finyear': stCurrenyYear,'options':c2})

def ajax_stdocregister(request):

    urls = {}
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    formFields = []
    tableparticulars = {}

    yearid = request.GET.get('yearid', '')
    groupid = (request.GET.get('groupid', ''))

    formFields = ["docno","doctype","won","warrant","des","refid","docdate"]
    tableFields_verbose = {"docno":"docno","doctype":"doctype","won":"won","warrant":"warrant","des":"des","refid":"refid","docdate":"docdate"}
    sql = "select yearid,groupid,doctype,max(docno) as maxdocno from stdocregister where yearid='" + yearid + "' and groupid=" + groupid + "  group by yearid,groupid,doctype"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    a = {}
    [a.update({str(c['doctype']): c['maxdocno']+1}) for c in c1]
    p=  {yearid: {str(groupid):a }}

    tableparticulars['maxdocs']=p
    #print(p)

    sql = "select yearid,doctype,groupid,docno,won,warrant,stauth,refid,isnull(des,'') as des,replace(convert(varchar(11),docdate,106),' ','-') as docdate from stdocregister where yearid='" + yearid + "' and groupid=" + groupid + "  order by doctype,docno desc"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)


    try:
        urls['urlcreate'] = request.build_absolute_uri(reverse('stdocregistercreate',
                                    kwargs={'yearid': yearid, 'groupid': groupid, 'docno': 0, 'doctype':0}))
    except:
        urls['urlcreate'] = ''

    success = "true"
    if len(c1) > 0:
        tableData = c1

        tableFields = list(c1[0].keys())
        # print(tableFields)

        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('stdocregisteredit', kwargs={'yearid': item['yearid'], 'groupid': item['groupid'],
                                                            'docno': item['docno'], 'doctype': item['doctype']}))
            item['urldel'] = request.build_absolute_uri(reverse('stdocregisterdel', kwargs={'yearid': item['yearid'], 'groupid': item['groupid'],
                                                            'docno': item['docno'], 'doctype': item['doctype']}))
            #item['urlprint'] = reverse('stdocregisterprint', kwargs={'yearid': item['yearid'], 'groupid': item['groupid'],
                                                          #  'docno': item['docno'], 'doctype': item['doctype']})

            color = 'default'
            item['rowcolor'] = color
            for f in formFields:
                color = 'default'
                item['fieldcolor'] = {f: color}
        #print(tableData)
    else:
        tableData = []
        tableFields = formFields


    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,
                         'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars}, safe=False)

def stdocregisteredit(request,yearid,groupid,docno,doctype):
    pass

def stdocregistercreate(request,yearid,groupid,docno,doctype):
    submitbuttondisabled = "false"


    success = 'False'
    if request.method == 'GET':
        #print('d')
        form = stdocregistereditForm(
            initial={'yearid': yearid, 'groupid': groupid,})
        # form.fields['mrrdate'].widget.attrs['readonly'] = True

        context = {'form': form, 'save': 'saveMe_add', 'yearid': yearid, 'groupid': groupid, 'docno': docno, 'doctype': doctype,
                   'formaction': 'stdocregistercreate', 'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/stdocregisteredit.html', context, request=request)
        # print(html_form)

    if request.method == 'POST':
        #print('dffgg')
        form = stdocregistereditForm(request.POST)
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
        context = {'form': form, 'save': 'saveMe_add', 'yearid': yearid, 'groupid': groupid, 'docno': docno, 'doctype': doctype,
                   'formaction': 'stdocregistercreate', 'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/stdocregisteredit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})

def stdocregisterdel(request,yearid,groupid,docno,doctype):
    pass

def ajax_stdocledger(request):

    urls = {}
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    formFields = []
    tableparticulars = {}

    yearid = request.GET.get('yearid', '')
    groupid = (request.GET.get('groupid', ''))
    doctype = (request.GET.get('doctype', ''))
    docno = (request.GET.get('docno', ''))

    formFields = ["stockno", "qtyin", "qtyout",]
    tableFields_verbose = {"stockno": "stockno", "qtyin": "receipt", "qtyout": "issue",}
    sql = "select yearid,doctype,groupid,docno,won,warrant,qtyin,qtyout,trdate,stockno from sttransactions where yearid='" + yearid + "' and groupid=" + str(groupid) + " and doctype=" + str(doctype) + " and docno=" + str(docno) + " and [status]='a'  order by groupid,docno,stockno"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    # print(p)



    try:
        urls['urlcreate'] = ''
    except:
        urls['urlcreate'] = ''

    success = "true"
    if len(c1) > 0:
        tableData = c1

        tableFields = list(c1[0].keys())
        # print(tableFields)

        for item in c1:
            item['urledit'] =''
            item['urldel'] = ''
            # item['urlprint'] = reverse('stdocregisterprint', kwargs={'yearid': item['yearid'], 'groupid': item['groupid'],
            #  'docno': item['docno'], 'doctype': item['doctype']})

            color = 'default'
            item['rowcolor'] = color
            for f in formFields:
                color = 'default'
                item['fieldcolor'] = {f: color}
        #print(tableData)
    else:
        tableData = []
        tableFields = formFields

    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,
                         'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars}, safe=False)


@login_required
def stmislipsview(request):
    username = str(request.user.get_username())
    #print(username)
    if request.user.is_authenticated and (request.user.groups.filter(name='mainstore').exists()):
        pass
    else:
        return
    sql = "select yearid from stcurrentyear"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    stCurrenyYear = c1[0]['yearid']
    #stCurrenyYear = '2020-2021'
    return render(request, 'mi_website/stmislipsview.html', {'finyear': stCurrenyYear})

def ajax_stmislips(request):

    urls = {}
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    formFields = []
    tableparticulars = {}

    dated = request.GET.get('dated', '')
    finyear=request.GET.get('finyear', '')


    formFields = ["mst_auth","mislipno","mrrno","matgrp","recdby","pono","mprno","misref",'mst_auth_date']
    [tableFields_verbose.update(f) for f in [{c:c} for c in formFields]]


    sql ="select mst_auth,Mislipno,matgrp,recdby,pono,mprno,suppname,finyear,misref,replace(convert(varchar(11),mst_auth_date,106),' ','-') as mst_auth_date,replace(convert(varchar(11),mislipdate,106),' ','-') as mislipdate from mislipviewins where mislipdate='" + dated + "' and me_auth=1 and finyear='" + finyear + "'"

    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)


    try:
        urls['urlcreate'] = ''
    except:
        urls['urlcreate'] = ''

    success = "true"
    if len(c1) > 0:
        tableData = c1

        tableFields = list(c1[0].keys())
        # print(tableFields)

        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('stmislipedit', kwargs={'finyear': item['finyear'], 'mislipno': item['mislipno'],
                                                            'matgrp': item['matgrp'], 'mislipdate': item['mislipdate']}))

            #item['urledit'] = reverse('stmislipsedit', kwargs={'finyear': item['finyear'], 'groupid': item['matgrp'],
                                                       #     'docno': item['mislipno'], 'doctype': 3})
            #item['urldel'] = reverse('stmislipsdel', kwargs={'finyear': item['finyear'], 'groupid': item['matgrp'],
                                                        #    'docno': item['mislipno'], 'doctype': 3})
            #item['urlprint'] = reverse('stdocregisterprint', kwargs={'yearid': item['yearid'], 'groupid': item['groupid'],
                                                          #  'docno': item['docno'], 'doctype': item['doctype']})

            color = 'default'
            item['rowcolor'] = color
            for f in formFields:
                color = 'default'
                item['fieldcolor'] = {f: color}
        #print(tableData)
    else:
        tableData = []
        tableFields = formFields


    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,
                         'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars}, safe=False)

def stmislipedit(request,finyear,mislipno,matgrp,mislipdate):
    submitbuttondisabled="false"
    html_form=''
    #print(request.method)
    sql = "SELECT FinYear, replace(convert(varchar(11),mislipDate,106),' ','-') as mislipdate, MiSlipNo, MatGrp, RecDBy, isnull(Note,'') AS NOTE,suppname, St_Auth, isnull(Ins_Auth,0) as ins_auth, Pono, Mprno, MSt_auth, ME_auth, replace(convert(varchar(11),mst_auth_date,23),' ','-') as mst_auth_date FROM MiSlip WHERE (FinYear ='%s') AND (Matgrp =%s) AND (MiSlipno =%s) ORDER BY MiSlipNo" % (
    finyear, matgrp, mislipno)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    print(c1[0])
    success = 'False'
    if len(c1)>0:
        submitbuttondisabled= "true" if c1[0]['mst_auth'] else "false"
        #print(submitbuttondisabled)
        if request.method == 'GET':
            form = mislipeditForm(initial=c1[0])

            form.fields['st_auth'].widget.attrs['onclick'] = 'return  false' if c1[0]['ins_auth'] else 'return  true'
            form.fields['recdby'].widget.attrs['readonly'] = True
            form.fields['note'].widget.attrs['readonly'] = True
            form.fields['suppname'].widget.attrs['readonly'] = True
            form.fields['pono'].widget.attrs['readonly'] = True
            form.fields['mprno'].widget.attrs['readonly'] = True

            context = {'form': form,'save':'saveMe_edit','finyear':finyear,'mislipno':mislipno,'matgrp':matgrp,'mislipdate':mislipdate,'formaction':'mislipedit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('mi_website/mislipedit.html', context, request=request)
            #print(html_form)
            success='True'
        if request.method == 'POST':
            #print('save form')
            #print(dict(request.POST))
            #print(c1[0])
            #a={k:v[0] if len(v)==1 else v for k,v in request.POST.lists()}
            form=mislipeditForm(request.POST,initial=c1[0])
            form.fields['st_auth'].widget.attrs['onclick'] = 'return  false' if c1[0]['ins_auth'] else 'return  true'
            form.fields['recdby'].widget.attrs['readonly'] = True
            form.fields['note'].widget.attrs['readonly'] = True
            form.fields['suppname'].widget.attrs['readonly'] = True
            form.fields['pono'].widget.attrs['readonly'] = True
            form.fields['mprno'].widget.attrs['readonly'] = True
            #print(form.changed_data)
            if form.is_valid():
                print('edit new mislip')
                data=form.save_update(request)
                if not data['success']:
                    form.add_error(field=None, error=str(data['exception']))
                    success='False'
                else:
                    success = 'True'
            else:
                pass

            context = {'form': form, 'save': 'saveMe_edit', 'finyear':finyear,'mislipno':mislipno,'matgrp':matgrp,'mislipdate':mislipdate,'formaction':'mislipedit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('mi_website/mislipedit.html', context, request=request)
    return JsonResponse({'html_form': html_form,'success':success})

def ajax_stmislipitems(request):

    urls = {}
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    formFields = []
    tableparticulars = {}


    finyear=request.GET.get('finyear', '')
    mislipno = request.GET.get('mislipno', '')
    matgrp = request.GET.get('matgrp', '')
    docref = request.GET.get('docref', '')

    formFields = ["stockno",'des','unit','qtyaccepted','qtyin','trdate']
    [tableFields_verbose.update(f) for f in [{c:c} for c in formFields]]


    sql ="SELECT FinYear, MatGrp, MiSlipNo, DetailId, StocKNo, Des,Unit,round(QtyRecd,3) as qtyrecd, round(QtyAccepted,3) as qtyaccepted, DateAccepted,PersonAccepted , isnull(qtyIn,-1)as qtyin,replace(convert(varchar(11),trdate,106),' ','-') as trdate FROM MISlipDet_Mst where mislipno=" + mislipno + " and matgrp=" + matgrp + " and finyear='" + finyear + "'"


    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)


    try:
        urls['urlcreate'] = ''
    except:
        urls['urlcreate'] = ''
    """yearid,docyearid,groupid,docno,doctype,qtyin,stockno,docref,trdate"""
    success = "true"
    if len(c1) > 0:
        tableData = c1

        tableFields = list(c1[0].keys())
        # print(tableFields)

        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('stmislipitemsedit', kwargs={'yearid': finyear,'docref': docref, 'stockno':item['stockno'], }))
            #item['urldel'] = reverse('stmislipsdel', kwargs={'finyear': item['finyear'], 'groupid': item['matgrp'],
                                                        #    'docno': item['mislipno'], 'doctype': 3})
            #item['urlprint'] = reverse('stdocregisterprint', kwargs={'yearid': item['yearid'], 'groupid': item['groupid'],
                                                          #  'docno': item['docno'], 'doctype': item['doctype']})

            color = 'default'
            item['rowcolor'] = color
            item['fieldcolor']={}
            for f in formFields:
                color = 'default'
                if f=='qtyin':
                    color='red'
                item['fieldcolor'] .update( {f: color})
        print(item['fieldcolor'])
    else:
        tableData = []
        tableFields = formFields


    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,
                         'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars}, safe=False)


def stmislipitemsedit(request,yearid,docref,stockno):
    submitbuttondisabled = "false"
    html_form = ''
    # print(request.method)
    sql = "select * from sttransactions  where docref=" + str(docref) + " and doctype=3 and stockno='" + stockno + "' and status='a'"

    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    sql = "select * from mislip where misref=" + str(docref) +""
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c2 = dictfetchall(cursor)
    # print(c1[0]['ins_auth'])
    success = 'False'
    if len(c1) > 0:
        submitbuttondisabled= "true" if c2[0]['mst_auth'] else "false"
        # print(submitbuttondisabled)
        if request.method == 'GET':
            form = stmislipitemeditForm(initial=c1[0])


            context = {'form': form, 'save': 'saveMe_edit', 'yearid':yearid,'docref': docref, 'stockno': stockno,
                       'formaction': 'stmislipitemsedit', 'submitbuttondisabled': submitbuttondisabled}
            html_form = render_to_string('mi_website/stmislipitemedit.html', context, request=request)
            # print(html_form)
            success = 'True'
        if request.method == 'POST':

            form =stmislipitemeditForm(request.POST, initial=c1[0])

            if form.is_valid():
                #print('edit new stmislipitem')
                data = form.save_update(request)
                if not data['success']:
                    form.add_error(field=None, error=str(data['exception']))
                    success = 'False'
                else:
                    success = 'True'
            else:
                pass

            context = {'form': form, 'save': 'saveMe_edit', 'yearid': yearid, 'docref': docref, 'stockno': stockno,
                       'formaction': 'stmislipitemsedit', 'submitbuttondisabled': submitbuttondisabled}
            html_form = render_to_string('mi_website/stmislipitemedit.html', context, request=request)
    else:


        sql = "select * from mislip where misref=" + str(docref) + ""
        with open_db_connection('incomingstore') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
        submitbuttondisabled = "true" if c1[0]['mst_auth'] else "false"
        docyearid=c1[0]['finyear']
        groupid = c1[0]['matgrp']
        docno=c1[0]['mislipno']
        doctype=3

        sql="select * from mislipdet where finyear='%s' and mislipno=%s and matgrp=%s and stockno='%s'"%(docyearid,docno,groupid,stockno)
        with open_db_connection('incomingstore') as cursor:
            cursor.execute(sql)
            c2 = dictfetchall(cursor)
        qty=c2[0]["qtyaccepted"]
        success = 'False'
        if request.method == 'GET':
            #print('d')
            form = stmislipitemeditForm(
                initial={'yearid': yearid, 'docyearid': docyearid, 'groupid': groupid, 'docno': docno, 'doctype': doctype, 'stockno': stockno,'qtyin': qty,'docref':docref })
            # form.fields['mrrdate'].widget.attrs['readonly'] = True

            context = {'form': form, 'save': 'saveMe_add', 'yearid': yearid, 'docref': docref, 'stockno': stockno,
                       'formaction': 'stmislipitemsedit', 'submitbuttondisabled': submitbuttondisabled}
            html_form = render_to_string('mi_website/stmislipitemedit.html', context, request=request)
            # print(html_form)

        if request.method == 'POST':
            #print('dffgg')
            form = stmislipitemeditForm(request.POST)
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
            context = {'form': form, 'save': 'saveMe_add','yearid': yearid, 'docref': docref, 'stockno': stockno,
                       'formaction':  'stmislipitemsedit', 'submitbuttondisabled': submitbuttondisabled}
            html_form = render_to_string('mi_website/stmislipitemedit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})


def stmislipitemscreate(request,yearid,docref,stockno):
    pass

def stmislipitemsdel(request,yearid,groupid,docno,doctype):
    pass

@login_required
def ststockmasterview(request):
    username = str(request.user.get_username())
    # print(username)
    if request.user.is_authenticated and (request.user.groups.filter(name='mainstore').exists()):
        pass
    else:
        login_url = None

        from django.contrib.auth.views import redirect_to_login
        from django.contrib.auth import REDIRECT_FIELD_NAME
        from django.shortcuts import resolve_url
        from django.conf import settings
        resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
        path = request.get_full_path()
        redirect_field_name = REDIRECT_FIELD_NAME
        return redirect_to_login(
            path, resolved_login_url, redirect_field_name)
    sql = "select yearid from stcurrentyear"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    stCurrenyYear = c1[0]['yearid']
    #stCurrenyYear = '2020-2021'
    return render(request, 'mi_website/ststockmasterview.html', {'finyear': stCurrenyYear})

def ajax_ststockmaster(request):
    urls = {}
    tableData = []
    tableFields = []
    tableFields_verbose = {}
    formFields = []
    tableparticulars = {}

    finyear = request.GET.get('finyear', '')
    stockno = request.GET.get('stockno', '')

    #fields = {'machinename': {'verbose': 'Name', 'align': 'center','summary':'','summaryinfo':''},
             # 'machinedes': {'verbose': 'Description', 'align': 'right'}}
    #formFields = list(fields.keys())
    #tableFields_verbose = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('verbose',k) for k in fields])}
    #tableFields_align = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('align','center') for k in fields])}


    formFields = ["stockno", 'drwgno', 'ldrwgno', 'altindex', 'des', 'openingbal', 'unit']
    [tableFields_verbose.update(f) for f in [{c: c} for c in formFields]]
    groups = "0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,90,91,92,93,94,95,96,97,98,99"

    sql = "SELECT     dbo.stmaster.stockno, ltrim(rtrim(dbo.stMaster.des)) as des, dbo.stMaster.matgroup, isnull(dbo.stMaster.ItemCodeSuffix,'') +isnull(dbo.stMaster.ItemCodeNo,'') as drwgno, ISNULL(dbo.allItems1.ItemCodeSuffix, '') + ISNULL(dbo.allitems1.ItemCodeNo, '') AS ldrwgno,rtrim(isnull( dbo.allitems1.AltIndex,'')) as altindex,loca,locb,isnull((select isnull(qty,0) from stopeningbal where stopeningbal.stockno=stmaster.stockno and stopeningbal.yearid='" + finyear + "'),0) as openingBal,stmaster.[unit] FROM         dbo.stMaster LEFT OUTER JOIN dbo.allItems1 ON dbo.stMaster.ItemCodeSuffix = dbo.allItems1.ItemCodeSuffix AND dbo.stMaster.ItemCodeNo = dbo.allItems1.ItemCodeNo WHERE     (dbo.stMaster.matgroup IN (" + groups + ")) and stmaster.stockno like '" + stockno + "%' order by stmaster.stockno"
    #print(sql)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    try:
        urls['urlcreate'] = request.build_absolute_uri(reverse('ststockmastercreate', kwargs={'stockno': '0', }))
    except:
        urls['urlcreate'] = ''

    success = "true"
    #print(c1)
    if len(c1) > 0:
        tableData = c1

        tableFields = list(c1[0].keys())
        # print(tableFields)

        for item in c1:
            item['urledit'] =request.build_absolute_uri(reverse('ststockmasteredit', kwargs={'stockno': item['stockno'], }))
            # item['urldel'] = reverse('stmislipsdel', kwargs={'finyear': item['finyear'], 'groupid': item['matgrp'],
            #    'docno': item['mislipno'], 'doctype': 3})
            # item['urlprint'] = reverse('stdocregisterprint', kwargs={'yearid': item['yearid'], 'groupid': item['groupid'],
            #  'docno': item['docno'], 'doctype': item['doctype']})


            color = 'default'
            item['rowcolor'] = color
            item['fieldcolor'] = {}
            for f in formFields:
                color = 'default'
                if f == 'des':
                    color = 'red'
                item['fieldcolor'].update({f: color})
        #print(item['fieldcolor'])
    else:
        tableData = []
        tableFields = formFields

    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,
                         'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars}, safe=False)

def ststockmasteredit(request,stockno):
    submitbuttondisabled="false"
    html_form=''
    #print(request.method)
    sql = "SELECT * from stmaster where stockno='%s'"%(stockno)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #print(c1[0])
    success = 'False'
    if len(c1)>0:

        if request.method == 'GET':
            form = ststockmastereditForm(initial=c1[0])
            form.fields['stockno'].widget.attrs['readonly'] = True



            context = {'form': form,'save':'saveMe_edit','stockno':stockno,'formaction':'ststockmasteredit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('mi_website/ststockmasteredit.html', context, request=request)
            #print(html_form)
            success='True'
        if request.method == 'POST':
            #print('save form')
            #print(dict(request.POST))
            #print(c1[0])
            #a={k:v[0] if len(v)==1 else v for k,v in request.POST.lists()}
            form=ststockmastereditForm(request.POST,initial=c1[0])
            form.fields['stockno'].widget.attrs['readonly'] = True
            #print(form.changed_data)
            if form.is_valid():
                print('edit new stock master')
                data=form.save_update(request)
                if not data['success']:
                    form.add_error(field=None, error=str(data['exception']))
                    success='False'
                else:
                    success = 'True'
            else:
                pass

            context = {'form': form, 'save': 'saveMe_edit', 'stockno':stockno,'formaction':'ststockmasteredit','submitbuttondisabled':submitbuttondisabled}
            html_form = render_to_string('mi_website/ststockmasteredit.html', context, request=request)
    return JsonResponse({'html_form': html_form,'success':success})

def ststockmastercreate(request,stockno):
    submitbuttondisabled = "false"

    success = 'False'
    if request.method == 'GET':
        # print('d')
        form = ststockmastereditForm()
        # form.fields['mrrdate'].widget.attrs['readonly'] = True

        context = {'form': form, 'save': 'saveMe_add',
                   'formaction': 'ststockmastercreate','stockno':stockno, 'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/ststockmasteredit.html', context, request=request)
        # print(html_form)

    if request.method == 'POST':
        # print('dffgg')
        form = ststockmastereditForm(request.POST)
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
                   'formaction': 'ststockmastercreate','stockno':stockno, 'submitbuttondisabled': submitbuttondisabled}
        html_form = render_to_string('mi_website/ststockmasteredit.html', context, request=request)
    return JsonResponse({'html_form': html_form, 'success': success})

def ststockmasterdel(request,stockno):
    pass


def ajax_tablename(request):
    """
    urls.urlcreate if equal to '' then add button and the table header represented by formFields are not displayed and must be provided and  cannot be undefined
    urlcreate, urledit, urldel, urlprint are required in case useActionButton is true and table is a CRUD table
    tableData:[{<field_name>:<field_value>},] is list of dictionary, each dictionary is a row item of table
    tableFields:list(tableData[0].keys()) is all the keys in the table data
    fields:{<fieldname>:{<field_charaterstics1>:<value>,<field_charaterstics1>:<value>...},...} set of fields to be displayed as opposed to all fields contained in tableFields as reteived fro database
    field_charaterstic are of four  types
    (1)verbose: actual field name to be displayed as different from that used in table definition
    (2) align: how the data to be aligned in each column
    (3) summary: if summary row is to be displayed, then it will contain the value of summary data to be displayed below each column
    (4)summaryinfo: type of summary data e.g. total or average
    formFields: list(fields.keys()) is a list containing all the fields as contained in the table data to be displayed  as opposed to tableFields
    normally these also correspond to the form fields if CRUD operation is required

    to make any column hidden, set its tableFields_width[<field>] equal to '0%'
    """
    urls = {}
    tableData = []
    tableFields = []
    fields = {{}}
    formFields = []
    tableFields_verbose = {}
    tableparticulars = {}
    tableFields_align={}
    tableFields_width={}
    tableFields_summary={}
    tableFields_summaryinfo = {}

    finyear = request.GET.get('finyear', '')
    stockno = request.GET.get('stockno', '')

    group=request.GET.get('group','')

    fields = {'machinename': {'verbose': 'Name', 'align': 'center','summary':'','summaryinfo':''},
    'machinedes': {'verbose': 'Description', 'align': 'right'}}
    formFields = list(fields.keys())
    tableFields_verbose = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('verbose',k) for k in fields])}
    tableFields_align = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('align','center') for k in fields])}
    tableFields_width = {i: j for (i, j) in
                         zip(list(fields.keys()), [fields[k].get('width', '10%') for k in fields])}
   
    tableFields_summary = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summary','center') for k in fields])}
    tableFields_summaryinfo = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summaryunfo','center') for k in fields])}

    sql = ""

    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    try:
        urls['urlcreate'] = request.build_absolute_uri(reverse('ststockmastercreate', kwargs={'stockno': '0', }))
    except:
        urls['urlcreate'] = ''

    success = "true"
    # print(c1)
    if len(c1) > 0:
        tableData = c1

        tableFields = list(c1[0].keys())
        # print(tableFields)

        for item in c1:
            item['urledit'] = request.build_absolute_uri(reverse('ststockmasteredit', kwargs={'stockno': item['stockno'], }))

            color = 'default'
            item['rowcolor'] = color
            item['fieldcolor'] = {}
            for f in formFields:
                color = 'default'
                if f == 'des':
                    color = 'red'
                item['fieldcolor'].update({f: color})
                # print(item['fieldcolor'])
        for k in formFields[::-1]:
        #print(k)
            sortedc1 = sorted(c1, key=lambda c: float(str(c[k]).strip().lower()) if str(
            c[k]).strip().lower().replace('.', '', 1).isdigit() else str(c[k]).strip().lower())
            n = 0
            for c in sortedc1:
                c['sortkey_' + k] = n
                n += 1
        tableData=sortedc1
        if group=='yes':
        
            fields=json.loads(request.GET.get('fields',''))
            function=json.loads(request.GET.get('function',''))
            filter=json.loads(request.GET.get('filter',''))
            print(function)
            df = pd.DataFrame(tableData)
            if len(filter)>0:
                f=[]
                for key,value in filter.items():
                    f.append((df[key].isin(value)))
                for index,f1 in enumerate(f):
                    if index==0:
                        filt=f1     
                    else:
                        filt=(filt) & (f1)

                df=df.loc[filt]
            print(function)
            fields_sum=[key for key,value in function.items() if value=='sum']
            agg_dict={key:val for key, val in function.items() if val != 'group'}
            fields_group=[key for key,value in function.items() if value=='group']
            fields_count=[key for key,value in function.items() if value=='count']
            print(fields_group)
            #grouped_df=df.sort_values(fields_group).groupby(fields_group).agg(agg_dict)
            grouped_df=df.groupby(fields_group,as_index=False).agg(agg_dict)
           
            #df_sum = grouped_df[fields_sum].sum()
            #df_count=grouped_df[fields_count].count()

            #df=pd.merge(df_sum, df_count, left_index=True, right_index=True).reset_index()
            c2=grouped_df.to_dict('records')
            print(c2)
            formFields=fields
            for item in c2:
                for f in formFields:
                    color='default'
                    item['fieldcolor']={f:color}
            tableData=c2
            
            # for k in formFields[::-1]:
            # #print(k)
            #     sortedc1 = sorted(c1, key=lambda c: float(str(c[k]).strip().lower()) if str(
            #         c[k]).strip().lower().replace('.', '', 1).isdigit() else str(c[k]).strip().lower())
            #     n = 0
            #     for c in sortedc1:
            #         c['sortkey_' + k] = n
            #         n += 1
            #tableData=sortedc1
            #groupdata=grouped_df.to_html(escape=False)
            #soup = BeautifulSoup(groupdata, "html.parser")
            #for r in soup.find_all('table'):
            #    r['class'] = 'table table-bordered table-striped table-hover table-condensed compact'
            #    r['style']='width:80%'
                
            
            return JsonResponse({'success':success,'tableData': tableData,'formFields':formFields,'fields_group':fields_group})

    else:
        tableData = []
        tableFields = formFields

    return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                         'tableFields_verbose': tableFields_verbose,
                         'formFields': formFields, 'urls': urls, 'tableparticulars': tableparticulars,'tableFields_align': tableFields_align,'tableFields_width':tableFields_width,'tableFields_summary': tableFields_summary,'tableFields_summaryinfo': tableFields_summaryinfo}, safe=False)


def transferMisliptoAccess(finyear,matgrp,mislipno):
    #cursor = conInStr.cursor()
    sql ="SELECT * From MiSlip WHERE (FinYear ='%s') AND (MiSlipno =%s) AND (Matgrp =%s)"%(finyear,mislipno,matgrp)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)

    if c1[0]['ins_auth']:
        MislipRef = "MN/" + finyear + "/" + str(matgrp) + "-" + str(mislipno)
    else:
        MislipRef = ""
    if c1[0]['st_auth'] and  matgrp==27:
        MislipRef = "MN/" + finyear + "/" + str(matgrp) + "-" + str(mislipno)


    miSlipDate =c1[0]["mislipdate"].strftime("%d-%b-%Y")
    poRef = str(c1[0]["mprno"]) + "/" + str(c1[0]["pono"])
    ReceivedBy = c1[0]["recdby"]
    party = c1[0]["suppname"]
    note = "" if c1[0]["note"] is None else c1[0]["note"]
    verdicts = "" if c1[0]["verdicts"] is None else c1[0]["verdicts"]

    sql = "SELECT dbo.MiSlipMrr.Mrrno, dbo.Mrr.MrrDate, dbo.Mrr.GrcNo, dbo.Mrr.SuppName, dbo.Mrr.CollectedBy, dbo.Mrr.CenventNo, dbo.Mrr.CenventDate,dbo.Mrr.EdAmount FROM         dbo.MiSlip INNER JOIN dbo.MiSlipMrr ON dbo.MiSlip.FinYear = dbo.MiSlipMrr.FinYear AND dbo.MiSlip.MatGrp = dbo.MiSlipMrr.MatGrp AND dbo.MiSlip.MiSlipNo = dbo.MiSlipMrr.MislipNo INNER JOIN dbo.Mrr ON dbo.MiSlipMrr.FinYear = dbo.Mrr.FinYear AND dbo.MiSlipMrr.Mrrno = dbo.Mrr.MrrNo where mislip.finyear='%s' and mislip.mislipno=%s and mislip.matgrp=%s order by mrr.mrrdate"%(finyear,mislipno,matgrp)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c2 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c2 = dictfetchall(cursor)

    if len(c2) > 0:
        n = 1
        Grdetail=""
        Mrrs=""
        CollectedBy=""
        for  item  in c2:
            if n == 1:
                Mrrs = Mrrs + str(item["mrrno"]) + " (" + (item["mrrdate"]).strftime("%d-%b-%Y") + ")"
                CollectedBy = CollectedBy + ('' if item["collectedby"]== None else item["collectedby"])
            else:
                Mrrs = Mrrs + "; " + str(item["mrrno"]) + " (" + (item["mrrdate"]).strftime("%d-%b-%Y") + ")"
                CollectedBy = CollectedBy + "; " + ('' if item["collectedby"]== None else item["collectedby"])
            if item["grcno"] != 0:
                Grdetail = Grdetail + '\n' + FindGrdetail(finyear, item["grcno"])
            n = n + 1
    sql = "select * from mislipbills where  finyear='%s' and mislipno=%s and matgrp=%s order by billtype"%(finyear,mislipno,matgrp)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c3 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c3 = dictfetchall(cursor)
    if len(c3)>0:
        m = 1
        n = 1
        Bills=""
        GST=""
        for item in c3:
            if n==1:
                Bills = Bills + item["billtype"] + " " + item["billno"] + " (" + (item["dated"]).strftime("%d-%b-%Y") + ")"
            else:
                Bills = Bills + ";" + item["billtype"] + " " + item["billno"] + " (" + item["dated"] + ")"

            if item["cenventno"] != "":
                if m==1:
                    GST = GST + "GST Invoice No:" + str(item["cenventno"]) + " (" + item["cenventdate"] + "), SGST:" + str(round(item["sgst"],2)) + ", CGST:" + str(round(item["cgst"],2)) + ", IGST:" + str(round(item["igst"],2)) + ""
                    m = 2
                else:
                    GST = GST + "\n" + "GST Invoice No:" + str(item["cenventno"]) + " (" + item["cenventdate"] + "), SGST:" + str(round(item["sgst"],2)) + ", CGST:" + str(round(item["cgst"],2)) + ", IGST:" + str(round(item["igst"],2)) + ""

        n = n + 1

    sql = "SELECT MIslipBills.FinYear, MIslipBills.MatGrp, MIslipBills.MislipNo, Sum(MIslipBills.Value) AS SumOfValue From MIslipBills  where  finyear='%s' and mislipno=%s and matgrp=%s GROUP BY MIslipBills.FinYear, MIslipBills.MatGrp, MIslipBills.MislipNo"%(finyear,mislipno,matgrp)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c4 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c4 = dictfetchall(cursor)
    if len(c4)>0:
        totalAmt = round(c4[0]["sumofvalue"],2)


    sql = "SELECT     TOP 100 PERCENT dbo.MiSlip.FinYear, dbo.MiSlip.MatGrp, dbo.MiSlip.MiSlipNo, dbo.MiSlip.MiSlipDate, dbo.MiSlip.RecDBy, dbo.MiSlip.Note,dbo.MislipDet.StocKNo, dbo.MislipDet.Des, dbo.MislipDet.QtyRecd, dbo.MislipDet.QtyAccepted, dbo.MislipDet.Unit, isnull(p.qtyIn,0) as qtyin,isnull(p.docType,0) as doctype,mislipdet.stdwt,mislipdet.scalewt,mislipdet.billedwt FROM         dbo.MiSlip INNER JOIN dbo.MislipDet ON dbo.MiSlip.FinYear = dbo.MislipDet.FinYear AND dbo.MiSlip.MatGrp = dbo.MislipDet.MatGrp AND dbo.MiSlip.MiSlipNo = dbo.MislipDet.MiSlipNo LEFT OUTER JOIN (select * from edssql.dbo.stTransactions where (edssql.dbo.stTransactions.status='a' or edssql.dbo.stTransactions.status =null)) p ON dbo.MislipDet.StocKNo = p.stockno AND dbo.MislipDet.FinYear = p.YearId AND dbo.MislipDet.MatGrp = p.GroupID AND dbo.MislipDet.mislipno = p.docNo and dbo.mislipdet.doctype=p.doctype WHERE     (dbo.MiSlip.FinYear ='%s')  AND (dbo.MiSlip.MiSlipNo =%s) AND (dbo.MiSlip.MatGrp =%s)    ORDER BY dbo.MislipDet.StocKNo"%(finyear,mislipno,matgrp)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c5 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c5 = dictfetchall(cursor)
    if len(c5)>0:
        print('c5')
        database = "C:\My Documents\IncomingStore_New_GST.mdb"
        constr = 'Provider=Microsoft.Jet.OLEDB.4.0; Data Source=%s' % database
        tablename = "table1"
        FrDetail=''
        # connect to the database
        conn = adodbapi.connect(constr)
        cursor = conn.cursor()
        sql = "delete * from mislipprint"
        cursor.execute(sql)
        conn.commit()
        for item in c5:
            if matgrp == 0:
                ItemDes = item["des"] + "\n" + "STANDARD WT.=" + str(item[ "stdwt"]) + "  " + " SCALE WT.=" + str(item["scalewt"]) + "  " + "BILLED WT.=" + str(item["billedwt"])
            else:
                ItemDes = item["des"].replace("'","''")

            sql = "INSERT INTO MislipPrint ( MislipRef, Mislipdate, Mrrs, poref, bills, CollectedBy, [Note], ReceivedBy, party, grdetail, frdetail, excise, totalamt, stockno, Des, unit, qty ,qtyaccepted,verdicts,qtystcharged) values ('"+ MislipRef + "','" + str(miSlipDate) + "','" + Mrrs + "','" + poRef + "','" + Bills + "','" + CollectedBy + "','" + note + "','" + ReceivedBy + "','" + party + "','" + Grdetail + "','" + FrDetail + "','" + GST + "','" + str(totalAmt) + "','" + item["stockno"] + "','" + ItemDes + "','" + item["unit"] + "','" + str(round(item["qtyrecd"],3)) + "','" + str('NA' if item["qtyaccepted"]==-1 else round(item["qtyaccepted"],3) ) + "','" + verdicts + "',%s)"%("-1" if item["qtyin"] is None else item["qtyin"])
            cursor.execute(sql)
            conn.commit()
        return True
    else:
        return False

def FindGrdetail(finyear, grcno):
    #cursor = conInStr.cursor()
    sql = "SELECT * From grc WHERE (FinYear ='%s') AND (grcno =%s)"%(finyear,grcno)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)
    item=c1[0]
    Grdetail = "St.Ch.No. " + ifNull(item["stnchnno"],"") + " dated " + ifNull((item["stnchndate"]),"") + ", GR No: " + ifNull(item["grno"],"") + " dated " + ifNull(item["grdate"].strftime("%d-%b-%Y"),"") + " of " + ifNull(item["trname"],"") + ", Cases as per GR:" + str(ifNull(item["noofcases"], "")) + " Received: " + str(ifNull(item["casesrec"],"")) + ", Weight as per GR: " + str(ifNull(item["wtact"], "")) + ifNull(item["wtunit"], "") + ", Weight charged: " + str(ifNull(item["wtcharged"], "")) + ifNull(item["wtunit"], "") + ""
    FrDetail = "Freight " + item["frghtpaymode"] + "::" + FindFrDetail(finyear, grcno)
    Grdetail = Grdetail + '\n' + FrDetail
    return Grdetail


def FindFrDetail(finyear, grcno):
    sql = " SELECT dbo.FreightPay.*, dbo.FrtPayMthd.Method AS FrMethod FROM dbo.FreightPay INNER JOIN  dbo.FrtPayMthd ON dbo.FreightPay.Method = dbo.FrtPayMthd.MethodId WHERE (FinYear ='%s') AND (grcno =%s)"%(finyear,grcno)
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #cursor = conInStr.cursor()
    #cursor.execute(sql)
    #c1 = dictfetchall(cursor)

    if len(c1)>0:
        FrDetail=""
        for item in c1:
            FrDetail = FrDetail + item["frmethod"] + " against Receipt no:" + item["frghtrtno"] + " dated:" + item["frghtrtdate"] + " amount:" + item["frghtamnt"] + ";"
    else:
        FrDetail=""
    return FrDetail
def ifNull(data,r):
    return r if data is None else data

def getReportfromAccess(rptname):
    #print (len(d))
    ac=win32.gencache.EnsureDispatch('Access.Application')
    #ac.Visible=False
    print('p')
    strdb = "c:\my documents\incomingstore_new_gst.mdb"
    ac.OpenCurrentDatabase (strdb)
    db=ac.CurrentDb()
    #strReportName = "MiSlipPrintQuery1"
    strReportName=rptname
    #ac.DoCmd.OpenReport (strReportName)
    #rpt = ac.Reports(strReportName)
    #ac.DoCmd.OpenReport(strReportName, 1)
    #ac.Visible = True
    x=ac.Run ('ConvertReportToPDF',"MiSlipPrintQuery1", "", "MiSlipPrintQuery1" + ".PDF")
    ac.Application.Quit()

def mislipprint(request,finyear,matgrp,mislipno):

    if transferMisliptoAccess(finyear, matgrp, mislipno):
        getReportfromAccess('MiSlipPrintQuery1')
        fs=FileSystemStorage(r"C:\users\kkaggarwal2\documents")
        filename="MiSlipPrintQuery1.pdf"
        if fs.exists(filename):
            with fs.open(filename) as pdf:
                response=HttpResponse(pdf,content_type='application/pdf')
                response['Content-Disposition']='attachment;filename="mypdf.pdf"'
                return response
        else:
            return HttpResponseNotFound('the rquested pdf not found')
    else:
        return HttpResponse('MI slip cannot be transferred')
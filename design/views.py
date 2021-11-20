"""I just installed python3.8 on a completely fresh installation of Windows 10 1909 and 
ran into this issue. All I had to do was install the lastest x64 version of the 
visual c redistributable vc_redist from here 
https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads
and my import problem went away."""

from django.shortcuts import render
from django.http import JsonResponse
import json
import pandas as pd
from pandas.core.arrays import boolean
from bs4 import BeautifulSoup

from djangovue.connections import open_db_connection,dictfetchall
# Create your views here.

def Index(request):
    template = "design/index_d.html"
    return render(request,template,context={'a':'kk'})

def ajax_products(request):
    field = request.GET.get('field', '')
    group=request.GET.get('group','')
    

    if field == '':
        sql = "SELECT * FROM [Machines] order by machinename"

    else:
        sql = "SELECT * FROM [Machines] order by %s"%field
    fields = {'machinename': {'verbose': 'Name', 'align': 'center','summary':'1','summaryinfo':'b'},
     'machinedes': {'verbose': 'Description', 'align': 'right','summary':'1','summaryinfo':'a'}}
    formFields = list(fields.keys())
    tableFields_verbose = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('verbose',k) for k in fields])}
    tableFields_align = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('align','center') for k in fields])}
    tableFields_summary = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summary', '1') for k in fields])}
    tableFields_summaryinfo = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summaryinfo', '2') for k in fields])}

    #print(tableFields_align)
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        #formFields = [ 'machinename', 'machinedes']
        n=0
        for item in c1:
            
            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
        #tableFields_verbose={ 'machinename':'machine name', 'machinedes':'machine des'}

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
            #.agg(agg_dict)
           
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



        return JsonResponse({'success':success,'tableData': tableData, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields,'tableFields_align':tableFields_align,'tableFields_summary':tableFields_summary ,'tableFields_summaryinfo':tableFields_summaryinfo}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success,}, safe=False)

def ajax_partlists(request):
    mcid = int(request.GET.get('machineid', ''))
    field=(request.GET.get('field', ''))
    if field=='':
        sql = "SELECT [Partlists].[PartlistNo], [Partlists].[PartlistDes],assylists.remarks,assylists.[optional],  [Partlists].[Type]  FROM Partlists  INNER JOIN (Machines INNER JOIN Assylists ON Machines.MachineID = Assylists.MachineID) ON Partlists.PartlistNo = Assylists.PartlistNo  where machines.machineid=%d order by partlists.partlistno" % mcid
    else:
        sql = "SELECT [Partlists].[PartlistNo], [Partlists].[PartlistDes],assylists.remarks,assylists.[optional],  [Partlists].[Type]  FROM Partlists  INNER JOIN (Machines INNER JOIN Assylists ON Machines.MachineID = Assylists.MachineID) ON Partlists.PartlistNo = Assylists.PartlistNo  where machines.machineid=%d order by partlists.%s" % (mcid,field)

    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1) > 0:
        success = 'true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = [ 'partlistno', 'partlistdes','remarks', 'type','optional']
        for item in c1:
            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
        tableFields_verbose={ 'partlistno':'partlistno', 'partlistdes':'partlistdes','remarks':'remarks', 'type':'type','optional':'status'}

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success,}, safe=False)




def ajax_partlistdetail(request):
    plno = (request.GET.get('partlistno', ''))
    sql = "SELECT    item=0,PartlistDetail.PartlistNo, MainItems.ItemID, [MainItems].[ItemCodeSuffix] + [MainItems].[ItemCodeNo] + IsNull([MainItems].[AltIndex], '') AS DrwgNo,MainItems.ItemDesig + '(' + isnull(MainItems.MatSpec,'') + '--' +  Isnull(MainItems.PatternNo,'') + ')' + '--' + ISNULL(RawMatDes.matType,'') + '(' + isnull(RawMatDes.unit,'') + ')' + '(' + ISNULL(RawMatDes.StockNo, '') + ')'+ '--' + Isnull(MainItems.ParentSec,'') AS ItemDesig, PartlistDetail.Qty, MainItems.Unit as D_Unit,status = CASE mainitems.[sc] WHEN 1 THEN 'Sub Contract' WHEN 0 THEN CASE [mainitems].[of] WHEN 1 THEN 'OF' WHEN 0 THEN 'HOM' END END,Optional = CASE [partlistdetail].[or] WHEN 1 THEN CASE [partlistdetail].[requirement] WHEN 'RF' THEN 'Required For ' + [partlistdetail].[Option] WHEN 'NRF' THEN 'Not Required For ' + [partlistdetail].[Option] END WHEN 0 THEN '' END, "
    sql = sql + " MainItems.SizeOfDrwg + '(' + convert(varchar,MainItems.NoOfDrwg) + ')' as Drwg,MainItems.Weight as wt, [MainItems].[RwItemSuffix] + [MainItems].[RwItemNo] AS RwDrwgno, MainItems.[GROUP],PartlistDetail.Remarks,   MainItems.Breadth, MainItems.Length,MainItems.HoldAl , MainItems.[Len/Piece], RawMatDes.Rate, PartlistDetail.PartDetailID,rawmatdes.stockno,rawmatdes.unit,rawmatdes.shape,rawmatdes.dia,rawmatdes.thickness,rawmatdes.weight,mainitems.matspec"
    sql = sql + " ,mainitems.[group] FROM PartlistDetail INNER JOIN MainItems ON PartlistDetail.ItemID = MainItems.ItemID LEFT OUTER JOIN RawMatDes ON MainItems.StockNo = RawMatDes.StockNo WHERE     PartlistDetail.PartlistNo = '" + plno + "' order by drwgno"

    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1) > 0:
        success = 'true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = [ 'drwgno', 'itemdesig','qty','unit','remarks', 'type','status','optional','drwg']
        for item in c1:
            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
        tableFields_verbose={ 'drwgno':'drwgno', 'itemdesig':'itemdesig','qty':'qty','unit':'unit','remarks':'remarks', 'type':'type','status':'status','optional':'optional','drwg':'drwg'}

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success,}, safe=False)



def ajax_stditems(request):
    PartID= (request.GET.get('partdetailid', ''))
    sql = "SELECT MainItemSubItem.PartdetailID, SubItems.ItemCodeSuffix + SubItems.ItemCodeNo AS Drwgno, SubItems.ItemDesig, MainItemSubItem.SubItemQty, SubItems.unit, SubItems.[Group], MainItemSubItem.Remarks, SubItems.Rate  FROM MainItemSubItem INNER JOIN SubItems ON MainItemSubItem.SubItemID = SubItems.ItemID where partdetailid=%s order by drwgno" % PartID

    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = [ 'drwgno', 'itemdesig','subitemqty','unit', 'group','remarks']
        for item in c1:
            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
        tableFields_verbose={ 'drwgno':'drwgno', 'itemdesig':'itemdesig','subitemqty':'qty','unit':'unit','remarks':'remarks', 'group':'group'}

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success}, safe=False)


def ajax_weldments(request):
    itemid= int(request.GET.get('itemid', ''))
    sql = "SELECT MainSub.MainItemId, MainSub.Item, MainSub.SubItemDesig + '(' + isnull(MainSub.SubItemMatSpec,'') + ')' + '--' +  Isnull(RawMatDes.matType,'') + '(' + isnull(RawMatDes.unit,'') + ')' + '(' + isnull( RawMatDes.StockNo,'') + ')' + '--' + isnull(MainSub.ParentSec,'') as [ItemDesignation], MainSub.SubItemQty AS Qty, MainSub.Unit as unt,  MainSub.Breadth AS Br, MainSub.Length AS Len, MainSub.HoldAl AS HA, MainSub.[Len/Piece] AS LP, [ItemSuffix] + [itemcode] AS [DrwgNo] ,rawmatdes.stockno,rawmatdes.unit,rawmatdes.shape,rawmatdes.dia,rawmatdes.thickness,rawmatdes.weight,isnull(mainsub.subitemmatspec,'0') as subitemmatspec FROM MainSub LEFT outer JOIN RawMatDes ON MainSub.StockNo = RawMatDes.StockNo Where mainitemid = %s ORDER BY MainSub.MainItemId, MainSub.Item " % itemid

    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        success='true'
        tableFields = list(c1[0].keys())
        #print(tableFields)
        formFields = [ 'item', 'itemdesignation','qty','unit', 'drwgno']
        for item in c1:
            color='default'
            item['rowcolor']=color
            for f in formFields:
                color='default'
                item['fieldcolor']={f:color}
        tableFields_verbose={ 'item':'item', 'itemdesignation':'itemdesig','qty':'qty','unit':'unit','drwgno':'drwgno'}

        return JsonResponse({'success':success,'tableData': c1, 'tableFields': tableFields, 'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields}, safe=False)
    else:
        success='false'
        return JsonResponse({'success': success}, safe=False)


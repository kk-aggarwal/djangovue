from django.shortcuts import render
from django.http import JsonResponse
import json
import pandas as pd
import datetime

from djangovue.connections import open_db_connection,dictfetchall
# Create your views here.


def Index(request):
    template = "HR/index_d.html"
    return render(request,template,context={'a':'kk'})

def ajax_wgps(request):
    field = request.GET.get('field', '')
    group = request.GET.get('group', '')

    fields = {'ticketno': {}, 'name': {}, 'section': {},
              'grade': {'verbose': 'Grade', 'align': 'center', 'summary': '1', 'summaryinfo': 'b'},
              'channel': {'verbose': 'Channel', 'align': 'right', 'summary': '1','summaryinfo': 'a'},

              'rc': {'verbose': 'RC', 'align': 'right', },
              'dobnew': {'verbose': 'DOB', 'align': 'right', },
              'dojnew': {'verbose': 'DOJ', 'align': 'right', },
              'dopnew': {'verbose': 'DOP', 'align': 'right', },
              'designation': {'verbose': 'Desig', 'align': 'right', },
              'qualification': {'verbose': 'Quali', 'align': 'right', },
              'sex': {'verbose': 'Sex', 'align': 'right', },
              'ep': {'verbose': 'ep', 'align': 'right', },
              'pw': {'verbose': 'pw', 'align': 'right', },
              'empcd': {'verbose': 'empcd', 'align': 'right', },
              }
    formFields = list(fields.keys())
    print(formFields)
    tableFields_verbose = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('verbose', k) for k in fields])}
    tableFields_align = {i: j for (i, j) in
                         zip(list(fields.keys()), [fields[k].get('align', 'center') for k in fields])}
    tableFields_summary = {i: j for (i, j) in zip(list(fields.keys()), [fields[k].get('summary', '1') for k in fields])}
    tableFields_summaryinfo = {i: j for (i, j) in
                               zip(list(fields.keys()), [fields[k].get('summaryinfo', '2') for k in fields])}
    sql = """select ticketno,b.name,to_char(nvl(section,0))||NVL(b.sec_a,'') section,grade,to_char(nvl(channel,''))||nvl(channel_alpha,'') channel,rc,seniority_no,TO_DATE(TO_CHAR(dobnew, 'MON.DD.YYYY'),'MON.DD.YYYY') dobnew,TO_DATE(TO_CHAR(dojnew, 'MON.DD.YYYY'),'MON.DD.YYYY') dojnew,TO_DATE(TO_CHAR(dopnew, 'MON.DD.YYYY'),'MON.DD.YYYY') dopnew,
    designation,qualification,abb_des,sex,
    rc,b.ep,b.pw,d.empcd
    from gddes a,wgps b,minihris c,emp_mstr d
    where a.gd=b.gd
    and
    b.gd between 0 and 99
    and
    section between 0 and 900
    and
    c.tno = b.ticketno(+) and c.tno=d.tno(+)
    order by ticketno"""
    with open_db_connection('pyrl') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    print(c1)
    if len(c1) > 0:
        success = 'true'
        tableFields = list(c1[0].keys())
        # print(tableFields)
        # formFields = [ 'machinename', 'machinedes']

        for item in c1:

            color = 'default'
            item['rowcolor'] = color
            for f in formFields:
                color = 'default'
                item['fieldcolor'] = {f: color}
        # tableFields_verbose={ 'machinename':'machine name', 'machinedes':'machine des'}

        for k in formFields[::-1]:
            print(k)
            if k=='section':
                print(k)
                sortedc1=sorted(c1,key=lambda c:'' if c[k]==None else str(c[k]))
            elif k=='channel':
                sortedc1=sorted(c1,key=lambda c:'' if c[k]==None else str(c[k]))
            elif k=='rc':
                sortedc1=sorted(c1,key=lambda c:'' if c[k]==None else str(c[k]))
            elif k=='ep':
                sortedc1=sorted(c1,key=lambda c:'' if c[k]==None else str(c[k]))
            elif k=='pw':
                sortedc1=sorted(c1,key=lambda c:'' if c[k]==None else str(c[k]))
            else:
                print('e '+k)
                sortedc1 = sorted(c1, key= lambda c: c[k] if isinstance(c[k], datetime.date) else ("" if c[k]==None else (float(str(c[k]).strip().lower()) if str(
                c[k]).strip().lower().replace('.', '', 1).isdigit() else str(c[k]).strip().lower())))
            n = 0
            for c in sortedc1:
                c['sortkey_' + k] = n
                n += 1
        tableData = sortedc1
        #tableData=c1

        if group == 'yes':

            fields = json.loads(request.GET.get('fields', ''))
            function = json.loads(request.GET.get('function', ''))
            filter = json.loads(request.GET.get('filter', ''))
            print(function)
            df = pd.DataFrame(tableData)
            if len(filter) > 0:
                f = []
                for key, value in filter.items():
                    f.append((df[key].isin(value)))
                for index, f1 in enumerate(f):
                    if index == 0:
                        filt = f1
                    else:
                        filt = (filt) & (f1)

                df = df.loc[filt]
            print(function)
            fields_sum = [key for key, value in function.items() if value == 'sum']
            agg_dict = {key: val for key, val in function.items() if val != 'group'}
            fields_group = [key for key, value in function.items() if value == 'group']
            fields_count = [key for key, value in function.items() if value == 'count']
            print(fields_group)
            # grouped_df=df.sort_values(fields_group).groupby(fields_group).agg(agg_dict)
            grouped_df = df.groupby(fields_group, as_index=False).agg(agg_dict)
            # .agg(agg_dict)

            # df_sum = grouped_df[fields_sum].sum()
            # df_count=grouped_df[fields_count].count()

            # df=pd.merge(df_sum, df_count, left_index=True, right_index=True).reset_index()
            c2 = grouped_df.to_dict('records')
            print(c2)
            formFields = fields
            for item in c2:
                for f in formFields:
                    color = 'default'
                    item['fieldcolor'] = {f: color}
            tableData = c2

            # for k in formFields[::-1]:
            # #print(k)
            #     sortedc1 = sorted(c1, key=lambda c: float(str(c[k]).strip().lower()) if str(
            #         c[k]).strip().lower().replace('.', '', 1).isdigit() else str(c[k]).strip().lower())
            #     n = 0
            #     for c in sortedc1:
            #         c['sortkey_' + k] = n
            #         n += 1
            # tableData=sortedc1
            # groupdata=grouped_df.to_html(escape=False)
            # soup = BeautifulSoup(groupdata, "html.parser")
            # for r in soup.find_all('table'):
            #    r['class'] = 'table table-bordered table-striped table-hover table-condensed compact'
            #    r['style']='width:80%'


            return JsonResponse(
                {'success': success, 'tableData': tableData, 'formFields': formFields, 'fields_group': fields_group})

        return JsonResponse({'success': success, 'tableData': tableData, 'tableFields': tableFields,
                             'tableFields_verbose': tableFields_verbose,
                             'formFields': formFields, 'tableFields_align': tableFields_align,
                             'tableFields_summary': tableFields_summary,
                             'tableFields_summaryinfo': tableFields_summaryinfo}, safe=False)
    else:
        success = 'false'
        return JsonResponse({'success': success, }, safe=False)

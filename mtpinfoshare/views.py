from django.shortcuts import render
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect

from datetime import datetime
import pandas as pd
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from djangovue.connections import open_db_connection,dictfetchall
from mtpinfoshare.forms import *
# Create your views here.

def Index(request):
    template = "mtpinfoshare/index_d.html"
    return render(request,template,context={'a':'kk'})

def HomTransacDet(request):
    drwgno=request.GET.get('text','')
    s = ""
    if drwgno is None : return s
    sql = "SELECT top 200 HomTransac.AltIndex, HomTransac.Rec, HomTransac.Issue,replace(convert(varchar(11),HomTransac.TransacDate,106),' ','-') as TransacDate,TransacDate as dated, HomTransac.TransacDes, HomTransac.TransID, HomTransac.DrwgNo, AreaCodes.Des AS Tdes, AreaCodes1.Des AS Fdes,rito,rifrom,HomTransac.dno,docdes.des,won,wrtno FROM HomTransac INNER JOIN AreaCodes ON HomTransac.RITo = AreaCodes.AreaCode INNER JOIN AreaCodes AreaCodes1 ON HomTransac.RIFrom = AreaCodes1.AreaCode LEFT OUTER JOIN dbo.DocDes ON dbo.HomTransac.dno = dbo.DocDes.dno where drwgno='" + drwgno + "' and status !='d' order by dated desc ,transid desc"
    #cursor = con.cursor()
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    if len(c1) > 0:
        
        s = s + BalanceHOM(drwgno)
        s = s + "<TABLE class=""tabl tabl-sm"" BORDER=1 BGCOLOR=#ffffff CELLSPACING=0><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=6 color=#800040><B>Transactions Detail for the Drawing No=" + drwgno + "</B></font></CAPTION></FONT>"

        s = s + "<THEAD>"
        s = s + "<TR>"

        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Date</FONT></TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Index</FONT></TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Description</FONT></TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Work Order No</FONT></TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Warrant</FONT></TH>"

        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Receipt</FONT></TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Issue</FONT></TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>To</FONT></TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>From</FONT></TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Doc.No.</FONT></TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Doc.Description</FONT></TH>"
        s = s + "</TR>"
        s = s + "</THEAD>"
        s = s + "<TBODY>"

        for item in c1:
            if item["rec"] > 0 and item["rito"] == 0:
                s = s + "<TR bgcolor=#D7F0FD VALIGN=TOP>"
            elif  item["rito"] == -3 and item["rifrom"] == 0:
                s = s + "<TR bgcolor=#FDDED7 VALIGN=TOP>"
            elif item["rec"] > 0 and item["rito"] == 3:
                s = s + "<TR bgcolor=#CAFFCA VALIGN=TOP>"
            else:
                s = s + "<TR bgcolor=#FFFFBF VALIGN=TOP>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["transacdate"] is None else str(item["transacdate"])) + "<BR></FONT></TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["altindex"] is None else str(item["altindex"])) + "<BR></FONT></TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["transacdes"] is None else str(item["transacdes"])) + "<BR></FONT></TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["won"] is None else str(item["won"])) + "<BR></FONT></TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["wrtno"] is None else str(item["wrtno"])) + "<BR></FONT></TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["rec"] is None else str(item["rec"])) + "<BR></FONT></TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["issue"] is None else str(item["issue"])) + "<BR></FONT></TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["tdes"] is None else str(item["tdes"])) + "<BR></FONT></TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["fdes"] is None else str(item["fdes"])) + "<BR></FONT></TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["dno"] is None else str(item["dno"])) + "<BR></FONT></TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["des"] is None else str(item["des"]))+ "<BR></FONT></TD>"
            s = s + "</TR>"

        # If item["rito"] = -3 And item["rifrom"] = 0 Then
        #   subHomTransDet item["TransID"]

        
        return JsonResponse(
                {'result': [s], })

def BalanceHOM(drwgno):

    sql="select balance from homstockbalav where drwgno='" + drwgno + "'"
    #cursor = con.cursor()
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        BalanceHOM =  "<p><font size=4 color=""Blue"">Physical Balance: "+ str(c1[0]["balance"]) +"</font></p>"
    else:
        BalanceHOM = "<p><font size=4 color=""Blue"">Physical Balance: 0</font></p>"

    return  BalanceHOM

def balancebom(request):
    stockno=request.GET.get('text','')
    result=[]
    result.append("<p>" + balancestockstore(stockno)+"</p>" + "<p>" +findDes(stockno)+ "</p><div>" + meDetail(stockno)+"</div>")
    return JsonResponse({'result':result})
def findDes(stockno):
    if stockno is None: return ''
    if stockno[:1] == "0":
        raw = True
    elif stockno[:1] ==  "9" and stockno[1:2] ==  "0":
        raw = True
    else:
        raw = False
    if raw == False:
        sql = "select des from desmaster where stockno='" + stockno + "' and desid=0"
    #cursor = con.cursor()
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
        if len(c1) > 0:
            findDes = c1[0]['des']
        else:
            findDes = "Either stockno is wrong or description not available.Contct Mat. Engg.!"
    if raw == True:
        sql = "select mattype as des from rawmatdes where stockno='" + stockno + "'"
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
        if len(c1) > 0:
            findDes = c1[0]['des']
        else:
            findDes = "Either stockno is wrong or description not available.Contct Mat. Engg.!"
    return findDes
def balancestockstore(stockno):
    s = ""
    if stockno == "" or stockno is None: return s

    sql = "select isnull((sum(qtyin)-sum(qtyout)),0)+ isnull((select isnull(qty,0) from stopeningbal where yearid=(select yearid from stcurrentyear) and stockno='" + stockno + "' and [status]=1),0) as balance from sttransactions where yearid=(select yearid from stcurrentyear) and stockno='" + stockno + "' and status !='d'"
    #cursor = con.cursor()
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    item=c1[0]
    print(item['balance'])
    if len(c1) > 0:
        BalanceStockStore =("The balance is not available. Pl. contact STORE" if item["balance"] is None else ("Available balance in (Store) for stock no: " + str(stockno) +"= "+ str(item["balance"])))

    else:
        BalanceStockStore = "The balance is not available. Pl. contact Store"

    return BalanceStockStore
def meDetail(stk):
    sql = "select top 50 trandid,rec,issue,des,dated,dno,mctype,mcno from mattransac where stockno='%s' and status !='d' order by dated desc"%stk
    #cursor=con.cursor()
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1) > 0:
        s = '' + " " + "<TABLE BORDER=2 bordercolor=#6C0036 BGCOLOR=#ffffff CELLSPACING=0><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=4 color=#800040><B>ME transactions(last 50 enteries)</B></font></CAPTION></FONT>"

        s = s + " " + "<THEAD>"
        s = s + " " + "<TR>"

        s = s + " " + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Dated</FONT></TH>"
        s = s + " " + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Description</FONT></TH>"
        s = s + " " + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Demand note</FONT></TH>"

        s = s + " " + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Received Qty</FONT></TH>"
        s = s + " " + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Issue Qty</FONT></TH>"
        s = s + " " + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Machine type</FONT></TH>"
        s = s + " " + "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Machine no</FONT></TH>"
        s = s + " " + "</TR>"
        s = s + " " + "</THEAD>"
        s = s + " " + "<TBODY>"
        for item in c1:
            c = "#FFFFBF" if item["rec"] == 0 else "#EED7C1"
            s = s + " " + "<TR bgcolor=" + c + " VALIGN=TOP>"
            s = s + " " + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["dated"] is None else str(item["dated"])) + "<BR></FONT></TD>"
            s = s + " " + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["des"] is None else item["des"]) + "<BR></FONT></TD>"
            s = s + " " + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["dno"] is None else str(item["dno"])) + "<BR></FONT></TD>"
            s = s + " " + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["rec"] is None else str(round(item["rec"],3))) + "<BR></FONT></TD>"
            s = s + " " + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["issue"] is None else str(round(item["issue"],3))) + "<BR></FONT></TD>"
            s = s + " " + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["mctype"] is None else (item["mctype"])) + "<BR></FONT></TD>"
            s = s + " " + "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["mcno"] is None else str(item["mcno"])) + "<BR></FONT></TD>"
            s = s + " " + "</TR>"
        s = s + " " + "</TBODY>"
        s = s + " " + "<TFOOT></TFOOT>"
        s = s + " " + "</TABLE>"
        return s
    else:
        return ''
def searchdatabase(request):
    drwgno=request.GET.get('text','')
    result=[searhresults(drwgno)]
    return JsonResponse({'result':result})
def searhresults(drwgno):
    s=""
    
    if drwgno=="" or drwgno is None:return s
    #con = pyodbc.connect('DRIVER={SQL Server};SERVER=dc;DATABASE=edssql;Integrated Security=true')
    #cursor = con.cursor()
    sfx = ''.join(c for c in drwgno if not c.isnumeric()).lower()
    
    
    
    if sfx in ('a','b','c','d','e','f','g','h','skp','sk'):
        sql = "select * from mainitems where mainitems.itemcodesuffix + mainitems.itemcodeno = " + " '" + drwgno + "'"
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
        if len(c1) > 0:
            for item in c1:
                desig = item["itemdesig"]
                NoDrwg = ("" if item["noofdrwg"]is None else item["noofdrwg"])
                sizeDrwg =("" if item["sizeofdrwg"]is None else item["sizeofdrwg"])
                catcode = ("" if (item["group"]is None or item["group"] == "") else item["group"])
                DesignUpdated =("" if item["date_updated_d"]is None else item["date_updated_d"])
                PlanUpdated = ("" if item["date_updated_p"]is None else item["date_updated_p"])
                RwDrwg = ("" if item["rwitemsuffix"]is None else item["rwitemsuffix"]+("" if item["rwitemno"]is None else item["rwitemno"]))
                patternNo = ("" if item["patternno"]is None else item["patternno"])
                secno = ("" if item["parentsec"]is None else item["parentsec"])
                unit = item["unit"]
                altindex = ("" if item["altindex"]is None else item["altindex"])
                matspec =("" if item["matspec"]is None else item["matspec"])
                dateCreated = ("" if item["date_inserted"]is None else item["date_inserted"])
                status =  ("Sub Contract" if item["sc"] else ("Order Finish" if item["of"] else "In House Manufacture"))
                if status == "Sub Contract" or status == "Order Finish":
                    sql = "select Stockno,rate from desmaster where rtrim(ltrim(desmaster.itemcodesuffix)) + ltrim(rtrim(desmaster.itemcodeno))='" + drwgno + "' and desmaster.desid=0"
                    with open_db_connection('edssql') as cursor:
                        cursor.execute(sql)
                        c2 = dictfetchall(cursor)

                    Dimensions = ""
                    RawMat = ""
                    if len(c2) > 0:
                        stkno =','.join([("" if s['stockno'] is None else s['stockno']) for s in c2])
                        AppRate = ("" if c2[0]["rate"]is None else c2[0]["rate"])
                    else:
                        stkno = "#Could not be found in DesMaster#"
                        AppRate = "#Could not be found in DesMaster#"

                else:
                    sql = "select mattype,stockno,rate from rawmatdes where stockno='" + str(item["stockno"]) + "'"
                    with open_db_connection('edssql') as cursor:
                        cursor.execute(sql)
                        c3 = dictfetchall(cursor)
                    Dimensions = str(item["breadth"]) + "_" + str(item["length"]) + "_" + str(item["holdal"]) + "_" + str(item["len/piece"])

                    if len(c3) > 0:
                        item = c3[0]
                        RawMat = ("" if item["mattype"]is None else item["mattype"])
                        stkno = ("" if item["stockno"]is None else item["stockno"])
                        AppRate = ("" if item["rate"]is None else item["rate"])
                    else:
                        RawMat = "#Could not be found in RawMatTypes table#"
                        stkno = "#Could not be found in RawMatTypes table#"
                        AppRate = "#Could not be found in RawMatTypes table#"
        else:return s
    elif sfx in('m','n','np','p','mp','u','s'):

        sql = "select * from subitems where subitems.itemcodesuffix + subitems.itemcodeno = " + " '" + drwgno + "'"
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c4 = dictfetchall(cursor)

        if len(c4) > 0:
            item = c4[0]
            desig = item["itemdesig"]
            NoDrwg = ""
            sizeDrwg = ""
            catcode = ("" if item["group"]is None else item["group"])
            DesignUpdated = ("" if item["date_updated_d"]is None else item["date_updated_d"])
            PlanUpdated =  ("" if item["date_updated_p"]is None else item["date_updated_p"])
            RwDrwg = ""
            patternNo = ""
            secno = ""
            unit = ("" if item["unit"]is None else item["unit"])
            altindex = "#na#"
            matspec = "#na#"
            dateCreated = ("" if item["date_inserted"]is None else item["date_inserted"])
            status = "Order Finish"
            if status == "Sub Contract" or status == "Order Finish":
                sql = "select Stockno,rate from desmaster where rtrim(ltrim(desmaster.itemcodesuffix)) + ltrim(rtrim(desmaster.itemcodeno))='" + drwgno + "' and desmaster.desid=0"
                with open_db_connection('edssql') as cursor:
                    cursor.execute(sql)
                    c5 = dictfetchall(cursor)

                Dimensions = ""
                RawMat = ""
                if len(c5) > 0:
                    stkno = ','.join([("" if s['stockno'] is None else s['stockno']) for s in c5])
                    AppRate = round((0 if c5[0]["rate"]is None else c5[0]["rate"]),2)
                else:
                    stkno = "#Could not be found in DesMaster#"
                    AppRate = "#Could not be found in DesMaster#"
        else:return s
    else: return s
    
    s=s+"<TABLE BORDER=1 BGCOLOR=#ffffff CELLSPACING=0><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=2 color=#006A00<B>DRAWING NO=" + drwgno + "</B></font></CAPTION></FONT>"
    s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Designation<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + desig + "<BR></FONT></TD>"
    s=s+"</tr>"
    s=s+"</TABLE>"
    s=s+"<TABLE BORDER=1 BGCOLOR=#ffffff CELLSPACING=0>"
    s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Status<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + status + "<BR></FONT></TD>"
    
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Stock No<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + stkno + "<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Cat Code<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(catcode) + "<BR></FONT></TD>"
    s=s+"</tr>"
    s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Raw Material<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + RawMat + "<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Dimension<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + Dimensions + "<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>App. Rate<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(AppRate) + "<BR></FONT></TD>"
    
    s=s+"</tr>"
    s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Rework Drawing no<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + RwDrwg + "<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Pattern No<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + patternNo + "<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Alt. Index<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + altindex + "<BR></FONT></TD>"
    s=s+"</tr>"
    s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Drawing Size<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + sizeDrwg + "<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>No of Drawings<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(NoDrwg) + "<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Parent Sec.<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + secno + "<BR></FONT></TD>"
    s=s+"</tr>"
    s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Date Created<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(dateCreated) + "<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Date Updated(Design)<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(DesignUpdated) + "<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Date Updated(Planning)<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(PlanUpdated) + "<BR></FONT></TD>"
    s=s+"</tr>"
    s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Unit<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + unit + "<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0 bgcolor=#C7EDFA ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Mat. Spec.<BR></FONT></TD>"
    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + matspec + "<BR></FONT></TD>"
    s=s+"</tr>"
    s=s+"</TABLE>"
    sql=""
    if sfx in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'skp', 'sk'):
        sql = "SELECT Machines.MachineName, Partlists.PartlistDes, Assylists.PartlistNo, MainItems.ItemCodeSuffix + MainItems.ItemCodeNo as drwgno, MainItems.ItemDesig, Sum(PartlistDetail.Qty) AS itemQty,  isnull(PartlistDetail.[Option],'') as [option]  FROM MainItems INNER JOIN ((Partlists INNER JOIN (Machines INNER JOIN Assylists ON Machines.MachineID = Assylists.MachineID) ON Partlists.PartlistNo = Assylists.PartlistNo) INNER JOIN PartlistDetail ON Assylists.PartlistNo = PartlistDetail.PartlistNo) ON MainItems.ItemID = PartlistDetail.ItemID Where mainitems.itemcodesuffix + mainitems.itemcodeno = " + " '" + drwgno + "'" + " GROUP BY Machines.MachineName, Partlists.PartlistDes, Assylists.PartlistNo, MainItems.ItemCodeSuffix + MainItems.ItemCodeNo, MainItems.ItemDesig, PartlistDetail.Unit, PartlistDetail.[Option], Machines.MachineID "
    if sfx in ('m', 'n', 'np', 'p', 'mp', 'u', 's'):
        sql = "SELECT Machines.MachineName,Assylists.PartlistNo,Partlists.PartlistDes,MainItems.ItemCodeSuffix + MainItems.ItemCodeNo as drwgno,mainitems.itemdesig, Sum(MainItemSubItem.SubItemQty) AS ItemQty,isnull(PartlistDetail.[Option],'') as [option]   FROM (Partlists INNER JOIN (Machines INNER JOIN Assylists ON Machines.MachineID = Assylists.MachineID) ON Partlists.PartlistNo = Assylists.PartlistNo) INNER JOIN ((PartlistDetail INNER JOIN MainItems ON PartlistDetail.ItemID = MainItems.ItemID) INNER JOIN (SubItems INNER JOIN MainItemSubItem ON SubItems.ItemID = MainItemSubItem.SubItemID) ON PartlistDetail.PartDetailID = MainItemSubItem.PartdetailID) ON Assylists.PartlistNo = PartlistDetail.PartlistNo  Where subitems.itemcodesuffix + subitems.itemcodeno = " + " '" + drwgno + "'" + " GROUP BY Machines.MachineName,Assylists.PartlistNo,Partlists.PartlistDes,MainItems.ItemCodeSuffix +MainItems.ItemCodeNo,mainitems.itemdesig,PartlistDetail.[Option]"

    if sql == "":exit
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c = dictfetchall(cursor)
    
    if len(c)== 0:
        s=s+"<h3><font face=""Arial"">There are no entry in the database for the requested drawing no=" + drwgno + "</font></h3>"
        s=s+ "</body>"
        s=s+ "</html>"
        exit
    

    s=s+"<TABLE BORDER=1 BGCOLOR=#ffffff CELLSPACING=0><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=4 color=#006A00<B>DATABASE SEARCH RESULTS FOR DRAWING NO=" + drwgno + "</B></font></CAPTION></FONT>"
    
    s=s+"<THEAD>"
    s=s+"<TR >"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Mavhine Name No</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Partlistno</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Partlist Des.</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Drawing no</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Designation</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Quantity</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Option</FONT></TH>"
    s=s+"</TR>"
    s=s+"</THEAD>"
    s=s+"<TBODY>"
    
    for item in c:
        s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
        s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["machinename"] + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["partlistno"] + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["partlistdes"] + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["drwgno"] + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["itemdesig"] + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(item["itemqty"]) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["option"] + "<BR></FONT></TD>"
        s=s+"</TR>"

    
    s=s+"</body>"
    s=s+"</html>"
    #print(s)
    return s
def dailymislipitems(request):
    date = request.GET.get('text','')
    
    dated =  datetime.strptime(date, '%d-%m-%Y').strftime("%d-%b-%Y")

    
    return JsonResponse({'result': [resultsmislipitems(dated)]})

def resultsmislipitems(dated):


    sql = "SELECT     TOP 100 PERCENT dbo.MiSlip.FinYear, dbo.MiSlip.MatGrp, dbo.MiSlip.MiSlipNo, dbo.MiSlip.MiSlipDate, dbo.MiSlip.RecDBy, dbo.MiSlip.Note, dbo.MiSlip.Pono, dbo.MiSlip.Mprno, dbo.MiSlip.SuppName, dbo.MislipDet.StocKNo, dbo.MislipDet.Des, dbo.MislipDet.Unit, dbo.MislipDet.QtyRecd,dbo.InspectedItems.QtyAccepted"
    sql = sql + " FROM         dbo.MiSlip INNER JOIN dbo.MislipDet ON dbo.MiSlip.FinYear = dbo.MislipDet.FinYear AND dbo.MiSlip.MatGrp = dbo.MislipDet.MatGrp AND dbo.MiSlip.MiSlipNo = dbo.MislipDet.MiSlipNo LEFT OUTER JOIN dbo.InspectedItems ON dbo.MislipDet.DetailId = dbo.InspectedItems.DetailId WHERE     dbo.MiSlip.MiSlipDate = '" + str(dated) + "' AND dbo.MiSlip.St_Auth = 1 ORDER BY dbo.MislipDet.StocKNo"
    #cursor = conInStr.cursor()
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        df = pd.DataFrame(c1)
        df['MislipNo']=df.apply(lambda row:row.finyear+'/'+str(row.matgrp)+'-'+str(row.mislipno),axis=1)
        df['qtyAccepted']=df.apply(lambda row:"Unsder Insp." if row['qtyaccepted'] is None else row['qtyaccepted'],axis=1)
        #df['PoNo']=str(df['mprno'])+'/'+str(df['pono'])
        df['PoNo'] = df.apply(lambda row:row.mprno+ '/' + str(row.pono),axis=1)
        df = df[['stockno','des','unit','qtyrecd','qtyAccepted','MislipNo','PoNo']]

        df.columns = ['Stock No','Description','Unit','Received Qty','Accepted Qty','MI Slip No','PO Ref']

        #df['edit'] = "<a href='/mislipedit/?WCI=" + df.apply(lambda row: row.finyear + '_' + str(row.matgrp) + '_' + str(row.mislipno), axis=1) + "'>edit</a>"
        s=df.to_html(na_rep="0")
        s=s.replace("<tr","<TR VALIGN=TOP bgcolor=#FFFFBF")
        s = s.replace("<th", "<th BGCOLOR =  #c0c0c0 BORDERCOLOR=#000000")

        return s

    else:
        return "<P>No Item received so far !"

def oplayout(request):
    drwgno=request.GET.get('text','')
    itemno=request.GET.get('itemno','')
    result=[]
    if itemno=="":
        sql = "SELECT drwgno,item=0,itemdesig,matspec,itemid from mainitemsview where drwg='"+drwgno +"'"
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            rsMain = dictfetchall(cursor)
        if len(rsMain)>0:
            url=request.build_absolute_uri(reverse('oplayout'))+"?text="+ rsMain[0]['drwgno']+ "&itemno=0"
            result.append({'apiurl':url,'inputtext':rsMain[0]['drwgno']+", "+ rsMain[0]['itemdesig']+", "+str(rsMain[0]['item'])})
            #result.append("<a href="+ url +" target='_blank'><p>"+rsMain[0]['drwgno']+", "+ rsMain[0]['itemdesig']+", "+str(rsMain[0]['item'])+ "</p></a>")
            
            sql = "SELECT drwgno='" + rsMain[0]['drwgno']+ "',item,subitemdesig from mainsubview where mainitemid=" + str(rsMain[0]['itemid']) +" order by item"
            with open_db_connection('edssql') as cursor:
                cursor.execute(sql)
                rs = dictfetchall(cursor)
            if len(rs)>0:
                for item in rs:
                    url=request.build_absolute_uri(reverse('oplayout'))+"?text="+ rsMain[0]['drwgno']+ "&itemno="+ str(item['item'])
                    result.append({'apiurl':url,'inputtext':rsMain[0]['drwgno']+", "+ item['subitemdesig']+", "+str(item['item'])})
           
                    #result.append("<a href="+ url +" target='_blank'><p>"+item['drwgno']+", "+ item['subitemdesig']+", "+item['item']+ "</p></a>")

        else:
            result="<p>There are no entry in the database for the requested drawing no</p>"


        return JsonResponse({'result':result})
    else:
        result=[opllayoutresults(drwgno,itemno)]
        #return HttpResponse(result)
        return JsonResponse({'result':result})
   

        

def opllayoutresults(drwgno,itemno):
    print(itemno)
    if drwgno=='':return ''
    if itemno == '0':
        sqlMain = "select itemdesig,mat from mainitemsview where drwgno='%s'"%drwgno
        with open_db_connection('edssql') as cursor:
            cursor.execute(sqlMain)
            rsMain = dictfetchall(cursor)
    else:
        sqlMain = "select itemid from mainitemsview where drwgno='%s'"%drwgno
        with open_db_connection('edssql') as cursor:
            cursor.execute(sqlMain)
            Rsw = dictfetchall(cursor)
        m = Rsw[0]['itemid']
        sqlMain = "SELECT subitemdesig as itemdesig,mat from mainsubview where mainitemid=%s and item=%s"%(m,itemno)
        with open_db_connection('edssql') as cursor:
            cursor.execute(sqlMain)
            rsMain = dictfetchall(cursor)

    sql = "SELECT (suffix + itemcode) as drwgno,pbasis,product,item FROM oplmain where (suffix + itemcode)='%s' and item=%s"%(drwgno,itemno)
    with open_db_connection('opllayout') as cursor:
        cursor.execute(sql)
        rsOP = dictfetchall(cursor)
    s=''


    s=s+"<TABLE  BORDER=1 BGCOLOR=#ffffff CELLSPACING=0><CAPTION>Operation Layout</CAPTION>"

    s=s+"<THEAD>"
    s=s+"<TR >"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Drwgno</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Item</FONT></TH>"

    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Designation</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Material</FONT></TH>"

    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>PRoduct Base</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Product</FONT></TH>"

    s=s+"</TR>"
    s=s+"</THEAD>"
    s=s+"<TBODY>"

    if len(rsOP)>0:
        for item in rsOP:
            s=s+"<TR VALIGN=TOP bgcolor=#75BAFF>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["drwgno"] + "<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +  str(item["item"]) + "<BR></FONT></TD>"

            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +  rsMain[0]["itemdesig"] + "<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +  rsMain[0]["mat"] + "<BR></FONT></TD>"

            s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +  str(item["pbasis"]) + "<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +  str(item["product"]) + "<BR></FONT></TD>"

            s=s+"</TR>"
            sqlMain = "select itemid from mainitemsview where drwgno='%s'"%drwgno
            with open_db_connection('edssql') as cursor:
                cursor.execute(sqlMain)
                Rsw = dictfetchall(cursor)
            m = Rsw[0]['itemid']
            sqlMain = "Select * from mainsub where mainitemid=%s  order by item"%m
            with open_db_connection('edssql') as cursor:
                cursor.execute(sqlMain)
                Rsw = dictfetchall(cursor)
            if len(Rsw)>0 and itemno==0:
                for item in Rsw:
                    s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
                    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + "" + "<BR></FONT></TD>"
                    s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + Rsw["item"] + "<BR></FONT></TD>"
                    s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + Rsw["subitemdesig"] + "<BR></FONT></TD>"
                    s=s+"</TR>"
            s=s+OplOperations(drwgno, int(itemno))
    else:
        s="<p>Nothing is returned! Check Drawing No ?</p>"
    s=s+"</TBODY>"
    s=s+"<TFOOT></TFOOT>"
    s=s+"</TABLE>"

    return s


def OplOperations(drwgno, itemno ):
    s=''

    sqlOPR = "select * from oploperation where (suffix + itemcode)='%s' and item=%s order by opno "%(drwgno,itemno)
    with open_db_connection('opllayout') as cursor:
        cursor.execute(sqlOPR)
        rsOPR = dictfetchall(cursor)
    print(rsOPR)
    #s=s+ "<TABLE BORDER=1 BGCOLOR=#ffffff CELLSPACING=0><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=6 color=#006A00<B></B></font></CAPTION></FONT>"
    s=s+ "<THEAD>"
    s=s+ "<TR >"
    s=s+ "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Operation</FONT></TH>"
    s=s+ "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Machine No</FONT></TH>"
    s=s+ "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Machine Des</FONT></TH>"
    s=s+ "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Sec No</FONT></TH>"
    s=s+ "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>TS</FONT></TH>"
    s=s+ "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>TO</FONT></TH>"

    s=s+ "</TR>"
    s=s+ "</THEAD>"
    #s=s+ "<TBODY>"
    for item in rsOPR:
        s=s+ "<TR VALIGN=TOP bgcolor=#18D3CF>"
        s=s+ "<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(round(item["opno"],2)) + "<BR></FONT></TD>"
        s=s+ "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(item["mcno"]) + "<BR></FONT></TD>"
        s=s+ "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["machinedes"] + "<BR></FONT></TD>"
        s=s+ "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(item["secno"]) + "<BR></FONT></TD>"
        s=s+ "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(round(item["ts"],3))+ "<BR></FONT></TD>"
        s=s+ "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(round(item["to"],3)) + "<BR></FONT></TD>"

        s=s+ "</TR>"
        s=s+oplDes( drwgno, itemno, item["opno"])

    #s=s+ "</TBODY>"
    #s=s+ "<TFOOT></TFOOT>"
    #s=s+ "</TABLE>"
    return s
def oplDes(drwgno,itemno,opno):
    s=''
    sqlDES = "select * from opldes where (suffix + itemcode)='%s' and item=%s and opno=%s order by sno"%(drwgno,itemno,opno)
    with open_db_connection('opllayout') as cursor:
        cursor.execute(sqlDES)
        rsDES = dictfetchall(cursor)
    tools = getToolsstr(drwgno, itemno, opno)

    if tools !="":
        s=s+ "<TR VALIGN=TOP bgcolor=#EEC462>"

        s=s+ "<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + tools + "<BR></FONT></TD>"
        s=s+ "</TR>"

    for item in rsDES:
        s=s+ "<TR VALIGN=TOP bgcolor=#FFFFBF>"
        s=s+ "<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["description"] + "<BR></FONT></TD>"
        s=s+ "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["remarks"] + "<BR></FONT></TD>"

        s=s+ "</TR>"
    return s

def getToolsstr(drwgno, itemno, opno):
    getToolsstr=''
    sqlTL = "select * from opltools where (suffix + itemcode)='%s' and item=%s and opno=%s"%(drwgno,itemno,opno)
    with open_db_connection('opllayout') as cursor:
        cursor.execute(sqlTL)
        rsTL = dictfetchall(cursor)
    for item in rsTL:
        getToolsstr = getToolsstr + item["spltools"] + ("" if (item["remarks"] is None or item["remarks"] =="") else ":" + item["remarks"] + ",")
    return getToolsstr

def prodprogram(request):
    s=''
    #cursor = con.cursor()
    sql = "SELECT m,[month],[year] FROM [prodprogram]  group by m,[month],[year] order by [month]"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)>0:
        s=s+"<HTML>"
        s=s+"<HEAD>"
        s=s+"<META HTTP-EQUIV=""Content-Type"" CONTENT=""text/html;charset=windows-1252"">"
        s=s+"<TITLE>Production Program</TITLE>"
        s=s+"</HEAD>"
        s=s+"<BODY bgcolor=#FFB7B7>"
        s=s+"<TABLE BORDER=1 BGCOLOR=#ffffff CELLSPACING=0><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=6 color=#006A00<B>Monthly Prod Program</B></font></CAPTION></FONT>"
        s=s+"<THEAD>"
        s=s+"<TR >"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Fin. Year</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Month</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Machine No</FONT></TH>"
        s=s+"</TR>"
        s=s+"</THEAD>"
        s=s+"<TBODY>"
        for item in c1:
            s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +item[ "year"]+ "<BR></FONT></TD>"
            s=s+"</TR>"


            s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000><BR></FONT></TD>"

            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +str(item["m"])+ "<BR></FONT></TD>"
            s=s+"</TR>"
            s=s+MachineNos (item["month"],request)

        s=s+"</TBODY>"
        s=s+"<TFOOT></TFOOT>"
        s=s+"</TABLE>"
        s=s+"</BODY>"
        s=s+"</HTML>"
        return JsonResponse({'result':[s]})
def MachineNos(month,request):
    s=''
    sql = "SELECT machine,machineid,machineno FROM [prodprogram] where [month]=%s order by machine"%month
    #cursor = con.cursor()
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1) > 0:
        for item in c1:

            s=s+"<TR bgcolor=#83BCA0 VALIGN=TOP>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000><BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000><BR></FONT></TD>"

            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["machine"] is None else item["machine"]) + "<BR></FONT></TD>"
            url=request.build_absolute_uri(reverse('bom'))+"?WCI="+ str(item["machineid"])+ "," + str(item["machineno"])
            s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=arial COLOR=#000000><a target='_blank' href='" +url+ "'>Click for bom</a><BR></FONT></TD>"

            s=s+ "</TR>"
    return s

def bom(request):
    s=''
    mcid,mcno=request.GET.get('WCI').split(',')
    sql = "SELECT TOP 100 PERCENT Machine, [Group], drwgno, desig, sum(qty) as qty, unit,bal,max(dateupdated) as lastUpdated From dbo.StdItemsView WHERE (machineid =%s) AND (machineno =%s) group by Machine, [Group], drwgno, desig, unit,bal ORDER BY [Group], drwgno"%(mcid,mcno)
    #cursor = con.cursor()
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1) > 0:
        s=s+"<HTML>"
        s=s+"<HEAD>"
        s=s+"<META HTTP-EQUIV=""Content-Type"" CONTENT=""text/html;charset=windows-1252"">"
        s=s+"<TITLE>Bill of materials</TITLE>"
        s=s+"</HEAD>"
        s=s+"<BODY bgcolor=#FFB7B7>"
        s=s+"<TABLE BORDER=1 BGCOLOR=#ffffff CELLSPACING=0><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=5 color=#804040<B>Bill Of Materials(Last Updated On:" +str(c1[0]["lastupdated"]) + ")</B></font></CAPTION></FONT>"
        s=s+"<THEAD>"
        s=s+"<TR >"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Machine</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Cat. Code</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Drawing no</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Designation</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Quantity</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Unit</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Stock balance</FONT></TH>"
        s=s+"</TR>"
        s=s+"</THEAD>"
        s=s+"<TBODY>"



        n = 1

        s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
        s=s+ "<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +c1[0]["machine"]+ "<BR></FONT></TD>"
        s=s+"</TR>"
        catcode = ("" if c1[0]["group"]is None else c1[0]["group"])
        for item in c1:
            if(n / 2) == int((n / 2)):
                col = "#F8D8CD"
            else:
                col = "#FFFFBF"

            s=s+"<TR VALIGN=TOP bgcolor=" + col + ">"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>&nbsp<BR></FONT></TD>"
            if catcode != ("" if item["group"] is None else item["group"]):
                s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["group"]is None else item["group"]) + "<BR></FONT></TD>"
                catcode = ("" if item["group"]is None else item["group"])
            else:
                s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>&nbsp<BR></FONT></TD>"

            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +item["drwgno"]+ "<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +item["desig"]+ "<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(round(item["qty"],2)) +"<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +item["unit"]+ "<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=left><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +('0' if item["bal"]is None else str(item["bal"]))+ "<BR></FONT></TD>"
            s=s+"</TR>"
            n = n + 1

        s=s+"</TBODY>"
        s=s+"<TFOOT></TFOOT>"
        s=s+"</TABLE>"
        s=s+"</BODY>"
        s=s+"</HTML>"
        return HttpResponse(s)
    else:
        return HttpResponse("<h3>Not av. currently, contact admin</h3>")

def pendingMislips(request):
    s=''
    sql = "SELECT     TOP 100 PERCENT dbo.MiSlip.FinYear, dbo.MiSlip.MatGrp, dbo.MiSlip.MiSlipNo, replace(convert(varchar(11),mislipDate,106),' ','-') as mislipdate, dbo.MiSlip.Pono, dbo.MiSlip.St_Auth, dbo.MiSlip.Ins_Auth, dbo.MiSlip.ME_auth, dbo.MiSlip.MSt_auth, dbo.MIslipBills.value,dbo.MIslipBills.EdAmount, dbo.MIslipBills.EduCess, dbo.MIslipBills.BillType,dbo.MIslipBills.BillNo, edssql.dbo.ValidPOView.PayTerms,PendingIn=case st_auth when 0 then 'Incoming' else case ins_auth when 0 then 'Inspection' else case me_auth when 0 then 'Mat. engg' else case mst_auth when 0 then 'Store' end end end end"
    sql = sql + ",replace(convert(varchar(11),st_auth_date,106),' ','-') as st_auth_date,replace(convert(varchar(11),ins_auth_date,106),' ','-') as ins_auth_date,replace(convert(varchar(11),me_auth_date,106),' ','-') as me_auth_date,replace(convert(varchar(11),mst_auth_date,106),' ','-') as mst_auth_date,'MN/'+dbo.MiSlip.finyear+'/' +cast(dbo.MiSlip.matgrp as varchar)+'-' + cast(dbo.MiSlip.mislipno as varchar) as mnNo FROM         dbo.MiSlip LEFT OUTER JOIN edssql.dbo.ValidPOView ON dbo.MiSlip.Pono = edssql.dbo.ValidPOView.PONo LEFT OUTER JOIN dbo.MIslipBills ON dbo.MiSlip.FinYear = dbo.MIslipBills.FinYear AND dbo.MiSlip.MatGrp = dbo.MIslipBills.MatGrp AND dbo.MiSlip.MislipNo = dbo.MIslipBills.MislipNo"
    sql = sql + " WHERE      (dbo.MiSlip.MSt_auth = 0) AND (dbo.MiSlip.FinYear = '2018-2019' and mislip.matgrp not in(16,19)) ORDER BY dbo.mislip.mislipdate,dbo.MiSlip.MatGrp, dbo.MiSlip.MiSlipNo"
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    s=s+"<HTML>"
    s=s+"<HEAD>"
    s=s+"<META HTTP-EQUIV=""Content-Type"" CONTENT=""text/html;charset=windows-1252"">"
    s=s+"<TITLE>Pending MI Slips</TITLE>"
    s=s+"</HEAD>"

    s=s+"<TABLE BORDER=1 BGCOLOR=#ffffff CELLSPACING=0 width=100%><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=4 color=#006A00<B>Pending MI Slips</B></font></CAPTION></FONT>"

    s=s+"<THEAD>"
    s=s+"<TR >"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>MI Slip No</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Pending In</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Mi Slip date</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Store Auth</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Inspected</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Scrutnized</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Stock charged</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Value</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Ed. amount</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Edu. cess</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Bill Type</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Bill No</FONT></TH>"
    s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Pay Terms</FONT></TH>"

    s=s+"</TR>"
    s=s+"</THEAD>"
    s=s+"<TBODY>"

    n = 1

    for item in c1:
        if item["pendingin"] == "Incoming":
            RowColor = "#ccBb41"
        elif item["pendingin"] == "Inspection":
            RowColor = "#FFB871"
        elif item["pendingin"] == "Mat. Engg":
            RowColor = "#B9E9FF"
        elif item["pendingin"] == "Store":
            RowColor = "#FFD2D2"
        else:
            RowColor = "#FFFFC1"

        s=s+"<TR VALIGN=TOP bgcolor=" + RowColor + ">"

        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(item["mnno"]) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + item["pendingin"] + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(item["mislipdate"]) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(item["st_auth_date"]) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["ins_auth_date"] is None else str(item["ins_auth_date"])) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["me_auth_date"]is None else str(item["me_auth_date"])) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["mst_auth_date"] is None else str(item["mst_auth_date"])) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["value"] is None else str(round(item["value"],2))) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ( "" if item["edamount"] is None else str(round(item["edamount"],2))) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["educess"] is None else str(round(item["educess"],2))) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(item["billtype"]) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(item["billno"]) + "<BR></FONT></TD>"
        s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + str(item["payterms"]) + "<BR></FONT></TD>"

        s=s+"</TR>"



    s=s+"</TBODY>"
    s=s+"<TFOOT></TFOOT>"
    s=s+"</TABLE>"
    s=s+"</BODY>"
    s=s+"</HTML>"
    return HttpResponse(s)

def mtp01(request):
    data={}
    sql="select yymm as yymm,round(sum(tworkman)/count(distinct yymm),0),round(sum(aworkman)/count(distinct yymm),0),sum(tabs_hrs),sum(aabs_hrs) as aabs_hrs,sum(tprod_hrs),sum(tunprod_hrs),sum(tidle_hrs),sum(tabs_hrs),sum(tstd_hrs),sum(tact_hrs),round(sum(tdays)/count(distinct seca),0),round(sum(adays)/count(distinct seca),0),count(distinct yymm) from   comjbctrgt where  yymm > 201703  and section = 115 and seca in ('S','H','A','T') group by yymm"
    with open_db_connection('pyrl') as cursor:
        cursor.execute(sql)
        selcomjbctrgt= dictfetchall(cursor)
    sql="select yymm as yymm,sum(astd_hrs) as stdhrs,sum(aact_hrs) as acthrs,sum(aunplnd_hrs),sum(aidle_hrs) as aidle_hrs,sum(aunprod_hrs),sum(unprod1),sum(unprod2),sum(unprod3),sum(unprod4),sum(idle01) as idle01,sum(idle02) as idle02,sum(idle03) as idle03,sum(idle04) as idle04,sum(idle05) as idle05,sum(idle06) as idle06,sum(idle07) as idle07,sum(idle08) as idle08,sum(idle09) as idle09,sum(idle10) as idle10,sum(idle11) as idle11,sum(idle12) as idle12,sum(idle13) as idle13,sum(idle14) as idle14,sum(idle15) as idle15,sum(idle16) as idle16 from  mtpjobsum where  yymm > 201703  and section = 115 and seca in ('S','H','A','T') GROUP BY yymm"
    with open_db_connection('pyrl') as cursor:
        cursor.execute(sql)
        hrs= dictfetchall(cursor)

    sql="select	max(distribution) as dist  from 	shoprpt where	report_no = 'MTP01'"
    with open_db_connection('pyrl') as cursor:
        cursor.execute(sql)
        c1= dictfetchall(cursor)
        dist=c1[0]['dist']
    sql="select 	section as sec,nvl(section_a,' ') as seca from 	shoprpt  where	report_no = 'MTP01' group by section,nvl(section_a,' ')order by section,nvl(section_a,' ')"
    with open_db_connection('pyrl') as cursor:
        cursor.execute(sql)
        mast= dictfetchall(cursor)
        section=mast[0]['sec']
        seca=mast[0]['seca']

    labels = [d['yymm'] for d in hrs]
    dt1 = [d['acthrs'] for d in hrs]
    dt2 = [d['stdhrs'] for d in hrs]
    dt3 = [d['aidle_hrs'] for d in hrs]
    dt4 = [d['aabs_hrs'] for d in selcomjbctrgt]
    dt5 = [d['idle01'] for d in hrs]
    dt6 = [d['idle02'] for d in hrs]
    dt7 = [d['idle03'] for d in hrs]
    dt8 = [d['idle04'] for d in hrs]
    dt9 = [d['idle05'] for d in hrs]
    dt10 = [d['idle06'] for d in hrs]
    dt11 = [d['idle07'] for d in hrs]
    dt12= [d['idle08'] for d in hrs]
    dt13 = [d['idle09'] for d in hrs]
    dt14 = [d['idle10'] for d in hrs]
    dt15 = [d['idle11'] for d in hrs]
    dt16 = [d['idle12'] for d in hrs]
    dt17= [d['idle13'] for d in hrs]
    dt18 = [d['idle14'] for d in hrs]
    dt19 = [d['idle15'] for d in hrs]
    dt20 = [d['idle16'] for d in hrs]
    #print(labels)

    data['labels'] = labels
    data['data1'] = dt1
    data['data2'] = dt2
    data['data3'] = dt3
    data['data4'] = dt4
    data['data5'] = dt5
    data['data6'] = dt6
    data['data7'] = dt7
    data['data8'] = dt8
    data['data9'] = dt9
    data['data10'] = dt10
    data['data11'] = dt11
    data['data12'] = dt12
    data['data13'] = dt13
    data['data14'] = dt14
    data['data15'] = dt15
    data['data16'] = dt16
    data['data17'] = dt17
    data['data18'] = dt18
    data['data19'] = dt19
    data['data20'] = dt20

    return JsonResponse(data)

def mtp09(request):
    dt={}
    sql=("select yymm,section,section_a,	to_char(yymm) || '-' ||to_char(section)||section_a AS yymm_sect,count(*),sum(nvl(capacity,0)) as cap_av,sum(nvl(mrp,0)) as m_rep,sum(nvl(erp,0)) as e_rep,"
	    "sum(nvl(npr,0)) as no_pwr,sum(nvl(nop,0)) as no_opr,sum(nvl(ntl,0)) as no_tool,sum(nvl(njb,0)) as no_job,sum(nvl(loff,0)) as layoff,sum(nvl(misc,0)) as misc,(sum(nvl(capacity,0))-(sum(nvl(npr,0)) +sum(nvl(nop,0)) +sum(nvl(ntl,0))+sum(nvl(njb,0)) +sum(nvl(loff,0)) + sum(nvl(misc,0)) +sum(nvl(mrp,0))+sum(nvl(erp,0)))) as cap_util"
        " from	comidldata a where	yymm 	between 201807 and 201808 and section = 115 and mach_class='G' GROUP BY 	yymm,section,section_a")

    with open_db_connection('pyrl') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    sec={'115H':'HP','115R':'SP','115S':'TR','115T':'HT'}

    #years=set()
    #years={d['yymm'] for d in c1}
    #dt['years']=years
    #print(years)
    labels = [d['yymm_sect']for d in c1]
    dt['labels']=labels
    print(labels)

    dt['cap_util']=[d['cap_util'] for d in c1 ]
    dt['no_opr']=[d['no_opr'] for d in c1 ]
    dt['m_rep'] = [d['m_rep'] for d in c1 ]
    dt['e_rep'] = [d['e_rep'] for d in c1]
    dt['no_pwr'] = [d['no_pwr'] for d in c1 ]
    dt['no_tool'] = [d['no_tool'] for d in c1 ]
    dt['no_job'] = [d['no_job'] for d in c1 ]
    dt['misc']= [d['misc'] for d in c1 ]
    dt['layoff'] = [d['layoff'] for d in c1 ]
    data=dt
    return JsonResponse(data)
def mtp10(request):
    dt={}
    sql=""" SELECT MACH_GP,
       YYMM,
       TO_CHAR(SECTION) || a.SECTION_A AS secno,
       COUNT(MACH_SNO),
       
       TO_CHAR(section) ||  SECTION_A||'-'|| TO_CHAR(MACH_GP)|| mach_class||'('||to_char(COUNT(MACH_SNO))||')' AS yr_mgp,
       COUNT(*),
       SUM(NVL(CAPACITY, 0)) AS cap_av,
       SUM(NVL(MRP, 0)) AS m_rep,
       SUM(NVL(ERP, 0)) AS e_rep,
       SUM(NVL(NPR, 0)) AS no_pwr,
       SUM(NVL(NOP, 0)) AS no_opr,
       SUM(NVL(NTL, 0)) AS no_tool,
       SUM(NVL(NJB, 0)) AS no_job,
       SUM(NVL(LOFF, 0)) AS layoff,
       SUM(NVL(misc, 0)) AS misc,
       (SUM(NVL(CAPACITY, 0)) - (SUM(NVL(NPR, 0)) + SUM(NVL(NOP, 0)) + SUM(NVL(NTL, 0)) + SUM(NVL(NJB, 0)) + SUM(NVL(LOFF, 0)) + SUM(NVL(misc, 0))
       + SUM(NVL(MRP, 0)) + SUM(NVL(ERP, 0)))) AS cap_util
      FROM COMIDLDATA a
      WHERE YYMM between 201808 and 201808 
      GROUP BY YYMM,
           SECTION,
           SECTION_A,
           MACH_GP,mach_class
     """
    with open_db_connection('pyrl') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    machines= tuple([int(d['mach_gp']) for d in c1])

    sql = "select mach_gp,description from COMIDLMACH where mach_gp in %s order by mach_gp asc"%str(machines)

    with open_db_connection('pyrl') as cursor:
        cursor.execute(sql)
        c2 = dictfetchall(cursor)
    df = pd.DataFrame(c2)
    dt['machines']=df.to_html(escape=True)

    labels = [d['yr_mgp'] for d in c1]
    dt['labels'] = labels
    datalabels=['cap_util','no_opr','m_rep','e_rep','no_pwr','no_tool','no_job','misc','layoff']
    for dl in datalabels:
        dt[dl] = [d[dl] for d in c1]
    data = dt
    #print(data)
    return JsonResponse(data)

@login_required
def ratestockno(request):
    u=str(request.user.get_username())
    #print(u)
    if  request.user.is_authenticated() and (u=='67890' ):
        if request.method == 'POST':
            form = StockNoForm(request.POST)

        else:
            form = StockNoForm(initial={'stockno': ''})
        return render(request,'mtpinfoshare/ratedisplay.html',
                                  {'request':request,'form': form, 'search_results': queryRate(request.POST.get('stockno'))})


    else:
        return HttpResponseRedirect("/accounts/login/")

def homiteminforesults(request):
    drwgno=request.GET.get('text','')
    s=""
    
    
    s=s+    BalanceHOM(drwgno)
    s=s+    "<TABLE BORDER=1 BGCOLOR=#ffffff CELLSPACING=0><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=6 color=#800040><B>Transactions Detail for the Drawing No=" + drwgno + "</B></font></CAPTION></FONT>"
    s=s+    "<THEAD>"
    s=s+    "<TR>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Date</FONT></TH>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Index</FONT></TH>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Description</FONT></TH>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Work Order No</FONT></TH>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Warrant</FONT></TH>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Receipt</FONT></TH>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Issue</FONT></TH>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>To</FONT></TH>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>From</FONT></TH>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Doc.No.</FONT></TH>"
    s=s+    "<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Doc.Description</FONT></TH>"
    s=s+    "</TR>"
    s=s+    "</THEAD>"
    s=s+    "<TBODY>"

    # con = pyodbc.connect('DRIVER={SQL Server};SERVER=dc;DATABASE=edssql;Integrated Security=true')
    #cursor = con.cursor()
    sql = "SELECT top 200 s.AltIndex, s.Rec, s.Issue, s.TransacDate, s.TransacDes, s.TransID, s.DrwgNo, s.Tdes, s.Fdes,s.rito,s.rifrom,s.dno,s.des,s.won,s.wrtno FROM homtransacANDSmallpartsControlReg s where s.drwgno='" + drwgno + "'  order by s.transacdate desc ,s.transid desc"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1) > 0:
        for item in c1:
            if item["rec"] > 0 and item["rito"] == 0:
                s=s+            "<TR bgcolor=#D7F0FD VALIGN=TOP>"
            elif item["rito"] == -3 and item["rifrom"] == 0:
                s=s+            "<TR bgcolor=#FDDED7 VALIGN=TOP>"
            elif item["rec"] > 0 and item["rito"] == 3:
                s=s+            "<TR bgcolor=#CAFFCA VALIGN=TOP>"
            elif item["rec"] > 0 and item["rito"] == 4:
                s=s+            "<TR bgcolor=#14EB50 VALIGN=TOP>"
            elif item["rec"] > 0 and item["rito"] == 5:
                s=s+            "<TR bgcolor=#0C872E VALIGN=TOP>"
            elif item["rec"] > 0 and item["rito"] == 6:
                s=s+            "<TR bgcolor=#FF8000 VALIGN=TOP>"
            elif item["rec"] > 0 and item["rito"] == 7:
                s=s+            "<TR bgcolor=#4286f4 VALIGN=TOP>"
            else:
                s=s+            "<TR bgcolor=#FFFFBF VALIGN=TOP>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["transacdate"] is None else str(item["transacdate"])) + "<BR></FONT></TD>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["altindex"] is None else str(item["altindex"])) + "<BR></FONT></TD>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["transacdes"] is None else str(item["transacdes"])) + "<BR></FONT></TD>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["won"] is None else str(item["won"])) + "<BR></FONT></TD>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["wrtno"] is None else str(item["wrtno"])) + "<BR></FONT></TD>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["rec"] is None else str(item["rec"])) + "<BR></FONT></TD>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["issue"] is None else str(item["issue"])) + "<BR></FONT></TD>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["tdes"] is None else str(item["tdes"])) + "<BR></FONT></TD>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["fdes"] is None else str(item["fdes"])) + "<BR></FONT></TD>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["dno"] is None else str(item["dno"])) + "<BR></FONT></TD>"
            s=s+            "<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["des"] is None else str(item["des"])) + "<BR></FONT></TD>"
            s=s+            "</TR>"

            #If item["rito"] = -3 And item["rifrom"] = 0
            #subHomTransDetitem["TransID"]

        s=s+            "</TBODY>"
        s=s+            "<TFOOT></TFOOT>"
        s=s+            "</TABLE>"
        
        return JsonResponse({'result': [s]})

def resultspurDetail(request):
    stk=request.GET.get('text','')
    s=""
    if stk is None: return s
    #cursor = con.cursor()
    sql = "select isnull(drwgno,'')as drwgno from desmasterview where stockno='%s'" % stk
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        d = dictfetchall(cursor)
    if len(d)>0:
        drwgno = d[0]['drwgno']
    else:
        drwgno=""
    
    s = s + "<p > <font color=blue>" + drwgno + "</p>"
    s=s+"<p > <font color=blue>" + balancestockstore(stk) + "</p>"
    s=s+"<p>" + BalanceStock(stk) + "</p>"
    s=s+"<p>" + MIT(stk) + "</p>"
    #s=s+"<p>" + queryRate(stk) + "</p>"
    s=s+"<p>" + findDes(stk) + "</p>"

    sql = "SELECT   top 50  stockno,des, Issue, Rec, Dated, Type FROM dbo.PurDetStockNo  where stockno='" + stk + "' order by dated desc"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    if len(c1)> 0:
        s=s+"<TABLE BORDER=1 BGCOLOR=#ffffff CELLSPACING=0><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=3 color=#800040><B>Transactions Detail for the Stock No =" + stk + "</B></font></CAPTION></FONT>"
        s=s+"<THEAD>"
        s=s+"<TR>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Des</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Issue</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Rec</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Dated</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>type</FONT></TH>"
        s=s+"</TR>"
        s=s+"</THEAD>"
        s=s+"<TBODY>"
        desadd=''
        for item in c1:

            if item["type"] == "MI":
                s=s+"<TR bgcolor=#D7F0FD VALIGN=TOP>"
                w=item['des']
                pono=int(w[w.find('PO')+4:w.find('St')-1])
                pono=0 if pono is None else pono
                #print(pono,stk)
                sql="select mprno from poandmpr where pono=%s and stockno='%s'"%(pono,stk)
                with open_db_connection('edssql') as cursor:
                    cursor.execute(sql)
                    c1 = dictfetchall(cursor)

                desadd=' MPR: '+str([x['mprno'] for x in c1 ]).replace("'","").replace('[','').replace(']','')

            elif item["type"] == "PO":
                s=s+"<TR bgcolor=#FDDED7 VALIGN=TOP>"
                pono=int(item['des'])
                sql = "select mprno from poandmpr where pono=%s and stockno='%s'"%(pono,stk)
                with open_db_connection('edssql') as cursor:
                    cursor.execute(sql)
                    c1 = dictfetchall(cursor)
                #print(c1)
                desadd = ' MPR: ' + str([x['mprno'] for x in c1]).replace("'","").replace('[','').replace(']','')
            elif item["type"] == "MPR":
                s=s+"<TR bgcolor=#CAFFCA VALIGN=TOP>"
                w=item['des']
                mprno=(w[:w.find(':')])
                sql = "select pono from poandmpr where mprno='%s' and stockno='%s'" %(mprno,stk)
                with open_db_connection('edssql') as cursor:
                    cursor.execute(sql)
                    c1 = dictfetchall(cursor)

                desadd = ' PO: ' + str([x['pono'] for x in c1]).replace("'","").replace('[','').replace(']','')
            elif item["type"] == "ME":
                s=s+"<TR bgcolor=#14EB50 VALIGN=TOP>"
                desadd=''
            else:
                s=s+"<TR bgcolor=#FFFFBF VALIGN=TOP>"
                desadd=''
            s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["des"] is None else str(item["des"])+"<font color=""red"">"+desadd+"</font>")+ "<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["issue"] is None else str(item["issue"])) + "<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["rec"] is None else str(item["rec"])) + "<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["dated"] is None else str(item["dated"])) + "<BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" +("-" if item["type"] is None else str(item["type"])) + "<BR></FONT></TD>"
            s=s+"</TR>"
    s=s+"</TBODY>"
    s=s+"<TFOOT></TFOOT>"
    s=s+"</TABLE>"
    #s=s+searhresults(drwgno)
    
    return JsonResponse({'result': [s]})

def BalanceStock(stockno):
    sql = "select (round(sum(rec),3)-round(sum(issue),3)) as balance from mattransac where stockno='" + stockno + "' and status !='d'"
    #cursor = con.cursor()
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    item=c1[0]
    if len(c1)> 0:
       BalanceStock=( "The balance is not available. Pl. contact Mat. Engg." if item["balance"] is None else "Available balance in (Mat Engg)= " + str(item["balance"]))
    else:
        BalanceStock = "The balance is not available. Pl. contact Mat. Engg."
    return BalanceStock

def MIT(stockno):
    sql = "select poqty-qtyaccepted as MIT from MIT where stockno='" + stockno + "'"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)

    if len(c1) > 0:
        item = c1[0]
        MIT = "MIT = " + str(item["mit"])
    else:
        MIT = "MIT = 0"

    return MIT

def  resultsDailyMrr(request):
    date = request.GET.get('text','')
    
    dated =  datetime.strptime(date, '%d-%m-%Y').strftime("%d-%b-%Y")
    #print(dated)
    #cursor = conInStr.cursor()
    sql = "select MrrNo, MatCat , MrrDate, GrcNo, PoNo, SuppName,CollectedBy,Des, BilledQty, ActQty ,EdAmount,Act_Weight,Charged_Weight, SumOfValue from mrrvalues where mrrdate='" + str(dated) + "'"
    with open_db_connection('incomingstore') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #print(c1)
    if len(c1) > 0:
        df = pd.DataFrame(c1)
        df=df[['mrrno', 'matcat' , 'mrrdate', 'grcno', 'pono', 'suppname','collectedby','des', 'billedqty', 'actqty' ,'edamount','act_weight','charged_weight', 'sumofvalue']]
        df.columns=['MRR No','Category','Date','GRC No','PO No','Supplier Name','Collected By','Description','Billed Qty','Actual Qty','ED Amount','Actual Weight','Charged weight','Value']
        total=str(df['Value'].sum())
        s=df.to_html(na_rep="0").replace("<tr", "<TR VALIGN=TOP bgcolor=#FFFFBF")
        s=s.replace("<th", "<th BGCOLOR =  #c0c0c0 BORDERCOLOR=#000000")+"<p align=left><font size=4 color=red>Total Value:</font><font size=4 color=blue>" + total + "</font>"


        return JsonResponse({'result': [s]})
    else:
        return JsonResponse({'result': ["<p>No MRR for this Date</p>"]})


    #total = total + IIf(IsNull(item"sumofvalue"]), 0, item"sumofvalue"])

def systems(request):
    WCI=request.GET.get('WCI','')
    print('aaaa'+WCI)
    result=[]
    if WCI=='':
        s=''
        sql = "SELECT * FROM systems order by system"
        #cursor = con.cursor()
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)

        
        if len(c1)>0:
            for item in c1:
                url=request.build_absolute_uri(reverse('systems'))+"?WCI=systems&WCE="+str(item["sysid"])
                result.append({'apiurl':url,'inputtext':item["system"]})
  
        return JsonResponse({'result':result})
    elif WCI=='systems':
        s=''
        sql = "SELECT * FROM CNCPackagesDetail where sysid=" + request.GET.get('WCE',0) + " order by packageno "
        #cursor = con.cursor()
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c1 = dictfetchall(cursor)
        Sqlsys = "select system from systems where sysid=" + request.GET.get('WCE',0) + ""
        #cursor = con.cursor()
        with open_db_connection('edssql') as cursor:
            cursor.execute(Sqlsys)
            c2 = dictfetchall(cursor)
        sysname = c2[0]['system']
        

        s=s+"<TABLE BORDER=1 BGCOLOR=#ffffff >"

        
        s=s+"<TR >"
        s=s+"<TH BGCOLOR=#c0c0c0 >Package No</TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 >Description</TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 >Rapid Feed</TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 >Spindle Power</TH>"
        s=s+"<TH BGCOLOR=#c0c0c0>Max Spindle Speed</TH>"
        s=s+"<TH BGCOLOR=#c0c0c0>Base Spindle Speed</TH>"
        s=s+"<TH BGCOLOR=#c0c0c0>Driven</TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 >Scale</TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 >MMC</TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 >Monitor</TH>"
        s=s+"</TR>"
        
        for item in c1:
            s1=s
            url=request.build_absolute_uri(reverse('systems'))+"?WCI=packages&WCE="+ item["packageno"] 
            
            s1=s1+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
            s1=s1+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000><a href=?WCI=packages&WCE="+ item["packageno"] + ">" + item["packageno"] + "</a><BR></FONT></TD>"
            s1=s1+ " <TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""arial"" COLOR=#000000>" +('' if item["packdes"] is None else item["packdes"])+"<BR></FONT></TD>"
            s1=s1+ " <TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=1 FACE=""arial"" COLOR=#000000>" +('' if item["rapidfeed"] is None else item["rapidfeed"])+"<BR></FONT></TD>"
            s1=s1+ " <TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""arial"" COLOR=#000000>" +('' if item["spindlepower"] is None else item["spindlepower"])+"<BR></FONT></TD>"
            s1=s1+ " <TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=1 FACE=""arial"" COLOR=#000000>" +('' if item["smaxspeed"]  is None else str(item["smaxspeed"]))+"<BR></FONT></TD>"
            s1=s1+ " <TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""arial"" COLOR=#000000>" +('' if item["sbasespeed"] is None else str(item["sbasespeed"]))+"<BR></FONT></TD>"
            s1=s1+ " <TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=1 FACE=""arial"" COLOR=#000000>" +('' if item["driven"] is None else item["driven"])+"<BR></FONT></TD>"
            s1=s1+ " <TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""arial"" COLOR=#000000>" +('' if item["scale"] is None else item["scale"])+"<BR></FONT></TD>"
            s1=s1+ " <TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=1 FACE=""arial"" COLOR=#000000>" +('' if  item["mmc"] is None else item["mmc"])+"<BR></FONT></TD>"
            s1=s1+ " <TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""arial"" COLOR=#000000>" +('' if item["monitor"] is None else item["monitor"])+"<BR></FONT></TD>"
            s1=s1+ "</TR></TABLE>"
            result.append({'apiurl':url,'inputtext':s1})
        s = s + "</TBODY>"
        s = s + "<TFOOT></TFOOT>"
        s = s + "</TABLE>"
        
        return JsonResponse({'result':result})

    elif WCI=='packages':
        s = ''
        
        sql = "SELECT OrderCode,des,qty FROM CNCPackages where packageno='" + request.GET.get('WCE',
                                                                                              0) + "' order by ordercode"
        with open_db_connection('edssql') as cursor:
            cursor.execute(sql)
            c3 = dictfetchall(cursor)
        
        
        s = s + "<table border=1px><THEAD>"
        s = s + "<TR >"
        s = s + "<TH BGCOLOR=#c0c0c0 >Order Code</TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 >Description</TH>"
        s = s + "<TH BGCOLOR=#c0c0c0 >Quantity</TH>"
        s = s + "</TR>"
        s = s + "</THEAD>"
        s = s + "<TBODY>"
        
        for item in c3:
            
            s = s + "<TR VALIGN=TOP bgcolor=#FFFFBF>"
            s = s + "<TD BORDERCOLOR=#c0c0c0  ALIGN=left>" + item[
                "ordercode"] + "</TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 >" + item[
                "des"] + "</TD>"
            s = s + "<TD BORDERCOLOR=#c0c0c0 >" + str(
                item["qty"]) + "</TD>"
            s = s + "</TR>"

        
        s=s+"</TABLE>"
        
        return JsonResponse({'result':[s]})

def resultsfinddrwgno(request):
    stockno=request.GET.get('text','')
    if stockno is None or stockno=='': return ''
    stockno="" if stockno is None else stockno
    #cursor = con.cursor()
    sql = "SELECT isnull(itemcodesuffix,'') + isnull(itemcodeno,'') as Drwgno,des from desmaster where stockno='" + stockno + "'"
    with open_db_connection('edssql') as cursor:
        cursor.execute(sql)
        c1 = dictfetchall(cursor)
    #df=pd.DataFrame(c1)
    if len(c1)==0 or stockno is None:
        s= "<h5><font face=""Arial"">There are no entry in the database for the requested stock no=" +stockno + "</font></h5>"
    else:
        s=""
        s= s+"<TABLE BORDER=1 BGCOLOR=#ffffff CELLSPACING=0><FONT FACE=""Arial"" COLOR=#000000><CAPTION><font size=4 color=#006A00<B>Search Results for stock no= " + stockno + "</B></font></CAPTION></FONT>"
        s=s+"<THEAD>"
        s=s+"<TR >"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Drawing No</FONT></TH>"
        s=s+"<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>Designation</FONT></TH>"
        s=s+"</TR>"
        s=s+"</THEAD>"
        s=s+"<TBODY>"
        for item in c1:
            s=s+"<TR VALIGN=TOP bgcolor=#FFFFBF>"
            s=s+"<TD BORDERCOLOR=#c0c0c0 ><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["drwgno"] is None else str(item["drwgno"]))+ " <BR></FONT></TD>"
            s=s+"<TD BORDERCOLOR=#c0c0c0  ALIGN=RIGHT><FONT SIZE=2 FACE=""Arial"" COLOR=#000000>" + ("" if item["des"] is None else str(item["des"]))+ "<BR></FONT></TD>"
            s=s+"</TR>"
    return JsonResponse({'result':[s]})










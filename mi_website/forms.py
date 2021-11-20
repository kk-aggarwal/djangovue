
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import  Submit,Layout,Div,Button,Fieldset,Field
import datetime
from django.forms import widgets

from mi_website.formvalidators_choices import *

class bformdatepicker(widgets.TextInput):
    template_name='mi_website/widgets/b-form-datepicker.html'

class mislipeditForm(forms.Form):
    


    finyear = forms.CharField(max_length=50)
    finyear.widget.attrs['readonly'] = True
    mislipdate = forms.DateField(input_formats=["%d-%b-%Y"])
    mislipdate.widget.attrs['readonly'] = True
    matgrp=forms.IntegerField()
    matgrp.widget.attrs['readonly'] = True
    mislipno=forms.IntegerField()
    mislipno.widget.attrs['readonly'] = True
    pono=forms.IntegerField()
    suppname=forms.CharField(widget=forms.Textarea(attrs={'rows':5}),max_length=200)
    mprno = forms.CharField(max_length=50)
    recdby = forms.CharField(max_length=50)
    note = forms.CharField(max_length=50,required=False)
    st_auth = forms.BooleanField(required=False)
    mst_auth= forms.BooleanField(required=False)
    mst_auth_date=forms.DateField(widget=bformdatepicker(),required=False)
    #username = forms.CharField(widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(mislipeditForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Div(
                Div('st_auth', css_class="col-sm-2"),
                Div('mst_auth', css_class="col-sm-2"),
                Div('mst_auth_date', css_class="col-sm-5"),
                css_class="row"
            ),
            Div(
                Div('finyear', css_class="col-sm-3"),
                Div('mislipdate', css_class="col-sm-3"),
                Div('matgrp', css_class="col-sm-3"),
                Div('mislipno', css_class="col-sm-3"),
                css_class="row"
            ),
            Div(
                Div('pono', css_class="col-sm-4"),
                Div('mprno', css_class="col-sm-5"),
                Div('recdby', css_class="col-sm-3"),

                css_class="row"
            ),
            Div(

                Div('suppname', css_class="col-sm-8"),
                Div('note', css_class="col-sm-2"),

                css_class="row"
            ),

        )

        self.helper['pono'].wrap(Field, ref="ref_pono")
        self.helper['suppname'].wrap(Field, ref="ref_suppname")

    def clean(self):
        cleaned_data=super(mislipeditForm,self).clean()
        print(cleaned_data)

        pono=self.cleaned_data.get("pono")
        matgrp = self.cleaned_data.get("matgrp")
        if matgrp  in (16, 19, 27):
            pass
        else:
            if verifyPO(pono)==False:
                self.add_error('pono',forms.ValidationError('PO not valid'))
        mstauth = self.cleaned_data['mst_auth']        
        if mstauth:
            sql = "SELECT FinYear, MatGrp, MiSlipNo, DetailId, StocKNo, Des,Unit,QtyRecd, QtyAccepted, DateAccepted,PersonAccepted , qtyIn FROM MISlipDet_Mst where mislipno=" + str(self.cleaned_data['mislipno']) + " and matgrp=" + str(self.cleaned_data['matgrp']) + " and finyear='" + self.cleaned_data['finyear'] + "' and qtyin is null"
            c1=runQuery('edssql', sql)['cursor']
            if len(c1)>0:
                self.add_error(field=None, error=forms.ValidationError("This Mi slip cannot be authorized ! One or more item is not stock charged!"))
        else:
            sql="select * from accmislip where  mislipno=" + str(self.cleaned_data['mislipno']) + " and matgroup=" + str(self.cleaned_data['matgrp']) + " and docyearid='" + self.cleaned_data['finyear'] + "'"
            print(sql)
            c1 = runQuery('accounts', sql)['cursor']
            if len(c1) > 0:
                self.add_error(field=None, error=forms.ValidationError("This Mi slip authorization cannot be revoked!"))

    def clean_mislipdate(self):
        #print('dtate')
        return datetime.datetime.strptime(str(self.cleaned_data['mislipdate']), "%Y-%m-%d").strftime("%d-%b-%Y")

    def clean_matgrp(self):
        matgrp=self.cleaned_data['matgrp']
        if verifyMatgrp(matgrp):
            return matgrp
        else:
            self.add_error('matgrp', forms.ValidationError('Mat Group not valid'))
        return matgrp
    def clean_st_auth(self):
        stauth = self.cleaned_data['st_auth']
        #check for bill
        if stauth:
            sql = "select * from mislipbills where mislipno=" + str(self.cleaned_data['mislipno']) + " and matgrp=" + str(self.cleaned_data['matgrp']) + " and finyear='" + self.cleaned_data['finyear'] + "'"
            c1 = runQuery('incomingstore', sql)['cursor']
            if len(c1) > 0:
                return self.cleaned_data['st_auth']
            else:
                self.add_error('st_auth', forms.ValidationError("No Bill Enttered !"))
        else:
            return stauth
        # check for items
        if stauth:
            sql = "select * from mislipdet where mislipno=" + str(self.cleaned_data['mislipno']) + " and matgrp=" + str(self.cleaned_data['matgrp']) + " and finyear='" + self.cleaned_data['finyear'] + "'"
            c1 = runQuery('incomingstore', sql)['cursor']
            if len(c1) > 0:
                return self.cleaned_data['st_auth']
            else:
                self.add_error('st_auth', forms.ValidationError("No item Enttered !"))
        else:
            return stauth
        return stauth

    def clean_mst_auth(self):
        mstauth = self.cleaned_data['mst_auth']
        print(self.cleaned_data)
        

        return mstauth


    def clean_mst_auth_date(self):
        mstauth=self.cleaned_data['mst_auth']
        print(self.cleaned_data['mst_auth_date'])
        if mstauth and self.cleaned_data['mst_auth_date']==None:
            self.add_error('mst_auth_date', forms.ValidationError("Pl select date!"))
            return None
        elif mstauth and not(self.cleaned_data['mst_auth_date']==None):
            return datetime.datetime.strptime(str(self.cleaned_data['mst_auth_date']), "%Y-%m-%d").strftime("%d-%b-%Y")
        return None

    def save_update(self,request):

            sql='update mislip set '+update_values_of_query(self,request)+' where finyear=%r and matgrp=%r and mislipno=%r'%(self.cleaned_data['finyear'],self.cleaned_data['matgrp'],self.cleaned_data['mislipno'])
            print(sql)

            return runQuery('incomingstore', sql)

    def save_create(self,request):
        fields = ','.join(self.fields)

        sql = 'insert into mislip (%s) values(%s)' % ( insert_values_of_query(self,request))
        print(sql)
        # print(self.cleaned_data)
        return runQuery('incomingstore', sql)

class mislipitemeditForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(mislipitemeditForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
    finyear = forms.CharField(max_length=50)
    finyear.widget.attrs['readonly'] = True
    matgrp=forms.IntegerField()
    matgrp.widget.attrs['readonly'] = True
    mislipno=forms.IntegerField()
    mislipno.widget.attrs['readonly'] = True
    stockno=forms.CharField(max_length=50)
    stockno.widget.attrs['ref']='ref_stockno'
    des = forms.CharField(widget=forms.Textarea(attrs={'rows':5}),max_length=1000)
    des.widget.attrs['ref'] = 'ref_des'
    qtyrecd=forms.FloatField()
    unit = forms.CharField(max_length=50)
    stdwt = forms.FloatField(required=False)
    scalewt = forms.FloatField(required=False)
    billedwt = forms.FloatField(required=False)
    class Meta:
        exclude=('stdwt',)



    def clean(self):
        cleaned_data=super(mislipitemeditForm,self).clean()

    def clean_stockno(self):
        stockno=self.cleaned_data['stockno']
        #return stockno
        print(stockno)
        if verifyStockNoAgainstStmaster(stockno,self.cleaned_data['matgrp']):
            if verifyStocknoAgainstPO(stockno,self.cleaned_data['finyear'],self.cleaned_data['matgrp'],self.cleaned_data['mislipno']):
                return stockno
            else:
                self.add_error('stockno', forms.ValidationError('Stock no not in PO'))
        else:
            self.add_error('stockno', forms.ValidationError('Stock no not in Stock Master'))
        return stockno

    def save_update(self, request):
        sql = 'update mislipdet set ' + update_values_of_query(self,request) + ' where finyear=%r and matgrp=%r and mislipno=%r  and stockno=%r' % (
        self.cleaned_data['finyear'], self.cleaned_data['matgrp'], self.cleaned_data['mislipno'],
        self.cleaned_data['stockno'])

        print(sql)

        return runQuery('incomingstore', sql)

    def save_create(self, request):
        fields = ','.join(self.fields)

        sql = 'insert into mislipdet (%s) values(%s)' % insert_values_of_query(self, request)
        print(sql)
        # print(self.cleaned_data)
        return runQuery('incomingstore', sql)

class mislipmrreditForm(forms.Form):

    finyear = forms.CharField(max_length=50)
    finyear.widget.attrs['readonly'] = True
    matgrp=forms.IntegerField()
    matgrp.widget.attrs['readonly'] = True
    mislipno=forms.IntegerField()
    mislipno.widget.attrs['readonly'] = True
    mrrno=forms.ChoiceField()
    #addedit = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self,*args,**kwargs):
        super(mislipmrreditForm,self).__init__(*args,**kwargs)
        self.fields['mrrno'].choices=mrrchoices(self.initial['finyear'])
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True

    def clean(self):
        cleaned_data=super(mislipmrreditForm,self).clean()


    def save_update(self, request):
        sql = 'update mislipmrr set ' + update_values_of_query(self,request) + ' where finyear=%r and matgrp=%r and mislipno=%r  and mrrno=%r' % (
        self.cleaned_data['finyear'], self.cleaned_data['matgrp'], self.cleaned_data['mislipno'],
        self.cleaned_data['mrrno'])

        print(sql)

        return runQuery('incomingstore', sql)

    def save_create(self, request):
        fields = ','.join(self.fields)

        sql = 'insert into mislipmrr (%s) values(%s)' % ( insert_values_of_query(self, request))
        print(sql)
        # print(self.cleaned_data)
        return runQuery('incomingstore', sql)

class mislipbilleditForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(mislipbilleditForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
    finyear = forms.CharField(max_length=50)
    finyear.widget.attrs['readonly'] = True
    matgrp=forms.IntegerField()
    matgrp.widget.attrs['readonly'] = True
    mislipno=forms.IntegerField()
    mislipno.widget.attrs['readonly'] = True
    mrrno = forms.IntegerField()
    mrrno.widget.attrs['readonly'] = True
    #mrrno.widget.attrs['@change'] = "handlemrrnochange"
    billtype=forms.CharField(max_length=50)
    billtype.widget.attrs['readonly'] = True
    billno = forms.CharField(max_length=50)
    billno.widget.attrs['readonly'] = True
    dated=forms.DateField(input_formats=["%d-%b-%Y"])
    dated.widget.attrs['readonly'] = True
    cenventno=forms.CharField(label='GST No',max_length=50)
    cenventno.widget.attrs['readonly'] = True
    cenventdate=forms.CharField(label='GST Date',max_length=50,required=False)
    cenventdate.widget.attrs['readonly'] = True
    sgst = forms.FloatField(required=False)
    #igst = forms.FloatField(required=False)
    igst=forms.FloatField(required=False)
    cgst = forms.FloatField(required=False)
    value = forms.FloatField(required=False)
    #addedit = forms.CharField(widget=forms.HiddenInput(), required=False)
    def clean(self):
        cleaned_data=super(mislipbilleditForm,self).clean()

    def clean_dated(self):
        return datetime.datetime.strptime(str(self.cleaned_data['dated']), "%Y-%m-%d").strftime("%d-%b-%Y")

    def save_update(self,request):

        sql='update mislipbills set '+update_values_of_query(self,request)+' where finyear=%r and matgrp=%r and mislipno=%r  and billtype=%r and billno=%r'%(self.cleaned_data['finyear'],self.cleaned_data['matgrp'],self.cleaned_data['mislipno'],self.cleaned_data['billtype'],self.cleaned_data['billno'])
        print(sql)
        return runQuery('incomingstore', sql)

    def save_create(self, request):
        fields = ','.join(self.fields)

        sql = 'insert into mislipbills (%s) values(%s)' % (insert_values_of_query(self, request))
        print(sql)
        # print(self.cleaned_data)
        return runQuery('incomingstore', sql)

class mrreditForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(mrreditForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.fields['matcatid']=forms.ChoiceField(choices=[(3,'capital'),(4,'gst refundable'),(5,'gst not refundable')])
        self.fields['reg_unreg_comp']=forms.ChoiceField(choices=[(1, 'regular'), (2, 'unregular'), (3, 'composite')], initial=1)
        self.fields['imp_ind'] = forms.ChoiceField(choices=[(0,'indigenous'),(1,'imported')],initial=0)
        self.fields['cash_po'] = forms.ChoiceField(choices=[(0,'po'),(1,'cash')],initial=0)
        self.fields['rcm'] = forms.ChoiceField(choices=[(0,'yes'),(1,'no')],initial=0)
        self.fields['grcno'].choices = grcchoices()

    finyear = forms.CharField(max_length=50)
    finyear.widget.attrs['readonly'] = True
    mrrdate = forms.DateField(input_formats=["%d-%b-%Y"])
    mrrdate.widget.attrs['readonly'] = True
    mrrno = forms.IntegerField()
    matcatid=forms.ChoiceField()

    grcno=forms.ChoiceField()

    pono=forms.IntegerField(required=False)
    suppname=forms.CharField(max_length=200)
    suppname.widget.attrs['ref'] = 'ref_suppname'
    typeofsupp = forms.CharField(max_length=150,required=False)
    des = forms.CharField(max_length=50)
    suppcity = forms.CharField(max_length=50)
    eccno=forms.CharField(max_length=50,required=False)
    actqty = forms.CharField(max_length=50)
    billedqty = forms.CharField(max_length=50)
    unit= forms.CharField(max_length=50)
    wtact = forms.FloatField(required=False)
    wtcharged = forms.FloatField(required=False)
    wtunit = forms.CharField(max_length=50,required=False)
    cenventcopy = forms.CharField(max_length=50,required=False)
    cenventno = forms.CharField(max_length=50,required=False)
    cenventdate = forms.CharField(max_length=50,required=False)
    edamount = forms.CharField(max_length=50,required=False)
    collectedby = forms.CharField(max_length=50)
    reg_unreg_comp=forms.ChoiceField(required=False)
    imp_ind=forms.ChoiceField(required=False)
    cash_po=forms.ChoiceField(required=False)
    rcm=forms.ChoiceField(required=False)
    #addedit=forms.CharField(widget=forms.HiddenInput(),required=False)

    def clean_mrrdate(self):
        return datetime.datetime.strptime(str(self.cleaned_data['mrrdate']),"%Y-%m-%d").strftime("%d-%b-%Y")
    #def clean(self):
       #cleaned_data=super(mrreditForm,self).clean()

       #pono=self.cleaned_data.get("pono")
       #matgrp = self.cleaned_data.get("matgrp")
       #if matgrp  in (16, 19, 27):
        #pass
       #else:
         #if verifyPO(pono)==False:
          #self.add_error('pono',forms.ValidationError('PO not valid'))
    def save_update(self,request):

        sql='update mrr set '+update_values_of_query(self,request)+' where finyear=%r and mrrno=%r'%(self.cleaned_data['finyear'],self.cleaned_data['mrrno'])
        #print(sql)
        return runQuery('incomingstore', sql)

    def save_create(self, request):
        fields = ','.join(self.fields)

        sql = 'insert into mrr (%s) values(%s)' % (insert_values_of_query(self, request))
        print(sql)
        # print(self.cleaned_data)
        return runQuery('incomingstore', sql)



class mrrvalueeditForm(forms.Form):
    finyear = forms.CharField(max_length=50)
    finyear.widget.attrs['readonly'] = True
    mrrno = forms.IntegerField()
    mrrno.widget.attrs['readonly'] = True
    type = forms.ChoiceField()
    billno=forms.CharField(max_length=50,label='Invoice/Challan No')
    #dated = forms.DateField(input_formats=["%d-%b-%Y"])
    dated = forms.DateField(widget=bformdatepicker())

    cenventno=forms.CharField(max_length=50,label='GST Invoice No')
    cenventdate=forms.CharField(max_length=50,label='GST Invoice Date')
    tarrifno=forms.CharField(max_length=50,label='Tarrif/HSN Code')
    evalue=forms.FloatField(label='Basic Value')
    sgst=forms.FloatField()
    cgst = forms.FloatField()
    igst = forms.FloatField()
    value=forms.FloatField(label='Value')
    qty=forms.FloatField(label='Qty',required=False)
    #addedit = forms.CharField(widget=forms.HiddenInput(), required=False)
    def __init__(self,*args,**kwargs):
        super(mrrvalueeditForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.fields['type'] = forms.ChoiceField(label='Type',choices=[('invoice', 'Invoice'), ('challan', 'Challan')])


    def clean_dated(self):
        return datetime.datetime.strptime(str(self.cleaned_data['dated']), "%Y-%m-%d").strftime("%d-%b-%Y")
    def save_update(self,request):

        sql='update invoice set '+update_values_of_query(self,request)+' where finyear=%r and mrrno=%r and billno=%r'%(self.cleaned_data['finyear'],self.cleaned_data['mrrno'],self.cleaned_data['billno'])
        #print(sql)
        return runQuery('incomingstore', sql)

    def save_create(self, request):
        fields = ','.join(self.fields)

        sql = 'insert into invoice (%s) values(%s)' % (insert_values_of_query(self, request))
        print(sql)
        # print(self.cleaned_data)
        return runQuery('incomingstore', sql)

class ledgereditForm(forms.Form):
    transid=forms.IntegerField(widget = forms.HiddenInput(),required=False)
    transid.widget.attrs['readonly'] = True

    yearid = forms.CharField(widget = forms.HiddenInput(),max_length=50)
    yearid.widget.attrs['readonly'] = True

    stockno = forms.CharField(max_length=50)
    stockno.widget.attrs['readonly'] = True

    groupid = forms.IntegerField(widget = forms.HiddenInput(),)
    groupid.widget.attrs['readonly'] = True

    docyearid = forms.CharField(widget = forms.HiddenInput(),max_length=50)

    docyearid.required=False

    docyearid.widget.attrs['readonly'] = True
    rec_issue=forms.ChoiceField(choices=(('recpt','receive'),('issue','issue')),widget=forms.RadioSelect,)
    rec_issue.widget.attrs['ref'] = "recissue"
    rec_issue.widget.attrs['v-model'] = "$parent.$parent.$parent.rec_issue"
    doctype = forms.TypedChoiceField(choices=[(1,'DN'),(2,'RN'),(3,'MI'),(4,'RV'),(5,'VA'),(6,'SAV')],coerce=int)
    doctype.widget.attrs['ref'] = 'ref_doctype'
    doctype.widget.attrs['v-html'] = '$parent.$parent.$parent.doctype_choices'
    doctype.widget.attrs['disabled'] = True
    docno=forms.IntegerField()
    docno.widget.attrs['ref'] = 'ref_docno'
    won=forms.CharField(max_length=50)
    v="choices=[(1,'DN'),(2,'RN'),(3,'MI'),(4,'RV'),(5,'VA'),(6,'SAV')]"
    won.required = False

    won.widget.attrs['readonly'] = True
    won.widget.attrs['ref'] = 'ref_won'
    warrant = forms.IntegerField()

    warrant.required = False

    warrant.widget.attrs['readonly'] = True
    warrant.widget.attrs['ref'] = 'ref_warrant'
    #trdate=forms.DateField(input_formats=["%d-%b-%Y"])
    trdate=forms.DateField(widget=bformdatepicker())
    qtyin=forms.FloatField(required=False)
    qtyin.widget.attrs['disabled'] = True
    qtyin.widget.attrs['ref']="ref_qtyin"
    qtyout = forms.FloatField(required=False)
    qtyout.widget.attrs['disabled'] = True
    qtyout.widget.attrs['ref'] = "ref_qtyout"
    docref=forms.IntegerField()
    docref.widget.attrs['readonly'] = True
    docref.widget.attrs['ref'] = "ref_docref"
    docref.required = False

    #suppname.widget.attrs['ref'] = 'ref_suppname'



    def __init__(self,*args,**kwargs):
        super(ledgereditForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()

        #self.helper.form_id = "mislipedit"
        #self.helper.form_class = "mislipeditform"
        #self.helper.form_method = 'post'
        #self.helper.form_action = 'mislipedit'
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True

    def clean(self):
        cleaned_data=super(ledgereditForm,self).clean()
        print(self.cleaned_data['doctype'])
        #verify MI slip
        if self.cleaned_data['doctype']==3:
            print('ert')
            sql = "select * from mislipdetailview where finyear='" + self.cleaned_data['docyearid'] +"' and matgrp=" + str(self.cleaned_data['groupid']) + " and mislipno=" + str(self.cleaned_data['docno']) + " and ins_auth=1 and stockno='" + self.cleaned_data['stockno'] + "' and qtyaccepted=" + str(self.cleaned_data['qtyin']) + ""
            data=runQuery('incomingstore', sql)
            if len(data['cursor'])>0:
                pass
                #self.cleaned_data['docref']=data['cursor'][0]['misref']
            else:
                self.add_error(field=None, error=forms.ValidationError('Wrong MI slip No  !'))

        #       'verify balance for issues

        if self.cleaned_data['rec_issue'] == "issue":
            if self.cleaned_data['doctype'] in [1,5,6]:
                sql="select bal from stStockbalForTheYear where stockno='%s'"%self.cleaned_data['stockno']
                data = runQuery('edssql', sql)
                if len(data['cursor'])>0:
                    bal=data['cursor'][0]['bal']

                else:
                    bal=0
                if bal<(self.cleaned_data['qtyout']):
                    self.add_error(field=None, error=forms.ValidationError('Stock Balance not available!'))

        #verify won
        if self.cleaned_data['doctype'] in [1, 2,4,6]:
            if self.cleaned_data['won']=="":
                self.add_error(field=None, error=forms.ValidationError('DOC NO cannot be verified!'))
        #verify qty
        if self.cleaned_data['qtyin']=="" and self.cleaned_data['qtyout']=="":
            self.add_error(field=None, error=forms.ValidationError('Enter Quantity !!'))


    def clean_trdate(self):

        return datetime.datetime.strptime(str(self.cleaned_data['trdate']), "%Y-%m-%d").strftime("%d-%b-%Y")

    def save_update(self, request):
        sql = 'update sttransactions set ' + update_values_of_query(self,request) + ' where finyear=%r and matgrp=%r and mislipno=%r  and mrrno=%r' % (
        self.cleaned_data['finyear'], self.cleaned_data['matgrp'], self.cleaned_data['mislipno'],
        self.cleaned_data['mrrno'])

        print(sql)

        return runQuery('edssql', sql)

    def save_create(self, request):
        fields = ','.join(self.fields)

        sql = 'insert into sttransactions (%s) values(%s)' % ( insert_values_of_query(self, request))
        print(sql)
        # print(self.cleaned_data)
        return runQuery('edssql', sql)

class stdocregistereditForm(forms.Form):
    refid=forms.IntegerField(widget = forms.HiddenInput(),required=False)
    refid.widget.attrs['readonly'] = True
    yearid = forms.CharField(widget = forms.HiddenInput(),max_length=50)
    yearid.widget.attrs['readonly'] = True

    groupid = forms.IntegerField(widget = forms.HiddenInput(),)
    groupid.widget.attrs['readonly'] = True
    doctype = forms.TypedChoiceField(choices=[(1, 'DN'), (2, 'RN'), (3, 'MI'), (4, 'RV'), (5, 'VA'), (6, 'SAV')],
                                     coerce=int)
    doctype.widget.attrs['ref'] = 'ref_doctype'
    doctype.widget.attrs['v-model'] = '$parent.$parent.$parent.doctype_choices'
    docno = forms.IntegerField()
    docno.widget.attrs['readonly'] = True
    docno.widget.attrs['ref'] = 'ref_docno'


    docdate = forms.DateField(widget=bformdatepicker())
    won = forms.CharField(max_length=50)
    warrant = forms.IntegerField(required=False)
    warrant.widget.attrs['ref'] = 'ref_warrant'
    des = forms.CharField(max_length=50,required=False)




    def __init__(self,*args,**kwargs):
        super(stdocregistereditForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()

        #self.helper.form_id = "mislipedit"
        #self.helper.form_class = "mislipeditform"
        #self.helper.form_method = 'post'
        #self.helper.form_action = 'mislipedit'
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True

    def clean(self):
        cleaned_data=super(stdocregistereditForm,self).clean()
        print(self.cleaned_data)
        #verify won and warrant
        sql = "select * from workordernumbers where  won='" + self.cleaned_data['won'] + "' and warrantno=" + ('0' if self.cleaned_data['warrant']==None else str(self.cleaned_data['warrant']) )
        print(sql)
        data=runQuery('edssql', sql)
        if len(data['cursor'])>0:
            pass
                #self.cleaned_data['docref']=data['cursor'][0]['misref']
        else:
            self.add_error(field=None, error=forms.ValidationError('Work order no cannot be verified!'))




    def clean_docdate(self):

        return datetime.datetime.strptime(str(self.cleaned_data['docdate']), "%Y-%m-%d").strftime("%d-%b-%Y")

    def save_update(self, request):
        sql = 'update stdocregister set ' + update_values_of_query(self,request) + ' where yearid=%r and groupid=%r and doctype=%r  and docno=%r' % (
        self.cleaned_data['yearid'], self.cleaned_data['groupid'], self.cleaned_data['doctype'],
        self.cleaned_data['docno'])

        print(sql)

        return runQuery('edssql', sql)

    def save_create(self, request):
        fields = ','.join(self.fields)

        sql = 'insert into stdocregister (%s) values(%s)' % ( insert_values_of_query(self, request))
        print(sql)
        # print(self.cleaned_data)
        return runQuery('edssql', sql)

class stmislipitemeditForm(forms.Form):
    """yearid,docyearid,groupid,docno,doctype,qtyin,stockno,docref,trdate"""


    yearid = forms.CharField(widget = forms.HiddenInput(),max_length=50)
    yearid.widget.attrs['readonly'] = True

    groupid = forms.IntegerField(widget = forms.HiddenInput(),)
    groupid.widget.attrs['readonly'] = True
    doctype = forms.TypedChoiceField(choices=[(1, 'DN'), (2, 'RN'), (3, 'MI'), (4, 'RV'), (5, 'VA'), (6, 'SAV')],
                                     coerce=int)
    doctype.widget.attrs['readonly'] = True
    docno = forms.IntegerField()
    docno.widget.attrs['readonly'] = True


    docyearid = forms.CharField(max_length=50)
    docyearid.widget.attrs['readonly'] = True
    stockno = forms.CharField(max_length=50)
    stockno.widget.attrs['readonly'] = True
    docref = forms.IntegerField()
    docref.widget.attrs['readonly'] = True
    qtyin=forms.FloatField()
    trdate= forms.DateField(widget=bformdatepicker())

    def __init__(self, *args, **kwargs):
        super(stmislipitemeditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        # self.helper.form_id = "mislipedit"
        # self.helper.form_class = "mislipeditform"
        # self.helper.form_method = 'post'
        # self.helper.form_action = 'mislipedit'
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True

    def clean(self):
        cleaned_data = super(stmislipitemeditForm, self).clean()
        print(self.cleaned_data)

    def clean_trdate(self):

        return datetime.datetime.strptime(str(self.cleaned_data['trdate']), "%Y-%m-%d").strftime("%d-%b-%Y")

    def save_update(self, request):
        sql = 'update sttransactions set ' + update_values_of_query(self,
                                                                   request) + ' where yearid=%r and groupid=%r and doctype=%r  and docno=%r' % (
            self.cleaned_data['yearid'], self.cleaned_data['groupid'], self.cleaned_data['doctype'],
            self.cleaned_data['docno'])

        print(sql)

        return runQuery('edssql', sql)

    def save_create(self, request):
        fields = ','.join(self.fields)

        sql = 'insert into sttransactions (%s) values(%s)' % (insert_values_of_query(self, request))
        print(sql)
        # print(self.cleaned_data)
        return runQuery('edssql', sql)



class ststockmastereditForm(forms.Form):

    stockno = forms.CharField(max_length=50)
    #stockno.widget.attrs['readonly'] = True

    des = forms.CharField(widget=forms.Textarea(attrs={"rows":5}), max_length=200)
    itemcodesuffix = forms.CharField(max_length=50,required=False)
    itemcodeno = forms.CharField(max_length=50,required=False)
    matgroup = forms.IntegerField()
    matgroup.widget.attrs['readonly'] = False
    loca = forms.CharField(max_length=50,required=False)
    locb = forms.CharField(max_length=50,required=False)
    unit = forms.CharField(max_length=50)


    def __init__(self, *args, **kwargs):
        super(ststockmastereditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        # self.helper.form_id = "mislipedit"
        # self.helper.form_class = "mislipeditform"
        # self.helper.form_method = 'post'
        # self.helper.form_action = 'mislipedit'
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True

    def clean(self):
        cleaned_data = super(ststockmastereditForm, self).clean()
        print(self.cleaned_data)

    def clean_matgroup(self):
        matgrp = self.cleaned_data['matgroup']
        if verifyMatgrp(matgrp):
            return matgrp
        else:
            self.add_error('matgroup', forms.ValidationError('Mat Group not valid'))
        return matgrp

    def save_update(self, request):
        sql = 'update stmaster set ' + update_values_of_query(self,request) + ' where stockno=%r' % (self.cleaned_data['stockno'])
        print(sql)
        return runQuery('edssql', sql)

    def save_create(self, request):
        fields = ','.join(self.fields)

        sql = 'insert into stmaster (%s) values(%s)' % (insert_values_of_query(self, request))
        print(sql)
        # print(self.cleaned_data)
        return runQuery('edssql', sql)

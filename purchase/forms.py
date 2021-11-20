from django import  forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import  Submit,Layout,Div,Button,Fieldset,Field,HTML
import datetime
from django.forms import widgets

from purchase.formValidators_choices import *
from djangovue.form_base import baseform
class bformdatepicker(widgets.TextInput):
    template_name='mi_website/widgets/b-form-datepicker.html'



class poeditForm(baseform):
    year = forms.CharField(max_length=50)
    year.widget.attrs['readonly'] = True
    poid=forms.IntegerField(widget=forms.TextInput)
    poid.widget.attrs['readonly'] = True
    potype=forms.TypedChoiceField(choices=[(1,'indigenous'),(2,'imported')],coerce=int,initial=1)
    potype.widget.attrs['id'] = 'id_potype'
    pono=forms.IntegerField(widget=forms.TextInput)
    amendno=forms.IntegerField(widget=forms.TextInput,initial=0)
    amendno.widget.attrs['id'] = 'id_amendno'
    amendno.widget.attrs['readonly'] = True
    podate=forms.DateField(widget=bformdatepicker())
    #podate.widget.attrs['readonly'] = True
    suppcode=forms.ChoiceField(choices=suppcodechoices,)
    supprefno = forms.CharField(max_length=50)
    payterms = forms.CharField(max_length=50)
    despatch=forms.TypedChoiceField(choices=despatchchoices,coerce=int)
    despatchmode = forms.CharField(max_length=50,label="Transport",required=False)
    insurance = forms.CharField(max_length=50,required=False)
    currency = forms.TypedChoiceField(choices=currencychoices,coerce=int)
    price= forms.TypedChoiceField(choices=pricechoices,coerce=int)
    pfcharges= forms.CharField(max_length=50,label="P/F Charges")
    sgst=forms.FloatField(widget=forms.TextInput)
    cgst=forms.FloatField(widget=forms.TextInput)
    igst=forms.FloatField(widget=forms.TextInput)
    gstic = forms.CharField(max_length=50,label="GSTIC")
    revcharge = forms.CharField(max_length=50,label="Rev Charge")
    hsncode=forms.IntegerField(widget=forms.TextInput)
    discountapp=forms.BooleanField(label="Discount apply to all Items",initial=True)
    discountval=forms.FloatField(widget=forms.TextInput,label="Discount")
    inspection= forms.CharField(max_length=50,required=False)
    refprefix= forms.CharField(max_length=50,label="Prefix",initial="PINJ/4.2/")
    deliverynote= forms.CharField(widget=forms.Textarea(attrs={'rows':5}),max_length=200,label="Delivery note",required=False)
    bottomnote= forms.CharField(widget=forms.Textarea(attrs={'rows':5}),max_length=200,label="Bottom note")
    poreason= forms.CharField(widget=forms.Textarea(attrs={'rows':5}),max_length=200,label="PO Reason")
    adate=forms.DateField(widget=bformdatepicker(),label="A. date",required=False)
    arefno=forms.CharField(max_length=50,label="A. ref no",required=False)
    areason=forms.CharField(max_length=50,label="A. reason",required=False)
    abottomnote=forms.CharField(max_length=50,label="A. note",required=False)
    agentcode=forms.IntegerField(widget=forms.TextInput,label="Agent code",required=False)
    cd=forms.FloatField(widget=forms.TextInput,label="Custom duty",required=False)
    sd=forms.FloatField(widget=forms.TextInput,label="Special duty")
    interest=forms.FloatField(widget=forms.TextInput,label="Special duty",required=False)
    intper=forms.IntegerField(widget=forms.TextInput,label="Int. Per.",required=False)
    implicense=forms.CharField(max_length=50,label="License no",required=False)
    catcode=forms.CharField(max_length=50,label="Code",required=False)
    ccr=forms.IntegerField(widget=forms.TextInput,label="Currency conv. rate",required=False)





    def __init__(self, *args, **kwargs):
        super(poeditForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Div(
                Div('year', css_class="col-sm-3"),
                Div('potype', css_class="col-sm-3"),
                Div('poid', css_class="col-sm-2"),
                Div('pono', css_class="col-sm-3"),
                Div('amendno', css_class="col-sm-1"),
                css_class="row"
            ),
            Div(
                Div('podate', css_class="col-sm-3"),
                Div('suppcode',HTML("<div ref='suppcode_id'></div>"), css_class="col-sm-6"),
                
                Div('supprefno', css_class="col-sm-3"),
                
                css_class="row"
            ),
            Div(
                Div('payterms', css_class="col-sm-4"),
                Div('despatch', css_class="col-sm-4"),
                Div('despatchmode', css_class="col-sm-4"),

                css_class="row"
            ),
            Div(

                Div('insurance', css_class="col-sm-3"),
                Div('currency', css_class="col-sm-3"),
                Div('price', css_class="col-sm-3"),
                Div('pfcharges', css_class="col-sm-3"),
                css_class="row"
            ),
            Div(

                Div('sgst', css_class="col-sm-2"),
                Div('cgst', css_class="col-sm-2"),
                Div('igst', css_class="col-sm-2"),
                Div('gstic', css_class="col-sm-2"),
                Div('revcharge', css_class="col-sm-2"),
                Div('hsncode', css_class="col-sm-2"),
                css_class="row"
            ),
            Div(

                Div('discountapp', css_class="col-sm-2"),
                Div('discountval', css_class="col-sm-2"),
                Div('inspection', css_class="col-sm-2"),
                Div('refprefix', css_class="col-sm-2"),
                css_class="row"
            ),
             Div(

                Div('deliverynote', css_class="col-sm-4"),
                Div('bottomnote', css_class="col-sm-4"),
                Div('poreason', css_class="col-sm-4"),
               
                css_class="row"
            ),
             Div(

                Div('adate', css_class="col-sm-3"),
                Div('arefno', css_class="col-sm-2"),
                Div('areason', css_class="col-sm-2"),
                Div('abottomnote', css_class="col-sm-5"),
                css_class="row",
                id='amend',
            ),
            Div(

                Div('agentcode', css_class="col-sm-2"),
                Div('cd', css_class="col-sm-2"),
                Div('sd', css_class="col-sm-2"),
                Div('interest', css_class="col-sm-2"),
                Div('intper', css_class="col-sm-2"),
                id='import',
                css_class="row"
            ),
            Div(
                Div('ccr', css_class="col-sm-3"),
                Div('implicense', css_class="col-sm-5"),
                Div('catcode', css_class="col-sm-2"),
                id='importa',
                css_class="row"
            ),
        )
        
        self.helper['pono'].wrap(Field, ref="ref_pono")
        self.helper['suppcode'].wrap(Field, ref="ref_suppcode")
        
        #self.helper.layout[1][1].append(HTML("<div ref='suppcode_id'></div>"))

    def clean(self):
        cleaned_data=super(poeditForm,self).clean()
        print(cleaned_data)

        
    def clean_podate(self):
        #print('dtate')
        return datetime.datetime.strptime(str(self.cleaned_data['podate']), "%Y-%m-%d").strftime("%d-%b-%Y")

    def clean_adate(self):
        #print('dtate')
        return datetime.datetime.strptime(str(self.cleaned_data['adate']), "%Y-%m-%d").strftime("%d-%b-%Y")

    
        
    
    def save_update(self,request):

            sql='update po set '+self.update_values_of_query(request)+' where poid=%r '%(self.cleaned_data['poid'])
            print(sql)

            return self.runQuery('edssql', sql)

    def save_create(self,request):
        fields = ','.join(self.fields)

        sql = 'insert into po (%s) values(%s)' % ( self.insert_values_of_query(request))
        print(sql)
        # print(self.cleaned_data)
        return self.runQuery('edssql', sql)
class poitemeditForm(baseform):
    poid=forms.IntegerField(widget=forms.TextInput)
    poid.widget.attrs['readonly'] = True
    stockno = forms.CharField(max_length=50)
    stockno.widget.attrs['ref'] = 'ref_stockno'
    des= forms.CharField(widget=forms.Textarea(attrs={'rows':4}),max_length=200,label="Designation")
    des.widget.attrs['ref'] = 'ref_des'
    drwgno = forms.CharField(max_length=50,label="Drawing No",required=False,)
    drwgno.widget.attrs['ref'] = 'ref_drwgno'
    qty=forms.FloatField(widget=forms.TextInput,label="Qty",required=True)
    qty.widget.attrs['ref'] = 'ref_qty'
    rate=forms.FloatField(widget=forms.TextInput,label="Rate",required=True)
    ratebase=forms.IntegerField(widget=forms.TextInput,required=False,initial=1)
    unit=forms.CharField(max_length=50)
    unit.widget.attrs['ref'] = 'ref_unit'
    discount=forms.FloatField(widget=forms.TextInput,label="Discount",required=False)
    discountbase=forms.IntegerField(widget=forms.TextInput,label="Discount Base",required=False)
    mprno=forms.CharField(max_length=50,label="MPR No")
    mprno.widget.attrs['ref'] = 'ref_mprno'

    itemdelivery=forms.CharField(max_length=50,label="Delivery",required=False)
    isservice=forms.BooleanField(required=False,initial=False)
    #signal=forms.BooleanField(required=False,initial=False)
    def __init__(self, *args, **kwargs):
        super(poitemeditForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Div(
                Div('poid', css_class="col-sm-2"),
                Div('stockno', css_class="col-sm-4"),
                Div('drwgno', css_class="col-sm-4"),
                css_class="row"
            ),
             Div(
                Div('des', css_class="col-sm-6"),
                Div('mprno', css_class="col-sm-4"),
                Div('unit', css_class="col-sm-2"),
                css_class="row"
            ),
            Div(
                Div('qty', css_class="col-sm-2"),
                Div('rate', css_class="col-sm-2"),
                Div('ratebase', css_class="col-sm-2"),
                Div('discount', css_class="col-sm-2"),
                Div('discountbase', css_class="col-sm-3"),
                css_class="row"
            ),
             Div(
                Div('itemdelivery', css_class="col-sm-6"),
                
                css_class="row"
            ),
             Div(
               
                Div('isservice', css_class="col-sm-2"),
                #Div('signal', css_class="col-sm-2"),
                  
                css_class="row"
            ),
        )
    def clean(self):
        cleaned_data=super(poitemeditForm,self).clean()
        print(cleaned_data)

    def save_update(self,request):

        sql='update poitems set '+self.update_values_of_query(request)+' where poid=%r and stockno=%r'%(self.cleaned_data['poid'],self.cleaned_data['stockno'])
        print(sql)

        return self.runQuery('edssql', sql)

    def save_create(self,request):
        fields = ','.join(self.fields)

        sql = 'insert into poitems (%s) values(%s)' % ( self.insert_values_of_query(request))
        print(sql)
        # print(self.cleaned_data)
        return self.runQuery('edssql', sql)

class poauthForm(baseform):
    poid=forms.IntegerField(widget=forms.TextInput)
    poid.widget.attrs['readonly'] = True
    name = forms.CharField(max_length=50)
    name.widget.attrs['ref'] = 'ref_name'
    password = forms.CharField(widget=forms.PasswordInput,max_length=50)
    password.widget.attrs['ref'] = 'ref_password'

    
    def __init__(self, *args, **kwargs):
        super(poauthForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Div(
                Div('poid', css_class="col-sm-4"),
                
                css_class="row"
            ),
             Div(
                Div('name', css_class="col-sm-4"),
               
                css_class="row"
            ),
            Div(
                Div('password', css_class="col-sm-4"),
                
                css_class="row"
            ),
             
        )
    def clean(self):
        cleaned_data=super(poauthForm,self).clean()
        print(cleaned_data)

    def save_update(self,request):

        sql='update poauth set '+self.update_values_of_query(request)+' where poid=%r'%(self.cleaned_data['poid'])
        print(sql)

        return self.runQuery('edssql', sql)

    def save_create(self,request):
        fields = ','.join(self.fields)

        sql = 'insert into poauth (%s) values(%s)' % ( self.insert_values_of_query(request))
        print(sql)
        # print(self.cleaned_data)
        return self.runQuery('edssql', sql)










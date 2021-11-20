from django import  forms

class StockNoForm(forms.Form):
    stockno=forms.CharField(initial='')
    stockno.label='Stock No'
    stockno.help_text='Enter Stock no to search!'
from django import forms





class VolumeChangeForm(forms.Form):
    choices = [('increase', 'increase'), ('decrease', 'decrease')]
    user = forms.IntegerField(required=True)
    operation_type = forms.ChoiceField(choices=choices , required=True)
    size = forms.FloatField(required=True)
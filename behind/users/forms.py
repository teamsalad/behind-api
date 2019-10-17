from django import forms


class ConfirmPaymentTransactionForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    charging_points = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'vIntegerField'}),
        label='Charging points'
    )

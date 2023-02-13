from django import forms


class FindForm(forms.Form):
    start = forms.IntegerField(
        label='Введите номер павильона, в котором вы находитесь',
        max_value=80,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'style': 'width:100px'
            }
        )
    )
    finish = forms.IntegerField(
        label='Введите номер павильона, на котором хотите завершить маршрут',
        max_value=80,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'style': 'width:100px'
            }
        )
    )
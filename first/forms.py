from django import forms


class FindForm(forms.Form):
    start = forms.IntegerField(
        label='Введите номер павильона, в котором вы находитесь',
        max_value=38,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'style': 'width:100px'
            }
        )
    )
    finish = forms.IntegerField(
        label='Введите номер павильона, на котором хотите завершить маршрут',
        max_value=38,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'style': 'width:100px'
            }
        )
    )
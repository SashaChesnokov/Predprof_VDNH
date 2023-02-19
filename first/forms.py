from django import forms


class PointsForm(forms.Form):
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


class TimeForm(forms.Form):
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
    time = forms.IntegerField(
        label='Введите время, за которое хотите пройти маршрут',
        max_value=60,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'style': 'width:100px'
            }
        )
    )


class InterestForm(forms.Form):
    theme = forms.CharField(
        label='Введите тему маршрута',
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style': 'width:100px'
            }
        )
    )
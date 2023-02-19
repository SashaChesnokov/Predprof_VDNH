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


vote_type = [("без темы", "без темы"), ("наука", "наука"), ("выставка", "выставка"),
                 ("технологии", "технологии"), ("история", "история"),
                 ("архитектура", "архитектура"), ("фонтан", "фонтан"),
                 ("народы ссср", "народы ссср"), ("искусство", "искусство")]


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
    vote_type = forms.ChoiceField(
        label='Выберите тему маршрута',
        widget=forms.Select,
        choices=vote_type
    )


class InterestForm(forms.Form):

    vote_type = forms.ChoiceField(
        label='Выберите тему маршрута',
        widget=forms.Select,
        choices=vote_type
    )
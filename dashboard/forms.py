from django import forms
from .models import SnipeModel

GRADES = (
    ('0.5', '0.5'),
    ('1.0', '1.0'),
    ('1.5', '1.5'),
    ('1.8', '1.8'),
    ('2.0', '2.0'),
    ('2.5', '2.5'),
    ('3.0', '3.0'),
    ('3.5', '3.5'),
    ('4.0', '4.0'),
    ('4.5', '4.5'),
    ('5.0', '5.0'),
    ('5.5', '5.5'),
    ('6.0', '6.0'),
    ('6.5', '6.5'),
    ('7.0', '7.0'),
    ('7.5', '7.5'),
    ('8.0', '8.0'),
    ('8.5', '8.5'),
    ('9.0', '9.0'),
    ('9.2', '9.2'),
    ('9.4', '9.4'),
    ('9.6', '9.6'),
    ('9.8', '9.8'),
)


class SnipeForm(forms.ModelForm):
    class Meta:
        model = SnipeModel
        fields = [
            'gocollect_link',
            'price_percentage',
            'floor_price',
            'lowest_grade',
            'highest_grade',
            'negative_words',
            'positive_words',
            'title'
           # 'image',
        ]

        widgets = {
            'gocollect_link': forms.TextInput(attrs={
                'class': 'form-control form-control-solid',
                'id': 'go-collect-link',
            }),
            'price_percentage': forms.NumberInput(attrs={
                'class': 'form-control form-control-solid',
            }),
            'floor_price': forms.NumberInput(attrs={
                'class': 'form-control form-control-solid',
            }),
            'lowest_grade': forms.Select(attrs={
                'class': 'form-control form-control-solid',
            }, choices=GRADES),
            'highest_grade': forms.Select(attrs={
                'class': 'form-control form-control-solid',
            }, choices=GRADES),
            'negative_words': forms.TextInput(attrs={
                'class': 'form-control form-control-solid',
            }),
            'positive_words': forms.TextInput(attrs={
                'class': 'form-control form-control-solid'}),
            'title': forms.TextInput(attrs={
                'id': 'title',
            'class': 'form-control form-control-solid'}),
            #'image': forms.FileInput(attrs={
            #    'class': 'form-control form-control-solid',
            #})

        }

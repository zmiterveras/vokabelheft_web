from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Dictionary


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label="Электронная почта", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ChangeUserData(UserChangeForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label="Электронная почта", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


# class ChangeUserData(forms.ModelForm):
#     username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
#     email = forms.EmailField(label="Электронная почта", widget=forms.EmailInput(attrs={'class': 'form-input'}))
#     first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-input'}))
#     last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-input'}))
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name')


class DictionaryEngModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.lang = kwargs.pop('lang', None)
        super(DictionaryEngModelForm, self).__init__(*args, **kwargs)

    def clean_key(self):
        data = self.cleaned_data['key']
        keys = Dictionary.objects.filter(user=self.user).filter(language=self.lang).values_list('key', flat=True)
        if data in keys:
            raise ValidationError('Это слово есть в словаре')
        return data

    class Meta:
        model = Dictionary
        fields = ('key', 'keyfonetic', 'word', 'form', 'plural', 'part')


class DictionaryDeModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.lang = kwargs.pop('lang', None)
        super(DictionaryDeModelForm, self).__init__(*args, **kwargs)

    def clean_key(self):
        data = self.cleaned_data['key']
        keys = Dictionary.objects.filter(user=self.user).filter(language=self.lang).values_list('key', flat=True)
        if data in keys:
            raise ValidationError('Это слово есть в словаре')
        return data

    class Meta:
        CHOICES = (('', ''), ('der', 'der'), ('die', 'die'), ('das', 'das'))
        CHOICES_E = zip(['', '-e', '-¨e', '-en', '-n', '-¨er', '-¨en', '-¨', '-s', '-er'],
                        ['', '-e', '-¨e', '-en', '-n', '-¨er', '-¨en', '-¨', '-s', '-er'])
        model = Dictionary
        fields = ('key', 'keyfonetic', 'word', 'form', 'plural', 'part')
        widgets = {'keyfonetic': forms.Select(choices=CHOICES), 'plural': forms.Select(choices=CHOICES_E)}
        labels = {'keyfonetic': ('Артикль')}


class ChooseTrenningForm(forms.Form):
    CHOICES = [('1', 'Случайный выбор'), ('2', 'Последние 20'), ('3', 'Последние 40'), ('4', 'Постранично')]
    choose_trenning = forms.CharField(label='', widget=forms.RadioSelect(choices=CHOICES))


class ChoosePageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page', None)
        super(ChoosePageForm, self).__init__(*args, **kwargs)
        print('PAGE in Forms:', self.page)
        seits = range(1, self.page+1)
        self.fields['choose_page'].choices = zip(seits, seits)


    # seits = range(1, self.page)
    # CHOICES = zip(seits, seits)
    # CHOICES = [('1', 'Случайный выбор'), ('2', 'Последние 20'), ('3', 'Последние 40'), ('4', 'Постранично')]
    choose_page = forms.ChoiceField(label='', widget=forms.Select) #, choices=[('1', '1'), ('2', '2')])


class GetAnswersForm(forms.Form):
    answer = forms.CharField(label='', required=True)


class SearchForm(forms.Form):
    search = forms.CharField(label='', required=True) #, widget=forms.TextInput(attrs={'class': 'form-control me-2'}))









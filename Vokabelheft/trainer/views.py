# -*- coding: utf-8 -*-

import random
import time
import io

from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

from .forms import *
from .models import Dictionary, Dictionaries


# def index(request):
#     return render(request, 'index.html')


def my_serializer(query):
    my_dict = {}
    for obj in query:
        obj_list = []
        obj_list.append(obj.key)
        obj_list.append(obj.keyfonetic)
        obj_list.append(obj.word)
        obj_list.append(obj.form)
        obj_list.append(obj.plural)
        obj_list.append(obj.part.name)
        my_dict[obj.pk] = obj_list
    return my_dict


def get_question(request):
    keys = request.session['trening_keys']
    id = random.choice(keys)
    keys.remove(id)
    request.session['trening_keys'] = keys
    question = request.session['dictionary'][id]
    return question

def result_pdf(request):
    buffer= io.BytesIO()
    can = canvas.Canvas(buffer, bottomup=0)
    textobj = can.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont('Helvetica', 14)
    lines = [
        "Data: " + time.asctime(),
        "Set Question: " + str(request.session['amount_answer']),
        "Get true answers: " + str(request.session['amount_true']),
        "Get false answers: " + str(request.session['amount_false']),
    ]
    for line in lines:
        textobj.textLine(line)

    can.drawText(textobj)
    can.showPage()
    can.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='result.pdf')


class Index(generic.TemplateView):
    template_name = "index.html"


class About(generic.TemplateView):
    template_name = "about.html"


class ChooseTrenning(generic.TemplateView):
    form_class = ChooseTrenningForm
    template_name = "choose_trenning.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.request.session['amount_answer'] = 0
        self.request.session['amount_true'] = 0
        self.request.session['amount_false'] = 0
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            trening_keys = (list((self.request.session['dictionary']).keys()))
            trening_keys.sort(key=int)
            self.request.session['trening_keys'] = trening_keys
            print('Chosed:', form.cleaned_data)
            if form.cleaned_data['choose_trenning'] == '1':
                pass
            elif form.cleaned_data['choose_trenning'] == '2':
                if self.request.session['dict_count'] < 20:
                    pass
                else:
                      trening_keys = trening_keys[-20:]
                      self.request.session['trening_keys'] = trening_keys
            elif form.cleaned_data['choose_trenning'] == '3':
                if self.request.session['dict_count'] < 40:
                    pass
                else:
                    trening_keys = trening_keys[-40:]
                    self.request.session['trening_keys'] = trening_keys
            else:
                return redirect('choose_page')
            self.request.session['start_time'] = time.time()
            return redirect('get_answer')
        return redirect('home')


class ChoosePage(generic.TemplateView):
    form_class = ChoosePageForm
    template_name = 'choose_page.html'

    def get(self, request, *args, **kwargs):
        page_in = int(self.request.session['dict_count']/40)
        form = self.form_class(page=page_in)
        if self.request.GET.get('choose_page', None):
            page = int(self.request.GET.get('choose_page', None))
            start = (page - 1) * 40
            trening_keys = (list((self.request.session['dictionary']).keys()))
            trening_keys.sort(key=int)
            trening_keys = trening_keys[start:start+40]
            self.request.session['trening_keys'] = trening_keys
            return redirect('get_answer')
        return render(request, self.template_name, {'form': form})


class GetAnswer(generic.TemplateView):
    form_class = GetAnswersForm
    template_name = 'get_answer.html'

    def get(self, request, *args, **kwargs):
        if not self.request.session['trening_keys']:
            redirect('total_results')
        question = get_question(self.request)
        self.request.session['question'] = question
        # self.request.session['key'] = question[0]
        # self.request.session['word'] = question[2]
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        amount_answer = request.session.get('amount_answer', 0)
        amount_true = request.session.get('amount_true', 0)
        amount_false = request.session.get('amount_false', 0)
        if form.is_valid():
            answer = self.request.POST.get('answer', None)
            request.session['answer'] = answer
            request.session['amount_answer'] = amount_answer + 1
            if answer == self.request.session['question'][0]:
                self.request.session['result'] = True
                self.request.session['amount_true'] = amount_true + 1
            else:
                self.request.session['result'] = False
                self.request.session['amount_false'] = amount_false + 1
            return redirect('result')
            # print('answer: ', answer)
            # print('KEYS: ', self.request.session['trening_keys'])
            # if self.request.session['trening_keys']:
            #     return redirect('get_answer')
        else:
            return redirect('home')


class Result(generic.TemplateView):
    template_name = 'result.html'


class TotalResults(generic.TemplateView):
    template_name = 'total_results.html'

    def get(self, request, *args, **kwargs):
        seconds = int(time.time() - self.request.session['start_time'])
        minutes = '0'
        if seconds > 60:
            minutes = seconds // 60
            seconds = seconds % 60
        trenning_time = "%s %s %s %s" % (minutes, 'минут', seconds, 'секунд')
        if self.request.session['amount_true'] >= 0.8 * self.request.session['amount_answer']:
            estimate = 3
        elif self.request.session['amount_true'] < 0.4 * self.request.session['amount_answer']:
            estimate = 1
        else:
            estimate = 2
        return render(request, 'total_results.html', context={'trenning_time': trenning_time, 'estimate': estimate})


class SearchWords(generic.TemplateView):
    template_name = 'search.html'
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            search = self.request.POST.get('search', None)
            word = Dictionary.objects.filter(user=self.request.user).filter(language__exact=self.request.session['lang']).filter(key__exact=search).values()
            if word:
                return redirect('dictionary_detail/' + str(word[0]['id']))
            else:
                self.request.session['search_word'] = search
                return redirect('word_not_found')
        else:
            return redirect('home')


class WordNotFound(generic.TemplateView):
    template_name = 'word_not_found.html'


def logout_user(request):
    logout(request)
    return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy("home")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def form_validate(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class DictionaryListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 40

    def get_queryset(self):
        if not self.kwargs.get('lang'): # для пути без аргументов из добавления нового слова
            language = self.request.session['lang']
        else:
            language = self.kwargs['lang']
            self.request.session['lang'] = language
        self.request.session['dict_count'] = Dictionary.objects.filter(user=self.request.user).filter(language__exact=language).count()
        self.request.session['dictionary'] = my_serializer(Dictionary.objects.filter(user=self.request.user).filter(language__exact=language))
        print("Язык: ", self.request.session['lang'])
        return Dictionary.objects.filter(user=self.request.user).filter(language__exact=language)


class DictionaryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dictionary


class DictionaryCreate(LoginRequiredMixin, generic.CreateView):
    form_class = DictionaryEngModelForm
    model = Dictionary
    template_name = 'trainer/dictionary_form.html'
#     # initial = {'key': 'value',}
#     # fields = '__all__' # не разрешено вместе с  form_class [model+fields or form_class+[model]]
    success_url = reverse_lazy('dictionary_list')

    def get_form_kwargs(self):
        kwargs = super(DictionaryCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['lang'] = self.request.session['lang']
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user # значения для полей не добавленых в форму
        if self.request.session['lang'] == '1':
            form.instance.language = Dictionaries(id=1)
        else:
            form.instance.language = Dictionaries(id=2)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.session['lang'] == '1':
            request.session['fonetic'] = ('ə', 'əʊ', 'ɔ', 'ʌ', 'ʘ', 'ɶ', 'ʊ', 'ʃ', 'ɚ', 'ɳ', 'ʧ', 'ʤ', 'ʒ', 'ɜ')
        else:
            request.session['umlaut'] = ('ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü')
            self.form_class = DictionaryDeModelForm
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class DictionaryEngUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Dictionary
    form_class = DictionaryEngModelForm
    success_url = reverse_lazy('dictionary_list')


class DictionaryDeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Dictionary
    form_class = DictionaryDeModelForm
    success_url = reverse_lazy('dictionary_list')


class DictionaryDelete(LoginRequiredMixin, generic.DeleteView):
    model = Dictionary
    success_url = reverse_lazy('dictionary_list')










from django.urls import path
from django.urls import re_path
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    # path('', views.index, name='home'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('dictionary/<str:lang>', views.DictionaryListView.as_view(), name='dictionary_list'),
    path('dictionary', views.DictionaryListView.as_view(), name='dictionary_list'),
    path('dictionary_detail/<int:pk>', views.DictionaryDetailView.as_view(), name='dictionary-detail'),
    path('dictionary/create/', views.DictionaryCreate.as_view(), name='dictionary_create'),
    path('dictionaryeng/update/<int:pk>', views.DictionaryEngUpdate.as_view(), name='dictionaryeng_update'),
    path('dictionaryde/update/<int:pk>', views.DictionaryDeUpdate.as_view(), name='dictionaryde_update'),
    path('dictionary/delete/<int:pk>', views.DictionaryDelete.as_view(), name='dictionary_delete'),
    path('choose_trenning/<str:card>', views.ChooseTrenning.as_view(), name='choose_trenning'),
    path('choose_trenning', views.ChooseTrenning.as_view(), name='choose_trenning'),
    path('choose_page', views.ChoosePage.as_view(), name='choose_page'),
    path('get_answer', views.GetAnswer.as_view(), name='get_answer'),
    path('result', views.Result.as_view(), name='result'),
    path('total_results', views.TotalResults.as_view(), name='total_results'),
    path('search', views.SearchWords.as_view(), name='search'),
    path('word_not_found', views.WordNotFound.as_view(), name='word_not_found'),
    path('about', views.About.as_view(), name='about'),
    path('result_pdf', views.result_pdf, name='result_pdf'),
    path('cards', views.Cards.as_view(), name='cards'),

]

from django.urls import path
from . import views
urlpatterns = [
    path('bible_esv', views.Bible_ESV, name = 'bible_esv'),
    path('', views.setting, name = 'setting'),
    path('bible_chinese', views.bible_chinese, name = 'bible_chinese'),
    path('bible_korean', views.bible_korean, name = 'bible_korean'),
    path('bible_greek', views.bible_greek, name = 'bible_greek'),
    path('bible_hebrew', views.bible_hebrew, name = 'bible_hebrew'),
]
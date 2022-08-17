from django.urls import path
from . import views
urlpatterns = [
    path('',views.login, name='login' ),
    path('bible_esv', views.Bible_ESV, name = 'bible_esv'),
    path('setting', views.setting, name = 'setting'),
    path('bible_chinese', views.bible_chinese, name = 'bible_chinese'),
    path('bible_korean', views.bible_korean, name = 'bible_korean'),
    path('bible_greek', views.bible_greek, name = 'bible_greek'),
    path('bible_hebrew', views.bible_hebrew, name = 'bible_hebrew'),
    path('user_profile', views.user_profile, name = 'user_profile'),
    path('meditation', views.add_meditaion, name = 'meditation'),
    path('show_meditation', views.show_meditation, name = 'show_meditation'),
    path('meditation_like/<int:pk>',views.likes_view,name='meditation_like'),
    path('p_meditation',views.p_meditation,name='p_meditation'),
    path('u_meditation/<int:id>',views.u_meditation,name='u_meditation'),
    path('r_meditation/<int:id>',views.r_meditation,name='r_meditation'),
    path('del_replies/<int:id>',views.del_reply,name='del_replies')
    
]
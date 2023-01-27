from django.urls import path,re_path
from . import views
urlpatterns = [
    path('',views.login, name='login' ),
    path('bible_esv', views.Bible_ESV, name = 'bible_esv'),
    path('setting', views.setting, name = 'setting'),
    path('bible_chinese', views.bible_chinese, name = 'bible_chinese'),
    path('bible_korean', views.bible_korean, name = 'bible_korean'),
    path('orig_language', views.orig_language, name = 'orig_language'),
    path('user_profile', views.user_profile, name = 'user_profile'),
    path('meditation', views.add_meditaion, name = 'meditation'),
    path('show_meditation', views.show_meditation, name = 'show_meditation'),
    path('prayer',views.prayer, name= 'prayer'),
    path('my_prayer',views.my_prayer, name= 'my_prayer'),
    path('u_prayer/<int:id>',views.u_prayer, name= 'u_prayer'),
    path('show_prayer',views.show_prayer, name= 'show_prayer'),
    path('meditation_like/<int:pk>',views.likes_view,name='meditation_like'),
    path('p_meditation',views.p_meditation,name='p_meditation'),
    path('u_meditation/<int:id>',views.u_meditation,name='u_meditation'),
    path('r_meditation/<int:id>',views.r_meditation,name='r_meditation'),
    path('go_back/<int:id>',views.go_back,name='go_back'),
    path('del_replies/<int:id>',views.del_reply,name='del_replies'),
    path('copy_past',views.copy_past,name='copy_past'),
    path('iframe_test',views.iframe_test,name='iframe_test'),
    path('calendar',views.my_calendar,name='calendar'),
    path('add_event',views.add_event,name='add_event'),
    path('update', views.update, name='update'),
    path('remove', views.remove, name='remove')
]
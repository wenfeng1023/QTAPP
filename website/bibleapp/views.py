from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from .forms import DateSaveForm, MyMeditationForm, UpdateUserProfileForm, UserUpdateForm, PrayerForm
from .models import *
from django.db.models import Q
from django.db.models import IntegerField
from django.db.models.functions import Cast
import datetime as dt
from datetime import date
from django.contrib import messages
import os
from django.http import HttpResponseRedirect
from django.urls import reverse
import win32clipboard
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import numpy as np
import requests
import re
import os
from bs4 import BeautifulSoup
import json
# Create your views here.


@login_required(login_url='login')
def setting(request):
    obj, created = CustomSetting.objects.get_or_create(user=request.user)
    start_date = obj.start_date
    no_sunday = obj.no_sunday

    if request.method == 'POST':
        checks = request.POST.getlist('checks[]')
        obj.lang_1 = checks[0] if checks else "한국어"
        obj.lang_2 = ','.join(checks[1:]) if len(checks) > 1 else ""
        obj.bible_plan = request.POST['qt']
        obj.start_date = start_date
        obj.no_sunday = no_sunday
        obj.save()

        if obj.lang_1 == '영어':
            return redirect('bible_esv')
        elif obj.lang_1 == '한국어':
            return redirect('bible_korean')
        elif obj.lang_1 == '원어':
            return redirect('orig_language')
        else:
            return redirect('bible_chinese')

    return render(request, 'setting.html', {})



'''English Bible ESV Version '''


@login_required(login_url='login')
def Bible_ESV(request):
    try:
        bible_qt = CustomSetting.objects.get(user=request.user).bible_plan
        language_1 = CustomSetting.objects.get(user=request.user).lang_1
        language_2 = CustomSetting.objects.get(user=request.user).lang_2
        length = 1
    except:
        return redirect("setting")
    if request.method == 'POST':
        date = request.POST.get('date')
        f_date = date.replace('-', '')[2:]
        daily_bible = bible_plan(request, date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book
    else:
        date = dt.datetime.today().strftime("%Y-%m-%d")
        f_date = date.replace('-', '')[2:]
        daily_bible = bible_plan(request, date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book

    # yesterday = (dt.datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")

    if cont > 1:
        text = (daily_bible.Text).split("-")
        start_ch = int(text[0].split(":")[0])
        end_ch = int(text[1].split(":")[0])
        start_v = int(text[0].split(":")[1])
        end_v = int(text[1].split(":")[1])
        strat_id = (
            English_ESV.objects.annotate(
                Verse_as_int=Cast("Verse", IntegerField()),
                Chapter_as_int=Cast("Chapter", IntegerField()),
            )
            .get(Book_No=book_no, Chapter_as_int=start_ch, Verse_as_int=start_v)
            .id
        )
        end_id = (
            English_ESV.objects.annotate(
                Verse_as_int=Cast("Verse", IntegerField()),
                Chapter_as_int=Cast("Chapter", IntegerField()),
            )
            .get(Book_No=book_no, Chapter_as_int=end_ch, Verse_as_int=end_v).id
        )

        scripture = English_ESV.objects.annotate(
            Chapter_as_int=Cast("Chapter", IntegerField())
        ).filter(
            Book_No=book_no,
            Chapter_as_int__range=(start_ch, end_ch),
            id__range=(strat_id, end_id),
        )
    else:
        text = (daily_bible.Text).split(":")
        chapter = int(text[0])
        start_v = text[1].split("-")[0]
        end_v = text[1].split("-")[1]
        scripture = English_ESV.objects.annotate(
            Verse_as_int=Cast('Verse', IntegerField())
        ).filter(
            Book_No=book_no,
            Chapter=chapter,
            Verse_as_int__range=(start_v, end_v)
        )
    if language_2 == None or '영어' in language_2:
        fina_scripture = scripture
    else:
        language_2 = language_2.split(',')
        length = len(language_2)+1
        data = data = second_lang(request, language_2, book_no)
        if len(language_2) == 3:
            fina_scripture = zip(scripture, data[0], data[1], data[2])
        elif len(language_2) == 2:
            fina_scripture = zip(scripture, data[0], data[1])
        else:
            fina_scripture = zip(scripture, data[0])

    if language_1 == '영어' or 'bible_esv' in request.get_full_path():
        return render(request, 'bible.html', {'scripture': scripture, 'language_1': language_1,
                                              'language_2': language_2,
                                              'daily_verse': daily_verse, 'today': date,
                                              'book_name': book_name, 'f_date': f_date,
                                              'bible_qt': bible_qt, "fina_scripture": fina_scripture, 'length': length, 'book_no': int(book_no)})
    else:
        return scripture


'''
Chinese Bible Version
'''


@login_required(login_url='login')
def bible_chinese(request):
    try:
        bible_qt = CustomSetting.objects.get(user=request.user).bible_plan
        language_1 = CustomSetting.objects.get(user=request.user).lang_1
        language_2 = CustomSetting.objects.get(user=request.user).lang_2
        length = 1
    except:
        return redirect("setting")
    if request.method == 'POST':
        date = request.POST.get('date')
        f_date = date.replace('-', '')[2:]
        daily_bible = bible_plan(request, date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book
    else:
        date = dt.datetime.today().strftime("%Y-%m-%d")
        f_date = date.replace('-', '')[2:]
        daily_bible = bible_plan(request, date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book

    # yesterday = (dt.datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    book_name = Chinese_Bible.objects.filter(Book_No=book_no).first().Book
    if cont > 1:
        text = (daily_bible.Text).split("-")
        start_ch = int(text[0].split(":")[0])
        end_ch = int(text[1].split(":")[0])
        start_v = int(text[0].split(":")[1])
        end_v = int(text[1].split(":")[1])
        strat_id = (
            Chinese_Bible.objects.annotate(
                Verse_as_int=Cast("Verse", IntegerField()),
                Chapter_as_int=Cast("Chapter", IntegerField()),
            )
            .get(Book_No=book_no, Chapter_as_int=start_ch, Verse_as_int=start_v)
            .id
        )
        end_id = (
            Chinese_Bible.objects.annotate(
                Verse_as_int=Cast("Verse", IntegerField()),
                Chapter_as_int=Cast("Chapter", IntegerField()),
            )
            .get(Book_No=book_no, Chapter_as_int=end_ch, Verse_as_int=end_v).id
        )

        scripture = Chinese_Bible.objects.annotate(
            Chapter_as_int=Cast("Chapter", IntegerField())
        ).filter(
            Book_No=book_no,
            Chapter_as_int__range=(start_ch, end_ch),
            id__range=(strat_id, end_id),
        )
    else:
        text = (daily_bible.Text).split(":")
        chapter = int(text[0])
        start_v = text[1].split("-")[0]
        end_v = text[1].split("-")[1]
        scripture = Chinese_Bible.objects.annotate(
            Verse_as_int=Cast('Verse', IntegerField())
        ).filter(
            Book_No=book_no,
            Chapter=chapter,
            Verse_as_int__range=(start_v, end_v)
        )

    if language_2 == None or '중국어' in language_2:
        fina_scripture = scripture
    else:
        language_2 = language_2.split(',')
        length = len(language_2)+1
        data = data = second_lang(request, language_2, book_no)
        if len(language_2) == 3:
            fina_scripture = zip(scripture, data[0], data[1], data[2])
        elif len(language_2) == 2:
            fina_scripture = zip(scripture, data[0], data[1])
        else:
            fina_scripture = zip(scripture, data[0])

    if language_1 == '중국어' or 'bible_chinese' in request.get_full_path():
        return render(request, 'bible.html', {'scripture': scripture, 'language_1': language_1,
                                              'language_2': language_2,
                                              'daily_verse': daily_verse, 'today': date,
                                              'book_name': book_name, 'f_date': f_date,
                                              'bible_qt': bible_qt, "fina_scripture": fina_scripture, 'length': length, 'book_no': int(book_no)})
    else:
        return scripture
    # return render(request, 'bible.html', {'scripture': scripture,
    #                                       'daily_verse': daily_verse, 'today': date,
    #                                       'book_name': book_name, 'f_date': f_date,
    #                                       'bible_plan': bible_plan})


'''

Koran Bible. 개역한글
'''


def bible_korean(request):
    # yesterday = (dt.datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    if request.user.is_authenticated:
        try:
            bible_qt = CustomSetting.objects.get(user=request.user).bible_plan
            language_1 = CustomSetting.objects.get(user=request.user).lang_1
            language_2 = CustomSetting.objects.get(user=request.user).lang_2
            length = 1
        except:
            return redirect("setting")

    else:
        bible_qt = "매일성경 읽기"
        language_1 = "한국어"
        language_2 = None
        length = 1

    if request.method == 'POST':
        date = request.POST.get('date')
        f_date = date.replace('-', '')[2:]

        # if bible_plan == '생명의삶':
        #     daily_bible = living_life.objects.get(Date=date)
        # else:
        #     daily_bible = Daily_Bible.objects.get(Date=date)
        daily_bible = bible_plan(request, date)

        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book
    else:
        date = dt.datetime.today().strftime("%Y-%m-%d")
        f_date = date.replace('-', '')[2:]

        # if bible_plan == '생명의삶':
        #     daily_bible = living_life.objects.get(Date=date)
        # else:
        #     daily_bible = Daily_Bible.objects.get(Date=date)
        daily_bible = bible_plan(request, date)

        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book

    if cont > 1:
        text = (daily_bible.Text).split("-")
        start_ch = int(text[0].split(":")[0])
        end_ch = int(text[1].split(":")[0])
        start_v = int(text[0].split(":")[1])
        end_v = int(text[1].split(":")[1])
        strat_id = (
            Korean_Bible.objects.annotate(
                Verse_as_int=Cast("Verse", IntegerField()),
                Chapter_as_int=Cast("Chapter", IntegerField()),
            )
            .get(Book_No=book_no, Chapter_as_int=start_ch, Verse_as_int=start_v)
            .id
        )
        end_id = (
            Korean_Bible.objects.annotate(
                Verse_as_int=Cast("Verse", IntegerField()),
                Chapter_as_int=Cast("Chapter", IntegerField()),
            )
            .get(Book_No=book_no, Chapter_as_int=end_ch, Verse_as_int=end_v).id
        )

        scripture = Korean_Bible.objects.annotate(
            Chapter_as_int=Cast("Chapter", IntegerField())
        ).filter(
            Book_No=book_no,
            Chapter_as_int__range=(start_ch, end_ch),
            id__range=(strat_id, end_id),
        )
    else:
        text = (daily_bible.Text).split(":")
        chapter = int(text[0])
        start_v = text[1].split("-")[0]
        end_v = text[1].split("-")[1]
        scripture = Korean_Bible.objects.annotate(
            Verse_as_int=Cast('Verse', IntegerField())
        ).filter(
            Book_No=book_no,
            Chapter=chapter,
            Verse_as_int__range=(start_v, end_v)
        )
    if language_2 == None:
        fina_scripture = scripture
    else:
        language_2 = language_2.split(',')
        length = len(language_2)+1
        data = second_lang(request, language_2, book_no)
        if data:
            if len(language_2) == 3:
                fina_scripture = zip(scripture, data[0], data[1], data[2])
            elif len(language_2) == 2:
                fina_scripture = zip(scripture, data[0], data[1])
            else:
                fina_scripture = zip(scripture, data[0])
        else:
            fina_scripture = scripture

    if language_1 == '한국어' or 'bible_korean' in request.get_full_path():
        return render(request, 'bible.html', {'scripture': scripture, 'language_1': language_1,
                                              'language_2': language_2,
                                              'daily_verse': daily_verse, 'today': date,
                                              'book_name': book_name, 'f_date': f_date,
                                              'bible_qt': bible_qt, "fina_scripture": fina_scripture, 'length': length, 'book_no': int(book_no)})
    else:
        return scripture


'''
Biblical original languages(Hebrew and Greek)
'''


@login_required(login_url='login')
def orig_language(request):
    try:

        bible_qt = CustomSetting.objects.get(user=request.user).bible_plan
        language_1 = CustomSetting.objects.get(user=request.user).lang_1
        language_2 = CustomSetting.objects.get(user=request.user).lang_2
        length = 1
    except:
        return redirect("setting")

    if request.method == 'POST':
        date = request.POST.get('date')
        f_date = date.replace('-', '')[2:]
        daily_bible = bible_plan(request, date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book
    else:
        date = dt.datetime.today().strftime("%Y-%m-%d")
        f_date = date.replace('-', '')[2:]
        daily_bible = bible_plan(request, date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book

    if int(book_no) >= 40:
        book_name = Greek_Bible.objects.filter(Book_No=book_no).first().Book
        if cont > 1:
            text = (daily_bible.Text).split("-")
            start_ch = int(text[0].split(":")[0])
            end_ch = int(text[1].split(":")[0])
            start_v = int(text[0].split(":")[1])
            end_v = int(text[1].split(":")[1])
            strat_id = (
                Greek_Bible.objects.annotate(
                    Verse_as_int=Cast("Verse", IntegerField()),
                    Chapter_as_int=Cast("Chapter", IntegerField()),
                )
                .get(Book_No=book_no, Chapter_as_int=start_ch, Verse_as_int=start_v)
                .id
            )
            end_id = (
                Greek_Bible.objects.annotate(
                    Verse_as_int=Cast("Verse", IntegerField()),
                    Chapter_as_int=Cast("Chapter", IntegerField()),
                )
                .get(Book_No=book_no, Chapter_as_int=end_ch, Verse_as_int=end_v).id
            )

            scripture = Greek_Bible.objects.annotate(
                Chapter_as_int=Cast("Chapter", IntegerField())
            ).filter(
                Book_No=book_no,
                Chapter_as_int__range=(start_ch, end_ch),
                id__range=(strat_id, end_id),
            )
        else:
            text = (daily_bible.Text).split(":")
            chapter = int(text[0])
            start_v = text[1].split("-")[0]
            end_v = text[1].split("-")[1]
            scripture = Greek_Bible.objects.annotate(
                Verse_as_int=Cast('Verse', IntegerField())
            ).filter(
                Book_No=book_no,
                Chapter=chapter,
                Verse_as_int__range=(start_v, end_v)
            )

        if language_2 == None or '원어' in language_2:
            fina_scripture = scripture
        else:
            language_2 = language_2.split(',')
            length = len(language_2)+1
            data = data = second_lang(request, language_2, book_no)
            if len(language_2) == 3:
                fina_scripture = zip(scripture, data[0], data[1], data[2])
            elif len(language_2) == 2:
                fina_scripture = zip(scripture, data[0], data[1])
            else:
                fina_scripture = zip(scripture, data[0])

        if language_1 == '원어' or 'orig_language' in request.get_full_path():
            return render(request, 'bible.html', {'scripture': scripture, 'language_1': language_1,
                                                  'language_2': language_2,
                                                  'daily_verse': daily_verse, 'today': date,
                                                  'book_name': book_name, 'f_date': f_date,
                                                  'bible_qt': bible_qt, "fina_scripture": fina_scripture, 'length': length, 'book_no': int(book_no)})
        else:
            return scripture
    else:
        book_name = Hebrew_Bible.objects.filter(Book_No=book_no).first().Book
        if cont > 1:
            text = (daily_bible.Text).split("-")
            start_ch = int(text[0].split(":")[0])
            end_ch = int(text[1].split(":")[0])
            start_v = int(text[0].split(":")[1])
            end_v = int(text[1].split(":")[1])
            strat_id = (
                Hebrew_Bible.objects.annotate(
                    Verse_as_int=Cast("Verse", IntegerField()),
                    Chapter_as_int=Cast("Chapter", IntegerField()),
                )
                .get(Book_No=book_no, Chapter_as_int=start_ch, Verse_as_int=start_v)
                .id
            )
            end_id = (
                Hebrew_Bible.objects.annotate(
                    Verse_as_int=Cast("Verse", IntegerField()),
                    Chapter_as_int=Cast("Chapter", IntegerField()),
                )
                .get(Book_No=book_no, Chapter_as_int=end_ch, Verse_as_int=end_v).id
            )

            scripture = Hebrew_Bible.objects.annotate(
                Chapter_as_int=Cast("Chapter", IntegerField())
            ).filter(
                Book_No=book_no,
                Chapter_as_int__range=(start_ch, end_ch),
                id__range=(strat_id, end_id),
            )
        else:
            text = (daily_bible.Text).split(":")
            chapter = int(text[0])
            start_v = text[1].split("-")[0]
            end_v = text[1].split("-")[1]
            scripture = Hebrew_Bible.objects.annotate(
                Verse_as_int=Cast('Verse', IntegerField())
            ).filter(
                Book_No=book_no,
                Chapter=chapter,
                Verse_as_int__range=(start_v, end_v)
            )
        if language_2 == None or '원어' in language_2:
            fina_scripture = scripture
        else:
            language_2 = language_2.split(',')
            length = len(language_2)+1
            data = data = second_lang(request, language_2, book_no)
            if len(language_2) == 3:
                fina_scripture = zip(scripture, data[0], data[1], data[2])
            elif len(language_2) == 2:
                fina_scripture = zip(scripture, data[0], data[1])
            else:
                fina_scripture = zip(scripture, data[0])

        if language_1 == '원어' or 'orig_language' in request.get_full_path():
            return render(request, 'bible.html', {'scripture': scripture, 'language_1': language_1,
                                                  'language_2': language_2,
                                                  'daily_verse': daily_verse, 'today': date,
                                                  'book_name': book_name, 'f_date': f_date,
                                                  'bible_qt': bible_qt, "fina_scripture": fina_scripture, 'length': length, 'book_no': int(book_no)})
        else:
            return scripture


def login(request):
    if request.user.is_authenticated:
        obj = CustomSetting.objects.filter(user=request.user)
        if obj.exists():
            data = CustomSetting.objects.filter(user=request.user).first()
            language = data.lang_1
            if language == '영어':
                return redirect('bible_esv')
            elif language == '한국어':
                return redirect('bible_korean')
            elif language == '원어':
                return redirect('orig_language')
            elif language == '중국어':
                return redirect('bible_chinese')
            else:
                return redirect('setting')
        else:
            return redirect('setting')
    else:
        return render(request, 'login.html', {})


@login_required(login_url='login')
def user_profile(request):
    user = User_Profile.objects.get(user=request.user)
    old_img = user.profile_img.url
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        update_form = UpdateUserProfileForm(
            request.POST, request.FILES, instance=request.user.user_profile)
        if update_form.is_valid() and u_form.is_valid():
            if old_img != '/media/img/user.png':
                os.remove(os.path.join(user.profile_img.path))
            update_form.save()
            return redirect('login')
        else:
            print(update_form.errors)
    else:
        update_form = UpdateUserProfileForm(instance=request.user.user_profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {'update_form': update_form, 'u_form': u_form}
    return render(request, 'user_profile.html', context)


'''
    Add a New meditation
'''


@login_required(login_url='login')
def add_meditaion(request):
    data = CustomSetting.objects.filter(user=request.user).first()
    date = request.GET.get('new_date')
    # win32clipboard.OpenClipboard()
    # scripture_data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    # win32clipboard.CloseClipboard()
    # print(data)
    if request.method == 'POST':
        m_form = MyMeditationForm(request.POST)
        if m_form.is_valid():

            # create an unsave database object
            post = m_form.save(commit=False)
            # get users
            post.owner = request.user

            post.save()
            return redirect('login')
    else:
        if data.lang_1 == '한국어':
            today = dt.datetime.today().strftime("%Y-%m-%d")
            daily_bible = bible_plan(request, date)
            book_no = daily_bible.Book_No
            daily_verse = daily_bible.Text
            book_name = korean_title.objects.get(Book_ID=book_no).Book
            scripture = book_name + " " + daily_verse
            # scripture = scripture_data
            m_form = MyMeditationForm(
                initial={'scripture': scripture, 'choice': 1, 'created_date': date})
            return render(request, 'meditation.html', {'m_form': m_form})
        else:
            today = dt.datetime.today().strftime("%Y-%m-%d")
            daily_bible = bible_plan(request, date)
            book_no = daily_bible.Book_No
            book_name = English_ESV.objects.filter(
                Book_No=book_no).first().Book
            daily_verse = daily_bible.Text
            scripture = book_name + " " + daily_verse
            # scripture = scripture_data
            m_form = MyMeditationForm(
                initial={'scripture': scripture, 'choice': 1, 'created_date': date})
            return render(request, 'meditation.html', {'m_form': m_form})


'''
    add prayer request
'''


@login_required(login_url='login')
def prayer(request):
    if request.method == 'POST':
        P_form = PrayerForm(request.POST)
        if P_form.is_valid():
            # create an unsave database object
            post = P_form.save(commit=False)
            # get users
            post.owner = request.user

            post.save()
            return redirect('login')
    else:
        P_form = PrayerForm(initial={'choice': 1})
        return render(request, 'prayer.html', {"P_form": P_form})


'''
    show my prayer request
'''


@login_required(login_url='login')
def my_prayer(request):
    today = dt.datetime.today().strftime('%Y-%m-%d')
    year_date = list(Prayer.objects.filter(owner=request.user.id, created_date__year=str(
        dt.datetime.today().year)).values_list('created_date', flat=True))
    mark_date = []
    for md in year_date:
        mark_date.append(md.strftime("%Y-%m-%d").replace('-0', '-'))

    if request.method == 'POST':
        date = request.POST.get('date')
        obj = Prayer.objects.filter(
            owner=request.user.id, created_date__date=request.POST.get('date'))
        return render(request, 'p_prayer.html', {'obj': obj, 'date': date, 'mark_date': mark_date})
    else:
        obj = Prayer.objects.filter(
            owner=request.user.id, created_date__date=today)
        return render(request, 'p_prayer.html', {'obj': obj, 'date': today, 'mark_date': mark_date})


'''
    show all prayers
'''


@login_required(login_url='login')
def show_prayer(request):
    today = dt.datetime.today().strftime('%Y-%m-%d')
    year_date = list(Prayer.objects.filter(choice='1', created_date__year=str(
        dt.datetime.today().year)).values_list('created_date', flat=True))
    mark_date = []
    for md in year_date:
        mark_date.append(md.strftime("%Y-%m-%d").replace('-0', '-'))

    if request.method == 'POST':
        date = request.POST.get('date')
        obj = Prayer.objects.filter(
            choice='1', created_date__date=request.POST.get('date'))
        return render(request, 'show_prayer.html', {'obj': obj, 'date': date, 'mark_date': mark_date})
    else:
        obj = Prayer.objects.filter(
            choice='1', created_date__date=today)
        return render(request, 'show_prayer.html', {'obj': obj, 'date': today, 'mark_date': mark_date})


'''
    update my prayer
'''


@login_required(login_url='login')
def u_prayer(request, id):
    obj = Prayer.objects.get(id=id)
    if request.method == 'POST':
        update_form = PrayerForm(request.POST, instance=obj)
        if update_form.is_valid():
            # create an unsave database object
            post = update_form.save(commit=False)
            # get users
            post.owner = request.user
            post.save()
            return redirect('my_prayer')
    else:
        update_form = PrayerForm(instance=obj)
        return render(request, 'u_prayer.html', {'update_form': update_form})


'''
    show the user's meditation
'''


@login_required(login_url='login')
def show_meditation(request, *args, **kwargs):
    # print(slug)
    comments = Comments.objects.all()
    # form = DateSaveForm()
    obj = DateSave()
    year_date = list(My_Meditation.objects.filter(created_date__year=str(
        dt.date.today().year)).values_list('created_date', flat=True))
    mark_date = []
    for md in year_date:
        mark_date.append(md.strftime("%Y-%m-%d").replace('-0', '-'))
    if request.method == 'POST':
        data = DateSave.objects.all()
        if data.exists():
            data.delete()
            # input_date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
            obj.date = request.POST.get('date')
            obj.save()
            date = request.POST.get('date')
            meditation = My_Meditation.objects.filter(
                choice='1', created_date__date=request.POST.get('date'))

            return render(request, 'show_meditation.html', {'meditation': meditation, 'date': date, 'comments': comments, 'mark_date': mark_date})
    else:
        today = dt.datetime.today().strftime('%Y-%m-%d')
        data = DateSave.objects.all().first()
        re_date = request.GET.get('item')
        # Go back to specify page when someone relied messages
        if re_date != None:
            meditation = My_Meditation.objects.filter(
                choice='1', created_date=re_date)
            return render(request, 'show_meditation.html', {'meditation': meditation, 'date': re_date, 'comments': comments, 'mark_date': mark_date})

        elif re_date == None and data != None:
            meditation = My_Meditation.objects.filter(
                choice='1', created_date__date=today)
            date = data.date
            data.delete()
            obj.date = today
            obj.save()
            return render(request, 'show_meditation.html', {'meditation': meditation, 'date': today, 'comments': comments, 'mark_date': mark_date})
        else:
            obj.date = dt.datetime.today().strftime('%Y-%m-%d')
            obj.save()
            date = dt.datetime.today().strftime('%Y-%m-%d')
            meditation = My_Meditation.objects.filter(
                choice='1', created_date__date=today)
            return render(request, 'show_meditation.html', {'meditation': meditation, 'date': date, 'comments': comments, 'mark_date': mark_date})


'''
    show personal meditations
'''


@login_required(login_url='login')
def p_meditation(request):
    today = dt.datetime.today().strftime('%Y-%m-%d')
    year_date = list(My_Meditation.objects.filter(owner=request.user.id, created_date__year=str(
        dt.datetime.today().year)).values_list('created_date', flat=True))
    mark_date = []
    for md in year_date:
        mark_date.append(md.strftime("%Y-%m-%d").replace('-0', '-'))
    if request.method == 'POST':
        date = request.POST.get('date')
        obj = My_Meditation.objects.filter(
            owner=request.user.id, created_date__date=request.POST.get('date'))
        return render(request, 'p_meditation.html', {'obj': obj, 'date': date, 'mark_date': mark_date})
    else:
        obj = My_Meditation.objects.filter(
            owner=request.user.id, created_date__date=today)
        return render(request, 'p_meditation.html', {'obj': obj, 'date': today, 'mark_date': mark_date})


'''
    upatea personal meditaions
'''


@login_required(login_url='login')
def u_meditation(request, id):
    obj = My_Meditation.objects.get(id=id)
    if request.method == 'POST':
        update_form = MyMeditationForm(request.POST, instance=obj)
        if update_form.is_valid():
            # create an unsave database object
            post = update_form.save(commit=False)
            # get users
            post.owner = request.user
            post.save()
            return redirect('p_meditation')
    else:
        update_form = MyMeditationForm(instance=obj)
        return render(request, 'u_meditation.html', {'update_form': update_form})


'''
    Likes meditation
'''


def likes_view(request, pk):
    meditation = get_object_or_404(
        My_Meditation, id=request.POST.get('Meditation_id'))

    if meditation.likes.filter(id=request.user.id).exists():
        meditation.likes.remove(request.user)
    else:
        meditation.likes.add(request.user)
    return HttpResponseRedirect(reverse('iframe_test'))


'''
    reply meditaion
'''


def r_meditation(request, id):
    obj = My_Meditation.objects.get(id=id)
    comments = Comments.objects.filter(post=obj)
    date = obj.created_date.strftime('%Y-%m-%d')
    if request.method == 'POST':
        comments = Comments(owner=request.user, post=obj,
                            content=request.POST.get('textAreaExample'))
        comments.save()
        # return redirect(reverse('show_meditation')+ '?item='+date+'')
        return redirect('r_meditation', id=id)
    else:
        return render(request, 'r_meditation.html', {'obj': obj, 'comments': comments})


'''
    Go back specify page when someone click the button
'''


def go_back(request, id):
    obj = My_Meditation.objects.get(id=id)
    date = obj.created_date.strftime('%Y-%m-%d')
    return redirect(reverse('show_meditation') + '?item='+date+'')


'''
    delete replies
'''


def del_reply(request, id):
    comments = Comments.objects.get(id=id)
    comments.delete()
    post_id = comments.post.id

    return redirect('r_meditation', id=post_id)


def copy_past(request):
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    print(data)

    return render(request, 'copy_past.html', {'data': data})


def iframe_test(request):
    comments = Comments.objects.all()
    obj = DateSave()

    today = dt.datetime.today().strftime('%Y-%m-%d')
    data = DateSave.objects.all().first()

    if data != None:
        meditation = My_Meditation.objects.filter(
            choice='1', created_date__date=data.date)
        date = data.date
        return render(request, 'icontent.html', {'meditation': meditation, 'date': date, 'comments': comments})
    else:
        obj.date = dt.datetime.today().strftime('%Y-%m-%d')
        obj.save()
        date = dt.datetime.today().strftime('%Y-%m-%d')
        meditation = My_Meditation.objects.filter(
            choice='1', created_date__date=today)
        return render(request, 'icontent.html', {'meditation': meditation, 'date': today, 'comments': comments})


def my_calendar(request):
    events = AddEvents.objects.filter(user=request.user.id)
    return render(request, 'calendar.html', {'events': events})


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = AddEvents(user=request.user, name=str(title), start=start, end=end)
    event.save()
    return redirect('calendar')


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = AddEvents.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return redirect('calendar')


def remove(request):
    id = request.GET.get("id", None)
    event = AddEvents.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)


'''Deal with the second language'''


def second_lang(request, lang, book_no):
    data = []
    # date = dt.datetime.today().strftime("%Y-%m-%d")
    # daily_bible = bible_plan(request, date)
    # book_no = daily_bible.Book_No
    for l in lang:

        if l == '영어':
            data_1 = Bible_ESV(request)
            data.append(data_1)
        elif l == '중국어':
            data_2 = bible_chinese(request)
            data.append(data_2)
        elif l == '원어':
            data_3 = orig_language(request)
            data.append(data_3)
        else:
            data_4 = "orig_language(request)"
            data.append(data_4)
    return data


'''Deal with daily bible plan'''


def bible_plan(request, date):
    if request.user.is_authenticated:

        bible_plan = CustomSetting.objects.get(user=request.user).bible_plan

        if bible_plan == '생명의삶':
            daily_bible = living_life.objects.get(Date=date)
        else:
            daily_bible = Daily_Bible.objects.get(Date=date)
    else:
        daily_bible = Daily_Bible.objects.get(Date=date)
    return daily_bible


''''
PRS bible reading plan
'''

@login_required(login_url='login')
def prs_bible(request):

    obj, created = CustomSetting.objects.get_or_create(user=request.user)
    start_date = obj.start_date
    no_sunday = obj.no_sunday

    if start_date is None:

        if request.method == 'POST':

            # get the data by custom selected.
            date_string = request.POST.get('datepicker')
            sunday_check = request.POST.get('sundayCheck')

            # covert date from '%m/%d/%Y' to  '%Y-%m-%d'
            date_object = dt.datetime.strptime(date_string, "%m/%d/%Y")
            new_date_string = date_object.strftime("%Y-%m-%d")

            obj.user = request.user
            obj.start_date = new_date_string
            obj.no_sunday = sunday_check == 'true'
            obj.save(update_fields=['start_date', 'no_sunday'])

            # Calculating the number of days between dates
            start_date = dt.datetime.strptime(new_date_string, "%Y-%m-%d")
            today = dt.datetime.strptime(
                dt.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
            dalta = today-start_date
            num = str(dalta.days)

            # get PRS website's url
            url = "https://bible.prsi.org/ko/Player/getplaylist?playlistID=ac1fb6b0-158f-4725-8d57-47b730616466&sectionIndex=" + \
                num+"&presenterMode=false"

            # getting data from PRS website
            response = requests.get(url, verify=True)

            # coverting data
            result = response.json()
            soup = BeautifulSoup(result['HTML'], 'html.parser')
            
            # Find the first p tag with class "subheader"
            subheader = soup.find('p', {'class': 'subheader'})

            # Get the text content of the tag
            subtitle = subheader.text
            html = str(soup)

            # From here it will deal with audio for prs bible.
            # Extract data from td tags
            td_tags = soup.find_all('td', style='padding-left: 20px')
            td_list = [td.text for td in td_tags]
            my_list = [x for x in td_list if "분" not in x]
            book_list = ["".join(filter(str.isalpha, item)).strip() for item in my_list]

            chapter_list=[]
            for item in my_list:
                numbers = re.findall(r'\d+(?:-\d+)?', item)
                if len(numbers) > 1:
                    chapter_list.append('-'.join(numbers))
                else:
                    chapter_list.append(numbers[0])


            # Extract chapter list for OT and NT
            if '-' in chapter_list[1]:
                start, end = chapter_list[1].split("-")
                ot_chapter_list = list(range(int(start), int(end)+1))
            else:
                ot_chapter_list = chapter_list[1]
            
            if '-' in chapter_list[2]:
                
                start, end = chapter_list[2].split("-")
                nt_chapter_list = list(range(int(start), int(end)+1))
            else:
                nt_chapter_list = chapter_list[1]
                

            Book_num = korean_title.objects.filter(Book__in=book_list).values_list('Book_ID',flat=True)
            open_url = "https://bible.prsi.org/ko/Player/getaudiomedia?book=19&chapter="+chapter_list[0]+""
            end_url = "https://bible.prsi.org/ko/Player/getaudiomedia?book=19&chapter="+chapter_list[3]+""
            OT_url =[]
            NT_url =[]


            for num in Book_num:
                if num >=40 and num!=19:
                    for item in nt_chapter_list:
                        NT_url.append("https://bible.prsi.org/ko/Player/getaudiomedia?book="+str(num)+"&chapter="+str(item)+"")
                elif num!=19:
                    for item in ot_chapter_list:
                        OT_url.append("https://bible.prsi.org/ko/Player/getaudiomedia?book="+str(num)+"&chapter="+str(item)+"")

            # Get audio data from PRS website
            open_response = requests.get(open_url, verify=True)
            end_response = requests.get(end_url, verify=True)
            result_1 = open_response.json()
            result_2 = end_response.json()
            open_mp3 = result_1['mp3']
            end_mp3 =result_2['mp3']

            ot_mp3 =[]
            nt_mp3 =[]

            for url in OT_url:
                res = requests.get(url, verify=True)
                resul = res.json()
                ot_mp3.append(resul['mp3'])
            
            for url in NT_url:
                res = requests.get(url, verify=True)
                resul = res.json()
                nt_mp3.append(resul['mp3'])


            return render(request, 'prs_reading.html', {"html": html,"subtitle":subtitle,"open_mp3":open_mp3,"end_mp3":end_mp3,"ot_mp3":ot_mp3,"nt_mp3":nt_mp3})

        else:

            return render(request, 'prs_bible.html', {})
    else:

        new_date_string = start_date.strftime("%Y-%m-%d")
        start_date = dt.datetime.strptime(new_date_string, "%Y-%m-%d")
        today = dt.datetime.strptime(dt.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        delta = today - start_date
        num = str(delta.days)
        if no_sunday:
            num_sun = np.busday_count(new_date_string, today.strftime("%Y-%m-%d"), weekmask='Sun')
            num = str(delta.days - num_sun)

        # get PRS website's url
        url = "https://bible.prsi.org/ko/Player/getplaylist?playlistID=ac1fb6b0-158f-4725-8d57-47b730616466&sectionIndex=" + \
            num+"&presenterMode=false"

        # getting data from PRS website
        response = requests.get(url, verify=True)

        # coverting data
        result = response.json()
        soup = BeautifulSoup(result['HTML'], 'html.parser')
        html = str(soup)
        # Find the first p tag with class "subheader"
        subheader = soup.find('p', {'class': 'subheader'})
        subtitle = subheader.text
    

        # From here it will deal with audio for prs bible.
        # Extract data from td tags
        td_tags = soup.find_all('td', style='padding-left: 20px')
        td_list = [td.text for td in td_tags]
        my_list = [x for x in td_list if "분" not in x]
        book_list = ["".join(filter(str.isalpha, item)).strip() for item in my_list]

        chapter_list=[]
        for item in my_list:
            numbers = re.findall(r'\d+(?:-\d+)?', item)
            if len(numbers) > 1:
                chapter_list.append('-'.join(numbers))
            else:
                chapter_list.append(numbers[0])


        # Extract chapter list for OT and NT
        if '-' in chapter_list[1]:
            start, end = chapter_list[1].split("-")
            ot_chapter_list = list(range(int(start), int(end)+1))
        else:
            ot_chapter_list = chapter_list[1]
        
        if '-' in chapter_list[2]:
            
            start, end = chapter_list[2].split("-")
            nt_chapter_list = list(range(int(start), int(end)+1))
        else:
            nt_chapter_list = chapter_list[1]
            

        Book_num = korean_title.objects.filter(Book__in=book_list).values_list('Book_ID',flat=True)
        open_url = "https://bible.prsi.org/ko/Player/getaudiomedia?book=19&chapter="+chapter_list[0]+""
        end_url = "https://bible.prsi.org/ko/Player/getaudiomedia?book=19&chapter="+chapter_list[3]+""
        OT_url =[]
        NT_url =[]


        for num in Book_num:
            if num >=40 and num!=19:
                for item in nt_chapter_list:
                    NT_url.append("https://bible.prsi.org/ko/Player/getaudiomedia?book="+str(num)+"&chapter="+str(item)+"")
            elif num!=19:
                for item in ot_chapter_list:
                    OT_url.append("https://bible.prsi.org/ko/Player/getaudiomedia?book="+str(num)+"&chapter="+str(item)+"")

        # Get audio data from PRS website
        open_response = requests.get(open_url, verify=True)
        end_response = requests.get(end_url, verify=True)
        result_1 = open_response.json()
        result_2 = end_response.json()
        open_mp3 = result_1['mp3']
        end_mp3 =result_2['mp3']

        ot_mp3 =[]
        nt_mp3 =[]

        for url in OT_url:
            res = requests.get(url, verify=True)
            resul = res.json()
            ot_mp3.append(resul['mp3'])
        
        for url in NT_url:
            res = requests.get(url, verify=True)
            resul = res.json()
            nt_mp3.append(resul['mp3'])


        return render(request, 'prs_reading.html', {"html": html,"subtitle":subtitle,"open_mp3":open_mp3,"end_mp3":end_mp3,"ot_mp3":ot_mp3,"nt_mp3":nt_mp3})


'''
    Reset plan of prs bible
'''
def prs_reset(request):
    obj, created = CustomSetting.objects.get_or_create(user=request.user)
    obj.start_date = None
    obj.no_sunday = False

    obj.save()
    
    return redirect("prs_bible")
from email import message
from django.http import HttpResponse
from django.shortcuts import redirect, render
from matplotlib.pyplot import text
from soupsieve import select
from .forms import UpdateUserProfileForm,UserUpdateForm
from .models import *
from django.db.models import Q
from django.db.models import IntegerField
from django.db.models.functions import Cast
import datetime as dt
from django.contrib import messages
import os
# Create your views here.


def setting(request):
    if request.method == 'POST':
        select = request.POST['test']
        if select == '영어':
            return redirect('bible_esv')
        elif select == '한국어':
            return redirect('bible_korean')
        elif select == '그리스어(신약)':
            return redirect('bible_greek')
        elif select == '히브리어(국약)':
            return redirect('bible_hebrew')
        else:
            return redirect('bible_chinese')

    return render(request, 'setting.html', {})


'''English Bible ESV Version '''


def Bible_ESV(request):
    # verse = Hebrew.objects.filter(Book='Numbers')
    # for v in verse:
    #     verse = v.Text
    #     return HttpResponse(verse)
    # obj = Hebrew_Bible.objects.all()
    # obj.delete()
    # querysets = Q(book__icontains="43") & Q(
    #     chapter__icontains="1")& Q(
    #     content__range=('1','4'))
    today = dt.datetime.today().strftime("%Y-%m-%d")
    # yesterday = (dt.datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    daily_bible = Daily_Bible.objects.get(Date=today)
    book_no = daily_bible.Book_No
    cont = (daily_bible.Text).count(":")
    book_name = English_ESV.objects.filter(Book_No=book_no).first().Book
    daily_verse = daily_bible.Text
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

    return render(request, 'bible.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today,'book_name':book_name})

'''
Chinese Bible Version
'''


def bible_chinese(request):

    today = dt.datetime.today().strftime("%Y-%m-%d")
    # yesterday = (dt.datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    daily_bible = Daily_Bible.objects.get(Date=today)
    book_no = daily_bible.Book_No
    cont = (daily_bible.Text).count(":")
    daily_verse = daily_bible.Text
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

    return render(request, 'bible.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today,'book_name':book_name})


'''

Koran Bible. 개역한글
'''


def bible_korean(request):

    today = dt.datetime.today().strftime("%Y-%m-%d")
    # yesterday = (dt.datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    daily_bible = Daily_Bible.objects.get(Date=today)
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

    return render(request, 'bible.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today,'book_name':book_name})


'''
GreeK Bible(NT).
'''


def bible_greek(request):

    today = dt.datetime.today().strftime("%Y-%m-%d")
    # yesterday = (dt.datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    daily_bible = Daily_Bible.objects.get(Date=today)
    book_no = daily_bible.Book_No
    cont = (daily_bible.Text).count(":")
    daily_verse = daily_bible.Text
    book_name = Greek_Bible.objects.filter(Book_No=book_no).first().Book
    if int(book_no) >= 40:

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
            return render(request, 'bible_original.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today,'book_name':book_name})
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
            return render(request, 'bible_original.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today,'book_name':book_name})

    else:
        messages.info(request, "오늘 구약 말씀이 아니다.")

        return render(request, 'bible_original.html', {})


'''
Israeli Hebrew,
Modern Israeli Hebrew compilation from Westmister (OT) and Modern Hebrew(NT).

'''


def bible_hebrew(request):

    today = dt.datetime.today().strftime("%Y-%m-%d")
    # yesterday = (dt.datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    daily_bible = Daily_Bible.objects.get(Date=today)
    book_no = daily_bible.Book_No
    cont = (daily_bible.Text).count(":")
    daily_verse = daily_bible.Text
    book_name = Hebrew_Bible.objects.filter(Book_No=book_no).first().Book
    if int(book_no) < 40:
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
            return render(request, 'bible_original.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today,'book_name':book_name})
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
            return render(request, 'bible_original.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today,'book_name':book_name})
    else:
        messages.info(request,'오늘 구약 말씀이 아니다.')
        return render(request, 'bible_original.html', {})


def login (request):
    if request.user.is_authenticated:
        
        return redirect('setting')
    else:
        return render (request,'login.html',{})

def user_profile(request):
    user = User_Profile.objects.get(user=request.user)
    old_img = user.profile_img.url
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance=request.user)
        update_form = UpdateUserProfileForm(request.POST,request.FILES,instance=request.user.user_profile)
        if update_form.is_valid() and u_form.is_valid():
            if old_img != '/media/img/user.png':
                os.remove(os.path.join(old_img))
            update_form.save()
            return redirect('setting')
        else:
            print(update_form.errors)
    else:
        update_form = UpdateUserProfileForm(instance=request.user.user_profile)
        u_form = UserUpdateForm(instance=request.user)
    
    context={'update_form': update_form, 'u_form': u_form}
    return render(request, 'user_profile.html',context)

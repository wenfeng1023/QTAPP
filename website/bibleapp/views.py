from genericpath import exists
from msilib.schema import InstallExecuteSequence
from secrets import choice
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from .forms import DateSaveForm, MyMeditationForm, UpdateUserProfileForm, UserUpdateForm
from .models import *
from django.db.models import Q
from django.db.models import IntegerField
from django.db.models.functions import Cast
import datetime as dt
from datetime import datetime
from django.contrib import messages
import os
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def setting(request):
    obj = CustomSetting()
    if request.method == 'POST':
        data = CustomSetting.objects.filter(user= request.user)
        if data.exists():
            data.delete()
            select = request.POST['bible']
            obj.user = request.user
            obj.lang= select
            obj.bible_plan = request.POST['qt']
            obj.save()
        else:
            select = request.POST['bible']
            obj.user = request.user
            obj.lang= select
            obj.bible_plan = request.POST['qt']
            obj.save()


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

    return render(request, 'bible.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today, 'book_name': book_name})


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

    return render(request, 'bible.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today, 'book_name': book_name})


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

    return render(request, 'bible.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today, 'book_name': book_name})


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
            return render(request, 'bible_original.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today, 'book_name': book_name})
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
            return render(request, 'bible_original.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today, 'book_name': book_name})

    else:
        messages.info(request, "오늘 신약 말씀이 아니다.")

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
            return render(request, 'bible_original.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today, 'book_name': book_name})
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
            return render(request, 'bible_original.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': today, 'book_name': book_name})
    else:
        messages.info(request, '오늘 구약 말씀이 아니다.')
        return render(request, 'bible_original.html', {})


def login(request):
    if request.user.is_authenticated:
        obj = CustomSetting.objects.filter(user=request.user)
        if obj.exists():
            data = CustomSetting.objects.filter(user=request.user).first()
            language = data.lang
            if language == '영어':
                return redirect('bible_esv')
            elif language == '한국어':
                return redirect('bible_korean')
            elif language == '그리스어(신약)':
                return redirect('bible_greek')
            elif language == '히브리어(국약)':
                return redirect('bible_hebrew')
            else:
                return redirect('bible_chinese')
        else:
            return redirect('setting')
    else:
        return render(request, 'login.html', {})


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


def add_meditaion(request):
    m_form = MyMeditationForm()
    if request.method == 'POST':
        m_form = MyMeditationForm(request.POST)
        if m_form.is_valid():
            # create an unsave database object
            post = m_form.save(commit=False)
            # get users
            post.owner = request.user

            post.save()
            return redirect('setting')
    else:
        m_form = MyMeditationForm()
        return render(request, 'meditation.html', {'m_form': m_form})


'''
    show the user's meditation
'''


def show_meditation(request):

    # date = datetime(2022,8,5).strftime('%Y-%m-%d')
    # querysets = Q(created_date__date__icontains=today) and Q(
    #     choice='1')
    # # yesterday = dt.datetime.strptime(request.POST.get('date'),'%Y-%m-%d').strftime('%Y-%m-%d')
    # meditation = My_Meditation.objects.filter(choice='1',created_date__date=date).all()
    # return render (request, 'show_meditation.html',{'meditation':meditation})
    comments = Comments.objects.all()
    # form = DateSaveForm()
    obj = DateSave()

    if request.method == 'POST':
        data = DateSave.objects.all()
        if data.exists():
            data.delete()
            obj.date = request.POST.get('date')
            obj.save()
            date = request.POST.get('date')
            meditation = My_Meditation.objects.filter(
                choice='1', created_date__date=request.POST.get('date'))
            return render(request, 'show_meditation.html', {'meditation': meditation, 'date': date, 'comments': comments})
    else:
        today = dt.datetime.today().strftime('%Y-%m-%d')
        data = DateSave.objects.all().first()
        if data != None:
            meditation = My_Meditation.objects.filter(
                choice='1', created_date__date=data.date)
            date = data.date
            # data.delete()
            # obj.date= today
            # obj.save()

            return render(request, 'show_meditation.html', {'meditation': meditation, 'date': date, 'comments': comments})
        else:
            obj.date = dt.datetime.today().strftime('%Y-%m-%d')
            obj.save()
            date = dt.datetime.today().strftime('%Y-%m-%d')
            meditation = My_Meditation.objects.filter(
                choice='1', created_date__date=today)
            return render(request, 'show_meditation.html', {'meditation': meditation, 'date': date, 'comments': comments})
        # if data.date != today:
        #     today = data.date
        #     meditation = My_Meditation.objects.filter(choice='1',created_date__date=data.date)
        #     data.delete()

        #     data.date = dt.datetime.today().strftime('%Y-%m-%d')
        #     data.save()
        #     return render (request, 'show_meditation.html',{'meditation':meditation,'today':today,'comments':comments})
        # elif data.date == today:
        #     data.delete()
        #     meditation = My_Meditation.objects.filter(choice='1',created_date__date=today)
        #     obj.date =today
        #     obj.save()
        #     return render (request, 'show_meditation.html',{'meditation':meditation,'today':today,'comments':comments})


'''
    show personal meditations
'''


def p_meditation(request):
    obj = My_Meditation.objects.filter(owner=request.user.id)
    return render(request, 'p_meditation.html', {'obj': obj})


'''
    upatea personal meditaions
'''


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
    return HttpResponseRedirect(reverse('show_meditation'))


'''
    reply meditaion
'''


def r_meditation(request, id):
    obj = My_Meditation.objects.get(id=id)
    comments = Comments.objects.filter(post=obj)
    if request.method == 'POST':
        comments = Comments(owner=request.user, post=obj,
                            content=request.POST.get('textAreaExample'))
        comments.save()
        return redirect('r_meditation', id=id)
    else:
        return render(request, 'r_meditation.html', {'obj': obj, 'comments': comments})


'''
    delete replies
'''


def del_reply(request, id):
    comments = Comments.objects.get(id=id)
    comments.delete()
    post_id = comments.post.id

    return redirect('r_meditation', id=post_id)

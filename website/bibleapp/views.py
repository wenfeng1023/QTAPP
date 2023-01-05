from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from .forms import DateSaveForm, MyMeditationForm, UpdateUserProfileForm, UserUpdateForm, PrayerForm
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
import win32clipboard
from django.http import JsonResponse
# Create your views here.

def setting(request):
    obj = CustomSetting()
    if request.method == 'POST':
        data = CustomSetting.objects.filter(user=request.user)
        if data.exists():
            data.delete()
            select_1 = request.POST['lang_1']
            select_2 = request.POST['lang_2']
            obj.user = request.user
            obj.lang_1 = select_1
            obj.lang_2 = select_2
            obj.bible_plan = request.POST['qt']
            obj.save()
        else:
            select_1 = request.POST['lang_1']
            select_2 = request.POST['lang_2']
            obj.user = request.user
            obj.lang_1 = select_1
            obj.lang_2 = select_2
            obj.bible_plan = request.POST['qt']
            obj.save()

        if select_1 == '영어':
            return redirect('bible_esv')
        elif select_1 == '한국어':
            return redirect('bible_korean')
        elif select_1 == '그리스어(신약)':
            return redirect('bible_greek')
        elif select_1 == '히브리어(국약)':
            return redirect('bible_hebrew')
        else:
            return redirect('bible_chinese')

    return render(request, 'setting.html', {})


'''English Bible ESV Version '''


def Bible_ESV(request):
    bible_qt = CustomSetting.objects.get(user=request.user).bible_plan
    language_1 = CustomSetting.objects.get(user=request.user).lang_1
    language_2 = CustomSetting.objects.get(user=request.user).lang_2
    if request.method == 'POST':
        date = request.POST.get('date')
        f_date = date.replace('-', '')[2:]
        daily_bible = bible_plan(request,date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book
    else:
        date = dt.datetime.today().strftime("%Y-%m-%d")
        f_date = date.replace('-', '')[2:]
        daily_bible = bible_plan(request,date)
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
    if language_2 != "영어":
        data = second_lang(request, language_2)
        fina_scripture = zip(scripture, data)
    else:
        fina_scripture = scripture

    if language_1 == '영어':
        return render(request, 'bible.html', {'scripture': scripture, 'language_1': language_1,
                                              'language_2': language_2,
                                              'daily_verse': daily_verse, 'today': date,
                                              'book_name': book_name, 'f_date': f_date,
                                              'bible_qt': bible_qt, "fina_scripture": fina_scripture})
    else:
        return scripture


'''
Chinese Bible Version
'''


def bible_chinese(request):
    bible_qt = CustomSetting.objects.get(user=request.user).bible_plan
    language_1 = CustomSetting.objects.get(user=request.user).lang_1
    language_2 = CustomSetting.objects.get(user=request.user).lang_2
    if request.method == 'POST':
        date = request.POST.get('date')
        f_date = date.replace('-', '')[2:]
        daily_bible = bible_plan(request,date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book
    else:
        date = dt.datetime.today().strftime("%Y-%m-%d")
        f_date = date.replace('-', '')[2:]
        daily_bible = bible_plan(request,date)
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

    if language_2 != "중국어":
        data = second_lang(request, language_2)
        fina_scripture = zip(scripture, data)
    else:
        fina_scripture = scripture

    if language_1 == '중국어':
        return render(request, 'bible.html', {'scripture': scripture, 'language_1': language_1,
                                              'language_2': language_2,
                                              'daily_verse': daily_verse, 'today': date,
                                              'book_name': book_name, 'f_date': f_date,
                                              'bible_qt': bible_qt, "fina_scripture": fina_scripture})
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
    bible_qt = CustomSetting.objects.get(user=request.user).bible_plan
    language_1 = CustomSetting.objects.get(user=request.user).lang_1
    language_2 = CustomSetting.objects.get(user=request.user).lang_2
    if request.method == 'POST':
        date = request.POST.get('date')
        f_date = date.replace('-', '')[2:]

        # if bible_plan == '생명의삶':
        #     daily_bible = living_life.objects.get(Date=date)
        # else:
        #     daily_bible = Daily_Bible.objects.get(Date=date)
        daily_bible = bible_plan(request,date)

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
        daily_bible = bible_plan(request,date)

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
    if language_2 != "한국어":
        data = second_lang(request, language_2)
        fina_scripture = zip(scripture, data)
    else:
        fina_scripture = scripture

    if language_1 == '한국어':
        return render(request, 'bible.html', {'scripture': scripture, 'language_1': language_1,
                                              'language_2': language_2,
                                              'daily_verse': daily_verse, 'today': date,
                                              'book_name': book_name, 'f_date': f_date,
                                              'bible_qt': bible_qt, "fina_scripture": fina_scripture})
    else:
        return scripture


'''
GreeK Bible(NT).
'''


def bible_greek(request):

    if request.method == 'POST':
        date = request.POST.get('date')
        daily_bible = bible_plan(request,date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book
    else:
        date = dt.datetime.today().strftime("%Y-%m-%d")
        daily_bible = bible_plan(request,date)
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
            return render(request, 'bible_original.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': date, 'book_name': book_name})
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
            return scripture

    else:
        messages.info(request, "오늘 신약 말씀이 아니다,그리스어없다!!")
        scripture = "오늘 신약 말씀이 아니다,그리스어없다!!"
        return scripture

        # return render(request, 'bible_original.html', {'today': date, })


'''
Israeli Hebrew,
Modern Israeli Hebrew compilation from Westmister (OT) and Modern Hebrew(NT).

'''


def bible_hebrew(request):

    if request.method == 'POST':
        date = request.POST.get('date')
        daily_bible = bible_plan(request,date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book
    else:
        date = dt.datetime.today().strftime("%Y-%m-%d")
        daily_bible = bible_plan(request,date)
        book_no = daily_bible.Book_No
        cont = (daily_bible.Text).count(":")
        daily_verse = daily_bible.Text
        book_name = korean_title.objects.get(Book_ID=book_no).Book

    # yesterday = (dt.datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    if int(book_no) < 40:
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
            return render(request, 'bible_original.html', {'scripture': scripture, 'daily_verse': daily_verse, 'today': date, 'book_name': book_name})
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
            return scripture
    else:
        messages.info(request, '오늘 구약 말씀이 아니다,히브리어없다!')
        scripture = '오늘 구약 말씀이 아니다,히브리어없다!'
        return scripture
        
        # return render(request, 'bible_original.html', {'today': date, })


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
            daily_bible = bible_plan(request,date)
            book_no = daily_bible.Book_No
            daily_verse = daily_bible.Text
            book_name = korean_title.objects.get(Book_ID=book_no).Book
            scripture = book_name + " " + daily_verse
            # scripture = scripture_data
            m_form = MyMeditationForm(
                initial={'scripture': scripture, 'choice': 1,'created_date':date})
            return render(request, 'meditation.html', {'m_form': m_form})
        else:
            today = dt.datetime.today().strftime("%Y-%m-%d")
            daily_bible = bible_plan(request,date)
            book_no = daily_bible.Book_No
            book_name = English_ESV.objects.filter(
                Book_No=book_no).first().Book
            daily_verse = daily_bible.Text
            scripture = book_name + " " + daily_verse
            # scripture = scripture_data
            m_form = MyMeditationForm(
                initial={'scripture': scripture, 'choice': 1,'created_date':date})
            return render(request, 'meditation.html', {'m_form': m_form})


'''
    add prayer request
'''


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


def second_lang(request, lang):
    if lang == '영어':
        data = Bible_ESV(request)
        return data
    elif lang == '한국어':
        data = bible_korean(request)
        return data
    elif lang == '중국어':
        data = bible_chinese(request)
        return data
    elif lang == '히브리어(국약)':
        data = bible_hebrew(request)
        return data
    else:
        data = bible_greek(request)
        return data

'''Deal with daily bible plan'''
def bible_plan(request,date):
    bible_plan = CustomSetting.objects.get(user=request.user).bible_plan

    if bible_plan == '생명의삶':
        daily_bible = living_life.objects.get(Date=date)
    else:
        daily_bible = Daily_Bible.objects.get(Date=date)
    return daily_bible
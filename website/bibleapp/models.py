# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from pickle import TRUE
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.forms import NullBooleanField



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'




class Hebrew_Bible(models.Model):
    Book = models.CharField(max_length=100)
    Book_No = models.CharField(max_length=100)
    Chapter = models.CharField(max_length=100)
    Verse = models.CharField(max_length=100)
    Text = models.TextField()

    def __str__(self):
        return self.Book

class Chinese_Bible(models.Model):
    Book = models.CharField(max_length=100)
    Book_No = models.CharField(max_length=100)
    Chapter = models.CharField(max_length=100)
    Verse = models.CharField(max_length=100)
    Text = models.TextField()
    
    
    def __str__(self):
        return self.Book

class Korean_Bible(models.Model):
    Book = models.CharField(max_length=100)
    Book_No = models.CharField(max_length=100)
    Chapter = models.CharField(max_length=100)
    Verse = models.CharField(max_length=100)
    Text = models.TextField()

    def __str__(self):
        return self.Book

class Greek_Bible(models.Model):
    Book = models.CharField(max_length=100)
    Book_No = models.CharField(max_length=100)
    Chapter = models.CharField(max_length=100)
    Verse = models.CharField(max_length=100)
    Text = models.TextField()

    def __str__(self):
        return self.Book

class English_ESV(models.Model):
    Book = models.CharField(max_length=100)
    Book_No = models.CharField(max_length=100)
    Chapter = models.CharField(max_length=100)
    Verse = models.CharField(max_length=100)
    Text = models.TextField()

    def __str__(self):
        return self.Book

class Daily_Bible(models.Model):
    Book_No = models.CharField(max_length=100)
    Text = models.CharField(max_length=100)
    Date = models.CharField(max_length=50)

    def __str__(self):
        return self.Date
class korean_title(models.Model):
    Book_ID = models.IntegerField()
    Book = models.CharField(max_length=50)

    def __str__(self):
        return self.Book

class User_Profile(models.Model):
    user = models.OneToOneField(User, null= True, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank = True, null= True)
    phoneNo = models.CharField(max_length=100, blank=True, null=True)
    self_introduce = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(upload_to= 'img',blank=True, null=True,default = "img/user.png")

    class Meta:
        verbose_name = 'user_profile'
        verbose_name_plural = 'user_profile'
    
    def __str__(self):
        return self.user.username
'''
    Add meditation messeages model 
    This model save uers' messsages about their meditation
'''
class My_Meditation(models.Model):
    owner = models.ForeignKey(User,null= True,on_delete=models.CASCADE)
    scripture = models.TextField(blank=True, null=True) 
    choice = models.CharField(max_length=10,default='1')
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes = models.ManyToManyField(User, related_name='meditation_like')



    def number_of_likes(self):
        return self.likes.count()
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'Meditation'
'''
    this model save user's replies
'''
class Comments(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(My_Meditation,on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering= ('-created_date',)
        verbose_name = 'Comment'
'''
    this model save date when user selects date for display meditation or scripure.
    
'''
class DateSave(models.Model):
    date = models.CharField(max_length=50, blank=TRUE,null=True)
    class Meta:
        verbose_name = 'DateSave'

'''
    this model save user's setting.
'''
class CustomSetting(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    lang = models.CharField(max_length=50)
    bible_plan = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'CustomSetting'

'''
    Adding event in Calendar
'''
class AddEvents(models.Model):
    user = models.ForeignKey(User, null= True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.CharField(max_length=50,null=True,blank=True)
    end = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.name



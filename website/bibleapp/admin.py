from django.contrib import admin
from .models import*
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class KoreanCAdmin(ImportExportModelAdmin):
    pass

class HebrewAdmin(ImportExportModelAdmin):
    pass

class Chines_BibleAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Hebrew_Bible,HebrewAdmin)
admin.site.register(Chinese_Bible,Chines_BibleAdmin)
admin.site.register(Korean_Bible,Chines_BibleAdmin)
admin.site.register(Greek_Bible,Chines_BibleAdmin)
admin.site.register(English_ESV,Chines_BibleAdmin)
admin.site.register(Daily_Bible,Chines_BibleAdmin)
admin.site.register(korean_title,Chines_BibleAdmin)

from django.contrib import admin
from .models import Account
from .models import AccountToken
from .models import MstClass
from .models import MstCompany
from .models import MstQualification
from .models import MstOS
from .models import MstLanguage
from .models import MstTool
from .models import MstDB
from .models import TblPerson
from .models import TblQualification
from .models import TblCareer

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'is_staff')   
admin.site.register(Account, AccountAdmin)

class AccountTokenAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'token', 'access_datetime')
admin.site.register(AccountToken, AccountTokenAdmin)

class MstClassAdmin(admin.ModelAdmin):
    list_display = ('class_cd', 'class_name', 'type_1', 'type_2', 'type_3')
admin.site.register(MstClass, MstClassAdmin)

class MstCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_cd', 'seq_no', 'company_name')
admin.site.register(MstCompany, MstCompanyAdmin)

class MstQualificationAdmin(admin.ModelAdmin):
    list_display = ('qualification_cd', 'seq_no', 'qualification_name')
admin.site.register(MstQualification, MstQualificationAdmin)

class MstOSAdmin(admin.ModelAdmin):
    list_display = ('os_cd', 'os_name')
admin.site.register(MstOS, MstOSAdmin)

class MstLanguageAdmin(admin.ModelAdmin):
    list_display = ('language_cd', 'language_name')
admin.site.register(MstLanguage, MstLanguageAdmin)

class MstToolAdmin(admin.ModelAdmin):
    list_display = ('tool_cd', 'tool_name')
admin.site.register(MstTool, MstToolAdmin)

class MstDBAdmin(admin.ModelAdmin):
    list_display = ('db_cd', 'db_name')
admin.site.register(MstDB, MstDBAdmin)

class TblPersonAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'last_name', 'first_name')
admin.site.register(TblPerson, TblPersonAdmin)

class TblQualificationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'qualification_cd', 'acquisition_date')
admin.site.register(TblQualification, TblQualificationAdmin)

class TblCareerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'career_no', 'start_date', 'project_name')
admin.site.register(TblCareer, TblCareerAdmin)
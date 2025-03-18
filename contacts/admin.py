from django.contrib import admin
from .models import (
    CompanyInfo,
    PrivacyPolicy, 
    PrivacyPolicyParagraph,
    DocumentationSection, 
    DocumentationFile,
    PopularQuestion,
    Partner,
    WorkStage,
    CityInfo,
)


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin): 
    list_display = ['__str__']


@admin.register(CityInfo) 
class CityInfoAdmin(admin.ModelAdmin): 
    list_display = ['name', 'phone', 'email']
    

class PrivacyPolicyParagraphInline(admin.TabularInline):
    model = PrivacyPolicyParagraph
    extra = 1  
    verbose_name = "Абзац"
    verbose_name_plural = "Абзацы"


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin): 
    list_display = ['__str__']
    inlines = [PrivacyPolicyParagraphInline]


class DocumentationFileAdminInline(admin.TabularInline):
    model = DocumentationFile
    extra = 1  
    verbose_name = 'файл документации'
    verbose_name_plural = 'файлы документации'


@admin.register(DocumentationSection)
class DocumentationSectionAdmin(admin.ModelAdmin): 
    list_display = ['__str__']
    inlines = [DocumentationFileAdminInline]


@admin.register(PopularQuestion)
class PopularQuestionAdmin(admin.ModelAdmin): 
    list_display = ['question', 'answer']
    search_fields = ['question', 'answer']


    
@admin.register(Partner)
class PopularQuestionAdmin(admin.ModelAdmin): 
    list_display = ['company_name']
    search_fields = ['company_name', 'company_member']


@admin.register(WorkStage)
class WorkStageAdmin(admin.ModelAdmin): 
    list_display = ['name']
    search_fields = ['name', 'description']
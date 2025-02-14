from django.contrib import admin
from .models import (
    CompanyInfo,
    PrivacyPolicy, 
    PrivacyPolicyParagraph,
)


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin): 
    list_display = ['__str__']
    

class PrivacyPolicyParagraphInline(admin.TabularInline):
    model = PrivacyPolicyParagraph
    extra = 1  
    verbose_name = "Абзац"
    verbose_name_plural = "Абзацы"


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin): 
    list_display = ['__str__']
    inlines = [PrivacyPolicyParagraphInline]
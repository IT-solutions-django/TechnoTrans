from django.shortcuts import render
from django.views import View 
from .models import (
    CompanyInfo, 
    PrivacyPolicy,
    DocumentationSection, 
    DocumentationFile,
    Partner,
    WorkStage,
)


class AboutCompanyView(View): 
    template_name = 'contacts/about-company.html'

    def get(self, request): 
        company_info = CompanyInfo.get_instance()
        partners = Partner.objects.all()
        stages = WorkStage.objects.all()

        context = {
            'company_info': company_info,
            'partners': partners,
            'stages': stages,
        }

        return render(request, self.template_name, context)
    

class PrivacyPolicyView(View): 
    template_name = 'contacts/privacy_policy.html' 

    def get(self, request): 
        privacy_policy =  PrivacyPolicy.get_instance()

        context = {
            'privacy_policy': privacy_policy,
        }

        return render(request, self.template_name, context)
    

class DocumentationView(View): 
    template_name = 'contacts/documentation.html' 

    def get(self, request): 
        doc_sections = DocumentationSection.objects.all()

        context = {
            'doc_sections': doc_sections,
        }

        return render(request, self.template_name, context)
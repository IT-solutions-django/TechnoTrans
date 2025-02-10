from django.shortcuts import render
from django.views import View 
from .models import CompanyInfo


class AboutCompanyView(View): 
    template_name = 'contacts/about-company.html'

    def get(self, request): 
        company_info = CompanyInfo.get_instance()

        context = {
            'company_info': company_info,
        }
        return render(request, self.template_name, context)
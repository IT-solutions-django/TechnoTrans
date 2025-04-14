from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views import View 
from .models import (
    CompanyInfo, 
    PrivacyPolicy,
    DocumentationSection, 
    Partner,
    WorkStage,
)
from home.forms import CargoTransportationForm


class AboutCompanyView(TemplateView): 
    template_name = 'contacts/about-company.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['company_info'] = CompanyInfo.get_instance()
        context['partners'] = Partner.objects.all() 
        context['stages'] = WorkStage.objects.all()

        return context
    

class PrivacyPolicyView(TemplateView):
    template_name = 'contacts/privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['privacy_policy'] = PrivacyPolicy.get_instance()
        return context
    

class DocumentationView(ListView):
    model = DocumentationSection
    template_name = 'contacts/documentation.html'
    context_object_name = 'doc_sections'


class ContactsView(View): 
    template_name = 'contacts/contacts.html' 

    def get(self, request): 
        return render(request, self.template_name, )
    

class CargoTransportationView(View): 
    template_name = 'contacts/cargo_transportation.html'

    def get(self, request): 
        cargo_form = CargoTransportationForm(request.GET)
        context = {
            'cargo_form': cargo_form
        }
        return render(request, self.template_name, context)
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from allocation.models import * 
from django.forms import modelformset_factory, formset_factory, modelform_factory, ModelForm
from django.views import generic
from django.views.generic.edit import *
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login
from django import forms
import csv
from django.urls import reverse_lazy
from django.utils import lru_cache
from django.utils._os import upath
from django.utils.encoding import force_text
from django.utils.functional import lazy
from django.utils.html import format_html
from django.utils.module_loading import import_string
from django.utils.six import string_types, text_type
from django.utils.translation import ugettext as _, ungettext
from django.contrib.auth import *
from allocation.forms import *
from alloc import *
from difflib import SequenceMatcher

from django.core.mail import send_mail
from django.core.mail import EmailMessage

from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)


# def send_mail(request):
# 	# send_mail('Subject here', 'Here is the message.', settings.EMAIL_HOST_USER,['to@example.com'], fail_silently=False)
# 	email = EmailMessage(
#     'subject_message',
#     'content_message',
#     'sender smtp gmail' +'<codemafia123@gmail.com>',
#     ['codemafia123@gmail.com'],)
# 	email.send()
# 	return HttpResponse("success")

def signup(request):
    if request.method == 'POST':
        form = InstiForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff=True
            user.save()
            new_insti=Institute(name=user.username)
            new_insti.save()
            return HttpResponseRedirect('/allocation/admin')
    else:
        form = InstiForm()
    return render(request, 'registration/register.html', {'form': form})


## View for the button 'Allocate'
# @brief On clicking the button 'Allocate' user is directed to this view and its url "/allocation/button_action" 
def button_action(request):
    institute=request.user.username #< login institute name
    allocator(institute) #< calls the function allocator in 'alloc.py'
    return HttpResponseRedirect("/allocation/admin") 

## View for the button 'Upload' in choice_list.html
# @brief On clicking the button 'Upload' all the .csv choices are validated and the uploaded
def choice_make(request):
    if request.method == "POST":
        csvfile = request.FILES['myfile'] #< Uploaded csv file
        file_data = csvfile.read().decode("utf-8") 
        lines = file_data.split("\n") #< split the csv file into lines
        user_name = request.user.username #< logged in institute name
        institute = get_object_or_404(Institute, name=user_name) #< Institute object corresponding to logged in institute
        repeated = [] #< this list keeps track of repeated choices
        for line in lines:
            line = line.split(',')
            number = len(line)
            if number != 2: #< If the number of columns is not equal to two then display error
            	return HttpResponse("Incorrect data format in uploaded .csv file.")
            existing_no = institute.choices.filter(choice_name=line[0]) #< Get existing choices(if exist) of the particular institute 
            if existing_no.count() != 0:
            	repeated.append(line[0])
        if len(repeated) != 0: #< If there exists Repeating choices then display all the repeated choices
        	str = ""
        	for rep in repeated:
        		str += rep + "," 
        	return HttpResponse(".csv file has choices: '"+ str + "' that already exists")
        for line in lines:
            line =  line.split(',')
            tmp = institute.choices.create(choice_name=line[0],capacity=line[1])
            tmp.save()
        return HttpResponseRedirect("/allocation/admin/choices") 
    return HttpResponse("Error") #< If not a 'POST' query then display error

## Django function for getting default password validators
@lru_cache.lru_cache(maxsize=None)
def get_default_password_validators():
    return get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)


def get_password_validators(validator_config):
    validators = []
    for validator in validator_config:
        try:
            klass = import_string(validator['NAME'])
        except ImportError:
            msg = "The module in NAME could not be imported: %s. Check your AUTH_PASSWORD_VALIDATORS setting."
            raise ImproperlyConfigured(msg % validator['NAME'])
        validators.append(klass(**validator.get('OPTIONS', {})))

    return validators

## View for the button 'Upload' in applciant_list.html 
def applicant_make(request):
    if request.method == "POST":
        csvfile = request.FILES['myfile'] #< Uploaded csv file
        file_data = csvfile.read().decode("utf-8")
        user_name = request.user.username #< Name of the logged in institute
        institute = get_object_or_404(Institute, name=user_name) #< Institute object corresponding to the logged in institute
        lines = file_data.split("\n") #< splits csv file into lines 
        rep_users = [] #< This list keeps track of the repeated users
        rep_applicant = [] #< This list keeps track of the repeated applicants
        errors = [] #< This list keeps track of the users with invalid passwords
        for line in lines:
        	line = line.split(',')
        	number = len(line)
        	if number != 4: #< Checks whether the number of columns is equal to 4 or not
        		return HttpResponse("Incorrect data format in uploaded .csv file")
        	existing_no_app = institute.applicants.filter(name = line[0]) #< Query set of applicants that already exist and match with the name of the applicant in csv file
        	existing_no_user = User.objects.filter(username=line[0]) #< Query set of users that already exist and match with the name of the applicant in csv file
        	if existing_no_app.count() != 0: 
        		rep_applicant.append(line[0])

        	if existing_no_user.count() != 0:
        		rep_users.append(line[0])

       		password_validators = get_default_password_validators() #< Get validators for validating the passwords
       		for validator in password_validators:
       			try:
        			validator.validate(line[3])
        		except ValidationError as error:
        			errors.append(line[0])
        if len(rep_applicant) != 0: #< if there already exist applicants matching our .csv file
        	str = ""
        	for appl in rep_applicant:
        		str += appl + "," 
        	return HttpResponse(".csv file has applicants: '"+ str + "' that already exists") 

        if len(rep_users)  != 0: #< if there already exist users matching our .csv file
        	str = ""
        	for appl in rep_users:
        		str += appl + "," 
        	return HttpResponse(".csv file has user with usernames : '"+ str + "' that already exists") 

        if len(errors)  != 0: #< if some passwords are invalid
        	str = ""
        	for appl in errors:
        		str +=  appl + "," 
        	return HttpResponse(".csv file usernames : '"+ str + "' have incorrect format of password") 

        for line in lines: #< All fields provided are valid and hence create Applicants and users
            line = line.split(',')
            tmp = institute.applicants.create(name = line[0],rank = line[1]) #< Creating Applicant
            tmp.save()
            user = User.objects.create_user(username=line[0],email=line[2],password=line[3]) #< Creating user
            user.is_staff = True #< Giving staff permission to the user
            user.save()
        return HttpResponseRedirect("/allocation/admin/applicants")
    return HttpResponse("Error")

## Makes the "fill choices" for the student login
# @param applicant The applicant whose form has to be displayed
# @return returns the form for the corresponding applicant
# This view requires login to be displayed. 
def make_application_form(applicant1):
    # The inbuilt Model form class is used for the form
    class ApplicationForm(forms.ModelForm):
        choice = forms.ModelChoiceField(queryset=Choice.objects.filter(institute=applicant1.institute))#< The queryset is the choices available in the dropdown in the form.
        applicant = forms.ModelChoiceField(widget=forms.HiddenInput(), initial=applicant1, queryset=Applicant.objects.all() )#<this field is hidden since an applicant can apply for himself only.
        class Meta:
            model = Application
            fields = ['applicant','choice', 'priority'] #< These are the fields to be displayed
    return ApplicationForm

## View for applicant login
# @param rerquest
# This view requires login to be displayed. 
@login_required(login_url='/admin/login')
def index(request):
    applicant=get_object_or_404(Applicant,name=request.user.username) #< If an applicant exists with the username of the account, this returns the applicant. Else it returns 404 error.
    ApplicationForm = make_application_form(applicant)
    ApplicationFormSet = modelformset_factory(Application, form=ApplicationForm, extra=5) # used inbuilt function to create a formset from a form.
    if request.method == "POST":
        formset = ApplicationFormSet(request.POST, queryset=Application.objects.filter(applicant=applicant))
        if formset.is_valid():#< checks if the given information is valid.
            #< if the formset is valid, then save the form and redirect to the same page giving success as the context
            formset.save()
            return render(request, 'allocation/index.html', {'applicant': applicant,  'formset': formset, 'success':True,})
        else:
            #< if the formset is invalid, then save the form and redirect to the same page giving errors as the context
            form_errors = formset.errors
            return render(request, 'allocation/index.html', {'applicant': applicant,  'formset': formset,'form_errors': form_errors})
    else:
        formset = ApplicationFormSet(queryset=Application.objects.filter(applicant=applicant),)
        return render(request, 'allocation/index.html', {'applicant': applicant,  'formset': formset,})

## View for institute login
# @param rerquest
# This view requires login to be displayed. 
@login_required(login_url='/admin/login')
def admin1(request):
	institute=get_object_or_404(Institute,name=request.user.username)#< If an institute exists with the username of the account, this returns the institute. Else it returns 404 error.
	return render(request, 'allocation/admin1.html',{'institute': institute})

## View for institute page which lists all the choices of the institute 
# This is a generic list view provided by django to easily create views of models.
# The page also includes button for uploading csv file for creation of multiple choices at once
# The corresponding html file is choice_list.html
class ChoiceListView(generic.ListView):
	model = Choice #< specifies the model for which the generic view is to be created
    ##Context
    # Used to pass an additional context in the html file
	def get_context_data(self, **kwargs):
		institute=get_object_or_404(Institute,name=self.request.user.username)
		context = super(ChoiceListView, self).get_context_data(**kwargs)
		context['institute'] = institute #< Because of this line we can access the institute information through the variable named 'institute' in the html file
		return context
    ##Queryset
    # Used to specify the list of choices which are to be displayed
	def get_queryset(self):
		institute=get_object_or_404(Institute,name=self.request.user.username)
		return Choice.objects.filter(institute__name=institute.name) #< this returns the list of choices corresponding to the institute which is logged in currently

## View for institute page which lists all the applicants of the institute 
# This is a generic list view provided by django to easily create views of models.
# The page also includes button for uploading csv file for creation of multiple applicants at once
# The corresponding html file is applicants_list.html
class ApplicantListView(generic.ListView):
    model = Applicant#< specifies the model for which the generic view is to be created
    ##Context
    # Used to pass an additional context in the html file
    def get_context_data(self, **kwargs):
        institute=get_object_or_404(Institute,name=self.request.user.username)
        context = super(ApplicantListView, self).get_context_data(**kwargs)
        context['institute'] = institute #< Because of this line we can access the institute information through the variable named 'institute' in the html file
        return context
    ##Queryset
    # Used to specify the list of applicants which are to be displayed
    def get_queryset(self):
        institute=get_object_or_404(Institute,name=self.request.user.username)
        return Applicant.objects.filter(institute__name=institute.name) #< this returns the list of choices corresponding to the institute which is logged in currently

## View for institute page which displays a particular choice of the institute in detail 
# This is a generic detail view provided by django to easily create detail views of models.
# The page also includes update choice and delete choice buttons
# The corresponding html file is choice_detail.html
class ChoiceDetailView(generic.DetailView):
    model = Choice #< specifies the model for which the generic view is to be created
    ##Context
    # Used to pass an additional context in the html file
    def get_context_data(self, **kwargs):
        institute=get_object_or_404(Institute,name=self.request.user.username)
        context = super(ChoiceDetailView, self).get_context_data(**kwargs)
        context['institute'] = institute #< Because of this line we can access the institute information through the variable named 'institute' in the html file
        return context

## View for institute page which displays profile of a particular applicant of the institute in detail 
# This is a generic detail view provided by django to easily detail create views of models.
# The page also includes update applicant and delete applicant buttons
# The corresponding html file is applicant_detail.html
class ApplicantDetailView(generic.DetailView):
    model = Applicant #< specifies the model for which the generic view is to be created
    ##Context
    # Used to pass an additional context in the html file
    def get_context_data(self, **kwargs):
        institute=get_object_or_404(Institute,name=self.request.user.username)
        context = super(ApplicantDetailView, self).get_context_data(**kwargs)
        context['institute'] = institute #< Because of this line we can access the institute information through the variable named 'institute' in the html file
        return context

## View for institute page which displays a form to update the details of choices
# This is a generic update view provided by django to easily create update views of models.
# The corresponding html file is choice_update.html
class ChoiceUpdate(UpdateView):
    model = Choice #< specifies the model for which the generic view is to be created
    fields = ['choice_name','capacity'] #< specifies the fields that will be displayed on the rendered form
    template_name_suffix = '_update' # Specifies that the html file is choice_update.html
    success_url = reverse_lazy('allocation:choice_list') #< this is the redirect URL upon successful updation of choice

## View for institute page which displays a form to delete the choices
# This is a generic delete view provided by django to easily create delete views of models.
# The html file for delete confirmation is choice_confirm_delete.html
class ChoiceDelete(DeleteView):
    model = Choice #< specifies the model for which the generic view is to be created
    success_url = reverse_lazy('allocation:choice_list') #< this is the redirect URL upon successful deletion of choice

## View for institute page which displays a form to update the details of applicants
# This is a generic update view provided by django to easily create update views of models.
# The corresponding html file is applicant_update.html
class ApplicantUpdate(UpdateView):
    model = Applicant #< specifies the model for which the generic view is to be created
    fields = ['name','rank']#< specifies the fields that will be displayed on the rendered form
    template_name_suffix = '_update' # Specifies that the html file is choice_update.html
    success_url = reverse_lazy('allocation:applicant_list')#< this is the redirect URL upon successful updation of applicant

## View for institute page which displays a form to delete the applicants
# This is a generic delete view provided by django to easily create delete views of models.
# The html file for delete confirmation is applicant_confirm_delete.html
class ApplicantDelete(DeleteView):
    model = Applicant #< specifies the model for which the generic view is to be created
    success_url = reverse_lazy('allocation:applicant_list')#< this is the redirect URL upon successful deletion of applicant

def freeze(request):
    if request.method == "POST":
        applicant=Applicant.objects.get(pk=request.POST["applicant"])
        applicant.is_float=False
        applicant.save()
        return HttpResponseRedirect('/allocation')
    else:
        return HttpResponseRedirect('/allocation')

def drop(request):
    if request.method == "POST":
        applicant=Applicant.objects.get(pk=request.POST["applicant"])
        applicant.is_float=False
        given_choice=applicant.alloted_choice.all()
        if given_choice:
            applicant.alloted_choice.clear()
        applicant.save()
        return HttpResponseRedirect('/allocation')
    else:
        return HttpResponseRedirect('/allocation')

def float(request):
    return HttpResponseRedirect('/allocation')
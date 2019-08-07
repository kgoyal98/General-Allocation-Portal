## Admin Site View
# Used to modify the admin site
from django.contrib import admin
from .models import *

class ChoiceInline(admin.TabularInline):
	model = Application  
	extra = 2 

class AllotedChoiceToAppInLine(admin.TabularInline):
	model=Allocationcl
	extra=0

class ApplicantAdmin(admin.ModelAdmin):
	fields = ['name', 'rank','institute', 'is_float']
	list_display=['name','institute']
	inlines = [ChoiceInline, AllotedChoiceToAppInLine]

class InstituteAdmin(admin.ModelAdmin):
	fields=['name', 'is_allocated', 'round_num']
	list_display=['name','is_allocated', 'round_num']

class ChoiceAdmin(admin.ModelAdmin):
	fields=['choice_name', 'capacity','institute']
	list_display=['choice_name','institute', 'capacity']

admin.site.register(Institute, InstituteAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Applicant, ApplicantAdmin)
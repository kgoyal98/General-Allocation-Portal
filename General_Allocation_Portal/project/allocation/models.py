## Models file
# It contains all the models used to define the database
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import csv
import os

## Institute Model
# @brief Stores information about all institutes in a table
class Institute(models.Model):
	name=models.CharField(max_length=200) #< name of the Institute
	round_num = models.IntegerField(default=1) #<Stores the number of rounds completed
	is_allocated=models.BooleanField(default=False) #< Stores if atleast \f$1^{st}\f$ round is over or not
	## String Conversion
	# @param self Pointer to itself
	# @return name Name of institute
	def __str__(self):
		return self.name
	## Metadata
	class Meta:
		verbose_name='Institute' #< Display name
		verbose_name_plural='Institutes' #< Plural display name

## Choice Model
# @brief Stores various choices in a table
class Choice(models.Model):
	choice_name = models.CharField(max_length=200) #< object containing name of choice
	institute=models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='choices') #< Object containing related institute primary key
	capacity = models.IntegerField() #< Object containing maximum number of applicants allowed
	## String Conversion
	# @param self Pointer to itself
	# @return name Name of Choice
	def __str__(self):
		return self.choice_name
	## Metadata
	class Meta:
		ordering = ['institute__name', 'choice_name']

## Applicant Model
# @brief Stores various applicants in a table
class Applicant(models.Model):
	institute=models.ForeignKey(Institute,on_delete=models.CASCADE,related_name='applicants') #< Object containing foreign key to relate Applicant and Institute
	choices = models.ManyToManyField(Choice, through='Application', related_name='applicants') #< Foreign Keys relating Applicant to all the preferred choices
	name = models.CharField(max_length=200) #< Object containing name of Applicant
	alloted_choice = models.ManyToManyField(Choice, through='Allocationcl', related_name='alloted_applicant') # Foreign Key to relate Applicant to allocated choice
	rank = models.IntegerField(validators=[MinValueValidator(1)]) #< Integer object storing rank of Applicant
	is_float=models.BooleanField(default=True) #< Boolean Field to store current status opted by  the student to determine fereze, float and drop
	## String Conversion
	# @param self Pointer to itself
	# @return name Name of Applicant
	def __str__(self):
		return self.name
	## Ordered Choices
	# @brief Function to give all the choices as per preference of the Applicant
	# @param self Pointer to itself
	# @return list of choices in order of preference
	def ordered_choices(self):  
		return self.choices.all().order_by('application__priority')
	## Metadata
	class Meta:
		ordering = ['institute__name', 'rank']


## Application Model
# @brief Links an Applicant to a Choice through a model
class Application(models.Model):
	applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE) #< Applicant to be linked
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE) #< Choice chosen to be linked
	priority = models.IntegerField(validators=[MinValueValidator(1)]) #< Preference given to the choice by the Applicant
	## Metadata
	class Meta:
		ordering = ['priority'] 

## Application Model
# @brief Links allocated Choices to their Applicants through a model
class Allocationcl(models.Model):
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE) #< Foreign key to link the allocated choice
	applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE) #< Foreign key to link the Applicants
	## Metadata
	class Meta:
		verbose_name='Allocated Choice' #< Display Name
		verbose_name_plural='Allocated Choice' #< Plural display name
		ordering = ['applicant__rank'] #< used to return applicants in order of their ranks
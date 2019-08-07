## File containing allocator function
from allocation.models import *
from django.shortcuts import get_object_or_404

## Allocator Function
# @brief Function to allocate choices to applicants based on their preferences
# @param univ Name of the institute
# @return list of applicants which also store their newly allocated choices
def allocator(univ):
	insti=get_object_or_404(Institute, name=univ)
	insti.round_num = insti.round_num + 1
	insti.is_allocated=True #< Sets that the institute has allocated atleast once
	insti.save() #< save changes to institute model instance
	a=Applicant.objects.filter(institute__name=univ).order_by('rank') #< variable \c a \ stores the list of applicants in order of their ranks
	for x in a: #< loop over all applicants
		choices=x.ordered_choices() #< variable \c choices \ stores choices in order of priority of the applicant
		i=0 
		flag=True
		while x.is_float and flag and i<len(choices): #< loop over all preferences till allocated
			l=len(choices[i].alloted_applicant.all())
			if choices[i].capacity>l:
				given_choice=x.alloted_choice.all() #< \c given_choice\ stores already alloted choice
				if given_choice:
					x.alloted_choice.clear()
					x.save()
				clalloc=Allocationcl(choice=choices[i],applicant=x) #< link Choice to Applicant using Application model
				clalloc.save()
				flag=False
			i=i+1
	return a
## URL File
# Contains Information about active urls of allocation app
from django.conf.urls import url, include
from . import views
from django.contrib.auth import urls
from django.contrib.auth import views as auth_views

app_name = 'allocation'

## URL Patterns
# @brief Matches the URL and redirects accordingly
urlpatterns = [
    url(r'^$', views.index, name='index'), #< creates URL for student login
    url(r'^admin$', views.admin1, name='admin1'), #< creates URL for Institute login
    url(r'^admin/choices$', views.ChoiceListView.as_view(), name='choice_list'), #< creates URL to display all choices in Institute Login
    url(r'^admin/applicants$', views.ApplicantListView.as_view(), name='applicant_list'), #< creates URL to display all applicants in Institute Login
    url(r'^choice/(?P<pk>\d+)$', views.ChoiceDetailView.as_view(), name='choice-detail'), #< creates URL to display a particular choice in Institute Login
    url(r'^applicant/(?P<pk>\d+)$', views.ApplicantDetailView.as_view(), name='applicant-detail'), #< creates URL to display a particular applicant in Institute Login
     url(r'^choice/(?P<pk>\d+)/update$', views.ChoiceUpdate.as_view(), name='choice-update'), #< creates URL to update a particular choice in Institute Login
    url(r'^choice/(?P<pk>\d+)/delete$', views.ChoiceDelete.as_view(), name='choice-delete'), #< creates URL to deleten a particular choice in Institute Login
    url(r'^applicant/(?P<pk>\d+)/update$', views.ApplicantUpdate.as_view(), name='applicant-update'), #< creates URL to update a particular applicant in Institute Login
    url(r'^applicant/(?P<pk>\d+)/delete$', views.ApplicantDelete.as_view(), name='applicant-delete'), #< creates URL to delete a particular applicant in Institute Login
    url(r'^choice_make$', views.choice_make, name='choice_make'), #< creates URL to create choices through csv file in Institute Login
    url(r'^applicant_make$', views.applicant_make, name='applicant_make'), #< creates URL to create applicants through csv file in Institute Login
    url(r'^button_action$', views.button_action, name='button_action'), #< Used to call the allocator function in Institute login
    url(r'^register/$', views.signup), #< creates URL for registration of new Institutes
    url(r'^freeze$', views.freeze, name='freeze'), #< URL for Freeze button in Applicant login
    url(r'^float$', views.float, name='float'), #< URL for Float button in Applicant login
    url(r'^drop$', views.drop, name='drop'), #< URL for Drop button in Applicant login
]
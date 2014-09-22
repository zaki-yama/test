from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	url(r'^gmail_actions_in_the_inbox/', include('gmail_actions_in_the_inbox.urls', app_name='gmail_actions_in_the_inbox', namespace='gmail_actions_in_the_inbox')),
	url(r'^', include('guestbook.urls')),
    # url(r'^gae_django_app/', include('gae_django_app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

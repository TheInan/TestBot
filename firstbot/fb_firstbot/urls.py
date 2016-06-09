# firstbot/fb_firstbot/urls.py
from django.conf.urls import include, url
from .views import FirstBotView
urlpatterns = [
				url(r'^monkey/?$', FirstBotView.as_view())
			]
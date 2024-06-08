# scraper/urls.py
# scraper/urls.py

from django.urls import path
from .views import StartScrapingView, ScrapingStatusView 
from scraper import views


urlpatterns = [
    
    path('start_scraping/', StartScrapingView.as_view(), name='start_scraping'),
    path('scraping_status/<str:job_id>/', ScrapingStatusView.as_view(), name='scraping_status'),
]

# urlpatterns = [
#     path('start_scraping/', views.StartScrapingView, name='start_scraping'),
#     path('scraping_status/<str:job_id>/',views.ScrapingStatusView.as_view(), name='scraping_status'),
# ]
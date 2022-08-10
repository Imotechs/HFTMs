
from django.urls import path,include
from .views import home,news,testimonial,terms,plans
urlpatterns = [
    path('', home, name = 'home'),
    path('news/', news, name = 'news'),
    path('our/privacy/policies/', terms, name = 'terms'),
    path('our/sub/plans/', plans, name = 'plans'),
    path('testimonials/',testimonial, name = 'testimonial'),

]

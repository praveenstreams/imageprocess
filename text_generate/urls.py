from django.urls import path
from text_generate.views import ImageTextGenerate

urlpatterns = [
    path('', ImageTextGenerate.as_view(), name='image_text_generate'),]

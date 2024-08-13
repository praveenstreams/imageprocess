from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
import cv2
import pytesseract
from PIL import Image
import numpy as np
from .models import CardData


class ImageTextGenerate(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

    def post(self, request, *args, **kwargs):
        image_file_extensions = [
            'jpg', 'jpeg', 'png', 'gif', 'bmp',
            'tiff', 'webp', 'heif', 'ico', 'svg', 'raw', 'exr'
        ]
        image = request.FILES.get('file')
        if image.name.split('.')[-1] not in image_file_extensions:
            return render(request, 'home.html', {'status': 'Not an image file!'})
        image = Image.open(image)
        image = np.array(image)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        binary_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, 11, 2)

        pil_image = Image.fromarray(binary_img)
        text = pytesseract.image_to_string(pil_image)
        if text:
            lines = text.splitlines()
            extracted_data = {}
            for line in lines:
                if line.lower().startswith('name'):
                    extracted_data['name'] = line.split(' ', 1)[1].strip()
                elif line.lower().startswith('place'):
                    extracted_data['place'] = line.split(' ', 1)[1].strip()
                elif line.lower().startswith('designation'):
                    extracted_data['designation'] = line.split(' ', 1)[1].strip()
                elif line.lower().startswith('phone'):
                    extracted_data['phone'] = line.split(' ', 1)[1].strip()
            card_obj = CardData.objects.create(**extracted_data)

            return render(request, 'home.html', {'status': 'Process is success!'})
        return render(request, 'home.html')

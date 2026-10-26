from django.shortcuts import render

from constant_state_detection.views import csd_index

#
# def home(request):
#     return render(request, 'index.html')
#     # return csd_index(request)

def terms_of_service(request):
    return render(request, 'terms_of_service.html')


def contacts(request):
    return render(request, 'contacts.html')

def about_us(request):
    return render(request, 'about_us.html')

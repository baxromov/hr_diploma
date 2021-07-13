
#
# def page_404(request, exception):
#     data = {}
#     return render(request, 'backoffice/errors/404.html', data)
from django.shortcuts import render


def page_404(request):
    data = {}
    return render(request, 'backoffice/errors/404.html', data)

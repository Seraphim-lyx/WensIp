from django.shortcuts import render_to_response,HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
class UpLoadFileForm(forms.Form):
    title=forms.CharField(max_length=50)
    file=forms.FileField

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form=UpLoadFileForm(request.POST,request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("yes")
    else:
        form=UpLoadFileForm()
    return HttpResponse("no")

@csrf_exempt
def handle_uploaded_file(f):
    name=f.name
    destination = open('f://ch8/'+name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

from django.shortcuts import render
 
#主页
def home(request):
    return render(request, "home.html")

from django.shortcuts import render

def server_status(request):
    return render(request, "server_status.html")

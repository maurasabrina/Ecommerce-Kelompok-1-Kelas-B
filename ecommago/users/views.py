from django.shortcuts import render

def dashboard_admin(request):
    return render(request, 'admin_dashboard.html')

from django.shortcuts import render

# Create your views here.
def dashboard_atlet(request):
    
    return render(request, 'dashboard_atlet.html')

def dashboard_u(request):
    
    return render(request, 'dashboard_u.html')

def dashboard_p(request):
    
    return render(request, 'dashboard_p.html')

from django.shortcuts import render

# Create your views here.
def event_cards(request):
    # events = Event.objects.all()
    return render(request, 'event_cards.html')

def event_cards_partai(request):
    # events = Event.objects.all()
    
    return render(request, 'event_cards_partai.html')

def sponsor_form(request):
    if request.method == 'POST':
        # Handle form submission
        nama_sponsor = request.POST.get('nama_sponsor')
        tanggal_mulai = request.POST.get('tanggal_mulai')
        tanggal_selesai = request.POST.get('tanggal_selesai')
        
        # Do something with the data (e.g. save to database)
        # ...
        
        # Render a success message
        return render(request, 'sponsor_form.html')
    
    # Render the form template
    return render(request, 'sponsor_form.html')



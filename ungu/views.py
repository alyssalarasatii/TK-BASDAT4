from django.shortcuts import render
from django.db import connection

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Create your views here.
def event_cards(request):
    # events = Event.objects.all()
    
    return render(request, 'event_cards.html')

def event_cards_partai(request):
    # events = Event.objects.all()
    query = """
        SELECT e.nama_event, e.tahun, e.nama_stadium, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai
            FROM babadu.event AS e, babadu.peserta_mendaftar_event AS pme, babadu.peserta_kompetisi AS pk
            WHERE pk.nomor_peserta = '1' 
            AND pme.nomor_peserta = pk.nomor_peserta
            AND pme.nama_event = e.nama_event
            AND pme.tahun = e.tahun
    """
    cursor = connection.cursor()
    cursor.execute('SET search_path TO babadu;')
    cursor.execute(query)

    data = fetch(cursor)

    response = {'data': data}
    print(response)
    return render(request, 'event_cards_partai.html', response)

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

def sponsor_cards(request):
    # events = Event.objects.all()
    query = """
        select nama_brand, tgl_mulai, tgl_selesai
        from sponsor as s, atlet_sponsor as asp, atlet as a
        where a.id='89c0bee8-0acc-4d61-8926-8c18482f3bdf' and s.id=asp.id_sponsor and a.id=asp.id_atlet;
    """
    cursor = connection.cursor()
    cursor.execute('SET search_path TO babadu;')
    cursor.execute(query)
    data = fetch(cursor)


    response = {'data': data}
    print(response)
    
    return render(request, 'sponsor_cards.html', response)



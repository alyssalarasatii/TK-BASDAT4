from django.shortcuts import redirect, render
from django.db import connection

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Create your views here.
def event_cards(request):
    # events = Event.objects.all()
    if request.method == 'GET':
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
        
        return render(request, 'event_cards.html', response)
    elif request.method == 'POST':
        return redirect('ungu:event_cards')





def event_cards_partai(request):
    # events = Event.objects.all()
    query = """
        SELECT e.nama_event, e.tahun, e.nama_stadium, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai, ppk.jenis_partai
            FROM event AS e, partai_kompetisi as pk, partai_peserta_kompetisi ppk
            WHERE ppk.nomor_peserta = 1
            AND pk.nama_event = ppk.nama_event
            AND pk.tahun_event = ppk.tahun_event
            AND pk.tahun_event = e.tahun
            AND pk.nama_event = e.nama_event
            AND pk.jenis_partai = ppk.jenis_partai;

    """
    cursor = connection.cursor()
    cursor.execute('SET search_path TO babadu;')
    cursor.execute(query)

    data = fetch(cursor)

    response = {'data': data}
    print(response)
    return render(request, 'event_cards_partai.html', response)

def sponsor_form(request):
    # Handle form submission
    if request.method == 'GET':

        query_dropdown = """
            select nama_brand from sponsor where id not in 
            (select id_sponsor from atlet_sponsor asp where asp.id_atlet='e692d88a-9a46-4ff4-b07f-a72567f2e34c');
        """
        cursor = connection.cursor()
        cursor.execute('SET search_path TO babadu;')
        cursor.execute(query_dropdown)

        dropdowns = fetch(cursor)

        response = {'dropdowns': dropdowns}
        print(response)

        # Do something with the data (e.g. save to database)
        # ...
        
        # Render a success message
        return render(request, 'sponsor_form.html', response)
    
    elif request.method == 'POST':
        # id_member = request.session['id']
        
        nama_sponsor = request.POST['nama_sponsor']
        tanggal_mulai = request.POST['tanggal_mulai']
        tanggal_selesai = request.POST['tanggal_selesai']

        cursor = connection.cursor()
        cursor.execute('SET search_path TO babadu;')

        query_find_sponsor = f"""
            select id from sponsor where nama_brand='{nama_sponsor}';
        """
        cursor.execute(query_find_sponsor)
        data_sponsor = fetch(cursor)
        print("data sponsorrrr")
        print(data_sponsor)

        id = data_sponsor[0].get('id')
        print(id)

        query = f"""
            INSERT INTO ATLET_SPONSOR(ID_Atlet, ID_Sponsor, Tgl_mulai, Tgl_selesai) 
            VALUES ('e692d88a-9a46-4ff4-b07f-a72567f2e34c', '{id}', '{tanggal_mulai}', '{tanggal_selesai}');
        """

        cursor.execute(query)

        # response = {'data': data}
        # print(response)
        return redirect('ungu:sponsor_cards')
  

    

def sponsor_cards(request):
    # events = Event.objects.all()
    query = """
        select nama_brand, tgl_mulai, tgl_selesai
        from sponsor as s, atlet_sponsor as asp, atlet as a
        where a.id='e692d88a-9a46-4ff4-b07f-a72567f2e34c' and s.id=asp.id_sponsor and a.id=asp.id_atlet;
    """
    cursor = connection.cursor()
    cursor.execute('SET search_path TO babadu;')
    cursor.execute(query)
    data = fetch(cursor)


    response = {'data': data}
    print(response)
    
    return render(request, 'sponsor_cards.html', response)



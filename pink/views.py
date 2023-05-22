from django.shortcuts import redirect, render
from django.http import JsonResponse, QueryDict, HttpResponse
from django.core import serializers
from django.db import connection
from django.db.models.functions import datetime

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def is_logged(request):
    try:
        request.session['email']
        return True
    except KeyError:
        return False

def data_partai_kompetisi_event(request):
    # if request.method == 'GET' and is_logged(request):
    #     if request.session['is_admin_satgas']:
            query = """
                SELECT E.nama_event, E.tahun, E.nama_stadium, PK.jenis_partai, E.kategori_superseries, E.tgl_mulai, E.tgl_selesai, COUNT(PME.nomor_peserta) || '/' || S.kapasitas AS Kapasitas
                FROM EVENT E, PARTAI_KOMPETISI PK, PESERTA_MENDAFTAR_EVENT PME, STADIUM S
                WHERE E.nama_event = PK.nama_event
                AND E.nama_event = PME.nama_event
                AND S.nama = E.nama_stadium
                GROUP BY 1,2,3,4,5,6,7, S.kapasitas;
            """
            cursor = connection.cursor()
            cursor.execute('SET search_path TO babadu;')
            cursor.execute(query)
            data = fetch(cursor)

            response = {'data': data}
            print(response)
            return render(request, 'partai_kompetisi_event.html', response)
        # return JsonResponse({'not_allowed': True})
    # return redirect("/authenticate/?next=/jadwal-faskes/")
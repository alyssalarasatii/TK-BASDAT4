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

# fitur no6
def r_daftar_atlet(request):
    # if request.method == 'GET' and is_logged(request):
    #     if request.session['is_admin_satgas']:
            query_kualifikasi = """
                SELECT
                    M.Name,
                    M.Email,
                    A.Tgl_Lahir,
                    A.Negara_Asal,
                    A.Play_Right,
                    A.Height,
                    A.World_Rank,
                    CASE WHEN A.Jenis_Kelamin THEN 'Laki-laki' ELSE 'Perempuan' END AS Jenis_Kelamin,
                    AK.World_Tour_Rank,
                    COALESCE(SUM(PH.Total_Point), 0) AS Total_Point
                FROM
                    MEMBER AS M
                    INNER JOIN ATLET AS A ON A.ID = M.ID
                    INNER JOIN ATLET_KUALIFIKASI AS AK ON AK.ID_Atlet = A.ID
                    LEFT JOIN POINT_HISTORY AS PH ON PH.ID_Atlet = A.ID
                GROUP BY
                    M.Name,
                    M.Email,
                    A.Tgl_Lahir,
                    A.Negara_Asal,
                    A.Play_Right,
                    A.Height,
                    A.World_Rank,
                    A.Jenis_Kelamin,
                    AK.World_Tour_Rank
                ORDER BY
                    A.World_Rank ASC;
            """
            cursor = connection.cursor()
            cursor.execute('SET search_path TO babadu;')
            cursor.execute(query_kualifikasi)
            data_kualifikasi = fetch(cursor) # data1
    
            query_non_kualifikasi = """
                SELECT
                    M.Name,
                    M.Email,
                    A.Tgl_Lahir,
                    A.Negara_Asal,
                    A.Play_Right,
                    A.Height,
                    A.World_Rank,
                    CASE WHEN A.Jenis_Kelamin THEN 'Laki-laki' ELSE 'Perempuan' END AS Jenis_Kelamin
                FROM
                    MEMBER as M
                    INNER JOIN ATLET as A ON A.ID = M.ID
                    INNER JOIN ATLET_NON_KUALIFIKASI as AK ON AK.ID_Atlet = A.ID;
            """
            cursor = connection.cursor()
            cursor.execute('SET search_path TO babadu;')
            cursor.execute(query_non_kualifikasi)
            data_non_kualifikasi = fetch(cursor) # data1

            query_ganda = f"""
                SELECT
                    AG.ID_Atlet_Ganda,
                    A1.Name AS Atlet1_Name,
                    A2.Name AS Atlet2_Name,
                    COALESCE(SUM(PH.Total_Point), 0) AS Total_Point
                FROM
                    ATLET_GANDA AG
                    INNER JOIN MEMBER A1 ON A1.ID = AG.ID_Atlet_Kualifikasi
                    INNER JOIN MEMBER A2 ON A2.ID = AG.ID_Atlet_Kualifikasi_2
                    LEFT JOIN POINT_HISTORY PH ON PH.ID_Atlet = AG.ID_Atlet_Ganda
                GROUP BY
                    AG.ID_Atlet_Ganda,
                    A1.Name,
                    A2.Name;
            """
            cursor = connection.cursor()
            cursor.execute('SET search_path TO babadu;')
            cursor.execute(query_ganda)
            data_ganda = fetch(cursor) # data2
            
            print(data_ganda)
            response = {'atlet_kualifikasi': data_kualifikasi,
                        'atlet_nonkualifikasi': data_non_kualifikasi,
                        'atlet_ganda': data_ganda}
            print(response)
            return render(request, 'r_daftar_atlet.html', response)
        # return JsonResponse({'not_allowed': True})
    # return redirect("/authenticate/?next=/jadwal-faskes/")

# fitur no7
def r_atlet_dilatih(request):
    # if request.method == 'POST' and is_logged(request):
        # if request.session['is_admin_satgas']:
            id_pelatih = '841be0cc-9587-4164-b6eb-75cac8e62f17' # request.session['id_pelatih']
            query = f"""
                SELECT M.name , M.email, A.world_rank
                FROM ATLET_PELATIH AP
                JOIN MEMBER M ON M.id = AP.id_atlet
                JOIN ATLET A ON A.id = AP.id_atlet
                WHERE AP.id_pelatih = '{id_pelatih}';
            """
            cursor = connection.cursor()
            cursor.execute('SET search_path TO babadu;')
            cursor.execute(query)
            data = fetch(cursor)

            print(data)
            response = {'data': data}
            print(response)
            return render(request, 'r_atlet_dilatih.html', response)
        # return JsonResponse({'not_allowed': True})
    # return redirect("/authenticate/?next=/jadwal-faskes/")

def c_latih_atlet(request):
    # if is_logged(request):
        # if request.session['is_pelatih']:
            if request.method == 'GET':
                query = """
                    SELECT M.id, M.name
                    FROM ATLET A
                    JOIN MEMBER M ON M.ID = A.ID;
                """
                cursor = connection.cursor()
                cursor.execute('SET search_path TO babadu;')
                cursor.execute(query)
                data = fetch(cursor)

                response = {'data': data}
                print(response)
                return render(request, 'c_latih_atlet.html', response)
            
            elif request.method == 'POST' :
                id_pelatih = '841be0cc-9587-4164-b6eb-75cac8e62f17' # request.session['id_pelatih']
                id_atlet = request.POST['id_atlet']

                query = f"""
                    INSERT INTO ATLET_PELATIH VALUES ('{id_pelatih}', '{id_atlet}');
                """
                cursor = connection.cursor()
                cursor.execute('SET search_path TO babadu;')
                cursor.execute(query)
                # data = fetch(cursor)

                # response = {'data': data}
                # print(response)
                return redirect('pink:r_latih_atlet')
        # return JsonResponse({'not_allowed': True})
    # return redirect("/authenticate/?next=/jadwal-faskes/")

# TODO: fitur 8&9 
# fitur no8
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

# fitur no9
def data_hasil_pertandingan(request):
    # if request.method == 'POST' and is_logged(request):
        # if request.session['is_admin_satgas']:
            nama_event = request.POST['nama_event']
            tahun_event = request.POST['tahun_event']
            jenis_partai = request.POST['jenis_partai']
            print(nama_event, tahun_event, jenis_partai)
            query1 = f"""
                SELECT e.nama_event, e.nama_stadium, e.tgl_mulai, e.tgl_selesai, e.total_hadiah, e.kategori_superseries, p.jenis_partai, s.kapasitas
                FROM event as e
                join partai_kompetisi as p on p.nama_event=e.nama_event and p.tahun_event=e.tahun
                join stadium s on e.nama_stadium = s.nama
                where e.nama_event = '{nama_event}' and e.tahun = {tahun_event} and p.jenis_partai='{jenis_partai}';
            """
            cursor = connection.cursor()
            cursor.execute('SET search_path TO babadu;')
            cursor.execute(query1)
            data1 = fetch(cursor) # data1

            query2 = f"""
                SELECT PMM.JENIS_BABAK, PMM.NOMOR_PESERTA
                FROM PESERTA_MENGIKUTI_MATCH PMM
                JOIN MATCH M ON M.jenis_babak = PMM.jenis_babak and M.tanggal = PMM.tanggal and M.waktu_mulai = PMM.waktu_mulai
                JOIN PARTAI_KOMPETISI PK ON PK.nama_event = M.nama_event and PK.tahun_event = M.tahun_event

                WHERE STATUS_MENANG = 't'
                AND PK.jenis_partai = '{jenis_partai}'
                AND PK.nama_event = '{nama_event}'
                AND PK.tahun_event = {tahun_event}
                
                ORDER BY 
                    array_position(array['Final','Semifinal','Perempat Final','R13','R16','R32'], 
                                    PMM.jenis_babak);
            """
            cursor = connection.cursor()
            cursor.execute('SET search_path TO babadu;')
            cursor.execute(query2)
            data2 = fetch(cursor) # data1

            print(data1)
            response = {'data1': data1[0], 'data2' : data2}
            print(response)
            return render(request, 'hasil_pertandingan.html', response)
        # return JsonResponse({'not_allowed': True})
    # return redirect("/authenticate/?next=/jadwal-faskes/")
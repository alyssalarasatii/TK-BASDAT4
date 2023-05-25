from django.shortcuts import redirect, render
from django.db import connection

# Create your views here.
def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dashboard_atlet(request):
    # events = Event.objects.all()
    query = """
        SELECT
            m.name,
            m.email,
            a.tgl_lahir,
            a.negara_asal,
            CASE WHEN a.play_right = FALSE THEN 'left' ELSE 'right' END AS play_right,
            a.height,
            CASE WHEN a.jenis_kelamin = FALSE THEN 'female' ELSE 'male' END AS jenis_kelamin,
            ph.total_point,
            a.world_rank,
            p.name AS pelatih_name,
            p.email AS pelatih_email,
            CASE
                WHEN ak.id_atlet IS NOT NULL THEN 'qualified'
                WHEN ank.id_atlet IS NOT NULL THEN 'not qualified'
                ELSE 'unknown'
            END AS status
        FROM
            member m
            JOIN atlet a ON m.id = a.id
            JOIN point_history ph ON ph.id_atlet = a.id
            LEFT JOIN atlet_pelatih ap ON ap.id_atlet = a.id
            LEFT JOIN member p ON p.id = ap.id_pelatih
            LEFT JOIN atlet_kualifikasi ak ON ak.id_atlet = a.id
            LEFT JOIN atlet_non_kualifikasi ank ON ank.id_atlet = a.id
        WHERE
            a.id = 'e692d88a-9a46-4ff4-b07f-a72567f2e34c';
    """
    cursor = connection.cursor()
    cursor.execute('SET search_path TO babadu;')
    cursor.execute(query)

    data = fetch(cursor)

    response = {'data': data}
    print(response)
    
    return render(request, 'dashboard_atlet.html', response)

def dashboard_u(request):
    query = """
        SELECT m.name, m.email, u.negara
        FROM member m, umpire u
        where u.id = '51710ad9-8fd7-4735-b75a-45a58c22c319'
        and m.id = u.id;
    """
    cursor = connection.cursor()
    cursor.execute('SET search_path TO babadu;')
    cursor.execute(query)

    data = fetch(cursor)

    response = {'data': data}
    print(response)
    
    return render(request, 'dashboard_u.html', response)

def dashboard_p(request):
    query = """
        SELECT m.name, m.email, STRING_AGG(sp.spesialisasi, ', ') AS specializations, p.tanggal_mulai
        FROM member m
        JOIN pelatih p ON m.id = p.id
        JOIN pelatih_spesialisasi ps ON p.id = ps.id_pelatih
        JOIN spesialisasi sp ON ps.id_spesialisasi = sp.id
        WHERE p.id = '4af839cc-51f8-4c17-a8d7-9655d63005f3'
        GROUP BY m.name, m.email, p.tanggal_mulai;
    """
    cursor = connection.cursor()
    cursor.execute('SET search_path TO babadu;')
    cursor.execute(query)

    data = fetch(cursor)

    response = {'data': data}
    print(response)
    
    return render(request, 'dashboard_p.html', response)

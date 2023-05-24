from django.shortcuts import redirect, render
from django.http import JsonResponse, QueryDict, HttpResponse
from django.core import serializers
from django.db import connection
from django.db.models.functions import datetime
import uuid
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def is_logged(request):
    try:
        request.session['email']
        return True
    except KeyError:
        return False

SESSION_ROLE_KEYS = {
    'atlet': 'is_atlet',
    'pelatih': 'is_pelatih',
    'umpire': 'is_umpire',
}

# login
@csrf_exempt
def login(request):
    if request.method == 'POST':
        # print("b4 login")
        # print(request.session['is_atlet'])
        # print(request.session['is_pelatih'])
        # print(request.session['is_umpire'])

        name = request.POST['name']
        email = request.POST['email']
        query = f"""
            SELECT m.ID, m.Name, m.Email, COALESCE(u.ID, p.ID, a.ID) AS Member_ID,
                CASE
                    WHEN u.ID IS NOT NULL THEN 'umpire'
                    WHEN p.ID IS NOT NULL THEN 'pelatih'
                    WHEN a.ID IS NOT NULL THEN 'atlet'
                    ELSE 'Unknown'
                END AS Member_Type,
                u.Negara, p.Tanggal_Mulai, a.Tgl_Lahir, a.Negara_Asal, 
                a.Play_Right, a.Height, a.World_Rank, a.Jenis_Kelamin
            FROM MEMBER m 
            LEFT JOIN UMPIRE u ON m.ID = u.ID
            LEFT JOIN PELATIH p ON m.ID = p.ID
            LEFT JOIN ATLET a ON m.ID = a.ID
            WHERE m.name = '{name}' and m.email = '{email}';
        """

        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        cursor.execute(query)
        data = fetch(cursor)
        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False
        if len(data) == 1:
            temp = data[0]
            for attr in temp:
                if isinstance(temp[attr], uuid.UUID):
                    request.session[attr] = str(temp[attr])
                elif isinstance(temp[attr], datetime.date):
                    date = datetime.datetime.strptime(str(temp[attr]), '%Y-%m-%d')
                    formatted_date = date.strftime('%d %B %Y')
                    request.session[attr] = formatted_date
                else:
                    request.session[attr] = temp[attr]
            request.session[SESSION_ROLE_KEYS[temp['member_type']]] = True

            print("after login")
            print(request.session['is_atlet'])
            print(request.session['is_pelatih'])
            print(request.session['is_umpire'])
            return redirect('pink:r_daftar_atlet') # sementara ini pake ini karena blm ada dashboard
        else:
            messages.info(request,'Nama atau Email salah')

    if request.method == 'GET':
        return render(request, 'login.html')


def logout(request):
    if "id" in request.session:
        print("b4 logout")
        print(request.session['is_atlet'])
        print(request.session['is_pelatih'])
        print(request.session['is_umpire'])

        request.session.clear()
        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False

        print("after logout")
        print(request.session['is_atlet'])
        print(request.session['is_pelatih'])
        print(request.session['is_umpire'])
        return redirect('/')
    return redirect('/')
    # return redirect('pink:r_daftar_atlet') # sementara ini pake ini karena blm ada dashboard
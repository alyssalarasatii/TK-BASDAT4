from django.shortcuts import redirect, render
from django.db import connection
from collections import namedtuple


def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def is_logged(request):
    try:
        request.session['email']
        return True
    except KeyError:
        return False

'''from here'''
def namedtuplefetchall(cursor):
    """
    Return all rows from a cursor as a namedtuple.
    Assume the column names are unique.
    """
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def exec_query(query):
    result = None
    with connection.cursor() as cursor:
        try:
            cursor.execute('set search_path to babadu;')
            cursor.execute(query)
            
            if query.strip().lower()[:6] == 'select':
                result = namedtuplefetchall(cursor)
            else:
                result = cursor.rowcount
                connection.commit()
        except Exception as e:
            return str(e)
    return result


def index(request):
    return render(request, 'index.html')

def check_session(request):
    try:
        request.session["nama"]
        return True
    except:
        return False

def login(request):
    if request.method == 'POST':
        if check_session(request):
            print(request.session)
            nama = request.session["name"]
            email = request.session["email"]
        else:
            nama = request.POST["nama"]
            email = request.POST["email"]

        results = exec_query(f"select * from member where name='{nama}' and email='{email}'")
        if len(results) == 0:
            return render(request, 'login.html', {"failed": True})
        else:
            print('hello', results)
            id_member = results[0].id 
            role = get_role(id_member)
            print('sessionnn' + ' ' + str(request.session))
            for key, value in request.session.items():
                print('{} => {}'.format(key, value))
            request.session["id"] = str(id_member)
            request.session["name"] = nama
            request.session["email"] = email
            request.session["role"] = role
            request.session.set_expiry(0)
            request.session.modified = True

            print(request.session.keys())
            print(request.session.values())
            return redirect(f'/dashboard-{role}')
    
    return render(request, 'login.html')

def get_role(id_member):
    results = exec_query(f"select id from atlet where id='{id_member}'")
    if len(results) == 1:
        return "atlet"
    
    results = exec_query(f"select id from pelatih where id='{id_member}'")
    if len(results) == 1:
        return "pelatih"
    
    results = exec_query(f"select id from umpire where id='{id_member}'")
    if len(results) == 1:
        return "umpire"
    
def logout(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect('/')


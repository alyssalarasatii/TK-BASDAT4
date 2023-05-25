from django.shortcuts import render, redirect
import psycopg2
import uuid
from django.contrib import messages

# Create your views here.
def register(request):
    return render(request, 'regist.html')

def create_member(cursor, nama: str, ID: str, email: str) -> None:
    add_member = """
                INSERT INTO Member (Name, ID, email) VALUES
                (%s, %s, %s)
                """
    cursor.execute(add_member, (nama, ID,  email))


def create_atlet(cursor, ID: str, Negara_Asal: str, Tgl_Lahir: str, Play_Right: str, Height: str, Jenis_Kelamin: str) -> None:
    add_atlet = """
                INSERT INTO ATLET (ID, Tgl_Lahir, Negara_Asal, Play_Right, Height, World_Rank, Jenis_Kelamin) VALUES
                (%s, %s, %s, %s, %s, NULL, %s)
                """

    cursor.execute(add_atlet, (ID, Tgl_Lahir, Negara_Asal, Play_Right, Height, Jenis_Kelamin))


def create_pelatih(cursor, ID: str, kategori: str, tanggal_mulai: str) -> None:
    add_pelatih =   """
                    INSERT INTO PELATIH (ID, Tanggal_Mulai) VALUES
                    (%s, %s)
                    """
    cursor.execute(add_pelatih, (ID, tanggal_mulai))

    create_spesialisasi(cursor, ID, kategori)


def create_umpire(cursor, ID: str, negara: str) -> None:
    add_pelatih =   """
                    INSERT INTO UMPIRE (ID, Negara) VALUES
                    (%s, %s)
                    """
    cursor.execute(add_pelatih, (ID, negara))


def get_spesialisasi(cursor) -> dict[str:str]:
    get_spesialisasi =  """
                        SELECT * from SPESIALISASI
                        """
    cursor.execute(get_spesialisasi)

    result = cursor.fetchall()
    result = {name: ID for ID, name in result}

    return result


def create_spesialisasi(cursor, ID: str, kategori: str) -> None:
    spesialisasi = get_spesialisasi(cursor)
    add_pelatih_spesialisasi = """
                                INSERT INTO pelatih_spesialisasi (id_pelatih, id_spesialisasi)
                                VALUES (%s, %s)
                                """
    pelatih_spesialisasi_values = [(ID, spesialisasi[kategori]) for kategori in kategori]

    cursor.executemany(add_pelatih_spesialisasi, pelatih_spesialisasi_values)


def register_umpire(request):
    if (request.method == 'POST'):
        connection = psycopg2.connect(
            host="containers-us-west-18.railway.app",
            database = "railway",
            user="postgres",
            password="JuadAcvtaff6K9QktmsW",
            port = 7550
        )

        cursor = connection.cursor()
        cursor.execute("SET SEARCH_PATH TO BABADU")
        id = str(uuid.uuid4())
        name = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        try:
            create_member(cursor, name, id, email)
            create_umpire(cursor, id, negara)

            connection.commit()
            return redirect('login-logout:login')

        except Exception as e:
            connection.rollback()
            messages.error(request, "Gagal mendaftar perika input anda")


        connection.close()
    return render(request, 'umpire.html')


def register_atlet(request):
    if (request.method == 'POST'):
        print('test')
        connection = psycopg2.connect(
            host="containers-us-west-18.railway.app",
            database = "railway",
            user="postgres",
            password="JuadAcvtaff6K9QktmsW",
            port = 7550
    )

        cursor = connection.cursor()
        cursor.execute("SET SEARCH_PATH TO BABADU")
        id = str(uuid.uuid4())
        name = request.POST.get('name')
        print(name)
        email = request.POST.get('email')
        negara = request.POST.get('country')
        tgl_lahir = request.POST.get('birthdate')
        play_type = request.POST.get('play')
        if (play_type == 'Left'):
            play_type = False
        else:
            play_type = True
        height = request.POST.get('height')
        jenis_kelamin = request.POST.get('gender')
        if (jenis_kelamin == 'Perempuan'):
            jenis_kelamin = False
        else:
            jenis_kelamin = True
        try:
            create_member(cursor, name, id, email)
            create_atlet(cursor, id, negara, tgl_lahir, play_type, height, jenis_kelamin)

            connection.commit()
            connection.close()
            return redirect('login-logout:login')
        except Exception as e:
            connection.rollback()
            messages.error(request, "Gagal mendaftar perika input anda")
            connection.close()
        
    return render(request, 'atlet.html')

        
def register_pelatih(request):
    if (request.method == 'POST'):
        connection = psycopg2.connect(
            host="containers-us-west-18.railway.app",
            database = "railway",
            user="postgres",
            password="JuadAcvtaff6K9QktmsW",
            port = 7550
    )

        cursor = connection.cursor()
        cursor.execute("SET SEARCH_PATH TO BABADU")
        id = str(uuid.uuid4())
        name = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        kategori = request.POST.getlist('kategori')
        tgl_mulai = request.POST.get('tanggal_mulai')
        try:
            create_member(cursor, name, id, email)
            create_pelatih(cursor, id, kategori, tgl_mulai)
            connection.commit()
            connection.close()
            return redirect('login-logout:login')

        except Exception as e:
            connection.rollback()
            messages.error(request, "Gagal mendaftar perika input anda")
            connection.close()

        
    return render(request, 'pelatih.html')






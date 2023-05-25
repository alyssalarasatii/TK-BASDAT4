# from django.shortcuts import render
# import psycopg2
# import locale

# def get_stadium(name, cursor):
#     stadium = """
#                 select * from stadium where nama = %s
#               """
    
#     cursor.execute(stadium, name)
#     stadium_detail = cursor.fetchone()
#     return stadium_detail


# def get_event(name, year, cursor):
#     event = """
#             select * 
#             from event e
#             where e.nama_event = %s and e.tahun = %s
#             """
#     cursor.execute(event, (name, year))
#     event_detail = cursor.fetchone()
#     event_detail = (event_detail[0], event_detail[1], event_detail[2], event_detail[3], 
#                     event_detail[4].strftime('%d-%m-%Y'), event_detail[5].strftime('%d-%m-%Y'), 
#                     event_detail[6], locale.currency(event_detail[7], grouping=True))
                  
#     return event_detail

# def add_peserta_kompetisi(name, year, jenis_partai, nomor_peserta, cursor):
#     add_into_partai_peserta_kompetisi = """
#                                         INSERT INTO PARTAI_PESERTA_KOMPETISI (Jenis_Partai, Nama_Event, Tahun_Event, Nomor_Peserta) VALUES
#                                         VALUES (%s, %s, %s, %s)
#                                         """
#     cursor.execute(add_into_partai_peserta_kompetisi, jenis_partai, name, year, nomor_peserta)

# def create_peserta_kompetisi(rank, cursor, ID_Atlet_Ganda = None, ID_Atlet_Kualifikasi = None):
#     highest_nomor_peserta = """
#                             select nomor_peserta
#                             from peserta_kompetisi
#                             order by nomor_peserta desc limit 1
#                             """
#     cursor.execute(highest_nomor_peserta)
#     nomor_peserta = cursor.fecthone()[0] + 1

#     add_into_partai_peserta_kompetisi = """
#                                         INSERT INTO PESERTA_KOMPETISI (Nomor_Peserta, ID_Atlet_Ganda, ID_Atlet_Kualifikasi, World_Rank, World_Tour_Rank) VALUES
#                                         VALUES (%s, %s, %s, %s, %s)
#                                         """
#     cursor.execute(add_into_partai_peserta_kompetisi, nomor_peserta, ID_Atlet_Ganda, ID_Atlet_Kualifikasi, rank[0], rank[1])
#     return nomor_peserta

# def create_atlet_ganda(ID_Atlet_Ganda, ID_Atlet_Kualifikasi, ID_Atlet_Kualifikasi_2, cursor):
#     add_atlet_ganda =  """
#                         INSERT INTO PESERTA_KOMPETISI (ID_Atlet_Ganda, ID_Atlet_Kualifikasi, ID_Atlet_Kualifikasi_2) VALUES
#                         VALUES (%s, %s, %s)
#                         """
#     cursor.execute(add_atlet_ganda, ID_Atlet_Ganda, ID_Atlet_Kualifikasi, ID_Atlet_Kualifikasi_2)

# def get_id_atlet_ganda(id, id_pasangan, cursor):
#     find_pair = """
#                 select id_atlet_ganda
#                 from atlet_ganda
#                 where  (id_atlet_kualifikasi = %s AND  id_atlet_kualifikasi_2 = %s)
#                 """
    
#     cursor.execute(find_pair, )
#     id_atlet_ganda = cursor.fecthone()
#     return id_atlet_ganda


# def get_nomor_peserta_tunggal(id, cursor):
#     get_nomor_peserta = """
#                         select nomor_peserta from peserta_kompetisi 
#                         where ID_Atlet_Kualifikasi = %s
#                         """
#     cursor.execute(get_nomor_peserta, id)
#     nomor_peserta = cursor.fetchone()
#     return nomor_peserta


# def get_nomor_peserta_ganda(id, cursor):
#     get_nomor_peserta = """
#                         select nomor_peserta from peserta_kompetisi 
#                         where ID_Atlet_Ganda = %s
#                         """
#     cursor.execute(get_nomor_peserta, id)
#     nomor_peserta = cursor.fetchone()
#     return nomor_peserta


# def daftar_stadium(request):
#     dict_stadium = {}
#     connection = psycopg2.connect(
#         host="localhost",
#         database="postgres",
#         user="postgres",
#         password="dave1030"
#     )
#     cursor = connection.cursor()
#     cursor.execute("SET SEARCH_PATH TO BABADU")
#     cursor.execute("select * from stadium")

#     dict_stadium['stadium'] = cursor.fetchall

#     cursor.close()
#     connection.close()

#     return render(request, context = dict_stadium)


# def get_event_stadium(nama_stadium, cursor):
#     event = """
#                 select e.Nama_Event, e.Total_hadiah, e.Tgl_mulai, e.Kategori_Superseries, e.Tahun
#                 from event e
#                 where E.nama_stadium = %s and e.Tgl_Mulai > current_date
#             """
#     event_list = cursor.execute(event, nama_stadium)
#     event_list = cursor.fetchall()
#     event_list = [
#                 (event[0], locale.currency(event[1], grouping=True), 
#                  event[2].strftime('%d-%m-%Y'), 
#                  event[3], 
#                  event[4]
#                  ) 
#                  for event in event_list
#                 ]
#     return event_list



# def daftar_event(request, stadium):
#     connection = psycopg2.connect(
#         host="localhost",
#         database="postgres",
#         user="postgres",
#         password="dave1030"
#     )
#     cursor = connection.cursor()
#     cursor.execute("SET SEARCH_PATH TO BABADU")

#     connection.close()
#     return render(request, )




# def daftar_partai(request, stadium_name, event_name, event_year):

#     connection = psycopg2.connect(
#         host="localhost",
#         database="postgres",
#         user="postgres",
#         password="dave1030"
#     )

#     cursor = connection.cursor()
#     cursor.execute("SET SEARCH_PATH TO BABADU")

#     if (request.method == 'POST'):
#         if ('Ganda' in request.POST['jenis_partai']):
#             try:
#                 atlet = 




    

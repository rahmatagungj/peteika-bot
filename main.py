import backend as backend
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import wikipedia
from google_trans_new import google_translator
import math
import socket
import requests

bot = Updater(backend.token)


def start_callback(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Halo {update.effective_user.first_name}")


""" BAGIAN PERINTAH """


def show_command(update, context):
    command = f"""DAFTAR PERINTAH

/nims                  - Menampilkan seluruh nim
/nim (nama)     - Menampilkan nim 1 orang
/tugas                  - Menampilkan seluruh tugas
/kegiatan               - Menampilkan seluruh kegiatan
/informasi              - Menampilkan seluruh informasi
/wiki (topik)  - Mencari data di wikipedia
/logo (nama) - Menampilkan Logo Kampus
/translate (bahasa)|(text) - Menerjemahkan Text
/tan (nomor) - Mengubah bilangan ke Tan
/cos (nomor) - Mengubah bilangan ke Cos
/sin (nomor) - Mengubah bilangan ke Sin
/pangkat (nomor)|(base) - Mengubah bilangan ke Pangkat
/log (nomor) - Mengubah bilangan ke Log
	"""
    update.message.reply_text(command)


""" BAGIAN NIM """


def add_nim(update, context):
    info = " ".join(context.args)
    infos = info.split("|")
    if len(infos) < 2:
        update.message.reply_text(f"Format salah")
        return
    inserted = backend.db_insert("nim", infos[0], infos[1])
    if inserted:
        update.message.reply_text(
            f"Nim berhasil ditambahkan\n\nNama: {infos[0]}\nNim: {infos[1]}"
        )
    else:
        update.message.reply_text(f"Nim gagal ditambahkan")


def get_nim(update, context):
    result = backend.db_get("Nama", "MAHASISWA")
    if str(result) != "Null" or str(result) != "None":
        update.message.reply_text(f"DAFTAR NIM\n\n{result}")
    else:
        update.message.reply_text(f"Data Tidak Ada")


def get_one_nim(update, context):
    name = " ".join(context.args)
    if len(name) < 1:
        update.message.reply_text("Data Tidak Ada")
        return
    toGet = backend.db.child("MAHASISWA").child(name).get()
    result = ""
    try:
        for profiles in toGet.each():
            formats = str(f"Nama: {name}\nNim: {profiles.val()}")
            result += formats + "\n"
    except:
        result = "Data Tidak Ada"
    result = result.replace("'", "").replace("{", "").replace("}", "")
    update.message.reply_text(result)


def remove_nim(update, context):
    name = " ".join(context.args)
    if len(name) < 3:
        update.message.reply_text(f"Format salah")
        return
    deleted = backend.db_remove_child("MAHASISWA", name)
    if deleted:
        update.message.reply_text(f'Nim "{name}" berhasil dihapus')
    else:
        update.message.reply_text(f'Nim "{name}" gagal dihapus')


""" BAGIAN TUGAS """


def add_task(update, context):
    info = " ".join(context.args)
    infos = info.split("|")
    if len(infos) < 2:
        update.message.reply_text(f"Format salah")
        return
    inserted = backend.db_insert("tugas", infos[0], infos[1])
    if inserted:
        update.message.reply_text(
            f"Tugas berhasil ditambahkan\n\nMatkul: {infos[0]}\nTugas: {infos[1]}"
        )
    else:
        update.message.reply_text(f"Tugas gagal ditambahkan")


def get_task(update, context):
    result = backend.db_get("Matkul", "TUGAS")
    if str(result) != "Null" or str(result) != "None":
        update.message.reply_text(f"DAFTAR TUGAS\n\n{result}")
    else:
        update.message.reply_text(f"Tidak ada tugas")


def remove_task(update, context):
    task = " ".join(context.args)
    if len(task) < 2:
        update.message.reply_text(f"Format salah")
        return
    deleted = backend.db_remove_child("TUGAS", task)
    if deleted:
        update.message.reply_text(f'Tugas "{task}" berhasil dihapus')
    else:
        update.message.reply_text(f'Tugas "{task}" gagal dihapus')


""" BAGIAN KEGIATAN """


def add_event(update, context):
    info = " ".join(context.args)
    infos = info.split("|")
    if len(infos) < 2:
        update.message.reply_text(f"Format salah")
        return
    inserted = backend.db_insert("kegiatan", infos[0], infos[1])
    if inserted:
        update.message.reply_text(
            f"Kegiatan berhasil ditambahkan\n\nKegiatan: {infos[0]}\nWaktu: {infos[1]}"
        )
    else:
        update.message.reply_text(f"Kegiatan gagal ditambahkan")


def get_event(update, context):
    result = backend.db_get("Kegiatan", "KEGIATAN")
    if str(result) != "Null" or str(result) != "None":
        update.message.reply_text(f"DAFTAR KEGIATAN\n\n{result}")
    else:
        update.message.reply_text(f"Tidak ada kegiatan")


def remove_event(update, context):
    task = " ".join(context.args)
    if len(task) < 2:
        update.message.reply_text(f"Format salah")
        return
    deleted = backend.db_remove_child("KEGIATAN", task)
    if deleted:
        update.message.reply_text(f'Kegiatan "{task}" berhasil dihapus')
    else:
        update.message.reply_text(f'Kegiatan "{task}" gagal dihapus')


""" BAGIAN INFORMASI """


def add_info(update, context):
    info = " ".join(context.args)
    infos = info.split("|")
    if len(infos) < 2:
        update.message.reply_text(f"Format salah")
        return
    inserted = backend.db_insert("informasi", infos[0], infos[1])
    if inserted:
        update.message.reply_text(
            f"Informasi berhasil ditambahkan\n\nInformasi: {infos[0]}\nKeterangan: {infos[1]}"
        )
    else:
        update.message.reply_text(f"Informasi gagal ditambahkan")


def get_info(update, context):
    result = backend.db_get("informasi", "INFORMASI")
    if str(result) != "Null" or str(result) != "None":
        update.message.reply_text(f"DAFTAR INFORMASI\n\n{result}")
    else:
        update.message.reply_text(f"Tidak ada informasi")


def remove_info(update, context):
    task = " ".join(context.args)
    if len(task) < 2:
        update.message.reply_text(f"Format salah")
        return
    deleted = backend.db_remove_child("INFORMASI", task)
    if deleted:
        update.message.reply_text(f'Informasi "{task}" berhasil dihapus')
    else:
        update.message.reply_text(f'Informasi "{task}" gagal dihapus')


""" PERHITUNGAN """


def math_sum(update, context):
    esum = " ".join(context.args)
    if len(esum) < 2:
        update.message.reply_text(f"Format salah")
        return
    if "*" in esum:
        esums = esum.split("*")
        result = int(esums[0]) * int(esums[1])
    elif "+" in esum:
        esums = esum.split("+")
        result = int(esums[0]) + int(esums[1])
    elif "/" in esum:
        esums = esum.split("/")
        result = int(esums[0]) / int(esums[1])
    elif "-" in esum:
        esums = esum.split("-")
        result = int(esums[0]) - int(esums[1])
    elif "%" in esum:
        esums = esum.split("%")
        result = int(esums[0]) % int(esums[1])
    update.message.reply_text(f"Hasil: {result}")


""" WIKIPEDIA """


def get_wiki(update, context):
    esum = " ".join(context.args)
    wikipedia.set_lang("id")
    if len(esum) < 2:
        update.message.reply_text(f"Format salah")
        return
    try:
        result = wikipedia.summary(esum, sentences=2)
    except:
        result = "Data tidak ada"
    update.message.reply_text(f"{result}")


""" MEDIA """


def get_logo(update, context):
    find = " ".join(context.args)
    if len(find) <= 0:
        update.message.reply_text(f"Format salah")
        return
    if find == "kampus":
        url = "https://akupintar.id/documents/20143/0/Sekolah-Tinggi-Keguruan-dan-Ilmu-Pendidikan-Muhammadiyah-Kuningan.png"
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


""" TRANSLATE """


def to_translate(update, context):
    find = " ".join(context.args)
    if len(find) <= 0:
        update.message.reply_text(f"Format salah")
        return
    text = find.split("|")
    translator = google_translator()
    try:
        translate_text = translator.translate(text[1], lang_tgt=text[0])
    except:
        translate_text = "Data tidak dapat diproses"
    update.message.reply_text(f"{translate_text}")


""" MATEMATIKA """


def make_sin(update, context):
    find = " ".join(context.args)
    if len(find) <= 0:
        update.message.reply_text(f"Format salah")
        return
    if "." in find or "," in find:
        find = find.replace(",", "").replace(".", "")
        result = math.sin(float(find))
    else:
        result = int(math.sin(int(find)))
    update.message.reply_text(f"Hasil: {result}")


def make_cos(update, context):
    find = " ".join(context.args)
    if len(find) <= 0:
        update.message.reply_text(f"Format salah")
        return
    if "." in find or "," in find:
        find = find.replace(",", "").replace(".", "")
        result = math.cos(float(find))
    else:
        result = int(math.cos(int(find)))
    update.message.reply_text(f"Hasil: {result}")


def make_tan(update, context):
    find = " ".join(context.args)
    if len(find) <= 0:
        update.message.reply_text(f"Format salah")
        return
    if "." in find or "," in find:
        find = find.replace(",", "").replace(".", "")
        result = math.tan(float(find))
    else:
        result = int(math.tan(int(find)))
    update.message.reply_text(f"Hasil: {result}")


def make_log(update, context):
    find = " ".join(context.args)
    if len(find) <= 0:
        update.message.reply_text(f"Format salah")
        return
    if "." in find or "," in find:
        find = find.replace(",", "").replace(".", "")
        result = math.log(float(find))
    else:
        result = int(math.log(int(find)))
    update.message.reply_text(f"Hasil: {result}")


def make_pow(update, context):
    find = " ".join(context.args)
    if len(find) <= 0:
        update.message.reply_text(f"Format salah")
        return
    if "." in find or "," in find:
        find = find.replace(",", "").replace(".", "")
        find = find.split("|")
        result = math.pow(float(find[0]), float(find[1]))
    else:
        find = find.split("|")
        result = int(math.pow(int(find[0]), int(find[1])))
    update.message.reply_text(f"Hasil: {result}")


""" BAGIAN LAINNYA """


def get_covid(update, context):
    try:
        r = requests.get("https://api.kawalcorona.com/indonesia/")
        r = r.json()
        for i in r:
            negara = i["name"]
            positif = i["positif"]
            sembuh = i["sembuh"]
            meninggal = i["meninggal"]
            dirawat = i["dirawat"]
        result = f"""Data covid di {negara}

Positif : {positif}
Sembuh: {sembuh}
Meninggal: {meninggal}
Dirawat: {dirawat}"""
    except:
        result = "Data error"
    update.message.reply_text(result)


def get_kbbi(update, context):
    find = " ".join(context.args)
    if len(find) <= 0:
        update.message.reply_text(f"Format salah")
        return
    try:
        r = requests.get(f"https://kbbi-api-zhirrr.vercel.app/api/kbbi?text={find}")
        r = r.json()
        frasa = r["lema"]
        arti = r["arti"]
        result = f"""Hasil {find}

Frasa : {frasa}
Arti: {arti}"""
    except:
        result = "Data error"
    update.message.reply_text(result)


def get_pos(update, context):
    find = " ".join(context.args)
    if len(find) <= 0:
        update.message.reply_text(f"Format salah")
        return
    try:
        r = requests.get(f"https://kodepos.herokuapp.com/search?q={find}")
        r = r.json()
        for i in r["data"]:
            provinsi = i["province"]
            kabupaten = i["city"]
            kecamatan = i["subdistrict"]
            desa = i["urban"]
            kodepos = i["postalcode"]
        result = f"""Hasil {find}
	
Provinsi : {provinsi}
Kabupaten : {kabupaten}
Kecamatan : {kecamatan}
Desa : {desa}
kode pos : {kodepos}"""
    except:
        result = "Data error"
    update.message.reply_text(result)


def get_ip(update, context):
    find = " ".join(context.args)
    if len(find) <= 0:
        update.message.reply_text(f"Format salah")
        return
    try:
        host_ip = socket.gethostbyname(find)
        result = "IP : {}".format(host_ip)
    except:
        result = "Unable to get IP {}".format(find)
    update.message.reply_text(result)


def get_ip_type(update, context):
    IP = " ".join(context.args)
    if len(IP) <= 0:
        update.message.reply_text(f"Format salah")
        return

    def isIPv4(s):
        try:
            return str(int(s)) == s and 0 <= int(s) <= 255
        except:
            return False

    def isIPv6(s):
        if len(s) > 4:
            return False
        try:
            return int(s, 16) >= 0 and s[0] != "-"
        except:
            return False

    if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
        update.message.reply_text("Tipe IP {} adalah IPv4".format(IP))
        return
    if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
        update.message.reply_text("Tipe IP {} adalah IPv6".format(IP))
        return
    update.message.reply_text("Tipe IP {} adalah Neither".format(IP))


def command_list():
    bot.dispatcher.add_handler(CommandHandler("start", start_callback))

    bot.dispatcher.add_handler(CommandHandler("command", show_command))
    bot.dispatcher.add_handler(CommandHandler("cmd", show_command))
    bot.dispatcher.add_handler(CommandHandler("cmds", show_command))
    bot.dispatcher.add_handler(CommandHandler("help", show_command))

    bot.dispatcher.add_handler(CommandHandler("nims", get_nim))
    bot.dispatcher.add_handler(CommandHandler("nim", get_one_nim))
    bot.dispatcher.add_handler(CommandHandler("tambah_nim", add_nim))
    bot.dispatcher.add_handler(CommandHandler("hapus_nim", remove_nim))

    bot.dispatcher.add_handler(CommandHandler("tugas", get_task))
    bot.dispatcher.add_handler(CommandHandler("tambah_tugas", add_task))
    bot.dispatcher.add_handler(CommandHandler("hapus_tugas", remove_task))

    bot.dispatcher.add_handler(CommandHandler("kegiatan", get_event))
    bot.dispatcher.add_handler(CommandHandler("tambah_kegiatan", add_event))
    bot.dispatcher.add_handler(CommandHandler("hapus_kegiatan", remove_event))

    bot.dispatcher.add_handler(CommandHandler("informasi", get_info))
    bot.dispatcher.add_handler(CommandHandler("tambah_informasi", add_info))
    bot.dispatcher.add_handler(CommandHandler("hapus_informasi", remove_info))

    bot.dispatcher.add_handler(CommandHandler("hitung", math_sum))

    bot.dispatcher.add_handler(CommandHandler("wikipedia", get_wiki))
    bot.dispatcher.add_handler(CommandHandler("wiki", get_wiki))

    bot.dispatcher.add_handler(CommandHandler("logo", get_logo))

    bot.dispatcher.add_handler(CommandHandler("translate", to_translate))
    bot.dispatcher.add_handler(CommandHandler("terjemahkan", to_translate))

    bot.dispatcher.add_handler(CommandHandler("sin", make_sin))
    bot.dispatcher.add_handler(CommandHandler("cos", make_cos))
    bot.dispatcher.add_handler(CommandHandler("tan", make_tan))
    bot.dispatcher.add_handler(CommandHandler("log", make_log))
    bot.dispatcher.add_handler(CommandHandler("pangkat", make_pow))

    bot.dispatcher.add_handler(CommandHandler("ip", get_ip))
    bot.dispatcher.add_handler(CommandHandler("tipe_ip", get_ip_type))
    bot.dispatcher.add_handler(CommandHandler("covid", get_covid))
    bot.dispatcher.add_handler(CommandHandler("corona", get_covid))
    bot.dispatcher.add_handler(CommandHandler("kbbi", get_kbbi))
    bot.dispatcher.add_handler(CommandHandler("kodepos", get_pos))


if __name__ == "__main__":
    command_list()
    bot.start_polling()
    bot.idle()

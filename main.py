import backend as backend
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

bot = Updater(backend.token)

def start_callback(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(f'Halo {update.effective_user.first_name}')

""" BAGIAN PERINTAH """
def show_command(update, context):
	command = f'''DAFTAR PERINTAH

/nims                  - Menampilkan seluruh nim
/nim (nama)     - Menampilkan nim 1 orang
/tambah_nim (nama)|(nim)    - Menambah nim
/hapus_nim (nama)  - Menghapus nim
/tugas                  - Menampilkan seluruh tugas
/tambah_tugas (matkul)|(tugas)    - Menambah tugas
/hapus_tugas (matkul)  - Menghapus tugas
	'''
	update.message.reply_text(command)

""" BAGIAN NIM """
def add_nim(update, context):
	info = " ".join(context.args)
	infos = info.split('|')
	if len(infos) < 2:
		update.message.reply_text(f'Format salah')
		return
	inserted = backend.db_insert('nim',infos[0],infos[1])
	if inserted:
		update.message.reply_text(f'Nim berhasil ditambahkan\n\nNama: {infos[0]}\nNim: {infos[1]}')
	else:
		update.message.reply_text(f'Nim gagal ditambahkan')


def get_nim(update, context):
	result = backend.db_get('Nama','MAHASISWA')
	if str(result) != 'Null' or str(result) != 'None':
		update.message.reply_text(f'DAFTAR NIM\n\n{result}')
	else:
		update.message.reply_text(f'Data Tidak Ada')


def get_one_nim(update, context):
	name = " ".join(context.args)
	if len(name) < 1:
		update.message.reply_text('Data Tidak Ada')
		return
	toGet = backend.db.child('MAHASISWA').child(name).get()
	result = ""
	try:
		for profiles in toGet.each():
				formats = str(f'Nama: {name}\nNim: {profiles.val()}')
				result += formats + '\n'
	except:
		result = 'Data Tidak Ada'
	result = result.replace("'","").replace("{","").replace("}","")
	update.message.reply_text(result)


def remove_nim(update, context):
	name = " ".join(context.args)
	if len(name) < 3:
		update.message.reply_text(f'Format salah')
		return
	deleted = backend.db_remove_child('MAHASISWA',name)
	if deleted:
		update.message.reply_text(f'Nim "{name}" berhasil dihapus')
	else:
		update.message.reply_text(f'Nim "{name}" gagal dihapus')


""" BAGIAN TUGAS """
def add_task(update, context):
	info = " ".join(context.args)
	infos = info.split('|')
	if len(infos) < 2:
		update.message.reply_text(f'Format salah')
		return
	inserted = backend.db_insert('tugas',infos[0],infos[1])
	if inserted:
		update.message.reply_text(f'Tugas berhasil ditambahkan\n\nMatkul: {infos[0]}\nTugas: {infos[1]}')
	else:
		update.message.reply_text(f'Tugas gagal ditambahkan')


def get_task(update, context):
	result = backend.db_get('Matkul','TUGAS')
	if str(result) != 'Null' or str(result) != 'None':
		update.message.reply_text(f'DAFTAR TUGAS\n\n{result}')
	else:
		update.message.reply_text(f'Tidak ada tugas')


def remove_task(update, context):
	task = " ".join(context.args)
	if len(task) < 2:
		update.message.reply_text(f'Format salah')
		return
	deleted = backend.db_remove_child('TUGAS',task)
	if deleted:
		update.message.reply_text(f'Tugas "{task}" berhasil dihapus')
	else:
		update.message.reply_text(f'Tugas "{task}" gagal dihapus')


def command_list():
	bot.dispatcher.add_handler(CommandHandler("start", start_callback))

	bot.dispatcher.add_handler(CommandHandler("command", show_command))
	bot.dispatcher.add_handler(CommandHandler("cmd", show_command))
	bot.dispatcher.add_handler(CommandHandler("cmds", show_command))

	bot.dispatcher.add_handler(CommandHandler("nims", get_nim))
	bot.dispatcher.add_handler(CommandHandler("nim", get_one_nim))
	bot.dispatcher.add_handler(CommandHandler("tambah_nim", add_nim))
	bot.dispatcher.add_handler(CommandHandler("hapus_nim", remove_nim))

	bot.dispatcher.add_handler(CommandHandler("tugas", get_task))
	bot.dispatcher.add_handler(CommandHandler("tambah_tugas", add_task))
	bot.dispatcher.add_handler(CommandHandler("hapus_tugas", remove_task))

if __name__ == '__main__':
	command_list()
	bot.start_polling()
	bot.idle()



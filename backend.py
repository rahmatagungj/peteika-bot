import pyrebase

#Initialize Firebase
firebaseConfig={"apiKey": "AIzaSyB-eZ3mOKHzXIXwYyB49pbF5yZGYOdwYL8",
	"authDomain": "toke-id.firebaseapp.com",
	"databaseURL": "https://toke-id-default-rtdb.firebaseio.com",
	"projectId": "toke-id",
	"storageBucket": "toke-id.appspot.com",
	"messagingSenderId": "63309516471",
	"appId": "1:63309516471:web:6e1962a0132352a79dc732",
	"measurementId": "G-W4140HYN2D"}

firebase=pyrebase.initialize_app(firebaseConfig)

token = '1586774852:AAHteesmyGMa5YVhxniKOguux3oLlGuyBfU'
db=firebase.database()

def db_insert(mode,content,value):
	if mode == 'tugas':
		data={"Tugas":str(value)}
		try:
			db.child("TUGAS").child(str(content)).set(data)
			return True
		except:
			return False
	elif mode == 'nim':
		data={"Nim":str(value)}
		try:
			db.child("MAHASISWA").child(str(content)).set(data)
			return True
		except:
			return False


def db_get(context,name):
	toGet = db.child(name).get()
	result= ""
	try:
		for profiles in toGet.each():
			formats = str(f'{context}: {profiles.key()}\n{profiles.val()}\n')
			result += formats + '\n'
		return result.replace("'","").replace("{","").replace("}","")
	except:
		return 'Tidak ada'


def db_remove_child(head,name):
	try:
		result = db.child(head).child(name).remove()
		return True
	except:
		return False
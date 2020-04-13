from telegram.ext import Updater, CommandHandler as CH
import os, requests, json
from flask import Flask

app = Flask(__name__)
def tampil(update, text):
	update.message.reply_text(text)

def mulai(update, context):
	nama = (update.message.from_user)["username"]
	pesan = """
Hai @%s selamat datang di Corona Info

Disini anda bisa meminta informasi seputar corona

Tentang:
  Author : Billal Fauzan
  Version: 0.1
  Name   : Corona Info

Jadwal Aktif:
  senin - kamis = 06.00 WIB/20.00 WIB
  jumat = 06.00 WIB/11.00 WIB
  sabtu = 12.00 WIB/20.00 WIB

Bot Ini Masih Ilegal
"""%(nama)
	tampil(update, pesan)
	print ("[*] Memulai dgn command: /start")

def bantuan(update, context):
	print ("[*] Meminta Bantuan")
	text = """
Hai Selamat Datang Di Corona Info

Perintah
  help      = meminta bantuan
  local     = meminta informasi corona (indonesia)
  global    = meminta informasi corona (seluruh dunia)
  positif   = meminta informasi corona yang terjangkit
  meninggal = meminta informasi corona yang meninggal
  cegah     = lihat cara pencegahan
"""
	tampil(update, text)

def local(update, context):
	data = []
	psn = []
	try:
		prov = context.args[0]
		tampil(update, "Meminta Data Ke Server")
		print ("Meminta Data Ke Server")
		r = requests.get("https://api.kawalcorona.com/indonesia/provinsi").json()
		for a in r:
			data.append(a["attributes"])
		for db in data:
			provinsi = db["Provinsi"]
			if prov.lower() in provinsi.lower():
				pesan = """
Provinsi : %s
Positif  : %s
Meninggal: %s
Sembuh   : %s
"""%(provinsi, str(db["Kasus_Posi"]), str(db['Kasus_Meni']), str(db['Kasus_Semb']))
				psn.append(pesan)
		if len(psn) > 0:
			for msg in psn:
				tampil(update, msg)
		elif len(psn) < 0:
			tampil(update, "Provinsi Tidak Di Temukan")
	except IndexError:
		tampil(update, "/local <nama provinsi>")

def ginfo(update, context):
	data = []
	psn = []
	try:
		ngr = context.args[0]
		tampil(update, "Meminta Data Ke Server")
		print ("Meminta Data Ke Server")
		r = requests.get("https://api.kawalcorona.com").json()
		for a in r:
			data.append(a["attributes"])
		for db in data:
			negara = db['Country_Region']
			positif = db['Confirmed']
			meninggal = db['Deaths']
			sembuh = db['Recovered']
			if ngr.lower() in negara.lower():
				pesan = """ 
Negara   : %s
Positif  : %s
Meninggal: %s
Sembuh   : %s
"""%(negara, positif, meninggal, sembuh)
				psn.append(pesan)
		if len(psn) > 0:
			for msg in psn:
				tampil(update, msg)
	except IndexError:
		tampil(update, "/global <nama negara>")

def cegah(update, context):
	c = open("cegah.txt", "r").read()
	print ("Tunggu")
	tampil(update, "Tunggu Sebentar")
	tampil(update, c)

def positif(update, context):
	data = []
	try:
		type = context.args[0]
		nama = context.args[1]
		if type.lower() == "local":
			tampil(update, "Meminta Data Ke Server")
			print ("Meminta Data Ke Server")
			r = requests.get("https://api.kawalcorona.com/indonesia/provinsi").json()
			for a in r:
				data.append(a["attributes"])
			for db in data:
				prov = db["Provinsi"]
				if nama.lower() in prov.lower():
					pesan = """
Provinsi: %s
Positif : %s
					"""%(prov, db["Kasus_Posi"])
					tampil(update, pesan)
		elif type.lower() == "global":
			tampil(update, "Meminta Data Ke Server")
			print ("Meminta Data Ke Server")
			r = requests.get("https://api.kawalcorona.com").json()
			for a in r:
				data.append(a["attributes"])
			for db in data:
				negara = db['Country_Region']
				if nama.lower() in negara.lower():
					pesan = """
Negara : %s
Positif: %s
"""%(negara, db['Confirmed'])
					tampil(update, pesan)
		else:
			tampil("Type yang anda input tidak ada")
	except IndexError:
		tampil(update, """/positif {type} {nama negara/provinsi}

Type:
  local  = wilayah indonesia
  global = seluruh dunia

Negara: nama negara
Provinsi: nama provinsi indonesia
""")
	
def meninggal(update, context):
        data = []
        try:
                type = context.args[0]
                nama = context.args[1]
                if type.lower() == "local":
                        tampil(update, "Meminta Data Ke Server")
                        print ("Meminta Data Ke Server")
                        r = requests.get("https://api.kawalcorona.com/indonesia/provinsi").json()
                        for a in r:
                                data.append(a["attributes"])
                        for db in data:
                                prov = db["Provinsi"]
                                if nama.lower() in prov.lower():
                                        pesan = """
Provinsi: %s
Meninggal : %s
                                        """%(prov, db["Kasus_Meni"])
                                        tampil(update, pesan)
                elif type.lower() == "global":
                        tampil(update, "Meminta Data Ke Server")
                        print ("Meminta Data Ke Server")
                        r = requests.get("https://api.kawalcorona.com").json()
                        for a in r:
                                data.append(a["attributes"])
                        for db in data:
                                negara = db['Country_Region']
                                if nama.lower() in negara.lower():
                                        pesan = """
Negara : %s
Meninggal: %s
"""%(negara, db['Deaths'])
                                        tampil(update, pesan)
                else:
                        tampil("Type yang anda input tidak ada")
        except IndexError:
                tampil(update, """/meninggal {type} {nama negara/provinsi}

Type:
  local  = wilayah indonesia
  global = seluruh dunia

Negara: nama negara
Provinsi: nama provinsi indonesia
""")

@app.route("/")
def index():
#	up = Updater("1081432210:AAGBmcqslDCMvLIW2nmG8l8rAvVSvN19yIA", use_context=True)
	up = Updater("1058922067:AAEWYVrh0RjEHjSDAzZw3tPaTSnvQ40QeCA", use_context=True)
	ud = up.dispatcher
	ud.add_handler(CH("start", mulai))
	ud.add_handler(CH("help", bantuan))
	ud.add_handler(CH("local", local, pass_args=True))
	ud.add_handler(CH("global", ginfo, pass_args=True))
	ud.add_handler(CH("positif", positif, pass_args=True))
	ud.add_handler(CH("meninggal", meninggal, pass_args=True))
	ud.add_handler(CH("cegah", cegah))
	up.start_polling()
#	up.idle()
	return "Status: ON"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=os.environ.get("PORT"),debug=True)

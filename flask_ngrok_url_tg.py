from flask import Flask
from pyngrok import ngrok
import threading,time
import telebot

app = Flask(__name__)
port = 4567
bot_token = "1234567890:AABBCCDDEEffggaasadasb_hfgm6eJ5df"
telegram_user_id_for_new_url=123456789

bot = telebot.TeleBot(bot_token)

@app.route('/', methods=['post', 'get'])
def main():
	return 'working!'

def ngrok_run():
	while True:
		public_url = ngrok.connect(port,return_ngrok_tunnel=True)

		print("\n\t----------------------------\n\n\t"+public_url.public_url+"\n\n\t----------------------------\n")
		print('\t✅ ngrok Working')
		bot.send_message(telegram_user_id_for_new_url,str(public_url.public_url))
		save_time = int(time.time())
		while True:
			time.sleep(60*10)
			if((int(time.time())-save_time)>7*60*60):
				break

		try:
			ngrok.disconnect(ngrok.get_tunnels()[0].public_url)
			ngrok.kill()
			print("\t🔄 Restarting server\n\n\n\n")
		except Exception:
			pass

def bot_run():
	while True:
		try:
			print('\t✅ Bot Working')
			bot.polling()
			sys.exit()
		except Exception as e:
			print(e)
			print('\t🔄 Restart')

if __name__ == '__main__':
	threading.Thread(target=bot_run).start()
	time.sleep(5)
	threading.Thread(target=ngrok_run).start()
	app.run(host='0.0.0.0', port=port)
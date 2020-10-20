from flask import Flask
from pyngrok import ngrok
import urllib3,threading,time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
port = 4567

@app.route('/', methods=['post', 'get'])
def main():
	return 'working!'

def ngrok_run():
	while True:
		public_url = ngrok.connect(port,return_ngrok_tunnel=True)

		print("\n\t----------------------------\n\n\t"+public_url.public_url+"\n\n\t----------------------------\n")

		save_time = int(time.time())
		while True:
			time.sleep(60*10)
			if((int(time.time())-save_time)>7*60*60):
				break

		try:
			ngrok.disconnect(ngrok.get_tunnels()[0].public_url)
			ngrok.kill()
			print("\tRestarting server\n\n\n\n")
		except Exception:
			pass

if __name__ == '__main__':
	threading.Thread(target=ngrok_run).start()
	app.run(host='0.0.0.0', port=port)
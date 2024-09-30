from flask import Flask
import requests
import os, json, re, uuid
import socket
app = Flask(__name__)

def registration():
	mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
	name = socket.gethostname()
	headers = {'X-MAC-Addr':mac, 'X-PC-Name':name}
	data = requests.get('http://shh.stariybog.ru/auth_pc', headers=headers).content
	print(data)
	data = json.loads(data)
	data['tasks'] = {'completed':0, 'failed':0}
	print(data)
	with open('config.json', 'w') as f:
		f.write(json.dumps(data))

	return data['code']

def get_data():
	with open('config.json') as f:
		data = json.loads(f.read())
	return data

@app.route('/')
def main():
	if not os.path.exists('config.json'):
		registration()

	return json.dumps(get_data())

if __name__ == "__main__":
	app.run('0.0.0.0', 6124)
else:
	print(__name__)
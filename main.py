from app import app, get_data
from threading import Thread
from parser import main_parser

def run_server():
	app.run('0.0.0.0', 6124)

if __name__ == "__main__":
	server_thread = Thread(target=run_server)
	server_thread.setDaemon(True)
	server_thread.start()

	parser_thread = Thread(target=main_parser, args=(get_data(),))
	parser_thread.setDaemon(True)
	parser_thread.start()
	while True:
		pass
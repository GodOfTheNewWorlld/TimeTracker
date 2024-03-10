import platform
import sys
from datetime import datetime, timedelta
from os import makedirs, path, system
from time import time
from ast import literal_eval
from setup import setup
from utils import cyan, green, magenta, red, white
from utils import generate_activites_times
from utils import h

saved = True
timestamp = time()
activities = []

open("save.py", "a")  # Touch save file
from save import *

ARGS, ACTIVITIES = setup("tracker")
weeks = (timestamp - activities[0][1]) // (7 * 24 * h) if activities else 0


def data_save(saved=True) -> None:
	with open("save.py", "w", encoding='UTF-8') as file:
		file.write(f"{saved = }\n{timestamp = }\n")

		if not activities:  # Проверка на пустоту списка
			file.write("activities = []\n")
		else:
			file.write("activities = [\n")
			for i in activities:
				file.write(f"\t{i},\n")
			file.write("]\n")

	# Weekly dump
	global weeks
	if saved and activities:  # Проверка на пустоту списка
		if (timestamp - activities[0][1]) // (7 * 24 * h) > weeks:
			weeks += 1

			filename = f"./dumps/week-{round(weeks)} ({activities[-1][2][:10]}).py"
			makedirs(path.dirname(filename), exist_ok=True)

			with open(filename, "w") as file:
				file.write(f"{saved = }\ntimestamp = {activities[0][1] + weeks * 7 * 24 * h}\n")
				if not activities:  # Проверка на пустоту списка
					file.write("activities = []\n")
				else:
					file.write("activities = [\n")
					for i in activities:
						file.write(f"\t{i},\n")
					file.write("]\n")


def stages_formatter(stages, verb=0):
	if verb:
		form = ["этапа", "этапов", "этапов"]
	else:
		form = ["этап", "этапа", "этапов"]

	last_digit = int(str(stages)[-1])
	last_2_digits = int(str(stages)[-2:])

	if last_digit == 1 and last_2_digits != 11:
		return f"{magenta}{stages}{white} {form[0]}"

	if 1 <= last_digit <= 4 and (last_2_digits < 10 or last_2_digits > 20):
		return f"{magenta}{stages}{white} {form[1]}"

	return f"{magenta}{stages}{white} {form[2]}"


def analytics():
	if not activities:  # Проверка на пустоту списка
		return

	sum_all = timestamp - activities[0][1]
	print(
		f"Итоги {stages_formatter(len(activities), 1)} "
		f"({cyan}{timedelta(0, round(sum_all))}{white})"
	)
	print()
	activities_times = generate_activites_times(activities, timestamp)
	save_activities = set([i[0] for i in activities])

	# Analyze all data
	for activity_name in ACTIVITIES:
		if activity_name not in save_activities: continue

		activity_time = sum(activities_times[activity_name])
		if activity_time == 0:
			continue

		activity_percentage = activity_time / sum_all * 100
		activity_counter = len(activities_times[activity_name])
		activity_mean = activity_time / activity_counter

		print(
			f"{activity_name} ({stages_formatter(activity_counter)}) ({round(activity_percentage, 2)}%)\n"
			f"Всего: {cyan}{timedelta(0, round(activity_time))}{white}\n"
			f"В среднем {cyan}{timedelta(0, round(activity_mean))}{white} за этап\n"
		)


def clear_activities():
	global activities
	activities.clear()
	data_save()
	print(f'\n{cyan}Все активности удалены{white}')


# Error checking
if not saved:
	input(f"Последняя сессия была прервана: {activities[-1][0]} ({activities[-1][2]})")
	input(f"Добавление потерянного времени: {cyan}+{timedelta(0, int(time() - timestamp))}{white}\n")

	timestamp = time()
	data_save()

while True:
	system("cls" if platform.system() == "Windows" else "clear")

	# Header
	activity = len(activities)
	stageline = f"{red}Список занятий пуст{white}"

	# Изменено
	if activities:
		stageline = (
			f"Этап {magenta}{activity}{white}, {activities[-1][0]} "
			f"({datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')}) "
			f"({cyan}{timedelta(0, round(timestamp - activities[-1][1]))}{white})\n"
		)
		print(stageline)

	# Activities
	print("Выбор занятия:")
	for i, name in enumerate(ACTIVITIES):
		print(f"{green}{i + 1}{white}: {name}")

	print()

	for i, name in enumerate([
		"Завершить сессию",
		"Удалить последнее занятие",
		"Изменить время последнего занятия",
		"Добавить подпись к последнему занятию",
		"Очистить все занятия"
	]):
		print(f"{green}{'edcif'[i]}{white}: {name}")

	# Gain input
	try:
		session_id = input("\nВвод: ")
	except Exception as exc:
		print()
		input(f"\n{red}Неверный ввод{white}")
		continue

	if session_id.isdigit():
		session_id = int(session_id)
	elif session_id in ('e', 'd', 'c', 'i', 'f'):
		session_id = len(ACTIVITIES) + "edcif".index(session_id) + 1
	else:
		session_id = 0

	print()

	# Create new session
	if 1 <= session_id <= len(ACTIVITIES):
		activity_name = list(ACTIVITIES.keys())[session_id - 1]

		# If activity repeat
		if len(activities) and activity_name == activities[-1][0]:
			print(f"Продолжение предыдущей сессии -> {activities[-1][0]} ({activities[-1][2]})")
			note = activities[-1][3]

		else:
			note = ''
			if activity_name == ARGS["ANOTHER"]:
				note = input("Подпись: ") or (ARGS["ANOTHER_DEFAULT_NOTE"])

			activities.append([
				f"{activity_name}",
				timestamp,
				f"{datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M:%S')}",
				note
			])

		# Wait for input to end session
		data_save(saved=False)
		input(f"<< {activity_name}{'' if not note else ' (' + note + ')'} >>")

		timestamp = time()

	# End session
	if session_id == len(ACTIVITIES) + 1:
		data_save()
		analytics()
		sys.exit()

	# Delete last activity
	if session_id == len(ACTIVITIES) + 2:
		if not len(activities):
			input(stageline)
		else:
			print(f"Удалить: {activities[-1][0]} ({activities[-1][2]})?")
			if input("y/n: ").lower() == "y":
				activities.pop()
			else:
				input(f"\n{red}Удаление отменено{white}")

	# Change last activity time
	if session_id == len(ACTIVITIES) + 3:
		if not len(activities):
			input(stageline)
		else:
			activity_name = activities[-1][0]
			activity_start_time = activities[-1][2]

			activity_lasts = timedelta(0, round(timestamp - activities[-1][1]))
			print(f"Последний этап: {activity_name} ({activity_start_time}) {cyan}{activity_lasts}{white}")

			try:
				allocated_time = literal_eval(input("Этап закончился раньше на: "))
				if allocated_time < activity_lasts.total_seconds():
					timestamp -= allocated_time

					activity_lasts = timedelta(0, round(timestamp - activities[-1][1]))
					input(f"\nНовая продолжительность этапа: {cyan}{activity_lasts}{white}")

				else:
					input(f"\n{red}Этап становится отрицательным, действие отменено{white}")

			except Exception as val:
				input(f"\n{red}Действие отменено{white}")

	# Add a note
	if session_id == len(ACTIVITIES) + 4:
		if not len(activities):
			input(stageline)
		else:
			activity_name = activities[-1][0]
			activity_start_time = activities[-1][2]
			activity_lasts = timedelta(0, round(timestamp - activities[-1][1]))

			print(
				f"Добавление подписи к предыдущему занятию\n{activity_name} ({activity_start_time}) {cyan}{activity_lasts}{white}")
			note = input("\nПодпись: ")

			activities[-1][-1] = note

	if session_id == len(ACTIVITIES) + 5:
		if not len(activities):
			input(stageline)
		else:
			print("Вы уверены, что хотите удалить все занятия?")
			if input("y/n: ").lower() == "y":
				clear_activities()
			else:
				input(f"\n{red}Удаление отменено{white}")

	data_save()

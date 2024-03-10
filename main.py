import os
import subprocess
import sys

from utils import blue, green, red, white


def tracker_file_call(tracker_path: str) -> None:
	subprocess.run(['python', tracker_path])


def bar_file_call(bar_path: str) -> None:
	process = subprocess.run(['python', bar_path], capture_output=True, text=True)
	if process.returncode == 0:
		input(error_message)
	else:
		print(process.stdout)
		input(success_message)


def map_file_call(map_path: str) -> None:
	process = subprocess.run(['python', map_path], capture_output=True, text=True)
	if process.returncode == 0:
		input(error_message)
	else:
		print(process.stdout)
		input(success_message)


def density_file_call(density_path: str) -> None:
	process = subprocess.run(['python', density_path], capture_output=True, text=True)
	if process.returncode == 0:
		input(error_message)
	else:
		print(process.stdout)
		input(success_message)


def circles_file_call(circles_path: str) -> None:
	process = subprocess.run(['python', circles_path], capture_output=True, text=True)
	if process.returncode == 0:
		input(error_message)
	else:
		print(process.stdout)
		input(success_message)


success_message = f"{blue}Успешно выполнено{white}"
error_message = f"{red}Список занятий пуст{white}"

path = os.path.abspath
tracker_file_path = path('tracker.py')
bar_file_path = path('bar.py')
map_file_path = path('map.py')
density_file_path = path('density.py')
circles_file_path = path('circles.py')


# Если система Windows -> cls, иначе -> clear
def clear_screen():
	os.system("cls" if os.name == "nt" else "clear")


def date_request() -> int:
	options = [
		"Добавить занятия",
		"Посмотреть активность за последние две недели",
		"Посмотреть активность за все время",
		"Посмотреть среднее время активности по неделям",
		"Посмотреть активность в виде круга",
		"Завершить сессию"
	]
	for i, name in enumerate(options, start=1):
		print(f"{green}{i}{white}: {name}")

	while True:
		try:
			activity_operation = int(input('\nВвод: '))
			if activity_operation in (1, 2, 3, 4, 5, 6):
				return activity_operation
			else:
				raise ValueError
		except ValueError:
			input(f"\n{red}Неверный ввод{white}")
			clear_screen()


def basic_logic() -> None:
	activity_operation: int = date_request()

	match activity_operation:
		case 1:
			tracker_file_call(tracker_file_path)
		case 2:
			bar_file_call(bar_file_path)
		case 3:
			map_file_call(map_file_path)
		case 4:
			density_file_call(density_file_path)
		case 5:
			circles_file_call(circles_file_path)
		case 6:
			sys.exit()


def main():
	while True:
		clear_screen()
		basic_logic()


if __name__ == '__main__':
	main()

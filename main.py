import os
import subprocess
import sys

from utils import blue, green, red, white


# Если система Windows -> cls, иначе -> clear
def clear_screen():
	os.system("cls" if os.name == "nt" else "clear")


def date_request() -> int:
	options = (
		"Добавить занятия",
		"Посмотреть активность за последние две недели",
		"Посмотреть активность за все время",
		"Посмотреть среднее время активности по неделям",
		"Посмотреть активность в виде круга",
		"Завершить сессию"
	)

	while True:
		for ind, name in enumerate(options, start=1):
			print(f"{green}{ind}{white}: {name}")

		try:
			activity_operation = int(input('\nВвод: '))
			if activity_operation in (1, 2, 3, 4, 5, 6):
				return activity_operation
			else:
				raise ValueError
		except ValueError:
			input(f"\n{red}Неверный ввод{white}")
			clear_screen()


def file_call(file_path: str) -> None:
	try:
		process = subprocess.run(['python', file_path], capture_output=True, text=True)
		if process.returncode == 0:
			input(f"{red}Список занятий пуст{white}")
		else:
			print(process.stdout)
			input(f"{blue}Успешно выполнено{white}")
	except Exception as e:
		print(f"{red}{e}{white}")


def basic_logic() -> None:
	file_paths = {
		1: 'tracker.py',
		2: 'bar.py',
		3: 'map.py',
		4: 'density.py',
		5: 'circles.py'
	}
	while True:
		activity_operation: int = date_request()

		if activity_operation in file_paths:
			file_call(os.path.abspath(file_paths.get(activity_operation)))
		elif activity_operation == 6:
			sys.exit()


def main():
	while True:
		clear_screen()
		basic_logic()


if __name__ == '__main__':
	main()

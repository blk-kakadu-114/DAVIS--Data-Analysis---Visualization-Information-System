import cmd
import os

class MyConsole(cmd.Cmd):
    prompt = '> '  # Приглашение командной строки

    def do_hello(self, line):
        """Приветствие с именем"""
        print("Hello,", line)

    def do_sum(self, line):
        """Сложение чисел"""
        try:
            numbers = [int(x) for x in line.split()]
            print("Sum:", sum(numbers))
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")
    
    def do_ls(self, line):
        """Список файлов и каталогов в текущем каталоге"""
        files = os.listdir(os.getcwd())
        for file in files:
            print(file)

    def do_cd(self, line):
        """Смена текущего каталога"""
        try:
            os.chdir(line)
        except FileNotFoundError:
            print("Directory not found")
        except PermissionError:
            print("Permission denied")
        else:
            print("Directory changed to", os.getcwd())

    def do_quit(self, line):
        """Выход из программы"""
        return True

    def default(self, line):
        """Обработка неизвестных команд"""
        print("Invalid command")

if __name__ == '__main__':
    console = MyConsole()
    console.cmdloop('Starting prompt...')
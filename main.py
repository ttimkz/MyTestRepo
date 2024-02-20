import functions as f
import admin

print("Добро пожаловать в банк SkyLearn!")

try:
  current_user = None
  bank = f.BankSystem(None)
  while True:
    command = input("\nВыберите Действие:\n1. Войти\n2. Регистрация\n3. Выход\n\n>")
    if command == '1':
      current_user = bank.checklogin()
      if current_user == None:
        print("\n--Не верное имя пользователя или пароль!--")
      else:
        print(f"Добро пожаловать {current_user}!")
        while True:
          try:
            command = admin.goal(current_user)
            if command == '1':
              bank.deposit(current_user)
            elif command == '2':
              bank.extract_money(current_user)
            elif command == '3':
              bank.get_balance(current_user)
            elif command == '4':
              bank.history(current_user)
            elif command == '5':
              bank.transfer_money(current_user)
            elif command == '6':
              f.os.system('clear')
              print ("\n--ВЫ ВЫШЛИ ИЗ СИСТЕМЫ--\n")
              break
            elif command == '7' and current_user  == 'admin':
              continue
            else:
              print("\n--ОШИБКА ВВОДА--")
          except Exception as e:
            f.logging.error(f"Ошибка: {e}")
    elif command == '2':
      bank.registration()
    else:
      print("\n--ОШИБКА ВВОДА--")
except Exception as e:
  f.logging.error(f"Ошибка: {e}")
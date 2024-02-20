import time
import re
import logging
import json
import os

logging.basicConfig(filename='errors.log', level=logging.ERROR)

now = time.localtime()


class BankSystem:

  def __init__(self, bank_db_file):
    self._bank_db_file = bank_db_file
    self._bank_db = self.read_file()

  #-------Read File---------
  def read_file(self):
    try:
      with open('clients.json', 'r') as f:
        return json.load(f)
    except Exception as e:
      logging.error("Не удалось прочитать базу данных\nПричина: ", e)
#-------Write File---------

  def write_file(self):
    try:
      with open('clients.json', 'w') as f:
        json.dump(self._bank_db, f, ensure_ascii=False, indent=4)
    except Exception as e:
      logging.error("Не удалось написать в базу данных\nПричина: ", e)

  #-------Check Login---------
  def checklogin(self):
    try:
      os.system('clear')
      username = input("\nВведите логин\n>")
      password = input("Введите пароль\n>")
      for user in self._bank_db["users"]:
        if user["username"] == username and user["password"] == password:
          return username
      logging.error(
          f"Не верное имя пользователя '{username}' или пароль '{password}'")
    except Exception as e:
      logging.error(f"Ошибка: {e}")

#-------Get Current User---------

  def get_current_user(self, username):
    try:
      for user in self._bank_db["users"]:
        if user["username"] == username:
          return user
    except Exception as e:
      logging.error(f"Ошибка: {e}")

  #-------Balance-----------
  def get_balance(self, current_user):
    user = self.get_current_user(current_user)
    return print(f"Ваш баланс: {user['amount']}")
#-------Check Input----------

  def check_integer(self, command):
    try:
      user_input = int(input(command))
      if user_input > 0:
        return user_input
      else:
        return print("\n--Введите не отрицательное число--")
    except:
      return print("\n--Введите целое число--")
#-------Deposit money---------

  def deposit(self, current_user):
    os.system('clear')
    self.get_balance(current_user)
    money = self.check_integer("Введите сумму:\n>")
    user = self.get_current_user(current_user)
    user["amount"] += money
    current_time = time.strftime("%H:%M:%S", now)
    user["history"].append(
        f"UTC {current_time}: Пополнение счета - {money} USD")
    self.write_file()
    print("\nБаланс пополнен!")
    self.get_balance(current_user)

#-------Extarct money---------

  def extract_money(self, current_user):
    os.system('clear')
    self.get_balance(current_user)
    money = self.check_integer("Введите сумму:\n>")
    user = self.get_current_user(current_user)
    user["amount"] -= money
    current_time = time.strftime("%H:%M:%S", now)
    user["history"].append(
        f"UTC {current_time}: Снятие со счета - {money} USD")
    self.write_file()
    print("\nСнятие с баланса!")
    self.get_balance(current_user)
#-------History------------

  def history(self, current_user):
    os.system('clear')
    print("--История счета--")
    user = self.get_current_user(current_user)
    history = user["history"]
    if len(history) < 1:
      return print("\n(История пуста)")
    for act in history:
      print(f"\n{act}")
#-------Transfer------------

  def transfer_money(self, current_user):
    os.system('clear')
    self.get_balance(current_user)
    user = self.get_current_user(current_user)
    for user in self._bank_db['users']:
      if user['username'] != current_user:
        print(f"@ {user['username']}")
    recipient = input("Введите логин получателя:\n>")
    if current_user == recipient:
      return print("\nВы не можете перевести сами себе !--")
    try:
      user = self.get_current_user(current_user)
      money = self.check_integer("\nВведите сумму для перевода:\n>")
      if money > user["amount"]:
        return print("\n--Не достатчно баланса для перевода !--\n")
        logging.error(
            f"Не достаточно баланса '{money}' у '{current_user}' для перевода")
      user = self.get_current_user(recipient)
      user["amount"] += money
      current_time = time.strftime("%H:%M:%S", now)
      user["history"].append(
          f"UTC {current_time}: Пополнение средств от пользователя {current_user} - {money} USD"
      )
      user = self.get_current_user(current_user)
      user["amount"] -= money
      user["history"].append(
          f"UTC {current_time}: Перевод средств пользователю {recipient} - {money} USD"
      )
      print(f"Перевод на сумму {money} USD выполнен успешо")
      self.write_file()
    except Exception as e:
      return print("\n--Ошибка, пользователь не найден--")
      logging.error(f"Пользователь {recipient} не неайден {e}")


#---------REGISTER----------------

  def is_valid_password(self, password):
    pattern = re.compile(r'[!@#$%^&*()<>?/\|}{~:]')
    return not bool(pattern.search(password))

  def registration(self):
    try:
      os.system('clear')
      checkuser = False
      newuserlogin = input(
          "------Регистрация пользователя------\nВведите логин: ")
      if len(newuserlogin.strip()) <= 0:
        return print("\n--Вы ввели пустое значение !--")
      for user in self._bank_db["users"]:
        if user["username"] == newuserlogin:
          checkuser = True
      if checkuser == True:
        return print("\n--Пользователь с таким именем существует !--")
      newuserpassword = input(
          "\n--Пароль должен содержать не менее 3 символов и 1 регулярнове выражение !--\n\nСоздайте пароль: "
      )
      if len(newuserpassword.strip()) <= 3:
        return print("Пароль должен иметь не менее 3 символов")
      if self.is_valid_password(newuserpassword) == False:
        new_user = {
            "username": newuserlogin,
            "password": newuserpassword,
            "amount": 0,
            "history": [],
        }
        self._bank_db['users'].append(new_user)
        print(f"\nВы создали нового пользователя {newuserlogin} !")
        self.write_file()
      else:
        logging.error(f"Пароль '{newuserpassword}' не подходит")
        return print("\nПароль должен содержать регулярные выражения !")
    except Exception as e:
      logging.error(f"Ошибка: {e}")
      print

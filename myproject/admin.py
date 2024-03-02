import functions as f

def goal(current_user):
  try:    
    bank = f.BankSystem(None)
    print(f"\nВыберите действие:\n1. Пополнение счета\n2. Снятие со счета\n3. Просмотр баланса\n4. История транзакции\n5. Перевод средств\n6. Выход")
    if current_user == 'admin':
      print('7. База банных пользователей')
    command = input("\n>")
    if command == '7' and current_user == 'admin':
      print(f'\n----База данных пользователей----\n')
      for user in bank._bank_db['users']:
        print(f"Имя пользователя: {user['username']}\nПароль: {user['password']}\nБаланс: {user['amount']}\n--------------------")
      return command
    else:
      return command
  except Exception as e:
    f.logging.error(f"Ошибка: {e}")
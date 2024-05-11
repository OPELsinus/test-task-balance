import datetime
from pathlib import *


def date_inp():
    """
      Запрашивает у пользователя дату в формате ГГГГ-ММ-ДД или предлагает выбрать текущую дату.

      Returns:
          datetime.date: Введенная дата или сегодняшняя дата.
    """

    print('Укажите дату платежа:')
    print(' [1] Текущее')
    print(' [2] Указать вручную в формате YYYY-MM-DD')
    rec_date_ = None
    date_input = None
    while True:
        try:
            # Проверяем корректность введённых данных

            date_input = int(input()) if date_input is None else date_input
            if date_input == 1:
                rec_date_ = datetime.date.today()
                break

            elif date_input == 2:

                print('Дата: ', end='')
                try:
                    rec_date_ = input()
                    _ = datetime.date(int(rec_date_.split('-')[0]), int(rec_date_.split('-')[1]), int(rec_date_.split('-')[2]))
                    break
                except:
                    print(' [!] Укажите верную дату YYYY-MM-DD (ГГГГ-ММ-ДД)')
            else:
                raise Exception('')
        except:
            date_input = None
            print(' [!] Выберите 1 или 2')

    return rec_date_


def category_inp():
    """
      Запрашивает у пользователя категорию (Доход или Расход).

      Returns:
          str: Выбранная категория ("Доход" или "Расход").
    """

    print('Укажите категорию:')
    print(' [1] Доход')
    print(' [2] Расход')

    while True:
        try:
            # Проверяем корректность введённых данных

            category_input = input()
            if category_input == '1' or category_input == 'Доход':
                return 'Доход'
            elif category_input == '2' or category_input == 'Расход':
                return 'Расход'
            else:
                raise Exception('')
        except:
            print(' [!] Выберите 1 или 2')


def summ_inp():
    """
      Запрашивает у пользователя числовое значение суммы.

      Returns:
          int: Введенная сумма.
    """

    print('Укажите сумму: ', end='')

    while True:
        try:
            # Проверяем корректность введённых данных

            rec_summ = int(input())
            return rec_summ
        except:
            print(' [!] Напишите число')


def description_inp():
    """
      Запрашивает у пользователя описание записи.

      Returns:
          str: Введенное описание.
    """

    print('Укажите описание: ', end='')

    return input()


def additional_fields_inp():
    """
      Запрашивает у пользователя дополнительные пары ключ-значение для записи.

      Returns:
          list: Список словарей, где каждый словарь представляет собой дополнительное поле с его названием и значением.
    """

    additional_fields = []
    finish = False

    while True:

        print('Хотите добавить ещё поля?')
        print(' [1] Да')
        print(' [2] Нет')

        while True:
            try:
                # Проверяем корректность введённых данных

                choice = input()
                if choice == '1' or choice == 'Да':
                    print('Укажите название поля: ', end='')
                    field_name = input()
                    print('Укажите значение поля: ', end='')
                    field_value = input()
                    additional_fields.append({field_name: field_value})
                    break

                if choice == '2' or choice == 'Нет':
                    finish = True
                    break
                else:
                    raise Exception('')
            except:
                print(' [!] Выберите 1 или 2')

        if finish:
            break

    return additional_fields


def get_balance():
    """
      Считывает информацию о балансе из текстового файла, вычисляет общий баланс и печатает его.
    """
    print('\n---------------------------')
    print('Вывод текщуего баланса')

    all_recordings = dict()

    with open('testtask - balance.txt', 'rt', encoding='utf-8') as file:
        ind = 0
        for line in file:

            line = line.replace('\n', '')

            if line == '':
                ind += 1
                continue

            if ind not in all_recordings.keys():
                all_recordings.update({ind: {line.split(':')[0]: line.split(':')[1].strip()}})
            else:
                all_recordings.get(ind).update({line.split(':')[0]: line.split(':')[1].strip()})

    total_balance = 0
    for record in all_recordings.items():

        current_category = record[1].get('Категория').replace(' ', '')
        current_summ = int(record[1].get('Сумма').replace(' ', ''))

        if current_category == 'Расход':
            total_balance -= current_summ

        if current_category == 'Доход':
            total_balance += current_summ

    print(f'Текущий баланс: {total_balance}')


def add_recording():
    """
      Запрашивает у пользователя информацию о новой записи (дата, категория, сумма, описание, дополнительные поля)
      и добавляет ее в текстовый файл.
    """

    print('\n---------------------------')
    print('Добавление новой записи')

    rec_date = None
    rec_category = None
    rec_summ = None
    rec_description = None

    with open('testtask - balance.txt', 'a', encoding='utf-8') as file:

        file.write('\n')

        # ----- Определяем дату -----

        rec_date = date_inp()

        # ----- Определяем категорию -----

        rec_category = category_inp()

        # ----- Определяем сумму -----

        rec_summ = summ_inp()

        # ----- Определяем описание -----

        rec_description = description_inp()

        # ----- Определяем дополнительные поля -----

        additional_fields = additional_fields_inp()

        # ----- Вводим данные в текстовый файл -----

        file.write(f'Дата: {rec_date}\n')
        file.write(f'Категория: {rec_category}\n')
        file.write(f'Сумма: {rec_summ}\n')
        file.write(f'Описание: {rec_description}\n')
        for field in additional_fields:
            for field_name, field_value in field.items():
                file.write(f'{field_name}: {field_value}\n')


def edit_recording():
    """
      Позволяет пользователю выбрать существующую запись, отредактировать ее поля (дата, категория, сумма, описание)
      и сохранить изменения в текстовый файл.
    """
    print('\n---------------------------')
    print('Изменение существующей записи')

    all_recordings = dict()

    # Собираем все записи из текстового файла

    with open('testtask - balance.txt', 'rt', encoding='utf-8') as file:
        ind = 0
        for line in file:

            line = line.replace('\n', '')

            if line == '':
                ind += 1
                continue

            if ind not in all_recordings.keys():
                all_recordings.update({ind: {line.split(':')[0]: line.split(':')[1].strip()}})
            else:
                all_recordings.get(ind).update({line.split(':')[0]: line.split(':')[1].strip()})

    for record in all_recordings.items():
        print(f'------- [{record[0]}] --------')
        for record_key, record_val in record[1].items():
            print(f'{record_key}: {record_val}')
        print('')

    print('Выберите запись для редактирования: ')

    for record in all_recordings.items():
        print(f'[+] {record[0]}')

    # Ждём выбора нужной записи
    while True:
        try:
            id_input = int(input())
            if id_input < len(all_recordings):
                break
            else:
                raise Exception('')
        except:
            print(' [!] Выберите 1 или 2')

    for field_name, field_value in all_recordings.get(id_input).items():

        # Изменяем или пропускаем каждое поле данной записи
        print('------------------------------------------------------------')
        print(f' [*] Текущее поле | {field_name}: {field_value}')
        print(f' [+] Изменить?')
        print(f' [1] Да')
        print(f' [2] Нет')

        while True:
            try:
                choice = input()
                if choice == '1' or choice == 'Да':
                    if field_name == 'Дата':
                        all_recordings[id_input][field_name] = date_inp()
                        break
                    elif field_name == 'Категория':
                        all_recordings[id_input][field_name] = category_inp()
                        break
                    elif field_name == 'Сумма':
                        all_recordings[id_input][field_name] = summ_inp()
                        break
                    else:
                        print('Укажите значение поля: ', end='')
                        field_value_ = input()
                        all_recordings[id_input][field_name] = field_value_
                        break
                if choice == '2' or choice == 'Нет':
                    break
                else:
                    raise Exception('')
            except:
                print(' [!] Выберите 1 или 2')

    # Запимываем изменённые данные в текстовый файл
    Path.unlink('testtask - balance.txt')
    with open('testtask - balance.txt', 'w', encoding='utf-8') as file:
        for record in all_recordings.items():
            print(f'------- [{record[0]}] --------')
            for record_key, record_val in record[1].items():
                print(f'{record_key}: {record_val}')
                file.write(f'{record_key}: {record_val}\n')
            file.write('\n')
            print('')


def search_recording():
    """
      Позволяет пользователю искать записи по определенному полю (дата, категория, сумма, описание)
      и отображает все найденные совпадения.
    """

    print('\n---------------------------')
    print('Поиск записи')

    print('Укажите поле по которому искать:')
    print(' [1] Дата')
    print(' [2] Категория')
    print(' [3] Сумма')
    print(' [4] Описание')
    search_field = None
    search_value = None

    # Выбираем поле, по которому будет искатб выбранное значение
    while True:
        try:
            field_input = input()
            if field_input == '1' or field_input == 'Дата':
                search_field = 'Дата'
                search_value = date_inp()
                break
            elif field_input == '2' or field_input == 'Категория':
                search_field = 'Категория'
                search_value = category_inp()
                break
            elif field_input == '3' or field_input == 'Сумма':
                search_field = 'Сумма'
                search_value = summ_inp()
                break
            elif field_input == '4' or field_input == 'Описание':
                search_field = 'Описание'
                search_value = description_inp()
                break
            else:
                raise Exception('')
        except:
            print(' [!] Выберите 1 / 2 / 3 / 4')

    all_recordings = dict()

    with open('testtask - balance.txt', 'rt', encoding='utf-8') as file:
        ind = 0
        for line in file:

            line = line.replace('\n', '')

            if line == '':
                ind += 1
                continue

            if ind not in all_recordings.keys():
                all_recordings.update({ind: {line.split(':')[0]: line.split(':')[1].strip()}})
            else:
                all_recordings.get(ind).update({line.split(':')[0]: line.split(':')[1].strip()})

    # Ищем тотал совпадений по выбранному полю и значению
    all_matches = []
    for record in all_recordings.items():
        for record_key, record_val in record[1].items():
            if record_key == search_field and str(search_value) == str(record_val):
                all_matches.append(record[0])

    print(f'\nВсего найдено записей: {len(all_matches)}:')

    for record in all_recordings.items():
        if record[0] in all_matches:
            print(f'------- [{record[0]}] --------')
            for record_key, record_val in record[1].items():
                print(f'{record_key}: {record_val}')
            print('')


def delete_recording():
    """
    Позволяет пользователю выбрать существующую запись и удалить ее из текстового файла.
    """
    print('\n---------------------------')
    print('Удаление существующей записи')

    all_recordings = dict()

    # Собираем все записи
    with open('testtask - balance.txt', 'rt', encoding='utf-8') as file:
        ind = 0
        for line in file:

            line = line.replace('\n', '')

            if line == '':
                ind += 1
                continue

            if ind not in all_recordings.keys():
                all_recordings.update({ind: {line.split(':')[0]: line.split(':')[1].strip()}})
            else:
                all_recordings.get(ind).update({line.split(':')[0]: line.split(':')[1].strip()})

    # Выводим все записи
    for record in all_recordings.items():
        print(f'------- [{record[0]}] --------')
        for record_key, record_val in record[1].items():
            print(f'{record_key}: {record_val}')
        print('')

    print('Выберите запись для удаления: ')

    for record in all_recordings.items():
        print(f'[+] {record[0]}')

    # Ждём выбора номера записи
    while True:
        try:
            id_input = int(input())
            if id_input < len(all_recordings):
                break
            else:
                raise Exception('')
        except:
            print(' [!] Выберите 1 или 2')

    # Удаляем запись
    all_recordings.pop(id_input)

    # Сохраняем измененённые данные в файл
    Path.unlink('testtask - balance.txt')
    with open('testtask - balance.txt', 'w', encoding='utf-8') as file:
        for record in all_recordings.items():
            print(f'------- [{record[0]}] --------')
            for record_key, record_val in record[1].items():
                print(f'{record_key}: {record_val}')
                file.write(f'{record_key}: {record_val}\n')
            file.write('\n')
            print('')


def get_all_recordings():
    """
      Позволяет пользователю увидеть все записи
    """
    print('\n---------------------------')
    print('Вывод всех записей')

    all_recordings = dict()

    # Собираем все записи из текстового файла

    with open('testtask - balance.txt', 'rt', encoding='utf-8') as file:
        ind = 0
        for line in file:

            line = line.replace('\n', '')

            if line == '':
                ind += 1
                continue

            if ind not in all_recordings.keys():
                all_recordings.update({ind: {line.split(':')[0]: line.split(':')[1].strip()}})
            else:
                all_recordings.get(ind).update({line.split(':')[0]: line.split(':')[1].strip()})

    for record in all_recordings.items():
        print(f'------- [{record[0]}] --------')
        for record_key, record_val in record[1].items():
            print(f'{record_key}: {record_val}')
        print('')


if __name__ == '__main__':

    while True:

        print('\n\n----- Выберите действие -----')

        print(' [1] Посмотреть баланс')
        print(' [2] Добавить новую запись')
        print(' [3] Редактировать запись')
        print(' [4] Поиск по записям')
        print(' [5] Удалить запись')
        print(' [6] Посмотреть все записи')
        print(' [7] Выйти')
        is_exit = False

        while True:
            try:
                print('\nУкажите действие: ', end='')
                field_input = input()
                if field_input == '1' or field_input == 'Посмотреть баланс':
                    get_balance()
                    break
                elif field_input == '2' or field_input == 'Добавить новую запись':
                    add_recording()
                    break
                elif field_input == '3' or field_input == 'Редактировать запись':
                    edit_recording()
                    break
                elif field_input == '4' or field_input == 'Поиск по записям':
                    search_recording()
                    break
                elif field_input == '5' or field_input == 'Удалить запись':
                    delete_recording()
                    break
                elif field_input == '6' or field_input == 'Посмотреть все записи':
                    get_all_recordings()
                    break
                elif field_input == '7' or field_input == 'Выйти':
                    is_exit = True
                    break
                else:
                    raise Exception('')
            except:
                print(' [!] Выберите 1 / 2 / 3 / 4 / 5')

        if is_exit:

            print('До свидания!')
            break

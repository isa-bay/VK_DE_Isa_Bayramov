"""
python3 generate.py <dir to put files> <%Y-%m-%d date> <days_count> <unique emails count> <events count>
Ex.
python3 generate.py input 2024-09-16 15 15 500
"""


import datetime
import os
import random
import string
import sys


# DOMAIN NAME
EMAIL_PROVIDERS = [
    "gmail.com",
    "ya.ru",
    "mail.ru",
]

# CRUD-операции
ACTION_TYPES = [
    "CREATE",
    "READ",
    "UPDATE",
    "DELETE",
]


# Генерация рандомных string длиной char_num
def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))


# Генерация email
def generate_email():
    return f"{random_char(random.randrange(5, 15))}@{random.choice(EMAIL_PROVIDERS)}"


# Генерация CSV
if __name__ == "__main__":
    dirname = sys.argv[1]  # Имя директории
    dt = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')   # Стартовая дата
    days_cnt = int(sys.argv[3])  # Количество дней
    emails_cnt = int(sys.argv[4])  # Количество email
    emails = [generate_email() for _ in range(emails_cnt)]   # Генерация списка эл. адресов
    events_cnt = int(sys.argv[5])  # Количесвто ежедневных событий

    if not os.path.exists(dirname):  # Создать директорий, если его нет
        os.makedirs(dirname)

    for i in range(days_cnt):
        current_dt = dt + datetime.timedelta(days=i)  # Текущая дата
        filepath = os.path.join(dirname, f"{current_dt.strftime('%Y-%m-%d')}.csv")  # Путь/создание и имя - текущая дата
        with open(filepath, 'w') as out:  # Открывает файл для записи
            out.write("\n".join(  # Запись tmail, action, dt
                f"{random.choice(emails)},{random.choice(ACTION_TYPES)},{current_dt + datetime.timedelta(seconds=random.randrange(0, 60*60*24))}" 
                for _ in range(events_cnt)
                )
            )
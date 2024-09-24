import pandas as pd

import os
import sys
import datetime


# Агрегация данных за один день
def aggregate_daily(input_directory: str, intermediate_directory: str, current_date: datetime.datetime) -> pd.DataFrame:
    file_path = os.path.join(input_directory, f"{current_date.strftime('%Y-%m-%d')}.csv")
    # Путь к файлу с исходными данными
    temp_file_path = os.path.join(intermediate_directory, f"{current_date.strftime('%Y-%m-%d')}_daily.csv")
    # Путь для промежуточного хранения

    if os.path.exists(temp_file_path):  # Загрузка промеж. файла
        print(f"Использовать промежуточный файл: {temp_file_path}")
        return pd.read_csv(temp_file_path)

    if os.path.exists(file_path):  # Обработка исходного файла
        try:
            print(f"Чтение исходного файла: {file_path}")
            df = pd.read_csv(file_path, names=["email", "action", "datetime"])  # чтение csv in dataframe
            aggregated = df.groupby(["email", "action"]).size().unstack(fill_value=0)  # группировка
            aggregated.columns = [f"{col.lower()}_count" for col in aggregated.columns]  # переименовать

            aggregated.to_csv(temp_file_path, index=True)  # сохранение во временный файл
            print(f"Сохранить промежуточный файл: {temp_file_path}")

            return aggregated
        except Exception as e:  # при ошибке вывод
            print(f"Ошибка при обработке: {e}")
            return pd.DataFrame()
    else:
        print(f"Файл не найден: {file_path}, пропускаем.")
        return pd.DataFrame()


# Агрегации данных за неделю
def aggregate_weekly(input_directory, intermediate_directory, output_directory, date_str):
    target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")  # Строка даты в datatime
    data_frames = []  # Список для хранения данных за каждый день

    # Обработка последних 7 дней
    for i in range(7):
        current_date = target_date - datetime.timedelta(days=i)  # Текущая дата
        daily_aggregated = aggregate_daily(input_directory, intermediate_directory, current_date)  # Агрегация за день
        if not daily_aggregated.empty:
            data_frames.append(daily_aggregated)  # Если есть данные, добавляем в список

    # Если данных нет, то вывод и завершаем
    if not data_frames:
        print("Нет данных для агрегации.")
        return

    # Объединение и группируем по email
    print(f"Объединение данных за неделю: {target_date.strftime('%Y-%m-%d')}")
    all_data = pd.concat(data_frames).groupby(["email"]).sum()

    # Сохраняем полученные данные в указанный итоговый файл с недельной агрегацией
    output_file = os.path.join(output_directory, f"{target_date.strftime('%Y-%m-%d')}_weekly.csv")
    all_data.to_csv(output_file, index=True)
    print(f"Недельные агрегированные данные сохранены в {output_file}")


# Вход в программу
if __name__ == "__main__":
    # Аргументы командной строки
    input_dir: str = sys.argv[1]
    intermediate_dir: str = sys.argv[2]
    output_dir: str = sys.argv[3]
    date: str = sys.argv[4]

    # Запуск недельной агрегации
    aggregate_weekly(input_dir, intermediate_dir, output_dir, date)

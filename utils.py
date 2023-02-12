import requests
from datetime import datetime


def get_data(url):
    """
    Запрашивает и получает данные из внешнего ресурса
    :param url: глобальная переменная из main
    :return: данные в формате json (список) и статус ответа.
    Функция обрабатывает исключения: ошибку соединения, некорректного адреса и несоответствия
    формата данных. Возвращает "None " в перечисленных случаях.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:             # OK
            return response.json(), "INFO: Data received successfully\n"
        return None, f"ERROR: status code: {response.status_code}\n"
    except requests.exceptions.ConnectionError:   # connection error
        return None, "ERROR requests.exceptions.ConnectionError\n"
    except requests.exceptions.JSONDecodeError:   # format error
        return None, "ERROR requests.exceptions.JSONDecodeError\n"


def get_filtered_data(data, filtered_empty_from=False):
    """
    фильтрация данных: оставляем только операции с состоянием "EXECUTED"
    :param data: полученный нефильтрованный список с данными
    :param filtered_empty_from: флаг фильтрации из main
    :return: отфильтрованные данные (список)
    """
    data = [x for x in data if "state" in x and x["state"] == "EXECUTED"]   # если state существует и "EXECUTED"
    if filtered_empty_from:                                                 # фильтруем, если флаг True
        data = [x for x in data if "from" in x]                             # если from существует
    return data


def get_last_values(data, count_last_values):
    """
    сортировка данных по дате в обратном порядке и
    отделение указанного числа последних транзакций
    :param data: отфильтрованные, но несортированные данные
    :param count_last_values: число последних транзакций
    :return: данные с последними транзакциями
    """
    data = sorted(data, key=lambda x: x["date"], reverse=True)
    data = data[:count_last_values]
    return data


def get_formatted_data(data):
    """
    Изменяет представление данных и переупаковывает их в требуемом формате:
    <дата перевода> <описание перевода>
    <откуда> -> <куда>
    <сумма перевода> <валюта>
    :param data: указанное параметром количество (5) отсортированных по времени транзакций (операций) - список
    :return: переупакованный список операций клиента в требуемом формате
    """
    formatted_data = []
    for row in data:
        date = datetime.strptime(row["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        description = row["description"]
        from_info, from_bill = "", ""           # в случае отсутствия этих параметров
        if "from" in row:
            sender = row["from"].split()
            from_bill = sender.pop(-1)
            from_bill = f"{from_bill[:4]} {from_bill[4:6]}** **** {from_bill[-4:]}"
            from_info = " ".join(sender)
        to = f"{row['to'].split()[0]} **{row['to'][-4:]}"
        operation_amount = f"{row['operationAmount']['amount']} {row['operationAmount']['currency']['name']}"

        formatted_data.append(f"""\
{date} {description}
{from_info} {from_bill} -> {to}
{operation_amount}""")

    return formatted_data

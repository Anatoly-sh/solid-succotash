import requests
from pprint import pprint
from datetime import datetime


def get_data(url):
    try:
        response = requests.get(url)
#        print(response.status_code)
        if response.status_code == 200:             # OK
            return response.json(), "INFO: Data received successfully\n"
        return None, f"ERROR: status code: {response.status_code}\n"
    except requests.exceptions.ConnectionError:   # connection error
        return None, "ERROR requests.exceptions.ConnectionError\n"
    except requests.exceptions.JSONDecodeError:   # format error
#        print(response.url)
        return None, "ERROR requests.exceptions.JSONDecodeError\n"


def get_filtered_data(data, filtered_empty_from=False):
#    pprint(data[:5])
#    print(len(data))
    data = [x for x in data if "state" in x and x["state"] == "EXECUTED"]
#    print(len(data))
    if filtered_empty_from:
        data = [x for x in data if "from" in x]
#    print(len(data))
    return data


def get_last_values(data, count_last_values):
    data = sorted(data, key=lambda x: x["date"], reverse=True)
#    for x in data:
#        print(x["date"])
    data = data[:count_last_values]
    return data


def get_formatted_data(data):
    formatted_data = []
#    pprint(data[0])
    for row in data:
        date = datetime.strptime(row["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
#        print(date)
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

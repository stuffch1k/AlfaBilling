import datetime
import requests

BASE_URL = "http://127.0.0.1:8008"

clients = [
    {
      "name": "Иван",
      "surname": "Назаров",
      "patronymic": "Андреевич",
      "number": "9540449024",
      "contract_number": "1",
      "passport": "3638 630021",
      "password": "string"
    },
    {
      "name": "Николай",
      "surname": "Кузьмин",
      "patronymic": "Даниилович",
      "number": "9275996108",
      "contract_number": "2",
      "passport": "6453 302663",
      "password": "string"
    },
    {
      "name": "Анастасия",
      "surname": "Тетерина",
      "patronymic": "Оскаровна",
      "number": "9682133209",
      "contract_number": "3",
      "passport": "9095 770096",
      "password": "string"
    },
    {
      "name": "Егор",
      "surname": "Петров",
      "patronymic": "Александрович",
      "number": "9601786369",
      "contract_number": "4",
      "passport": "9830 578455",
      "password": "string"
    },
    {
      "name": "Ксения",
      "surname": "Родионова",
      "patronymic": "Александрович",
      "number": "9154872802",
      "contract_number": "5",
      "passport": "6680 072013",
      "password": "string"
    },
    {
      "name": "Оксана",
      "surname": "Сидорова",
      "patronymic": "Тимуровна",
      "number": "9779738659",
      "contract_number": "6",
      "passport": "0150 512098",
      "password": "string"
    },
    {
      "name": "Сергей",
      "surname": "Большаков",
      "patronymic": "Михайлович",
      "number": "9553622401",
      "contract_number": "7",
      "passport": "2760 760900",
      "password": "string"
    },
    {
      "name": "Михаил",
      "surname": "Котов",
      "patronymic": "Алексеевич",
      "number": "9850956313",
      "contract_number": "8",
      "passport": "2327 544115",
      "password": "string"
    },
    {
      "name": "Юлия",
      "surname": "Бурова",
      "patronymic": "Романовна",
      "number": "9155086928",
      "contract_number": "9",
      "passport": "8170 405415",
      "password": "string"
    },
    {
      "name": "Дарья",
      "surname": "Филиппова",
      "patronymic": "Васильевна",
      "number": "9803182580",
      "contract_number": "10",
      "passport": "5886 095674",
      "password": "string"
    }
]

operators = [
    {
      "name": "Мария",
      "surname": "Овчинникова",
      "email": "operator@gmail.com",
      "password": "string"
    },
    {
      "name": "Александр",
      "surname": "Котик",
      "email": "alex@gmail.com",
      "password": "string"
    }
]

services = [
    {
      "service_id": 1,
      "phone_number": "9540449024"
    },
    {
      "service_id": 2,
      "phone_number": "9275996108"
    },
    {
      "service_id": 3,
      "phone_number": "9682133209"
    },
    {
      "service_id": 4,
      "phone_number": "9601786369"
    },
    {
      "service_id": 5,
      "phone_number": "9154872802"
    },
    {
      "service_id": 16,
      "phone_number": "9779738659"
    },
    {
      "service_id": 3,
      "phone_number": "9553622401"
    },
    {
      "service_id": 1,
      "phone_number": "9850956313"
    },
    {
      "service_id": 4,
      "phone_number": "9155086928"
    },
    {
      "service_id": 2,
      "phone_number": "9803182580"
    },
    {
      "service_id": 18,
      "phone_number": "9540449024"
    },
    {
      "service_id": 21,
      "phone_number": "9540449024"
    }
]


def create_10_clients():
    for client in clients:
        requests.post(f"{BASE_URL}/api/auth/jwt/register", json=client)


def create_2_operators():
    for operator in operators:
        requests.post(f"{BASE_URL}/api/auth/jwt/register", json=operator)


def create_payments():
    payment = {
        "amount": 1500,
        "date": datetime.datetime.now().isoformat(),
        "number_id": None
    }

    for number_id in range(1, 11):
        payment["number_id"] = number_id
        requests.post(f"{BASE_URL}/api/payment", json=payment)


def add_services():
    for service in services:
        requests.post(f"{BASE_URL}/api/activated/", json=service)


if __name__ == '__main__':
    try:
        create_10_clients()
        create_2_operators()
        create_payments()
        add_services()
    except Exception as e:
        print(e)





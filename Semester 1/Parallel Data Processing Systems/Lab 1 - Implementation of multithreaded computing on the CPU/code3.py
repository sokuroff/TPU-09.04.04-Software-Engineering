import requests

# URL публичной базы доменов (пример)
url = "https://public-dns.info/nameservers.txt"

response = requests.get(url)
if response.status_code == 200:
    domains = [line.strip() for line in response.text.splitlines() if line.endswith(".ru")]
    with open("custom_ru.txt", "w") as file:
        file.write("\n".join(domains))
    print("Список доменов сохранен в custom_ru.txt")
else:
    print("Не удалось получить список доменов")

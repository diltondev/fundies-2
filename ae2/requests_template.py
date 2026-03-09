import requests


def reqA(): 
    res = requests.get("https://webtris.nationalhighways.co.uk/api/v1.0/sites")
    data = res.json()
    with open("./res.json", "w") as file:
        file.write(str(data).replace("'", '"'))

if __name__ == "__main__":
    reqA()
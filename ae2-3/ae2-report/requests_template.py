import requests


def reqA():
    res = requests.get(
        "https://webtris.nationalhighways.co.uk/api/v1.0/reports/daily?sites=8188&start_date=07032025&end_date=07032025&page=1&page_size=50"
    )
    data = res.json()
    with open("./res.json", "w") as file:
        file.write(str(data).replace("'", '"'))


if __name__ == "__main__":
    reqA()

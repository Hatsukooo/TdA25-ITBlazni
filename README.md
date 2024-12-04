# Tour de App - Django boiler plate

Šablona pro vývoj aplikace pro Tour de App společně s vytvořením a nahráním výstupu

## Lokální spuštění

### Pomocí pipenv

#### Prerekvizity

- Python 3 (pokud nemáš python nainstalovaný, podívej se na https://naucse.python.cz/course/pyladies/)
- pipenv (`pip install --user pipenv` pro Windows, https://pypi.org/project/pipenv/#installation pro Linux dle distribuce)

#### Spuštění

```
pipenv install
pipenv shell
```

```
python3 manage.py runserver 8000
```

Aplikace bude přístupná na `http://127.0.0.1:8000`

### Pomocí dockeru

#### Prerekvizity

- Docker
- (Windows) aktivovaný wsl2

#### Spuštění

```
docker build . -t tda-django
docker run -p 8080:80 -v ${PWD}:/app tda-django
```

Aplikace bude přístupná na `http://127.0.0.1:8080`

## Odevzdání

Jak odevzdat svojí aplikaci můžete najít v našich [vzdělávacích materiálech](https://tourde.app/vzdelavaci-materialy/jak-odevzdavat)

## Databáze

V kontejneru je nakonfigurovaná sqlite3 databáze, jejíž obsah se ukládá do souboru
db.sqlite3

Nastavení databáze lze upravit v souboru settings.py

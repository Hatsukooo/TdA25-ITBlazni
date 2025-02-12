# Tour de App - Flask boiler plate

Šablona pro vývoj aplikace pro Tour de App společně s vytvořením a nahráním výstupu.

## Lokální spuštění

### Python

#### Prerekvizity

- Python 3 (pokud nemáš python nainstalovaný, podívej se na https://naucse.python.cz/course/pyladies/),
- pipenv ( `pip install --user pipenv` pro Windows, https://pypi.org/project/pipenv/#installation pro Linux dle distribuce).
  (Pokud se při instalaci na Windows vyskytla [chyba s proměnnou PATH](PATH_warning.md).)

#### Spuštění

```
pipenv install
pipenv shell
```

Windows

```
flask --app app\app.py init-db
flask --app app\app.py run
```

(`flask is not recognized as an internal or external command, operable program or batch file.` -> Nainstalujte Flask pomocí `pip install Flask`)

Linux / macOS

```
flask --app app/app.py init-db
flask --app app/app.py run
```

Aplikace bude přístupná na `http://127.0.0.1:5000`

### Docker

#### Prerekvizity

- Docker.
- (Windows) aktivovaný wsl2.
  Návod zde: https://tourdeapp.cz/vzdelavaci-materialy/2738-instalace-dockeru-na-windows

#### Spuštění

```
docker build . -t tda-flask
docker run -p 8080:80 -v ${PWD}:/app tda-flask
```

Aplikace bude přístupná na `http://127.0.0.1:8080`

## Virtuální prostředí a správa balíčků

Jak využít nástroj [Pipenv](https://pypi.org/project/pipenv/), který kombinuje pip a virtualenv.

## Odevzdání

Jak odevzdat svojí aplikaci můžete najít v našich [vzdělávacích materiálech](https://tourde.app/vzdelavaci-materialy/jak-odevzdavat)

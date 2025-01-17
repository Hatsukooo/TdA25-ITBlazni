# TdA25-ITBlázni

## 1. Název a členové týmu

**Název týmu:** ITBlázni  
**Členové týmu:**
- Jan Novák (Frontend)
- Petr Svoboda (Backend)
- Jana Malá (DevOps)

Tento tým se účastní soutěže Tour de App pro rok 2025.

## 2. Jaké technologie používá

**Jazyk:** Python 3.9+  
**Framework:** Django 4.x + Django REST Framework  
**Databáze:** SQLite (ve výchozím nastavení)  
**Frontend:** HTML, CSS, JavaScript (případně React/Vue, pokud používáte)  
**Docker:** Pro kontejnerizaci a nasazení  
**GitHub Actions:** (Pokud jste nastavili CI/CD)

**Případně další použité knihovny:**
- pytest / unittest (pokud testujete lokálně)
- django-filter (pokud využíváte server-side filtrování)

## 3. Jak se aplikace spouští

### 3.1 Spuštění bez Dockeru

Naklonování repozitáře:
```sh
git clone https://github.com/Hatsukooo/TdA25-ITBlazni.git
cd TdA25-ITBlazni
```

Vytvoření a aktivace virtuálního prostředí (doporučeno):
```sh
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# nebo venv\Scripts\activate    # Windows
```

Instalace závislostí:
```sh
pip install -r requirements.txt
```

Migrace databáze:
```sh
python manage.py migrate
```

Spuštění vývojového serveru:
```sh
python manage.py runserver
```

Aplikace bude dostupná na adrese [http://127.0.0.1:8000](http://127.0.0.1:8000) (případně [http://localhost:8000](http://localhost:8000)).

### 3.2 Spuštění s Dockerem

Naklonování repozitáře:
```sh
git clone https://github.com/Hatsukooo/TdA25-ITBlazni.git
cd TdA25-ITBlazni
```

Vytvoření Docker image:
```sh
docker build -t tda25-itblazni .
```

Spuštění kontejneru:
```sh
docker run -p 8000:8000 tda25-itblazni
```

Poté navštivte [http://localhost:8000](http://localhost:8000), kde poběží vaše aplikace.

## 4. Struktura aplikace a hlavní funkcionality

### Backend (Django REST Framework)

Adresář `api/` obsahuje soubory:
- `models.py`: definuje datový model hry (Game).
- `views.py`: implementuje funkce (např. `game_list`, `game_detail`) pro CRUD operace (vytváření, čtení, aktualizace, mazání).
- `serializers.py`: definuje třídu `GameSerializer` pro serializaci dat.
- `urls.py`: mapuje cesty jako `/api/v1/games` na konkrétní view funkce.

Herní logika (např. validace 15×15, počtu X/O, detekce koncovky, atd.) může být v `api/utils/game_logic.py`.

Typické endpointy:
- `GET /api/v1/games`: získání seznamu her (podporuje filtrování podle názvu, obtížnosti, času poslední úpravy).
- `POST /api/v1/games`: vytvoření nové hry.
- `GET /api/v1/games/<uuid>`: získání detailu konkrétní hry.
- `PUT /api/v1/games/<uuid>`: aktualizace existující hry.
- `DELETE /api/v1/games/<uuid>`: mazání hry.

### Frontend

Složka `templates/` (pokud používáte Django templating) a `static/` (CSS, JS).
- `game_list.html`: zobrazuje seznam uložených “úloh” (her) s filtry (název, obtížnost, doba poslední úpravy). Každá “karta” má název, obtížnost, tlačítko pro spuštění hry, pro úpravu a pro smazání.
- `script.js`: obsahuje logiku pro volání API, renderování seznamu her, aplikaci filtrů a další interaktivní funkce (např. mazání hry, témata vzhledu, atd.).

### Koncovka / Classifikace

Aplikace umí klasifikovat stav hry na opening (zahájení), midgame (střední hra) nebo endgame (koncovka). Splňuje požadavky na validitu hry (jen symboly X, O, prázdné, 15×15 rozměr, X začíná, atd.).

### Další

- Soubor `Dockerfile`: obsahuje instrukce pro sestavení Docker image.
- Soubor `requirements.txt`: seznam Python balíčků pro instalaci.
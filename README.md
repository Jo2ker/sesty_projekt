# sesty_projekt
------------------------------------------------------------------------------------------------------------------------------------------------
**Šestý projekt ENGETO akademie Tester s Pythonem**
------------------------------------------------------
**Automatizované testy s Playwright a pytest**
------------------------------------------------------
**Popis projektu**
------------------------------------------------------
Tento projekt obsahuje sadu automatizovaných testů napsaných v Pythonu s využitím knihovny Playwright a pytest. 
Testy jsou zaměřené na webovou stránku opravy-telefonu.cz a provádějí kontrolu navigace, obsahu, cookies a kompatibility v různých prohlížečích.

------------------------------------------------------
**Instalace knihoven**
------------------------------------------------------
Knihovny, které jsou použity v kódu jsou uložené v souboru requirements.txt. Pro instalaci doporučuji použít nové virtuální prostředí a s naistalovaným manažerem spustit následovně:

Vytvořte virtual environment

$ python -m venv env
source env/bin/activate  # na Linuxu/macOS
.\env\Scripts\activate  # na Windows

$ pip3 --version # ověřím verzi manažeru $ pip3 --install -r requirements.txt # nainstalujeme knihovny

------------------------------------------------------------
**Spuštění projektu**

-----------------------------------------------------------
Spuštění souboru test_paty_projekt.py v rámci příkazového řádku.

-----------------------------------------------------------------
**Doporučení**
---------------------------------------------------------------

Pro vývoj a ladění používej headless=False a slow_mo=500 pro vizuální zpětnou vazbu.

Pro CI/CD nastav headless=True bez slow_mo, aby testy běžely rychle.

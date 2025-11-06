from playwright.sync_api import expect, sync_playwright, Page
import pytest
import re

@pytest.fixture()
def prohlizec():
    """
    Fixture, která spouští prohlížeč Chromium pro Playwright testy.

    Tento fixture:
    - spouští Chromium v režimu headless (bez vizuálního okna)
    - umožňuje rychlé a efektivní běhy v CI nebo automatických testech
    - po ukončení testu zavře prohlížeč
    """
    with sync_playwright() as p:
        prohlizec = p.chromium.launch(headless=True)
        yield prohlizec

@pytest.fixture()
def stranka(prohlizec):
    """
    Fixture, která vytvoří novou stránku v prohlížeči a načte zadanou adresu.

    Tato fixture:
    - přijímá jako parametr již spuštěný prohlížeč `prohlizec`
    - otevře novou stránku
    - načte stránku www.opravy-telefonu.cz
    - vrací stránku jako objekt, se kterou lze dále pracovat v testech.
    """
    stranka = prohlizec.new_page()
    stranka.goto("https://www.opravy-telefonu.cz/")
    yield stranka

def test_tlacitka(stranka: Page):
    """
    Test, který ověřuje, že po kliknutí na odkaz 'Tipy a triky' dojde ke změně URL a hlavní titulky stránky.

    Postup:
    - Vyhledá odkaz s rolí "link" a názvem "Tipy a triky" (stabilní lokátor).
    - Klikne na tento odkaz
    - Počká, až se URL stránky změní na URL obsahující 'opravy' a 'telefonu' (bez ohledu na velikost písmen).
    - Ověří, že titulek stránky obsahuje podobný vzor (opět 'opravy' a 'telefonu'), aby bylo ověření odolnější vůči drobným změnám.

    Pomocí `expect()` je test stabilnější a odolnější vůči flaketům.
    """
    odkaz = stranka.get_by_role("link", name="Tipy a triky").first
    odkaz.click()

    # Počká na změnu URL
    expect(stranka).to_have_url(re.compile(r"opravy.*telefonu", re.I))
    # Ověří titulek
    expect(stranka).to_have_title(re.compile(r"opravy.*telefonu", re.I))

def test_ruzne_prohlizece():
    """
    Test, který pomocí Playwright spouští v sekvenci dva různé prohlížeče (Chromium a Firefox),
    načítá stránku 'https://www.opravy-telefonu.cz/' a ověřuje, že titulkový text stránky je správný.

    Postup:
    - Spustí Playwright v režimu headless
    - Pro každý prohlížeč (chromium, firefox):
        - otevře nový prohlížeč
        - načte stránku
        - zkontroluje, že titulek odpovídá očekávanému textu

    Tento test ověřuje kompatibilitu a správnou funkčnost stránky v různých prohlížečích.
    """
    with sync_playwright() as p:
        prohlizece = ["chromium", "firefox"]
        for typ_prohlizece in prohlizece:
            prohlizec = getattr(p, typ_prohlizece).launch(headless=True)
            stranka = prohlizec.new_page()
            stranka.goto("https://www.opravy-telefonu.cz/")
            assert stranka.title() == "opravy-telefonu.cz - opravy a servis telefonu"

def test_pritomnosti_cookie(stranka):
    """
    Test ověřující přítomnost cookies '_ga' na stránce a její správnou strukturu.

    Postup:
    - Naviguje na danou stránku ("https://www.opravy-telefonu.cz/poradna-tipy-a-triky-pri-opravach-telefonu/")
    - Získá všechny cookies v rámci kontextu
    - Diagnosticky vypisuje všechny cookies do konzole
    - Ověří, že existuje cookie s názvem '_ga'
    - Ověří, že hodnota této cookies začíná na 'GA1.2', což je typické rozpoznávací počáteční část ID
    
    Tento test pomáhá potvrdit, že Google Analytics nebo jiné sledovací mechanismy
    jsou správně aktivní a cookies jsou nastavené.
    """
    stranka.goto("https://www.opravy-telefonu.cz/poradna-tipy-a-triky-pri-opravach-telefonu/")

    # Po načtení může být cookie, například Google Analytics nebo jiné
    cookies = stranka.context.cookies()

    # tiskne všechny cookies pro diagnostiku
    print(cookies)

     # kontrola, zda existuje cookie s názvem '_ga'
    ga_cookie = next((cookie for cookie in cookies if cookie['name'] == '_ga'), None)
    assert ga_cookie is not None  # ověření existence
    # ověření hodnoty, například že začíná na 'GA1.2'
    assert ga_cookie['value'].startswith('GA1.2')
    
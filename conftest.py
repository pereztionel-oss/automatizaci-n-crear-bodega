from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventarios_page import InventariosPage
from pages.bodega_page import BodegaPage
from utils.config import URL, ADMIN_USER,ADMIN_PASS
from utils.data_factory import DataFactory


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=2000)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        # Login
        page.goto(URL)
        login_page = LoginPage(page)
        login_page.login(ADMIN_USER,ADMIN_PASS)

        # Ir a gestión de bodegas
        inventory_page = InventariosPage(page)
        inventory_page.ir_a_gestion_bodegas()

         
        # Generar datos de bodega
        datos_bodega = DataFactory.generar_bodega()

        # Crear la bodega
        bodega_page = BodegaPage(page)
        bodega_page.crear_bodega(datos_bodega)

        browser.close()

if __name__ == "__main__":
    run()

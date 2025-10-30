from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventarios_page import InventariosPage
from pages.bodega_page import BodegaPage
from utils.config import URL, ADMIN_USER, ADMIN_PASS
from utils.data_factory import DataFactory


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=2000)
        context = browser.new_context(ignore_https_errors=True,viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        # ✅ (Opcional) Maximizar por completo si aún ves problemas
        page.evaluate("window.moveTo(0,0); window.resizeTo(screen.width, screen.height);")


        # Login
        page.goto(URL)
        login_page = LoginPage(page)
        login_page.login(ADMIN_USER, ADMIN_PASS)

        # Ir a gestión de bodegas
        inventory_page = InventariosPage(page)
        inventory_page.ir_a_gestion_bodegas()

        # Generar datos de bodega
        datos_bodega = DataFactory.generar_bodega()

        # Crear la bodega (incluye clic en Aceptar)
        bodega_page = BodegaPage(page)
        bodega_page.crear_bodega(datos_bodega)

        # Ahora eliminar la bodega recién creada
        print(f"\n🗑️  Eliminando bodega: {datos_bodega['nombre_bodega']}")
        bodega_page.eliminar_bodega(datos_bodega['nombre_bodega'])
        bodega_page.confirmar_eliminacion()
        bodega_page.validar_bodega_eliminada(datos_bodega['nombre_bodega'])

        page.wait_for_timeout(20000)
        browser.close()


if __name__ == "__main__":
    run()
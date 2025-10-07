# pages/inventarios_page.py
from playwright.sync_api import Page

class InventariosPage:
    def __init__(self, page: Page):
        self.page = page

    def ir_a_gestion_bodegas(self):
        # Selector más específico: el botón principal de Inventarios
        inventarios_button = self.page.locator("span.nav-text", has_text="Inventarios")
        inventarios_button.wait_for(state="visible", timeout=90000)
        inventarios_button.click()

        # Ahora ir al submenú Gestión de Bodegas
        gestion_bodegas_button = self.page.locator("span.submenu-text", has_text="Gestión Bodegas e Inventarios")
        gestion_bodegas_button.wait_for(state="visible", timeout=1000000)
        gestion_bodegas_button.click()

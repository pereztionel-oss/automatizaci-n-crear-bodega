from playwright.sync_api import expect

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Selectores ajustados
        self.username_input = "xpath=//input[@name='user' and @type='email']"
        self.password_input = "xpath=//input[@name='password']"
        self.login_button = "xpath=//button//span[normalize-space(text())='INGRESAR']"

    def login(self, usuario, password):
        # Esperar carga de la página
        self.page.wait_for_load_state("networkidle", timeout=60000)

        # Esperar y llenar correo
        self.page.wait_for_selector(self.username_input, state="visible", timeout=60000)
        self.page.fill(self.username_input, usuario)

        # Esperar y llenar contraseña
        self.page.wait_for_selector(self.password_input, state="visible", timeout=60000)
        self.page.fill(self.password_input, password)

        # Hacer clic en login
        self.page.click(self.login_button)

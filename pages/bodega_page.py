class BodegaPage:
    def __init__(self, page):
        self.page = page

        # -------------------- BOTONES PRINCIPALES --------------------
        self.btn_crear_bodega = "button:has-text('Crear Bodegas')"
        self.btn_siguiente = "button:has-text('Siguiente')"
        self.btn_atras = "button:has-text('Atrás')"
        self.btn_enviar = "button:has-text('Enviar')"
        self.btn_seleccionar_direccion = "button[aria-label='Seleccionar dirección de la bodega']"

        # -------------------- CAMPOS DE INFORMACIÓN --------------------
        self.nombre_bodega = "#input-bodega"
        self.codigo_bodega = "#input-code"

        # Campos de ubicación (mat-select)
        self.pais = "#mat-select-0"
        self.departamento = "#mat-select-1"
        self.ciudad = "#mat-select-2"
        self.tipo_bodega = "#mat-select-3"

        # Campo de dirección (readonly)
        self.direccion_display = "#input-direccion-display"

        # -------------------- CAMPOS DE CONFIGURACIÓN --------------------
        self.num_modulos = "#input-modulos"
        self.num_pisos = "#input-pisos"
        self.num_estantes = "#input-estantes"
        self.num_entrepanos = "#input-niveles"
        self.num_capacidad = "#input-capacidadEntrepanio"
        self.estandar = "#mat-select-4"

        # -------------------- CAMPOS DEL MODAL DE DIRECCIÓN --------------------
        self.modal_container = "mat-dialog-container"
        self.tipo_calle = "mat-select[formcontrolname='streetType']"
        self.numero_calle_principal = "input[formcontrolname='mainStreetNumber']"
        self.letra_calle_principal = "mat-select[formcontrolname='mainStreetLetter']"
        self.prefijo_bis = "mat-select[formcontrolname='prefixBis']"
        self.cuadrante = "mat-select[formcontrolname='quadrant']"
        self.numero_calle_secundaria = "input[formcontrolname='secondaryStreetNumber']"
        self.letra_calle_secundaria = "mat-select[formcontrolname='secondaryStreetLetter']"
        self.sufijo_bis = "mat-select[formcontrolname='suffixBis']"
        self.numero_complementario = "input[formcontrolname='additionalNumber']"
        self.complemento = "input[formcontrolname='complement']"
        self.btn_guardar_direccion = "button:has-text('Guardar')"
        self.btn_cancelar_direccion = "button[mat-dialog-close]"

        # -------------------- OTROS ELEMENTOS --------------------
        self.btn_editar_modulos = "div:has-text('Editar Módulos')"
        self.switch_aprobar_bodega = "button[role='switch'][id='mat-mdc-slide-toggle-0-button']"
        self.mensaje_exito = "text='Bodega creada con éxito'"

    # -------------------- MÉTODOS AUXILIARES --------------------

    def _seleccionar_mat_select(self, selector, texto, wait_enabled=False):
        """Selecciona opciones de un mat-select de forma robusta."""
        if wait_enabled:
            self.page.wait_for_selector(f"{selector}:not([aria-disabled='true'])", timeout=10000)
        self.page.locator(selector).click(force=True)
        self.page.wait_for_selector("mat-option", state="visible", timeout=5000)
        self.page.get_by_role("option", name=texto, exact=True).click()
        self.page.wait_for_timeout(300)

    def _llenar_direccion_detallada(self, data_direccion):
        """Llena el formulario de dirección detallada dentro del modal."""
        if "tipo_calle" in data_direccion and data_direccion["tipo_calle"]:
            self._seleccionar_mat_select(self.tipo_calle, data_direccion["tipo_calle"])
        if "numero_calle_principal" in data_direccion and data_direccion["numero_calle_principal"]:
            self.page.fill(self.numero_calle_principal, str(data_direccion["numero_calle_principal"]))
        if "letra_calle_principal" in data_direccion and data_direccion["letra_calle_principal"]:
            self._seleccionar_mat_select(self.letra_calle_principal, data_direccion["letra_calle_principal"])
        if "prefijo_bis" in data_direccion and data_direccion["prefijo_bis"]:
            self._seleccionar_mat_select(self.prefijo_bis, data_direccion["prefijo_bis"])
        if "cuadrante" in data_direccion and data_direccion["cuadrante"]:
            self._seleccionar_mat_select(self.cuadrante, data_direccion["cuadrante"])
        if "numero_calle_secundaria" in data_direccion and data_direccion["numero_calle_secundaria"]:
            self.page.fill(self.numero_calle_secundaria, str(data_direccion["numero_calle_secundaria"]))
        if "letra_calle_secundaria" in data_direccion and data_direccion["letra_calle_secundaria"]:
            self._seleccionar_mat_select(self.letra_calle_secundaria, data_direccion["letra_calle_secundaria"])
        if "sufijo_bis" in data_direccion and data_direccion["sufijo_bis"]:
            self._seleccionar_mat_select(self.sufijo_bis, data_direccion["sufijo_bis"])
        if "numero_complementario" in data_direccion and data_direccion["numero_complementario"]:
            self.page.fill(self.numero_complementario, str(data_direccion["numero_complementario"]))
        if "complemento" in data_direccion and data_direccion["complemento"]:
            self.page.fill(self.complemento, data_direccion["complemento"])

    def toggle_aprobar_bodega(self, activar=True):
        """Activa o desactiva el switch de 'Aprobar Bodega'."""
        self.page.wait_for_selector(self.switch_aprobar_bodega, state="visible", timeout=5000)
        estado_actual = self.page.get_attribute(self.switch_aprobar_bodega, "aria-checked")
        if (activar and estado_actual == "false") or (not activar and estado_actual == "true"):
            self.page.click(self.switch_aprobar_bodega)
            self.page.wait_for_timeout(300)

    # -------------------- FLUJO PRINCIPAL --------------------

    def crear_bodega(self, data):
        """Crea una nueva bodega con los datos proporcionados."""
        # Paso 1: Información general
        self.page.click(self.btn_crear_bodega)
        self.page.wait_for_timeout(500)

        self.page.fill(self.nombre_bodega, data["nombre_bodega"])
        self.page.fill(self.codigo_bodega, data["codigo_bodega"])

        self._seleccionar_mat_select(self.pais, data["pais"])
        self._seleccionar_mat_select(self.departamento, data["departamento"], wait_enabled=True)
        self._seleccionar_mat_select(self.ciudad, data["ciudad"], wait_enabled=True)
        self._seleccionar_mat_select(self.tipo_bodega, data["tipo_bodega"])

        # Dirección detallada
        self.page.click(self.btn_seleccionar_direccion)
        self.page.wait_for_selector(self.modal_container, state="visible", timeout=5000)
        self.page.wait_for_timeout(500)

        if "direccion_detallada" in data and data["direccion_detallada"]:
            self._llenar_direccion_detallada(data["direccion_detallada"])
            self.page.click(self.btn_guardar_direccion)

        self.page.wait_for_selector(self.modal_container, state="hidden", timeout=30000)
        self.page.wait_for_timeout(500)

        # Paso 2: Configuración
        self.page.fill(self.num_modulos, str(data["modulos"]))
        self.page.fill(self.num_pisos, str(data["pisos"]))
        self.page.fill(self.num_estantes, str(data["estantes"]))
        self.page.fill(self.num_entrepanos, str(data["entrepaños"]))
        self.page.fill(self.num_capacidad, str(data["capacidad"]))
        self._seleccionar_mat_select(self.estandar, data["tipo_estandar"])

        # Ir al siguiente paso
        self.page.click(self.btn_siguiente)
        self.page.wait_for_timeout(1000)

        # Activar switch de aprobación
        try:
            self.toggle_aprobar_bodega(activar=True)
        except:
            print("⚠️ Switch de aprobación no visible o no aplicable en este flujo.")

        # ✅ Scroll hasta el botón Enviar y hacer clic
        self.page.wait_for_selector(self.btn_enviar, state="visible", timeout=10000)
        self.page.locator(self.btn_enviar).scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        self.page.click(self.btn_enviar)
        self.page.wait_for_timeout(1500)
        print("✅ Formulario enviado correctamente.")

    # -------------------- VALIDACIÓN FINAL --------------------

    def validar_bodega_creada(self):
        """Valida que la bodega fue creada exitosamente."""
        try:
            self.page.wait_for_selector(self.mensaje_exito, timeout=10000)
            print("🎉 Bodega creada con éxito.")
            return True
        except:
            print("❌ No se detectó el mensaje de éxito.")
            return False

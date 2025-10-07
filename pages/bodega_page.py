class BodegaPage:
    def __init__(self, page):
        self.page = page

        # Botones principales
        self.btn_crear_bodega = "button:has-text('Crear Bodegas')"
        self.btn_siguiente = "button:has-text('Siguiente')"
        self.btn_atras = "button:has-text('Atrás')"
        self.btn_enviar = "button:has-text('Enviar')"
        self.btn_seleccionar_direccion = "button[aria-label='Seleccionar dirección de la bodega']"

        # Campos de Información de la Bodega
        self.nombre_bodega = "#input-bodega"
        self.codigo_bodega = "#input-code"

        # Campos de Ubicación (mat-select con IDs específicos)
        self.pais = "#mat-select-0"
        self.departamento = "#mat-select-1"
        self.ciudad = "#mat-select-2"
        self.tipo_bodega = "#mat-select-3"

        # Campo de dirección (readonly)
        self.direccion_display = "#input-direccion-display"

        # Campos de Configuración
        self.num_modulos = "#input-modulos"
        self.num_pisos = "#input-pisos"
        self.num_estantes = "#input-estantes"
        self.num_entrepanos = "#input-niveles"
        self.num_capacidad = "#input-capacidadEntrepanio"
        self.estandar = "#mat-select-4"

        # Selectores del Modal de Dirección Detallada
        self.modal_container = "mat-dialog-container"
        
        # Campos del formulario de dirección (usando formControlName)
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
        
        # Botones del modal
        self.btn_guardar_direccion = "button:has-text('Guardar')"
        self.btn_cancelar_direccion = "button[mat-dialog-close]"

        # Selectores del Paso 2: Configurar Módulos
        self.toggle_aprobar_bodega = "mat-slide-toggle:has-text('Aprobar Bodega')"
        self.btn_editar_modulos = "div:has-text('Editar Módulos')"
        
        # Mensaje de éxito
        self.mensaje_exito = "text='Bodega creada con éxito'"

    def _seleccionar_mat_select(self, selector, texto, wait_enabled=False):
        """
        Método auxiliar para seleccionar opciones de mat-select de forma robusta.
        
        Args:
            selector: Selector CSS del mat-select
            texto: Texto de la opción a seleccionar
            wait_enabled: Si True, espera que el elemento esté habilitado antes de hacer clic
        """
        if wait_enabled:
            # Esperar que el select no esté deshabilitado
            self.page.wait_for_selector(
                f"{selector}:not([aria-disabled='true'])", 
                timeout=10000
            )
        
        # Hacer clic en el mat-select con force=True para evitar interceptaciones
        self.page.locator(selector).click(force=True)
        
        # Esperar que el panel de opciones se abra
        self.page.wait_for_selector("mat-option", state="visible", timeout=5000)
        
        # Seleccionar la opción
        self.page.get_by_role("option", name=texto, exact=True).click()
        
        # Pequeña pausa para asegurar que el valor se procese
        self.page.wait_for_timeout(300)

    def _llenar_direccion_detallada(self, data_direccion):
        """
        Llena el formulario de dirección detallada en el modal.
        
        Args:
            data_direccion: Diccionario con los datos de la dirección detallada
        """
        # Tipo de Calle
        if "tipo_calle" in data_direccion and data_direccion["tipo_calle"]:
            self._seleccionar_mat_select(self.tipo_calle, data_direccion["tipo_calle"])
        
        # Número Calle Principal
        if "numero_calle_principal" in data_direccion and data_direccion["numero_calle_principal"]:
            self.page.fill(self.numero_calle_principal, str(data_direccion["numero_calle_principal"]))
        
        # Letra Calle Principal (opcional)
        if "letra_calle_principal" in data_direccion and data_direccion["letra_calle_principal"]:
            self._seleccionar_mat_select(self.letra_calle_principal, data_direccion["letra_calle_principal"])
        
        # Prefijo BIS (opcional)
        if "prefijo_bis" in data_direccion and data_direccion["prefijo_bis"]:
            self._seleccionar_mat_select(self.prefijo_bis, data_direccion["prefijo_bis"])
        
        # Cuadrante
        if "cuadrante" in data_direccion and data_direccion["cuadrante"]:
            self._seleccionar_mat_select(self.cuadrante, data_direccion["cuadrante"])
        
        # Número Calle Secundaria
        if "numero_calle_secundaria" in data_direccion and data_direccion["numero_calle_secundaria"]:
            self.page.fill(self.numero_calle_secundaria, str(data_direccion["numero_calle_secundaria"]))
        
        # Letra Calle Secundaria (opcional)
        if "letra_calle_secundaria" in data_direccion and data_direccion["letra_calle_secundaria"]:
            self._seleccionar_mat_select(self.letra_calle_secundaria, data_direccion["letra_calle_secundaria"])
        
        # Sufijo BIS (opcional)
        if "sufijo_bis" in data_direccion and data_direccion["sufijo_bis"]:
            self._seleccionar_mat_select(self.sufijo_bis, data_direccion["sufijo_bis"])
        
        # Número Complementario (opcional)
        if "numero_complementario" in data_direccion and data_direccion["numero_complementario"]:
            self.page.fill(self.numero_complementario, str(data_direccion["numero_complementario"]))
        
        # Complemento (opcional - texto libre)
        if "complemento" in data_direccion and data_direccion["complemento"]:
            self.page.fill(self.complemento, data_direccion["complemento"])
    
    def crear_bodega(self, data):
        """
        Crea una nueva bodega con los datos proporcionados.
        
        Args:
            data: Diccionario con los datos de la bodega. Debe incluir:
                - nombre_bodega: str
                - codigo_bodega: str
                - pais: str
                - departamento: str
                - ciudad: str
                - tipo_bodega: str
                - direccion_detallada: dict (opcional, con los campos del modal)
                - modulos: int
                - pisos: int
                - estantes: int
                - entrepaños: int
                - capacidad: int
                - tipo_estandar: str
                - config_modulos: dict (opcional, configuración del paso 2)
        """
        # Hacer clic en el botón crear bodega
        self.page.click(self.btn_crear_bodega)
        self.page.wait_for_timeout(500)

        # Información de la Bodega
        self.page.fill(self.nombre_bodega, data["nombre_bodega"])
        self.page.fill(self.codigo_bodega, data["codigo_bodega"])

        # Ubicación - País
        self._seleccionar_mat_select(self.pais, data["pais"])
        
        # Departamento (esperar que se habilite después de seleccionar país)
        self._seleccionar_mat_select(self.departamento, data["departamento"], wait_enabled=True)
        
        # Ciudad (esperar que se habilite después de seleccionar departamento)
        self._seleccionar_mat_select(self.ciudad, data["ciudad"], wait_enabled=True)

        # Tipo de Bodega
        self._seleccionar_mat_select(self.tipo_bodega, data["tipo_bodega"])

        # Seleccionar y llenar dirección detallada
        self.page.click(self.btn_seleccionar_direccion)
        
        # Esperar a que el modal se abra
        self.page.wait_for_selector(self.modal_container, state="visible", timeout=5000)
        self.page.wait_for_timeout(500)
        
        # Llenar el formulario de dirección detallada si se proporcionaron datos
        if "direccion_detallada" in data and data["direccion_detallada"]:
            self._llenar_direccion_detallada(data["direccion_detallada"])
            
            # Hacer clic en el botón Guardar del modal
            self.page.click(self.btn_guardar_direccion)
        
        # Esperar a que el modal se cierre antes de continuar
        self.page.wait_for_selector(self.modal_container, state="hidden", timeout=30000)
        
        # Pausa adicional para asegurar que la UI se estabilice
        self.page.wait_for_timeout(500)

        # Configuración
        self.page.fill(self.num_modulos, str(data["modulos"]))
        self.page.fill(self.num_pisos, str(data["pisos"]))
        self.page.fill(self.num_estantes, str(data["estantes"]))
        self.page.fill(self.num_entrepanos, str(data["entrepaños"]))
        self.page.fill(self.num_capacidad, str(data["capacidad"]))

        # Estándar
        self._seleccionar_mat_select(self.estandar, data["tipo_estandar"])

        # Ir al siguiente paso (Configurar Módulos)
        self.page.click(self.btn_siguiente)
        self.page.wait_for_timeout(1000)

        #self.page.click(self.btn_enviar)

    def validar_bodega_creada(self):
        """
        Valida que la bodega fue creada exitosamente.
        
        Returns:
            bool: True si el mensaje de éxito es visible
        """
        try:
            return self.page.locator(self.mensaje_exito).is_visible(timeout=10000)
        except:
            return False
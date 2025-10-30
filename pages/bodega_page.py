import time

class BodegaPage:
    def __init__(self, page):
        self.page = page
        
        # ... (tus selectores existentes se mantienen igual)
          # -------------------- BOTONES PRINCIPALES --------------------
        self.btn_crear_bodega = "button:has-text('Agregar')"
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
        self.switch_aprobar_bodega = "button[role='switch'][id='mat-mdc-slide-toggle-0-button']"
        self.mensaje_exito = "text='¡Bodega Creada!'"
        self.btn_aceptar_modal = "button:has-text('Aceptar')"
        
        # Selectores adicionales para búsqueda y eliminación
        self.input_buscar_bodegas = "input[placeholder*='Buscar bodegas']"
        self.btn_buscar = "button:has-text('Buscar')"
        self.btn_limpiar = "button:has-text('Limpiar')"

    # -------------------- MÉTODOS AUXILIARES --------------------
    def _seleccionar_mat_select(self, selector, texto, wait_enabled=False):
        if wait_enabled:
            self.page.wait_for_selector(f"{selector}:not([aria-disabled='true'])", timeout=10000)
        self.page.locator(selector).click(force=True)
        self.page.wait_for_selector("mat-option", state="visible", timeout=5000)
        self.page.get_by_role("option", name=texto, exact=True).click()
        self.page.wait_for_timeout(300)

    def _llenar_direccion_detallada(self, data_direccion):
        if "tipo_calle" in data_direccion:
            self._seleccionar_mat_select(self.tipo_calle, data_direccion["tipo_calle"])
        if "numero_calle_principal" in data_direccion:
            self.page.fill(self.numero_calle_principal, str(data_direccion["numero_calle_principal"]))
        if "letra_calle_principal" in data_direccion:
            self._seleccionar_mat_select(self.letra_calle_principal, data_direccion["letra_calle_principal"])
        if "prefijo_bis" in data_direccion:
            self._seleccionar_mat_select(self.prefijo_bis, data_direccion["prefijo_bis"])
        if "cuadrante" in data_direccion:
            self._seleccionar_mat_select(self.cuadrante, data_direccion["cuadrante"])
        if "numero_calle_secundaria" in data_direccion:
            self.page.fill(self.numero_calle_secundaria, str(data_direccion["numero_calle_secundaria"]))
        if "letra_calle_secundaria" in data_direccion:
            self._seleccionar_mat_select(self.letra_calle_secundaria, data_direccion["letra_calle_secundaria"])
        if "sufijo_bis" in data_direccion:
            self._seleccionar_mat_select(self.sufijo_bis, data_direccion["sufijo_bis"])
        if "numero_complementario" in data_direccion:
            self.page.fill(self.numero_complementario, str(data_direccion["numero_complementario"]))
        if "complemento" in data_direccion:
            self.page.fill(self.complemento, data_direccion["complemento"])

    def toggle_aprobar_bodega(self, activar=True):
        self.page.wait_for_selector(self.switch_aprobar_bodega, state="visible", timeout=5000)
        estado_actual = self.page.get_attribute(self.switch_aprobar_bodega, "aria-checked")
        if (activar and estado_actual == "false") or (not activar and estado_actual == "true"):
            self.page.click(self.switch_aprobar_bodega)
            self.page.wait_for_timeout(300)

    def click_siguiente(self, timeout=15000, interval=0.25):
        """Hace clic en 'Siguiente' o 'Continuar' visible y habilitado."""
        deadline = time.time() + (timeout / 1000.0)
        locator = self.page.locator("button:has-text('Siguiente'), button:has-text('Continuar')")
        while time.time() < deadline:
            count = locator.count()
            for i in range(count):
                btn = locator.nth(i)
                try:
                    if btn.is_visible() and btn.is_enabled():
                        btn.scroll_into_view_if_needed()
                        self.page.wait_for_timeout(200)
                        btn.click()
                        self.page.wait_for_timeout(800)
                        print("✅ Avanzando al siguiente paso...")
                        return
                except:
                    pass
            time.sleep(interval)
        self.page.screenshot(path="error_click_siguiente.png")
        raise Exception("Timeout esperando botón 'Siguiente' o 'Continuar' visible y habilitado.")
        

    # -------------------- MÉTODOS AUXILIARES MEJORADOS --------------------
    
    def _normalizar_texto(self, texto):
        """Normaliza texto para comparaciones más flexibles."""
        return (
            texto.lower()
            .replace(" ", "")
            .replace("_", "")
            .replace(".", "")
            .replace("-", "")
            .strip()
        )

    def _buscar_fila_por_nombre(self, nombre_bodega):
        """Busca una fila que contenga el nombre de bodega (coincidencia parcial)."""
        nombre_normalizado = self._normalizar_texto(nombre_bodega)
        
        # Buscar en todas las filas visibles
        filas = self.page.locator("datatable-body-row").all()
        
        for fila in filas:
            try:
                # Obtener todas las celdas de la fila
                celdas = fila.locator("datatable-body-cell").all()
                if celdas:
                    # La primera celda generalmente contiene el nombre
                    texto_celda = celdas[0].text_content().strip()
                    texto_normalizado = self._normalizar_texto(texto_celda)
                    
                    # Buscar coincidencia parcial
                    if nombre_normalizado in texto_normalizado:
                        return fila
            except:
                continue
        return None

    def _navegar_paginas_buscando_bodega(self, nombre_bodega):
        """Navega por todas las páginas buscando la bodega."""
        pagina_actual = 1
        max_paginas = 10  # Límite para evitar bucle infinito
        
        while pagina_actual <= max_paginas:
            print(f"📄 Buscando en página {pagina_actual}...")
            
            # Buscar en la página actual
            fila = self._buscar_fila_por_nombre(nombre_bodega)
            if fila:
                return fila
            
            # Intentar ir a siguiente página
            try:
                siguiente_btn = self.page.locator(
                    "button[aria-label='go to next page']:not(.disabled), "
                    "button:has-text('›'):not([disabled])"
                ).first
                
                if siguiente_btn.is_visible() and siguiente_btn.is_enabled():
                    siguiente_btn.click()
                    self.page.wait_for_timeout(2000)  # Esperar carga de nueva página
                    pagina_actual += 1
                else:
                    break  # No hay más páginas
            except:
                break
        
        return None

    # -------------------- MÉTODOS DE BÚSQUEDA MEJORADOS --------------------
    
    def buscar_bodega(self, nombre_bodega):
        """Busca una bodega por nombre con búsqueda más robusta."""
        print(f"🔎 Buscando si existe la bodega: {nombre_bodega}")
        
        # Primero intentar con búsqueda en filtro si existe
        try:
            if self.page.locator(self.input_buscar_bodegas).is_visible():
                self.page.fill(self.input_buscar_bodegas, nombre_bodega)
                self.page.click(self.btn_buscar)
                self.page.wait_for_timeout(2000)
        except:
            pass
        
        # Buscar en todas las páginas
        fila = self._navegar_paginas_buscando_bodega(nombre_bodega)
        
        if fila:
            print(f"✅ Bodega '{nombre_bodega}' encontrada.")
            return True
        else:
            print(f"❌ No se encontró la bodega '{nombre_bodega}' en ninguna página.")
            
            # Limpiar filtro de búsqueda si se usó
            try:
                if self.page.locator(self.btn_limpiar).is_visible():
                    self.page.click(self.btn_limpiar)
                    self.page.wait_for_timeout(1000)
            except:
                pass
            
            return False

    # -------------------- MÉTODOS DE ELIMINACIÓN MEJORADOS --------------------
    
    def eliminar_bodega(self, nombre_bodega):
        """Elimina una bodega con validación mejorada."""
        print(f"🗑️ Eliminando bodega: {nombre_bodega}")
        
        # Buscar la bodega en todas las páginas
        fila = self._navegar_paginas_buscando_bodega(nombre_bodega)
        
        if not fila:
            print(f"⚠️ No se encontró la bodega '{nombre_bodega}' para eliminar.")
            return False
        
        try:
            # Hacer clic en el menú de acciones (⁞)
            menu_acciones = fila.locator("mat-icon[aria-haspopup='menu']").first
            if menu_acciones.is_visible():
                menu_acciones.click()
                self.page.wait_for_timeout(1000)
                
                # Seleccionar opción eliminar
                opcion_eliminar = self.page.locator(
                    "button:has-text('Eliminar'), "
                    "button[mat-menu-item]:has(mat-icon:has-text('delete'))"
                ).first
                
                if opcion_eliminar.is_visible():
                    opcion_eliminar.click()
                    print(f"✅ Bodega '{nombre_bodega}' marcada para eliminar.")
                    return True
                else:
                    print("❌ No se encontró la opción 'Eliminar' en el menú.")
                    return False
            else:
                print("❌ No se encontró el menú de acciones.")
                return False
                
        except Exception as e:
            print(f"❌ Error al intentar eliminar: {e}")
            return False

    def confirmar_eliminacion(self):
        """Confirma la eliminación en el diálogo modal."""
        try:
            # Buscar botones de confirmación sin esperar modal específico
            btn_confirmar = self.page.locator(
                "button:has-text('Confirmar'), "
                "button:has-text('Aceptar'), "
                "button:has-text('Sí'), "
                "button:has-text('Eliminar')"
            ).first
            
            if btn_confirmar.is_visible(timeout=5000):
                btn_confirmar.click()
                self.page.wait_for_timeout(1000)
                print("✅ Eliminación confirmada.")
                return True
            else:
                print("⚠️ No se encontró botón de confirmación visible.")
                return True  # Si no hay confirmación, asumimos que se eliminó
                    
        except Exception as e:
            print(f"⚠️ No se pudo confirmar eliminación: {e}")
            return True  # Continuamos aunque falle la confirmación

    def validar_bodega_eliminada(self, nombre_bodega, timeout=10000):
        """Valida que la bodega ya no aparezca en la tabla."""
        print(f"🔍 Validando que la bodega '{nombre_bodega}' fue eliminada...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Buscar si la bodega aún existe (solo en página actual para ser rápido)
            fila = self._buscar_fila_por_nombre(nombre_bodega)
            
            if not fila:
                print(f"🎉 Bodega '{nombre_bodega}' eliminada con éxito.")
                return True
            
            time.sleep(1000)  # Esperar 1 segundo entre intentos
        
        # Si llegamos aquí, la bodega aún existe después del timeout
        print(f"❌ La bodega '{nombre_bodega}' aún aparece en la tabla después de {timeout/1000} segundos.")
        return False

    # -------------------- FLUJO PRINCIPAL MEJORADO --------------------
    
    def crear_bodega(self, data):
        """Crea una nueva bodega con validación mejorada de existencia."""
        nombre_bodega = data["nombre_bodega"]
        
        # Verificar si existe previamente
        bodega_existe = self.buscar_bodega(nombre_bodega)
        
        if bodega_existe:
            print(f"⚠️ La bodega '{nombre_bodega}' ya existe. Eliminándola...")
            
            # Intentar eliminar
            if self.eliminar_bodega(nombre_bodega):
                if self.confirmar_eliminacion():
                    if self.validar_bodega_eliminada(nombre_bodega):
                        print(f"✅ Bodega existente '{nombre_bodega}' eliminada correctamente.")
                        self.page.wait_for_timeout(2000)
                    else:
                        print(f"❌ No se pudo validar la eliminación de '{nombre_bodega}'")
                        return False
                else:
                    print(f"❌ No se pudo confirmar la eliminación de '{nombre_bodega}'")
                    return False
            else:
                print(f"❌ No se pudo iniciar la eliminación de '{nombre_bodega}'")
                return False
        else:
            print(f"✅ La bodega '{nombre_bodega}' no existe. Continuando con creación...")
        
        # CONTINUAR CON LA CREACIÓN DE LA BODEGA
        print("📝 Paso 1: Llenando Información de la Bodega...")
        try:
            self.page.click(self.btn_crear_bodega)
            self.page.wait_for_timeout(500)
            self.page.fill(self.nombre_bodega, data["nombre_bodega"])
            self.page.fill(self.codigo_bodega, data["codigo_bodega"])
            self.click_siguiente()

            print("📍 Paso 2: Llenando Información de Ubicación...")
            self._seleccionar_mat_select(self.pais, data["pais"])
            self._seleccionar_mat_select(self.departamento, data["departamento"], wait_enabled=True)
            self._seleccionar_mat_select(self.ciudad, data["ciudad"], wait_enabled=True)
            self._seleccionar_mat_select(self.tipo_bodega, data["tipo_bodega"])
            self.page.click(self.btn_seleccionar_direccion)
            self.page.wait_for_selector(self.modal_container, state="visible", timeout=10000)
            self.page.wait_for_timeout(2000)
            if "direccion_detallada" in data:
                self._llenar_direccion_detallada(data["direccion_detallada"])
                self.page.click(self.btn_guardar_direccion)
            self.page.wait_for_selector(self.modal_container, state="hidden", timeout=15000)
            self.page.wait_for_timeout(2000)
            self.click_siguiente()

            print("⚙️ Paso 3: Llenando Información de Configuración...")
            self.page.fill(self.num_modulos, str(data["modulos"]))
            self.page.fill(self.num_pisos, str(data["pisos"]))
            self.page.fill(self.num_estantes, str(data["estantes"]))
            self.page.fill(self.num_entrepanos, str(data["entrepaños"]))
            self.page.fill(self.num_capacidad, str(data["capacidad"]))
            self._seleccionar_mat_select(self.estandar, data["tipo_estandar"])
            self.click_siguiente()

            print("✅ Paso 4: Aprobando y enviando bodega...")
            try:
                self.toggle_aprobar_bodega(activar=True)
            except:
                print("⚠️ Switch no visible o no aplicable.")
            self.page.wait_for_selector(self.btn_enviar, state="visible", timeout=10000)
            self.page.locator(self.btn_enviar).scroll_into_view_if_needed()
            self.page.click(self.btn_enviar)
            print("⏳ Esperando confirmación...")
            self.page.wait_for_selector(self.mensaje_exito, timeout=10000)
            print("✅ Bodega creada con éxito.")
            self.page.click(self.btn_aceptar_modal)
            self.page.wait_for_timeout(1000)
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante la creación de la bodega: {e}")
            return False
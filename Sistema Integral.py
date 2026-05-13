"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas
Ejercicio 1 - Fase 4
Curso: Programación (213023)
UNAD

Temas: Clases abstractas, Herencia, Polimorfismo, Encapsulación,
       Manejo avanzado de excepciones, Log de errores
"""

import datetime
import traceback
from abc import ABC, abstractmethod


# ==================== ARCHIVO DE LOGS ====================

class Logger:
    """Clase para manejar el registro de eventos y errores"""
    
    _instancia = None  # Patrón Singleton
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    def _inicializar(self):
        self.archivo_log = "sistema_log.txt"
        with open(self.archivo_log, "w", encoding="utf-8") as f:
            f.write("="*70 + "\n")
            f.write("LOG DEL SISTEMA INTEGRAL DE GESTIÓN\n")
            f.write(f"Iniciado: {datetime.datetime.now()}\n")
            f.write("="*70 + "\n\n")
    
    def registrar(self, tipo, mensaje, detalle=None):
        """Registra un evento en el archivo de log"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.archivo_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {tipo.upper()}: {mensaje}\n")
            if detalle:
                f.write(f"    Detalle: {detalle}\n")
            f.write("\n")
    
    def registrar_error(self, error, contexto=None):
        """Registra un error con su traceback"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.archivo_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] ERROR: {str(error)}\n")
            if contexto:
                f.write(f"    Contexto: {contexto}\n")
            f.write(f"    Traceback: {traceback.format_exc()}\n")
            f.write("\n")


# ==================== EXCEPCIONES PERSONALIZADAS ====================

class SistemaError(Exception):
    """Excepción base del sistema"""
    pass

class ClienteError(SistemaError):
    """Error relacionado con clientes"""
    pass

class ServicioError(SistemaError):
    """Error relacionado con servicios"""
    pass

class ReservaError(SistemaError):
    """Error relacionado con reservas"""
    pass

class ValidacionError(SistemaError):
    """Error de validación de datos"""
    pass


# ==================== CLASE CLIENTE ====================

class Cliente:
    """Clase que representa un cliente con validaciones robustas"""
    
    def __init__(self, id_cliente, nombre, email, telefono):
        self._id_cliente = None
        self._nombre = None
        self._email = None
        self._telefono = None
        
        # Usar los setters para validar
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        
        Logger().registrar("INFO", f"Cliente creado: {self._nombre}")
    
    # Propiedades con encapsulación
    @property
    def id_cliente(self):
        return self._id_cliente
    
    @id_cliente.setter
    def id_cliente(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValidacionError("El ID del cliente no puede estar vacío")
        self._id_cliente = str(valor).strip()
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValidacionError("El nombre del cliente no puede estar vacío")
        if len(valor) < 3:
            raise ValidacionError("El nombre debe tener al menos 3 caracteres")
        self._nombre = str(valor).strip().title()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValidacionError("El email no puede estar vacío")
        if "@" not in valor or "." not in valor:
            raise ValidacionError("El email no tiene un formato válido")
        self._email = str(valor).strip().lower()
    
    @property
    def telefono(self):
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValidacionError("El teléfono no puede estar vacío")
        if not str(valor).isdigit():
            raise ValidacionError("El teléfono debe contener solo números")
        if len(str(valor)) < 7:
            raise ValidacionError("El teléfono debe tener al menos 7 dígitos")
        self._telefono = str(valor).strip()
    
    def obtener_info(self):
        """Retorna información completa del cliente"""
        return f"ID: {self._id_cliente} | Nombre: {self._nombre} | Email: {self._email} | Tel: {self._telefono}"
    
    def __str__(self):
        return self.obtener_info()


# ==================== CLASE ABSTRACTA SERVICIO ====================

class Servicio(ABC):
    """Clase abstracta base para todos los servicios"""
    
    def __init__(self, id_servicio, nombre, precio_base):
        self._id_servicio = id_servicio
        self._nombre = nombre
        self._precio_base = precio_base
        self._disponible = True
    
    @property
    def id_servicio(self):
        return self._id_servicio
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def precio_base(self):
        return self._precio_base
    
    @property
    def disponible(self):
        return self._disponible
    
    def set_disponible(self, estado):
        self._disponible = estado
    
    @abstractmethod
    def calcular_costo(self, duracion, **kwargs):
        """Método abstracto para calcular costo del servicio"""
        pass
    
    @abstractmethod
    def describir(self):
        """Método abstracto para describir el servicio"""
        pass
    
    @abstractmethod
    def validar_parametros(self, **kwargs):
        """Método abstracto para validar parámetros específicos"""
        pass
    
    # Sobrecarga del método calcular_costo (simulada con kwargs)
    def calcular_costo_con_descuento(self, duracion, descuento=0, impuesto=0):
        """
        Versión sobrecargada para calcular costo con descuento e impuesto
        """
        costo_base = self.calcular_costo(duracion)
        costo_con_descuento = costo_base - (costo_base * descuento / 100)
        costo_final = costo_con_descuento + (costo_con_descuento * impuesto / 100)
        return round(costo_final, 2)


# ==================== SERVICIOS ESPECIALIZADOS ====================

class ReservaSala(Servicio):
    """Servicio de reserva de salas"""
    
    def __init__(self, id_servicio, nombre, precio_base, capacidad_maxima, equipamiento):
        super().__init__(id_servicio, nombre, precio_base)
        self._capacidad_maxima = capacidad_maxima
        self._equipamiento = equipamiento
    
    def calcular_costo(self, duracion, **kwargs):
        """Calcula costo de reserva de sala (precio_base por hora)"""
        try:
            if duracion <= 0:
                raise ValueError("La duración debe ser positiva")
            
            costo = self._precio_base * duracion
            
            # Aplicar descuento si aplica por kwargs
            if "descuento" in kwargs:
                descuento = kwargs["descuento"]
                if 0 <= descuento <= 100:
                    costo = costo - (costo * descuento / 100)
            
            Logger().registrar("INFO", f"Costo calculado para {self._nombre}: ${costo}")
            return round(costo, 2)
        
        except Exception as e:
            Logger().registrar_error(e, f"calcular_costo - {self._nombre}")
            raise ServicioError(f"Error al calcular costo: {str(e)}")
    
    def describir(self):
        return f"📚 {self._nombre}: Sala para {self._capacidad_maxima} personas, equipada con {self._equipamiento}. Precio: ${self._precio_base}/hora"
    
    def validar_parametros(self, **kwargs):
        """Valida parámetros específicos para reserva de sala"""
        if "capacidad" in kwargs:
            if kwargs["capacidad"] > self._capacidad_maxima:
                raise ValidacionError(f"Capacidad solicitada ({kwargs['capacidad']}) excede la máxima ({self._capacidad_maxima})")
        return True


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos"""
    
    def __init__(self, id_servicio, nombre, precio_base, tipo_equipo, garantia):
        super().__init__(id_servicio, nombre, precio_base)
        self._tipo_equipo = tipo_equipo
        self._garantia = garantia  # en días
    
    def calcular_costo(self, duracion, **kwargs):
        """Calcula costo de alquiler (precio_base por día)"""
        try:
            if duracion <= 0:
                raise ValueError("La duración debe ser positiva")
            
            costo = self._precio_base * duracion
            
            # Seguro adicional opcional
            if "seguro" in kwargs and kwargs["seguro"]:
                seguro = costo * 0.10
                costo += seguro
            
            Logger().registrar("INFO", f"Costo calculado para {self._nombre}: ${costo}")
            return round(costo, 2)
        
        except Exception as e:
            Logger().registrar_error(e, f"calcular_costo - {self._nombre}")
            raise ServicioError(f"Error al calcular costo: {str(e)}")
    
    def describir(self):
        return f"💻 {self._nombre}: Equipo {self._tipo_equipo}, garantía de {self._garantia} días. Precio: ${self._precio_base}/día"
    
    def validar_parametros(self, **kwargs):
        """Valida parámetros específicos para alquiler de equipo"""
        if "cantidad" in kwargs:
            if kwargs["cantidad"] <= 0:
                raise ValidacionError("La cantidad debe ser mayor a 0")
            if kwargs["cantidad"] > 5:
                raise ValidacionError("No se pueden alquilar más de 5 equipos del mismo tipo")
        return True


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada"""
    
    def __init__(self, id_servicio, nombre, precio_base, area, nivel_experto):
        super().__init__(id_servicio, nombre, precio_base)
        self._area = area
        self._nivel_experto = nivel_experto  # Junior, Senior, Master
    
    def calcular_costo(self, duracion, **kwargs):
        """Calcula costo de asesoría (precio_base por hora con multiplicador según nivel)"""
        try:
            if duracion <= 0:
                raise ValueError("La duración debe ser positiva")
            
            multiplicador = {"Junior": 1.0, "Senior": 1.5, "Master": 2.0}.get(self._nivel_experto, 1.0)
            costo = self._precio_base * duracion * multiplicador
            
            # Descuento por paquete de horas
            if "paquete" in kwargs and kwargs["paquete"]:
                if duracion >= 10:
                    costo = costo * 0.85
                elif duracion >= 5:
                    costo = costo * 0.90
            
            Logger().registrar("INFO", f"Costo calculado para {self._nombre}: ${costo}")
            return round(costo, 2)
        
        except Exception as e:
            Logger().registrar_error(e, f"calcular_costo - {self._nombre}")
            raise ServicioError(f"Error al calcular costo: {str(e)}")
    
    def describir(self):
        return f"🎓 {self._nombre}: Asesoría en {self._area}, nivel {self._nivel_experto}. Precio base: ${self._precio_base}/hora"
    
    def validar_parametros(self, **kwargs):
        """Valida parámetros específicos para asesoría"""
        if "nivel_requerido" in kwargs:
            niveles_validos = ["Junior", "Senior", "Master"]
            if kwargs["nivel_requerido"] not in niveles_validos:
                raise ValidacionError(f"Nivel inválido. Use: {', '.join(niveles_validos)}")
        return True


# ==================== CLASE RESERVA ====================

class Reserva:
    """Clase que integra cliente, servicio, duración y estado"""
    
    def __init__(self, id_reserva, cliente, servicio, duracion, fecha=None):
        self._id_reserva = id_reserva
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._fecha = fecha or datetime.datetime.now()
        self._estado = "PENDIENTE"  # PENDIENTE, CONFIRMADA, CANCELADA
        self._costo_total = None
    
    @property
    def id_reserva(self):
        return self._id_reserva
    
    @property
    def estado(self):
        return self._estado
    
    def confirmar(self):
        """Confirma la reserva con manejo de excepciones"""
        try:
            if self._estado == "CANCELADA":
                raise ReservaError("No se puede confirmar una reserva cancelada")
            
            if not self._servicio.disponible:
                raise ReservaError(f"El servicio {self._servicio.nombre} no está disponible")
            
            # Validar parámetros del servicio
            self._servicio.validar_parametros()
            
            # Calcular costo total
            self._costo_total = self._servicio.calcular_costo(self._duracion)
            
            self._estado = "CONFIRMADA"
            Logger().registrar("INFO", f"Reserva {self._id_reserva} confirmada para {self._cliente.nombre}")
            return True, f"Reserva {self._id_reserva} confirmada. Total: ${self._costo_total}"
        
        except ReservaError as e:
            Logger().registrar_error(e, f"confirmar_reserva_{self._id_reserva}")
            raise
        except Exception as e:
            Logger().registrar_error(e, f"confirmar_reserva_{self._id_reserva}")
            raise ReservaError(f"Error inesperado al confirmar reserva: {str(e)}")
    
    def cancelar(self):
        """Cancela la reserva"""
        try:
            if self._estado == "CONFIRMADA":
                self._estado = "CANCELADA"
                Logger().registrar("INFO", f"Reserva {self._id_reserva} cancelada")
                return True, f"Reserva {self._id_reserva} cancelada exitosamente"
            elif self._estado == "CANCELADA":
                return False, "La reserva ya estaba cancelada"
            else:
                return False, "La reserva no se puede cancelar en su estado actual"
        except Exception as e:
            Logger().registrar_error(e, f"cancelar_reserva_{self._id_reserva}")
            raise ReservaError(f"Error al cancelar reserva: {str(e)}")
    
    def procesar(self):
        """Procesa la reserva (método con try/except/finally)"""
        resultado = None
        try:
            if self._estado == "PENDIENTE":
                resultado = self.confirmar()
            return resultado
        except Exception as e:
            Logger().registrar_error(e, f"procesar_reserva_{self._id_reserva}")
            return False, str(e)
        finally:
            Logger().registrar("INFO", f"Procesamiento de reserva {self._id_reserva} finalizado")
    
    def obtener_info(self):
        """Retorna información completa de la reserva"""
        costo_str = f"${self._costo_total}" if self._costo_total else "No calculado"
        return (f"Reserva #{self._id_reserva} | Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} hrs | "
                f"Estado: {self._estado} | Costo: {costo_str}")
    
    def __str__(self):
        return self.obtener_info()


# ==================== SISTEMA PRINCIPAL ====================

class SistemaGestion:
    """Clase principal que gestiona todo el sistema"""
    
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._logger = Logger()
        self._contador_clientes = 1
        self._contador_servicios = 1
        self._contador_reservas = 1
        
        self._cargar_datos_iniciales()
    
    def _cargar_datos_iniciales(self):
        """Carga servicios por defecto"""
        try:
            servicios_iniciales = [
                ReservaSala("S001", "Sala Ejecutiva", 50.0, 10, "Proyector, Pizarra, WiFi"),
                ReservaSala("S002", "Sala Pequeña", 30.0, 4, "TV, WiFi"),
                AlquilerEquipo("E001", "Laptop Gamer", 40.0, "Laptop", 30),
                AlquilerEquipo("E002", "Proyector 4K", 25.0, "Proyector", 15),
                AsesoriaEspecializada("A001", "Asesoría Python", 60.0, "Programación", "Senior"),
                AsesoriaEspecializada("A002", "Asesoría IA", 80.0, "Inteligencia Artificial", "Master"),
            ]
            
            for servicio in servicios_iniciales:
                self._servicios.append(servicio)
                self._contador_servicios += 1
            
            self._logger.registrar("INFO", f"Cargados {len(servicios_iniciales)} servicios iniciales")
        
        except Exception as e:
            self._logger.registrar_error(e, "cargar_datos_iniciales")
    
    def registrar_cliente(self, nombre, email, telefono):
        """Registra un nuevo cliente con manejo de excepciones"""
        try:
            # Validaciones
            if not nombre or not email or not telefono:
                raise ValidacionError("Todos los campos son obligatorios")
            
            # Crear cliente
            id_cliente = f"C{self._contador_clientes:03d}"
            cliente = Cliente(id_cliente, nombre, email, telefono)
            
            # Verificar si ya existe (por email)
            for c in self._clientes:
                if c.email == email:
                    raise ClienteError(f"Ya existe un cliente con el email {email}")
            
            self._clientes.append(cliente)
            self._contador_clientes += 1
            
            self._logger.registrar("INFO", f"Cliente registrado: {cliente.nombre}")
            return True, f"Cliente {cliente.nombre} registrado con ID {id_cliente}"
        
        except ValidacionError as e:
            self._logger.registrar_error(e, "registrar_cliente")
            return False, f"Error de validación: {str(e)}"
        except ClienteError as e:
            self._logger.registrar_error(e, "registrar_cliente")
            return False, str(e)
        except Exception as e:
            self._logger.registrar_error(e, "registrar_cliente")
            return False, f"Error inesperado: {str(e)}"
    
    def listar_clientes(self):
        """Lista todos los clientes"""
        if not self._clientes:
            print("No hay clientes registrados")
            return
        print("\n📋 CLIENTES REGISTRADOS:")
        print("-" * 60)
        for cliente in self._clientes:
            print(f"  {cliente}")
    
    def listar_servicios(self):
        """Lista todos los servicios disponibles"""
        if not self._servicios:
            print("No hay servicios disponibles")
            return
        print("\n🔧 SERVICIOS DISPONIBLES:")
        print("-" * 60)
        for servicio in self._servicios:
            print(f"  {servicio.describir()}")
    
    def crear_reserva(self, id_cliente, id_servicio, duracion):
        """Crea una nueva reserva con manejo de excepciones"""
        try:
            # Buscar cliente
            cliente = None
            for c in self._clientes:
                if c.id_cliente == id_cliente:
                    cliente = c
                    break
            
            if not cliente:
                raise ReservaError(f"Cliente con ID {id_cliente} no encontrado")
            
            # Buscar servicio
            servicio = None
            for s in self._servicios:
                if s.id_servicio == id_servicio:
                    servicio = s
                    break
            
            if not servicio:
                raise ReservaError(f"Servicio con ID {id_servicio} no encontrado")
            
            # Validar duración
            if duracion <= 0:
                raise ValidacionError("La duración debe ser mayor a 0")
            
            if duracion > 24:
                raise ValidacionError("La duración no puede exceder 24 horas")
            
            # Crear reserva
            id_reserva = f"R{self._contador_reservas:04d}"
            reserva = Reserva(id_reserva, cliente, servicio, float(duracion))
            
            self._reservas.append(reserva)
            self._contador_reservas += 1
            
            self._logger.registrar("INFO", f"Reserva creada: {id_reserva}")
            return True, reserva
        
        except ReservaError as e:
            self._logger.registrar_error(e, "crear_reserva")
            return False, str(e)
        except ValidacionError as e:
            self._logger.registrar_error(e, "crear_reserva")
            return False, str(e)
        except Exception as e:
            self._logger.registrar_error(e, "crear_reserva")
            return False, f"Error inesperado: {str(e)}"
    
    def confirmar_reserva(self, id_reserva):
        """Confirma una reserva existente"""
        try:
            reserva = None
            for r in self._reservas:
                if r.id_reserva == id_reserva:
                    reserva = r
                    break
            
            if not reserva:
                raise ReservaError(f"Reserva {id_reserva} no encontrada")
            
            resultado, mensaje = reserva.confirmar()
            return resultado, mensaje
        
        except ReservaError as e:
            self._logger.registrar_error(e, "confirmar_reserva")
            return False, str(e)
        except Exception as e:
            self._logger.registrar_error(e, "confirmar_reserva")
            return False, f"Error inesperado: {str(e)}"
    
    def cancelar_reserva(self, id_reserva):
        """Cancela una reserva"""
        try:
            reserva = None
            for r in self._reservas:
                if r.id_reserva == id_reserva:
                    reserva = r
                    break
            
            if not reserva:
                raise ReservaError(f"Reserva {id_reserva} no encontrada")
            
            resultado, mensaje = reserva.cancelar()
            return resultado, mensaje
        
        except ReservaError as e:
            self._logger.registrar_error(e, "cancelar_reserva")
            return False, str(e)
        except Exception as e:
            self._logger.registrar_error(e, "cancelar_reserva")
            return False, f"Error inesperado: {str(e)}"
    
    def listar_reservas(self):
        """Lista todas las reservas"""
        if not self._reservas:
            print("No hay reservas registradas")
            return
        print("\n📅 RESERVAS:")
        print("-" * 70)
        for reserva in self._reservas:
            print(f"  {reserva}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del sistema"""
        print("\n📊 ESTADÍSTICAS DEL SISTEMA:")
        print("-" * 50)
        print(f"  Clientes registrados: {len(self._clientes)}")
        print(f"  Servicios disponibles: {len(self._servicios)}")
        print(f"  Reservas creadas: {len(self._reservas)}")
        
        reservas_confirmadas = sum(1 for r in self._reservas if r.estado == "CONFIRMADA")
        reservas_canceladas = sum(1 for r in self._reservas if r.estado == "CANCELADA")
        
        print(f"  Reservas confirmadas: {reservas_confirmadas}")
        print(f"  Reservas canceladas: {reservas_canceladas}")


# ==================== DEMOSTRACIÓN COMPLETA ====================

def demostracion():
    """Función que demuestra el funcionamiento del sistema con 10+ operaciones"""
    
    print("\n" + "="*70)
    print("🏢 SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ 🏢")
    print("="*70)
    
    sistema = SistemaGestion()
    
    # ===== OPERACIÓN 1: Registrar cliente válido =====
    print("\n✅ 1. Registrando cliente válido...")
    ok, msg = sistema.registrar_cliente("Juan Perez", "juan@email.com", "3001234567")
    print(f"   Resultado: {msg}")
    
    # ===== OPERACIÓN 2: Registrar otro cliente válido =====
    print("\n✅ 2. Registrando otro cliente válido...")
    ok, msg = sistema.registrar_cliente("Maria Gomez", "maria@email.com", "3117654321")
    print(f"   Resultado: {msg}")
    
    # ===== OPERACIÓN 3: Registrar cliente inválido (email sin @) =====
    print("\n❌ 3. Registrando cliente con email inválido...")
    ok, msg = sistema.registrar_cliente("Pedro Lopez", "pedroemail.com", "322555888")
    print(f"   Resultado: {msg} (Error capturado correctamente)")
    
    # ===== OPERACIÓN 4: Registrar cliente con teléfono inválido =====
    print("\n❌ 4. Registrando cliente con teléfono inválido...")
    ok, msg = sistema.registrar_cliente("Ana Ramirez", "ana@email.com", "abc123")
    print(f"   Resultado: {msg} (Error capturado correctamente)")
    
    # ===== OPERACIÓN 5: Listar clientes =====
    print("\n📋 5. Listando clientes registrados...")
    sistema.listar_clientes()
    
    # ===== OPERACIÓN 6: Listar servicios =====
    print("\n🔧 6. Listando servicios disponibles...")
    sistema.listar_servicios()
    
    # ===== OPERACIÓN 7: Crear reserva válida =====
    print("\n✅ 7. Creando reserva válida...")
    ok, resultado = sistema.crear_reserva("C001", "S001", 3)
    if ok:
        reserva = resultado
        print(f"   Reserva creada: {reserva.id_reserva}")
    else:
        print(f"   Error: {resultado}")
    
    # ===== OPERACIÓN 8: Crear reserva con servicio inexistente =====
    print("\n❌ 8. Creando reserva con servicio inexistente...")
    ok, resultado = sistema.crear_reserva("C001", "X999", 2)
    print(f"   Resultado: {resultado} (Error capturado correctamente)")
    
    # ===== OPERACIÓN 9: Crear reserva con duración inválida =====
    print("\n❌ 9. Creando reserva con duración inválida...")
    ok, resultado = sistema.crear_reserva("C001", "E001", -5)
    print(f"   Resultado: {resultado} (Error capturado correctamente)")
    
    # ===== OPERACIÓN 10: Confirmar reserva =====
    print("\n✅ 10. Confirmando reserva creada...")
    ok, msg = sistema.confirmar_reserva("R0001")
    print(f"   Resultado: {msg}")
    
    # ===== OPERACIÓN 11: Crear segunda reserva =====
    print("\n✅ 11. Creando segunda reserva...")
    ok, resultado = sistema.crear_reserva("C002", "A001", 5)
    if ok:
        reserva2 = resultado
        print(f"   Reserva creada: {reserva2.id_reserva}")
        ok2, msg2 = sistema.confirmar_reserva(reserva2.id_reserva)
        print(f"   Confirmación: {msg2}")
    
    # ===== OPERACIÓN 12: Cancelar reserva =====
    print("\n✅ 12. Cancelando primera reserva...")
    ok, msg = sistema.cancelar_reserva("R0001")
    print(f"   Resultado: {msg}")
    
    # ===== OPERACIÓN 13: Listar todas las reservas =====
    print("\n📅 13. Listando todas las reservas...")
    sistema.listar_reservas()
    
    # ===== OPERACIÓN 14: Mostrar estadísticas =====
    print("\n📊 14. Estadísticas del sistema...")
    sistema.mostrar_estadisticas()
    
    # ===== OPERACIÓN 15: Demostración de sobrecarga =====
    print("\n🔄 15. Demostración de sobrecarga (calcular costo con descuento)...")
    servicio = sistema._servicios[0]  # Tomar primer servicio
    costo_normal = servicio.calcular_costo(5)
    costo_con_descuento = servicio.calcular_costo_con_descuento(5, descuento=10, impuesto=19)
    print(f"   Costo normal (5 horas): ${costo_normal}")
    print(f"   Costo con 10% descuento + 19% impuesto: ${costo_con_descuento}")
    
    # ===== OPERACIÓN 16: Demostración de try/except/else/finally =====
    print("\n🔄 16. Demostración de try/except/else/finally...")
    try:
        operacion_invalida = 10 / 2  # Operación válida
        print(f"   Operación exitosa: {operacion_invalida}")
    except ZeroDivisionError as e:
        print(f"   Error capturado: {e}")
    else:
        print("   Else: No hubo errores en el try")
    finally:
        print("   Finally: Este bloque siempre se ejecuta")
    
    print("\n" + "="*70)
    print("🏁 DEMOSTRACIÓN COMPLETADA - Sistema estable y robusto 🏁")
    print("="*70)
    print("\n📁 Revisa el archivo 'sistema_log.txt' para ver el registro de eventos y errores")
    print("="*70)


if __name__ == "__main__":
    demostracion()
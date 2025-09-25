#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente InnoAd para Raspberry Pi
==================================

Esta aplicación se ejecuta en dispositivos Raspberry Pi para:
- Conectar con el servidor InnoAd via WebSocket
- Reproducir contenido multimedia en pantalla
- Monitorear estado del dispositivo
- Reportar métricas del sistema

TAREAS PARA EL EQUIPO DE DESARROLLO:
1. Completar sistema de descarga de contenido con reintentos
2. Implementar reproducción de diferentes tipos de multimedia
3. Agregar sistema de cache inteligente de contenido
4. Implementar actualizaciones automáticas de software
5. Crear sistema de logs robusto
6. Agregar configuración via archivo de configuración

Autor: Equipo SENA ADSO
Versión: 1.0.0
"""

import asyncio
import websockets
import json
import logging
import subprocess
import psutil
import requests
import hashlib
import os
import signal
import sys
from datetime import datetime
from pathlib import Path
from threading import Thread
import time

# ========================================
# CONFIGURACIÓN GLOBAL
# ========================================

# Variables de entorno
SERVIDOR_INNOAD = os.getenv('INNOAD_SERVER', 'ws://localhost:8086/websocket/raspberry')
DIRECTORIO_CONTENIDO = Path(os.getenv('CONTENT_DIR', '/opt/innoad/content'))
DIRECTORIO_LOGS = Path(os.getenv('LOGS_DIR', '/opt/innoad/logs'))
DIRECTORIO_CONFIG = Path(os.getenv('CONFIG_DIR', '/opt/innoad/config'))

# Obtener MAC address del dispositivo
try:
    MAC_ADDRESS = subprocess.check_output(['cat', '/sys/class/net/eth0/address']).decode().strip()
except:
    # Fallback para testing
    MAC_ADDRESS = 'AA:BB:CC:DD:EE:FF'

DEVICE_ID = MAC_ADDRESS.replace(':', '')

# Crear directorios necesarios
for directorio in [DIRECTORIO_CONTENIDO, DIRECTORIO_LOGS, DIRECTORIO_CONFIG]:
    directorio.mkdir(parents=True, exist_ok=True)

# ========================================
# CONFIGURACIÓN DE LOGGING
# ========================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DIRECTORIO_LOGS / 'innoad_cliente.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ========================================
# CLASE PRINCIPAL DEL CLIENTE
# ========================================

class ClienteInnoAdRaspberry:
    """
    Cliente principal para comunicación con InnoAd

    Maneja toda la lógica de conexión, reproducción de contenido
    y monitoreo del dispositivo Raspberry Pi.
    """

    def __init__(self):
        self.websocket = None
        self.ejecutando = False
        self.contenido_actual = None
        self.proceso_reproduccion = None
        self.intervalo_heartbeat = 30  # segundos
        self.intentos_reconexion = 0
        self.max_intentos_reconexion = 10

        # Configurar manejadores de señales
        signal.signal(signal.SIGINT, self.manejar_señal)
        signal.signal(signal.SIGTERM, self.manejar_señal)

    def manejar_señal(self, signum, frame):
        """
        Maneja señales del sistema para cierre limpio
        """
        logger.info(f"Señal recibida: {signum}. Cerrando aplicación...")
        self.ejecutando = False

    async def conectar_servidor(self):
        """
        Establece conexión WebSocket con el servidor InnoAd

        TODO: Implementar autenticación robusta del dispositivo
        TODO: Agregar soporte para certificados SSL/TLS
        """
        try:
            headers = {
                'mac_address': MAC_ADDRESS,
                'device_type': 'raspberry_pi',
                'software_version': '1.0.0',
                'device_id': DEVICE_ID
            }

            logger.info(f"Conectando a servidor InnoAd: {SERVIDOR_INNOAD}")

            self.websocket = await websockets.connect(
                SERVIDOR_INNOAD,
                extra_headers=headers,
                ping_interval=20,
                ping_timeout=10,
                max_size=1024*1024,  # 1MB max message size
                max_queue=32
            )

            logger.info("✅ Conexión WebSocket establecida exitosamente")
            self.ejecutando = True
            self.intentos_reconexion = 0

            # Iniciar tareas concurrentes
            await asyncio.gather(
                self.bucle_heartbeat(),
                self.escuchar_mensajes(),
                return_exceptions=True
            )

        except Exception as e:
            logger.error(f"❌ Error conectando al servidor: {e}")
            await self.manejar_reconexion()

    async def escuchar_mensajes(self):
        """
        Escucha mensajes del servidor y los procesa

        TODO: Implementar validación de mensajes más robusta
        TODO: Agregar sistema de acknowledgments
        """
        try:
            async for mensaje in self.websocket:
                try:
                    datos = json.loads(mensaje)
                    await self.procesar_mensaje(datos)
                except json.JSONDecodeError as e:
                    logger.error(f"Error decodificando mensaje JSON: {e}")
                except Exception as e:
                    logger.error(f"Error procesando mensaje: {e}")

        except websockets.exceptions.ConnectionClosed:
            logger.warning("🔌 Conexión cerrada por el servidor")
            self.ejecutando = False
        except Exception as e:
            logger.error(f"❌ Error escuchando mensajes: {e}")

    async def procesar_mensaje(self, datos):
        """
        Procesa mensajes recibidos del servidor

        TODO: Implementar más tipos de comandos
        TODO: Agregar validación de permisos por comando
        """
        comando = datos.get('comando', 'UNKNOWN')
        logger.info(f"📨 Procesando comando: {comando}")

        try:
            if comando == 'REPRODUCIR_CONTENIDO':
                await self.reproducir_contenido(
                    datos.get('contenido', {}),
                    datos.get('configuracion', {})
                )

            elif comando == 'DETENER_REPRODUCCION':
                await self.detener_reproduccion()

            elif comando == 'ACTUALIZAR_CONFIGURACION':
                await self.actualizar_configuracion(datos.get('configuracion', {}))

            elif comando == 'REINICIAR_DISPOSITIVO':
                await self.reiniciar_dispositivo()

            elif comando == 'ACTUALIZAR_SOFTWARE':
                await self.actualizar_software()

            elif comando == 'OBTENER_ESTADO':
                await self.enviar_estado_completo()

            else:
                logger.warning(f"⚠️ Comando no reconocido: {comando}")
                await self.enviar_respuesta_error(f"Comando no soportado: {comando}")

        except Exception as e:
            logger.error(f"❌ Error ejecutando comando {comando}: {e}")
            await self.enviar_respuesta_error(f"Error en comando: {e}")

    async def reproducir_contenido(self, info_contenido, configuracion):
        """
        Descarga y reproduce contenido multimedia

        TODO: Implementar sistema de cache inteligente
        TODO: Agregar validación de formatos soportados
        TODO: Implementar reproducción en bucle configurable
        """
        try:
            contenido_id = info_contenido.get('id')
            tipo_contenido = info_contenido.get('tipo')
            logger.info(f"🎬 Iniciando reproducción de contenido ID: {contenido_id}")

            # Detener reproducción actual si existe
            await self.detener_reproduccion()

            # Descargar contenido si es necesario
            archivo_local = await self.descargar_contenido(info_contenido)
            if not archivo_local:
                await self.enviar_respuesta_error("Error descargando contenido")
                return

            # Aplicar configuración del dispositivo
            await self.aplicar_configuracion(configuracion)

            # Iniciar reproducción según tipo
            if tipo_contenido in ['imagen', 'jpg', 'png']:
                await self.mostrar_imagen(archivo_local, info_contenido.get('duracion', 30))

            elif tipo_contenido in ['video', 'mp4', 'avi', 'mov']:
                await self.reproducir_video(archivo_local)

            elif tipo_contenido == 'web':
                await self.abrir_pagina_web(info_contenido.get('url'))

            elif tipo_contenido == 'html':
                await self.mostrar_html(info_contenido.get('contenido_html', ''))

            else:
                logger.warning(f"⚠️ Tipo de contenido no soportado: {tipo_contenido}")
                await self.enviar_respuesta_error(f"Tipo no soportado: {tipo_contenido}")
                return

            # Notificar inicio de reproducción
            self.contenido_actual = info_contenido
            await self.enviar_estado_reproduccion("REPRODUCIENDO", contenido_id)

        except Exception as e:
            logger.error(f"❌ Error reproduciendo contenido: {e}")
            await self.enviar_respuesta_error(f"Error en reproducción: {e}")

    async def descargar_contenido(self, info_contenido):
        """
        Descarga contenido desde el servidor si no existe localmente

        TODO: Implementar reintentos con backoff exponencial
        TODO: Agregar soporte para resume de descargas parciales
        TODO: Implementar limpieza automática de archivos antiguos
        """
        try:
            contenido_id = info_contenido.get('id')
            url = info_contenido.get('url')
            checksum_esperado = info_contenido.get('checksum')

            if not url:
                logger.error("❌ URL de contenido no proporcionada")
                return None

            # Generar nombre de archivo local
            extension = self.obtener_extension_archivo(url, info_contenido.get('tipo'))
            archivo_local = DIRECTORIO_CONTENIDO / f"contenido_{contenido_id}.{extension}"

            # Verificar si ya existe y es válido
            if archivo_local.exists():
                if self.verificar_checksum(archivo_local, checksum_esperado):
                    logger.info(f"✅ Contenido ya existe y es válido: {archivo_local}")
                    return archivo_local
                else:
                    logger.info("🔄 Contenido existe pero checksum no coincide, descargando nuevamente")
                    archivo_local.unlink()

            # Descargar contenido
            logger.info(f"📥 Descargando contenido desde: {url}")

            with requests.get(url, stream=True, timeout=30) as response:
                response.raise_for_status()

                with open(archivo_local, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

            # Verificar integridad
            if checksum_esperado and not self.verificar_checksum(archivo_local, checksum_esperado):
                archivo_local.unlink()
                raise Exception("Checksum del archivo no coincide")

            logger.info(f"✅ Contenido descargado exitosamente: {archivo_local}")

            # Notificar descarga completada
            await self.enviar_mensaje({
                'tipo': 'DESCARGA_COMPLETADA',
                'contenido_id': contenido_id,
                'tamano_archivo': archivo_local.stat().st_size,
                'timestamp': datetime.now().isoformat()
            })

            return archivo_local

        except Exception as e:
            logger.error(f"❌ Error descargando contenido: {e}")
            return None

    def obtener_extension_archivo(self, url, tipo_contenido):
        """
        Obtiene la extensión correcta del archivo basada en URL y tipo
        """
        # Intentar obtener de la URL primero
        if '.' in url:
            return url.split('.')[-1].lower()

        # Fallback basado en tipo de contenido
        extensiones = {
            'imagen': 'jpg',
            'video': 'mp4',
            'web': 'html',
            'html': 'html',
            'texto': 'txt'
        }

        return extensiones.get(tipo_contenido, 'bin')

    def verificar_checksum(self, archivo, checksum_esperado):
        """
        Verifica integridad del archivo usando MD5

        TODO: Soportar otros algoritmos de hash (SHA256, etc.)
        """
        if not checksum_esperado:
            return True

        try:
            hash_md5 = hashlib.md5()
            with open(archivo, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)

            return hash_md5.hexdigest() == checksum_esperado
        except Exception as e:
            logger.error(f"❌ Error verificando checksum: {e}")
            return False

    async def mostrar_imagen(self, archivo_imagen, duracion_segundos):
        """
        Muestra imagen en pantalla completa usando feh

        TODO: Implementar transiciones suaves entre imágenes
        TODO: Agregar soporte para presentaciones de imágenes
        """
        try:
            comando = [
                'feh',
                '--fullscreen',
                '--hide-pointer',
                '--auto-zoom',
                '--borderless',
                str(archivo_imagen)
            ]

            logger.info(f"🖼️ Mostrando imagen: {archivo_imagen} por {duracion_segundos}s")

            self.proceso_reproduccion = subprocess.Popen(comando)

            # Programar cierre después de duración especificada
            if duracion_segundos > 0:
                await asyncio.sleep(duracion_segundos)
                await self.detener_reproduccion()

        except Exception as e:
            logger.error(f"❌ Error mostrando imagen: {e}")

    async def reproducir_video(self, archivo_video):
        """
        Reproduce video en pantalla completa usando omxplayer

        TODO: Implementar controles de reproducción (pause, skip, etc.)
        TODO: Agregar soporte para subtítulos
        """
        try:
            # Comando para Raspberry Pi con GPU
            comando = [
                'omxplayer',
                '--no-osd',
                '--no-keys',
                '--aspect-mode', 'fill',
                '--blank',
                str(archivo_video)
            ]

            logger.info(f"🎥 Reproduciendo video: {archivo_video}")

            self.proceso_reproduccion = subprocess.Popen(comando)

            # Monitorear proceso
            await self.monitorear_reproduccion()

        except FileNotFoundError:
            # Fallback a VLC si omxplayer no está disponible
            try:
                comando_vlc = [
                    'vlc',
                    '--intf', 'dummy',
                    '--fullscreen',
                    '--no-video-title-show',
                    str(archivo_video)
                ]

                self.proceso_reproduccion = subprocess.Popen(comando_vlc)
                await self.monitorear_reproduccion()

            except Exception as e:
                logger.error(f"❌ Error reproduciendo video: {e}")

        except Exception as e:
            logger.error(f"❌ Error reproduciendo video: {e}")

    async def abrir_pagina_web(self, url):
        """
        Abre página web en modo kiosko usando Chromium

        TODO: Implementar rotación automática de páginas web
        TODO: Agregar soporte para autenticación web
        """
        try:
            comando = [
                'chromium-browser',
                '--start-fullscreen',
                '--kiosk',
                '--incognito',
                '--noerrdialogs',
                '--disable-translate',
                '--no-first-run',
                '--disable-infobars',
                '--disable-features=TranslateUI',
                '--disable-session-crashed-bubble',
                url
            ]

            logger.info(f"🌐 Abriendo página web: {url}")

            self.proceso_reproduccion = subprocess.Popen(comando)

        except Exception as e:
            logger.error(f"❌ Error abriendo página web: {e}")

    async def mostrar_html(self, contenido_html):
        """
        Muestra contenido HTML personalizado

        TODO: Implementar sistema de templates
        TODO: Agregar soporte para CSS personalizado
        """
        try:
            # Crear archivo HTML temporal
            archivo_html = DIRECTORIO_CONTENIDO / 'temp_content.html'

            with open(archivo_html, 'w', encoding='utf-8') as f:
                f.write(contenido_html)

            await self.abrir_pagina_web(f'file://{archivo_html}')

        except Exception as e:
            logger.error(f"❌ Error mostrando HTML: {e}")

    async def detener_reproduccion(self):
        """
        Detiene la reproducción actual

        TODO: Implementar transición suave al detener
        """
        if self.proceso_reproduccion:
            try:
                self.proceso_reproduccion.terminate()
                await asyncio.sleep(2)

                if self.proceso_reproduccion.poll() is None:
                    self.proceso_reproduccion.kill()

                self.proceso_reproduccion = None
                self.contenido_actual = None

                logger.info("⏹️ Reproducción detenida")
                await self.enviar_estado_reproduccion("DETENIDO", None)

            except Exception as e:
                logger.error(f"❌ Error deteniendo reproducción: {e}")

    async def aplicar_configuracion(self, configuracion):
        """
        Aplica configuración del dispositivo (volumen, brillo, etc.)

        TODO: Implementar más opciones de configuración
        TODO: Persistir configuración entre reinicios
        """
        try:
            # Configurar volumen
            if 'volumen' in configuracion:
                volumen = configuracion['volumen']
                subprocess.run(['amixer', 'set', 'Master', f'{volumen}%'], 
                              check=False, capture_output=True)
                logger.info(f"🔊 Volumen configurado: {volumen}%")

            # Configurar brillo de pantalla
            if 'brillo' in configuracion:
                brillo = configuracion['brillo']
                brillo_path = '/sys/class/backlight/rpi_backlight/brightness'

                if os.path.exists(brillo_path):
                    try:
                        with open(brillo_path, 'w') as f:
                            f.write(str(int(255 * brillo / 100)))
                        logger.info(f"💡 Brillo configurado: {brillo}%")
                    except PermissionError:
                        logger.warning("⚠️ Sin permisos para cambiar brillo de pantalla")

        except Exception as e:
            logger.error(f"❌ Error aplicando configuración: {e}")

    async def monitorear_reproduccion(self):
        """
        Monitorea el estado del proceso de reproducción actual
        """
        while self.proceso_reproduccion and self.proceso_reproduccion.poll() is None:
            await asyncio.sleep(5)

        if self.proceso_reproduccion:
            codigo_salida = self.proceso_reproduccion.returncode
            if codigo_salida == 0:
                await self.enviar_estado_reproduccion("COMPLETADO", None)
            else:
                await self.enviar_estado_reproduccion("ERROR", None)

    async def bucle_heartbeat(self):
        """
        Envía heartbeat periódico al servidor con métricas del sistema
        """
        while self.ejecutando:
            try:
                await self.enviar_heartbeat()
                await asyncio.sleep(self.intervalo_heartbeat)
            except Exception as e:
                logger.error(f"❌ Error en heartbeat: {e}")
                await asyncio.sleep(5)  # Retry más rápido en caso de error

    async def enviar_heartbeat(self):
        """
        Envía información de estado y métricas del dispositivo

        TODO: Agregar más métricas específicas de Raspberry Pi
        TODO: Implementar alertas por métricas críticas
        """
        try:
            # Obtener métricas del sistema
            cpu_percent = psutil.cpu_percent(interval=1)
            memoria = psutil.virtual_memory()
            disco = psutil.disk_usage('/')

            # Temperatura de CPU (específico de Raspberry Pi)
            temperatura = self.obtener_temperatura_cpu()

            # Información de red
            ip_local = self.obtener_ip_local()

            datos_heartbeat = {
                'tipo': 'HEARTBEAT',
                'timestamp': datetime.now().isoformat(),
                'mac_address': MAC_ADDRESS,
                'ip_address': ip_local,
                'version_software': '1.0.0',
                'estado': 'CONECTADO',
                'metricas': {
                    'cpu_usage': round(cpu_percent, 2),
                    'memoria_total': memoria.total,
                    'memoria_usada': memoria.used,
                    'memoria_porcentaje': round(memoria.percent, 2),
                    'disco_total': disco.total,
                    'disco_usado': disco.used,
                    'disco_porcentaje': round((disco.used / disco.total) * 100, 2),
                    'temperatura_cpu': temperatura
                },
                'reproduccion': {
                    'activa': self.proceso_reproduccion is not None,
                    'contenido_id': self.contenido_actual.get('id') if self.contenido_actual else None
                }
            }

            await self.enviar_mensaje(datos_heartbeat)

        except Exception as e:
            logger.error(f"❌ Error enviando heartbeat: {e}")

    def obtener_temperatura_cpu(self):
        """
        Obtiene temperatura del CPU (específico de Raspberry Pi)
        """
        try:
            resultado = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
            temperatura = float(resultado.replace('temp=', '').replace("'C\n", ""))
            return temperatura
        except:
            return 0.0

    def obtener_ip_local(self):
        """
        Obtiene la dirección IP local del dispositivo
        """
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    async def enviar_mensaje(self, datos):
        """
        Envía mensaje al servidor WebSocket
        """
        try:
            if self.websocket and not self.websocket.closed:
                mensaje = json.dumps(datos, ensure_ascii=False)
                await self.websocket.send(mensaje)
        except Exception as e:
            logger.error(f"❌ Error enviando mensaje: {e}")

    async def enviar_estado_reproduccion(self, estado, contenido_id):
        """
        Notifica cambio de estado de reproducción al servidor
        """
        await self.enviar_mensaje({
            'tipo': 'ESTADO_REPRODUCCION',
            'estado': estado,
            'contenido_id': contenido_id,
            'timestamp': datetime.now().isoformat()
        })

    async def enviar_respuesta_error(self, mensaje_error):
        """
        Envía mensaje de error al servidor
        """
        await self.enviar_mensaje({
            'tipo': 'ERROR',
            'mensaje': mensaje_error,
            'timestamp': datetime.now().isoformat()
        })

    async def manejar_reconexion(self):
        """
        Maneja la reconexión automática al servidor
        """
        if self.intentos_reconexion >= self.max_intentos_reconexion:
            logger.error("❌ Máximo número de intentos de reconexión alcanzado")
            return

        self.intentos_reconexion += 1
        tiempo_espera = min(30, 2 ** self.intentos_reconexion)  # Backoff exponencial

        logger.info(f"🔄 Reintento de conexión {self.intentos_reconexion}/{self.max_intentos_reconexion} en {tiempo_espera}s")

        await asyncio.sleep(tiempo_espera)

        # Reintentar conexión
        await self.conectar_servidor()

# ========================================
# FUNCIÓN PRINCIPAL
# ========================================

async def main():
    """
    Función principal de la aplicación

    TODO: Agregar manejo de configuración desde archivo
    TODO: Implementar modo daemon para producción
    """
    logger.info("🚀 Iniciando Cliente InnoAd para Raspberry Pi")
    logger.info(f"📍 MAC Address: {MAC_ADDRESS}")
    logger.info(f"🔗 Servidor: {SERVIDOR_INNOAD}")

    cliente = ClienteInnoAdRaspberry()

    # Loop principal con reconexión automática
    while True:
        try:
            await cliente.conectar_servidor()
        except KeyboardInterrupt:
            logger.info("👋 Cliente detenido por usuario")
            break
        except Exception as e:
            logger.error(f"❌ Error en bucle principal: {e}")

        if not cliente.ejecutando:
            break

        logger.info("🔄 Reiniciando conexión en 10 segundos...")
        await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Aplicación terminada por usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        sys.exit(1)

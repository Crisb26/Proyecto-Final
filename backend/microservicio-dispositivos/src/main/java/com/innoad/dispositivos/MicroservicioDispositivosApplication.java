package com.innoad.dispositivos;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * Clase principal del microservicio de dispositivos Raspberry Pi
 * 
 * Este microservicio maneja toda la comunicación y gestión de dispositivos remotos:
 * - Conexión WebSocket bidireccional con Raspberry Pi
 * - Envío de contenido multimedia a pantallas
 * - Monitoreo en tiempo real de estado de dispositivos
 * - Programación automática de contenido
 * - Control remoto de dispositivos
 * 
 * TAREAS:
 * 1. Completar configuración WebSocket para comunicación con Raspberry Pi
 * 2. Implementar sistema de heartbeat y reconexión automática
 * 3. Crear sistema de descarga segura de contenido
 * 4. Implementar scheduler para programación de contenido
 * 5. Agregar sistema de métricas y monitoreo de dispositivos
 * 6. Crear panel de control en tiempo real
 */
@SpringBootApplication
@EnableScheduling  // Para tareas programadas (heartbeat, limpieza, etc.)
@EnableAsync      // Para operaciones asíncronas de comunicación
public class MicroservicioDispositivosApplication {

    public static void main(String[] args) {
        SpringApplication.run(MicroservicioDispositivosApplication.class, args);
        System.out.println("📺 Microservicio Dispositivos Raspberry Pi iniciado correctamente");
        System.out.println("🔗 WebSocket disponible en: ws://localhost:8086/websocket/raspberry");
    }
}

package com.innoad.usuarios;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Clase principal del microservicio de usuarios InnoAd
 * 
 * Este microservicio maneja toda la lógica relacionada con:
 * - Gestión de usuarios del sistema
 * - Autenticación y autorización
 * - Roles y permisos
 * - Recuperación de contraseñas
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Completar la configuración de seguridad JWT
 * 2. Implementar validaciones de negocio en los servicios
 * 3. Agregar logs de auditoría
 * 4. Implementar envío de emails para recuperación de contraseña
 * 5. Crear tests unitarios e integración
 * 
 * @author Equipo SENA ADSO
 * @version 1.0.0
 */
@SpringBootApplication
public class MicroservicioUsuariosApplication {

    public static void main(String[] args) {
        SpringApplication.run(MicroservicioUsuariosApplication.class, args);
        System.out.println("🚀 Microservicio Usuarios InnoAd iniciado correctamente");
    }
}

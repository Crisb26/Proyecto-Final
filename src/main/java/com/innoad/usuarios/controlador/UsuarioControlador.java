package com.innoad.usuarios.controlador;

import com.innoad.usuarios.dto.UsuarioDTO;
import com.innoad.usuarios.servicio.UsuarioServicio;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

/**
 * 
 * Controlador REST para gestión de usuarios
 * 
 * Este controlador expone los endpoints para todas las operaciones
 * relacionadas con usuarios: CRUD, búsquedas, cambio de estado, etc.
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Implementar validaciones de permisos con @PreAuthorize
 * 2. Agregar documentación Swagger/OpenAPI
 * 3. Implementar paginación en listados
 * 4. Agregar endpoints para reportes y estadísticas
 * 5. Implementar manejo de excepciones personalizado
 * 6. Agregar logs de auditoría en operaciones críticas
 * 
 * @author Equipo SENA ADSO
 */
@RestController
@RequestMapping("/api/usuarios")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "${cors.allowed-origins:http://localhost:4200}")
public class UsuarioControlador {
    private final UsuarioServicio usuarioServicio;
    /**Prueba */

    /**
     * Obtiene todos los usuarios del sistema
     * TODO: Implementar paginación y filtros
     * TODO: Agregar @PreAuthorize("hasRole('ADMIN') or hasRole('MANAGER')")
     */
    @GetMapping
    public ResponseEntity<List<UsuarioDTO>> obtenerTodosLosUsuarios() {
        log.info("GET /api/usuarios - Obteniendo todos los usuarios");

        try {
            List<UsuarioDTO> usuarios = usuarioServicio.obtenerTodosLosUsuarios();
            return ResponseEntity.ok(usuarios);
        } catch (Exception e) {
            log.error("Error obteniendo usuarios: {}", e.getMessage());
            return ResponseEntity.internalServerError().build();
        }
    }

    /**
     * Obtiene un usuario específico por ID
     * TODO: Validar permisos (solo admin o el mismo usuario)
     */
    @GetMapping("/{id}")
    public ResponseEntity<UsuarioDTO> obtenerUsuarioPorId(@PathVariable Long id) {
        log.info("GET /api/usuarios/{} - Obteniendo usuario por ID", id);

        return usuarioServicio.obtenerUsuarioPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo usuario
     * TODO: Agregar @PreAuthorize("hasRole('ADMIN')")
     * TODO: Validar datos de entrada
     */
    @PostMapping
    public ResponseEntity<UsuarioDTO> crearUsuario(@Valid @RequestBody UsuarioDTO usuarioDTO) {
        log.info("POST /api/usuarios - Creando nuevo usuario: {}", usuarioDTO.getCorreo());

        try {
            UsuarioDTO usuarioCreado = usuarioServicio.crearUsuario(usuarioDTO);
            return ResponseEntity.status(HttpStatus.CREATED).body(usuarioCreado);
        } catch (RuntimeException e) {
            log.error("Error creando usuario: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        } catch (Exception e) {
            log.error("Error interno creando usuario: {}", e.getMessage());
            return ResponseEntity.internalServerError().build();
        }
    }

    /**
     * Actualiza un usuario existente
     * TODO: Validar permisos y agregar auditoría
     */
    @PutMapping("/{id}")
    public ResponseEntity<UsuarioDTO> actualizarUsuario(
            @PathVariable Long id, 
            @Valid @RequestBody UsuarioDTO usuarioDTO) {
        log.info("PUT /api/usuarios/{} - Actualizando usuario", id);

        try {
            UsuarioDTO usuarioActualizado = usuarioServicio.actualizarUsuario(id, usuarioDTO);
            return ResponseEntity.ok(usuarioActualizado);
        } catch (RuntimeException e) {
            log.error("Error actualizando usuario {}: {}", id, e.getMessage());
            return ResponseEntity.badRequest().build();
        } catch (Exception e) {
            log.error("Error interno actualizando usuario {}: {}", id, e.getMessage());
            return ResponseEntity.internalServerError().build();
        }
    }

    /**
     * Cambia el estado activo/inactivo de un usuario
     * TODO: Agregar @PreAuthorize("hasRole('ADMIN')")
     */
    @PatchMapping("/{id}/estado")
    public ResponseEntity<Map<String, String>> cambiarEstadoUsuario(
            @PathVariable Long id,
            @RequestBody Map<String, Boolean> request) {
        log.info("PATCH /api/usuarios/{}/estado - Cambiando estado", id);

        try {
            Boolean activo = request.get("activo");
            if (activo == null) {
                return ResponseEntity.badRequest()
                    .body(Map.of("error", "El campo 'activo' es requerido"));
            }

            usuarioServicio.cambiarEstadoUsuario(id, activo);

            String mensaje = activo ? "Usuario activado" : "Usuario desactivado";
            return ResponseEntity.ok(Map.of("mensaje", mensaje));
        } catch (RuntimeException e) {
            log.error("Error cambiando estado usuario {}: {}", id, e.getMessage());
            return ResponseEntity.badRequest()
                .body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * Cambia la contraseña de un usuario
     * TODO: Implementar validaciones de seguridad adicionales
     */
    @PatchMapping("/{id}/contrasena")
    public ResponseEntity<Map<String, String>> cambiarContrasena(
            @PathVariable Long id,
            @RequestBody Map<String, String> request) {
        log.info("PATCH /api/usuarios/{}/contrasena - Cambiando contraseña", id);

        try {
            String contrasenaActual = request.get("contrasenaActual");
            String nuevaContrasena = request.get("nuevaContrasena");

            if (contrasenaActual == null || nuevaContrasena == null) {
                return ResponseEntity.badRequest()
                    .body(Map.of("error", "Contraseña actual y nueva son requeridas"));
            }

            usuarioServicio.cambiarContrasena(id, contrasenaActual, nuevaContrasena);
            return ResponseEntity.ok(Map.of("mensaje", "Contraseña cambiada exitosamente"));
        } catch (RuntimeException e) {
            log.error("Error cambiando contraseña usuario {}: {}", id, e.getMessage());
            return ResponseEntity.badRequest()
                .body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * Busca usuarios por nombre
     * TODO: Implementar búsqueda más avanzada
     */
    @GetMapping("/buscar")
    public ResponseEntity<List<UsuarioDTO>> buscarUsuarios(
            @RequestParam(required = false) String nombre,
            @RequestParam(required = false) Long rolId) {
        log.info("GET /api/usuarios/buscar - nombre: {}, rolId: {}", nombre, rolId);

        try {
            List<UsuarioDTO> usuarios;

            if (nombre != null && !nombre.trim().isEmpty()) {
                usuarios = usuarioServicio.buscarUsuariosPorNombre(nombre.trim());
            } else if (rolId != null) {
                usuarios = usuarioServicio.obtenerUsuariosPorRol(rolId);
            } else {
                usuarios = usuarioServicio.obtenerTodosLosUsuarios();
            }

            return ResponseEntity.ok(usuarios);
        } catch (Exception e) {
            log.error("Error en búsqueda de usuarios: {}", e.getMessage());
            return ResponseEntity.internalServerError().build();
        }
    }

    /**
     * Endpoint de salud para verificar el estado del microservicio
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of(
            "status", "UP",
            "service", "microservicio-usuarios",
            "version", "1.0.0"
        ));
    }

    // TODO: Implementar endpoints adicionales:
    // - POST /api/usuarios/{id}/resetear-contrasena
    // - GET /api/usuarios/estadisticas
    // - GET /api/usuarios/inactivos
    // - POST /api/usuarios/{id}/bloquear
    // - POST /api/usuarios/{id}/desbloquear
    // - GET /api/usuarios/export (exportar a Excel/CSV)
}

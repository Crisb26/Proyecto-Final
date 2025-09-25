package com.innoad.usuarios.servicio;

import com.innoad.usuarios.dto.UsuarioDTO;
import com.innoad.usuarios.modelo.Usuario;
import com.innoad.usuarios.modelo.Rol;
import com.innoad.usuarios.repositorio.UsuarioRepositorio;
import com.innoad.usuarios.repositorio.RolRepositorio;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Servicio de gestión de usuarios del sistema InnoAd
 * 
 * Esta clase contiene toda la lógica de negocio relacionada con usuarios:
 * - Creación, actualización, eliminación de usuarios
 * - Validaciones de negocio
 * - Conversión entre entidades y DTOs
 * - Operaciones de seguridad
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Completar la implementación de todos los métodos
 * 2. Agregar validaciones de negocio específicas
 * 3. Implementar logs de auditoría en operaciones críticas
 * 4. Agregar manejo de excepciones personalizado
 * 5. Implementar cache para consultas frecuentes
 * 6. Crear métodos para reportes y estadísticas
 * 
 * @author Equipo SENA ADSO
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class UsuarioServicio {

    private final UsuarioRepositorio usuarioRepositorio;
    private final RolRepositorio rolRepositorio;
    private final PasswordEncoder passwordEncoder;

    /**
     * Crea un nuevo usuario en el sistema
     * TODO: Implementar validaciones completas y logs de auditoría
     */
    @Transactional
    public UsuarioDTO crearUsuario(UsuarioDTO usuarioDTO) {
        log.info("Creando nuevo usuario: {}", usuarioDTO.getCorreo());

        // TODO: Validar que el correo no existe
        if (usuarioRepositorio.existsByCorreo(usuarioDTO.getCorreo())) {
            throw new RuntimeException("Ya existe un usuario con este correo");
        }

        // TODO: Validar formato de correo y otras reglas de negocio
        validarDatosUsuario(usuarioDTO);

        // TODO: Obtener el rol por ID
        Rol rol = rolRepositorio.findById(usuarioDTO.getIdRol())
            .orElseThrow(() -> new RuntimeException("Rol no encontrado"));

        // Crear nueva entidad usuario
        Usuario usuario = new Usuario();
        usuario.setNombre(usuarioDTO.getNombre());
        usuario.setCorreo(usuarioDTO.getCorreo());
        usuario.setContrasena(passwordEncoder.encode(usuarioDTO.getContrasena()));
        usuario.setRol(rol);
        usuario.setActivo(true);

        // Guardar usuario
        Usuario usuarioGuardado = usuarioRepositorio.save(usuario);

        // TODO: Enviar email de bienvenida
        // TODO: Registrar en auditoría

        log.info("Usuario creado exitosamente: ID {}", usuarioGuardado.getIdUsuario());
        return convertirADTO(usuarioGuardado);
    }

    /**
     * Obtiene todos los usuarios del sistema
     * TODO: Implementar paginación y filtros
     */
    public List<UsuarioDTO> obtenerTodosLosUsuarios() {
        log.info("Obteniendo todos los usuarios");

        // TODO: Considerar implementar paginación para grandes volúmenes
        List<Usuario> usuarios = usuarioRepositorio.findAll();

        return usuarios.stream()
                .map(this::convertirADTO)
                .collect(Collectors.toList());
    }

    /**
     * Obtiene un usuario por su ID
     * TODO: Agregar cache para consultas frecuentes
     */
    public Optional<UsuarioDTO> obtenerUsuarioPorId(Long id) {
        log.debug("Buscando usuario por ID: {}", id);

        return usuarioRepositorio.findById(id)
                .map(this::convertirADTO);
    }

    /**
     * Busca un usuario por correo electrónico
     * Método crítico para autenticación
     */
    public Optional<Usuario> buscarPorCorreo(String correo) {
        log.debug("Buscando usuario por correo: {}", correo);
        return usuarioRepositorio.findByCorreo(correo);
    }

    /**
     * Actualiza la información de un usuario
     * TODO: Implementar validaciones de permisos
     */
    @Transactional
    public UsuarioDTO actualizarUsuario(Long id, UsuarioDTO usuarioDTO) {
        log.info("Actualizando usuario ID: {}", id);

        Usuario usuario = usuarioRepositorio.findById(id)
            .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        // TODO: Validar permisos de actualización
        // TODO: Validar que el nuevo correo no esté en uso por otro usuario

        // Actualizar datos
        usuario.setNombre(usuarioDTO.getNombre());

        if (!usuario.getCorreo().equals(usuarioDTO.getCorreo())) {
            if (usuarioRepositorio.existsByCorreo(usuarioDTO.getCorreo())) {
                throw new RuntimeException("El correo ya está en uso");
            }
            usuario.setCorreo(usuarioDTO.getCorreo());
        }

        // Actualizar rol si cambió
        if (!usuario.getRol().getIdRol().equals(usuarioDTO.getIdRol())) {
            Rol nuevoRol = rolRepositorio.findById(usuarioDTO.getIdRol())
                .orElseThrow(() -> new RuntimeException("Rol no encontrado"));
            usuario.setRol(nuevoRol);
        }

        Usuario usuarioActualizado = usuarioRepositorio.save(usuario);

        // TODO: Registrar cambio en auditoría

        return convertirADTO(usuarioActualizado);
    }

    /**
     * Cambia la contraseña de un usuario
     * TODO: Implementar validaciones de seguridad
     */
    @Transactional
    public void cambiarContrasena(Long id, String contrasenaActual, String nuevaContrasena) {
        log.info("Cambiando contraseña para usuario ID: {}", id);

        Usuario usuario = usuarioRepositorio.findById(id)
            .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        // TODO: Validar contraseña actual
        if (!passwordEncoder.matches(contrasenaActual, usuario.getContrasena())) {
            throw new RuntimeException("Contraseña actual incorrecta");
        }

        // TODO: Validar política de contraseñas
        validarPoliticaContrasena(nuevaContrasena);

        usuario.setContrasena(passwordEncoder.encode(nuevaContrasena));
        usuarioRepositorio.save(usuario);

        // TODO: Invalidar sesiones activas
        // TODO: Enviar notificación de cambio de contraseña

        log.info("Contraseña cambiada exitosamente para usuario ID: {}", id);
    }

    /**
     * Activa o desactiva un usuario
     * TODO: Implementar validaciones de permisos
     */
    @Transactional
    public void cambiarEstadoUsuario(Long id, boolean activo) {
        log.info("Cambiando estado de usuario ID: {} a {}", id, activo);

        Usuario usuario = usuarioRepositorio.findById(id)
            .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        // TODO: Validar que no se desactive al último admin
        if (!activo && usuario.getRol().esAdministrador()) {
            long adminCount = usuarioRepositorio.findUsuariosActivosPorRol(usuario.getRol().getIdRol()).size();
            if (adminCount <= 1) {
                throw new RuntimeException("No se puede desactivar al último administrador");
            }
        }

        usuario.setActivo(activo);
        usuarioRepositorio.save(usuario);

        // TODO: Si se desactiva, invalidar sesiones activas
        // TODO: Registrar cambio en auditoría
    }

    /**
     * Registra un intento de login exitoso
     */
    @Transactional
    public void registrarLoginExitoso(String correo) {
        usuarioRepositorio.findByCorreo(correo).ifPresent(usuario -> {
            usuario.actualizarUltimoAcceso();
            usuario.reiniciarIntentosLogin();
            usuarioRepositorio.save(usuario);
        });
    }

    /**
     * Registra un intento de login fallido
     */
    @Transactional
    public void registrarLoginFallido(String correo) {
        usuarioRepositorio.findByCorreo(correo).ifPresent(usuario -> {
            usuario.incrementarIntentosLogin();
            usuarioRepositorio.save(usuario);

            // TODO: Enviar alerta si el usuario se bloquea
            if (usuario.estaBloqueado()) {
                log.warn("Usuario bloqueado por exceso de intentos: {}", correo);
            }
        });
    }

    /**
     * Obtiene usuarios por rol
     * TODO: Implementar paginación
     */
    public List<UsuarioDTO> obtenerUsuariosPorRol(Long rolId) {
        log.debug("Obteniendo usuarios del rol ID: {}", rolId);

        return usuarioRepositorio.findUsuariosActivosPorRol(rolId).stream()
                .map(this::convertirADTO)
                .collect(Collectors.toList());
    }

    /**
     * Busca usuarios por nombre
     * TODO: Mejorar búsqueda con algoritmos de similitud
     */
    public List<UsuarioDTO> buscarUsuariosPorNombre(String nombre) {
        log.debug("Buscando usuarios por nombre: {}", nombre);

        return usuarioRepositorio.findByNombreContainingIgnoreCase(nombre).stream()
                .map(this::convertirADTO)
                .collect(Collectors.toList());
    }

    // ==========================================
    // MÉTODOS PRIVADOS DE UTILIDAD
    // ==========================================

    /**
     * Convierte entidad Usuario a DTO
     * TODO: Considerar usar MapStruct para mappings complejos
     */
    private UsuarioDTO convertirADTO(Usuario usuario) {
        UsuarioDTO dto = new UsuarioDTO();
        dto.setIdUsuario(usuario.getIdUsuario());
        dto.setNombre(usuario.getNombre());
        dto.setCorreo(usuario.getCorreo());
        dto.setIdRol(usuario.getRol().getIdRol());
        dto.setNombreRol(usuario.getRol().getNombre());
        dto.setActivo(usuario.getActivo());
        dto.setUltimoAcceso(usuario.getUltimoAcceso());
        dto.setCreatedAt(usuario.getCreatedAt());
        // No incluir contraseña en el DTO
        return dto;
    }

    /**
     * Valida los datos básicos de un usuario
     * TODO: Implementar validaciones más robustas
     */
    private void validarDatosUsuario(UsuarioDTO usuarioDTO) {
        // TODO: Validar formato de correo colombiano
        // TODO: Validar política de nombres
        // TODO: Validar que el rol existe y está activo

        if (usuarioDTO.getContrasena() != null) {
            validarPoliticaContrasena(usuarioDTO.getContrasena());
        }
    }

    /**
     * Valida que la contraseña cumpla con la política de seguridad
     * TODO: Implementar política configurable
     */
    private void validarPoliticaContrasena(String contrasena) {
        if (contrasena == null || contrasena.length() < 8) {
            throw new RuntimeException("La contraseña debe tener al menos 8 caracteres");
        }

        // TODO: Validar mayúsculas, minúsculas, números y símbolos
        // TODO: Validar que no sea una contraseña común
        // TODO: Validar que no contenga información personal
    }
}

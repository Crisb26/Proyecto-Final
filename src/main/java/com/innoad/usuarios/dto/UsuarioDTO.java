package com.innoad.usuarios.dto;

import jakarta.validation.constraints.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;

/**
 * DTO (Data Transfer Object) para transferencia de datos de usuarios
 * 
 * Esta clase define la estructura de datos que se intercambia entre
 * el frontend y backend, sin exponer detalles internos de la entidad.
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Agregar validaciones específicas para campos colombianos
 * 2. Implementar grupos de validación para diferentes operaciones
 * 3. Agregar documentación de API con anotaciones Swagger
 * 4. Crear DTOs específicos para diferentes casos de uso
 * 5. Implementar serialización/deserialización personalizada
 * 
 * @author Equipo SENA ADSO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UsuarioDTO {

    private Long idUsuario;

    @NotBlank(message = "El nombre es obligatorio")
    @Size(min = 2, max = 50, message = "El nombre debe tener entre 2 y 50 caracteres")
    @Pattern(regexp = "^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]+$", 
             message = "El nombre solo puede contener letras y espacios")
    private String nombre;

    @NotBlank(message = "El correo es obligatorio")
    @Email(message = "Debe ser un correo electrónico válido")
    @Size(max = 100, message = "El correo no puede exceder 100 caracteres")
    private String correo;

    // Solo se incluye en creación/actualización, nunca en respuestas
    @Size(min = 8, message = "La contraseña debe tener al menos 8 caracteres")
    private String contrasena;

    @NotNull(message = "El rol es obligatorio")
    @Positive(message = "El ID del rol debe ser positivo")
    private Long idRol;

    // Campo calculado - nombre del rol para mostrar en frontend
    private String nombreRol;

    private Boolean activo;

    private LocalDateTime ultimoAcceso;

    private LocalDateTime createdAt;

    // Campos adicionales para el frontend
    private Integer intentosLogin;
    private Boolean bloqueado;

    /**
     * Constructor para creación de usuario (sin ID)
     * TODO: Usar para requests de creación
     */
    public UsuarioDTO(String nombre, String correo, String contrasena, Long idRol) {
        this.nombre = nombre;
        this.correo = correo;
        this.contrasena = contrasena;
        this.idRol = idRol;
        this.activo = true;
    }

    /**
     * Verifica si el usuario está activo
     * TODO: Usar en validaciones del frontend
     */
    public boolean estaActivo() {
        return Boolean.TRUE.equals(activo);
    }

    /**
     * Obtiene el nombre completo del usuario con formato
     * TODO: Personalizar según necesidades de la aplicación
     */
    public String getNombreCompleto() {
        return nombre != null ? nombre.trim() : "";
    }

    /**
     * Verifica si el usuario es administrador
     * TODO: Usar para mostrar/ocultar opciones en frontend
     */
    public boolean esAdministrador() {
        return "ADMIN".equals(nombreRol) || "ADMINISTRADOR".equals(nombreRol);
    }

    // TODO: Agregar métodos de utilidad adicionales:
    // - getTiempoSinAcceso()
    // - getEstadoDescripcion()
    // - formatearFechaUltimoAcceso()
}

/**
 * DTO específico para actualización de usuario (sin contraseña)
 * TODO: Implementar para operaciones de actualización
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
class ActualizarUsuarioDTO {

    @NotBlank(message = "El nombre es obligatorio")
    @Size(min = 2, max = 50, message = "El nombre debe tener entre 2 y 50 caracteres")
    private String nombre;

    @NotBlank(message = "El correo es obligatorio")
    @Email(message = "Debe ser un correo electrónico válido")
    private String correo;

    @NotNull(message = "El rol es obligatorio")
    private Long idRol;
}

/**
 * DTO para cambio de contraseña
 * TODO: Implementar para endpoint de cambio de contraseña
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
class CambiarContrasenaDTO {

    @NotBlank(message = "La contraseña actual es obligatoria")
    private String contrasenaActual;

    @NotBlank(message = "La nueva contraseña es obligatoria")
    @Size(min = 8, message = "La nueva contraseña debe tener al menos 8 caracteres")
    private String nuevaContrasena;

    @NotBlank(message = "La confirmación de contraseña es obligatoria")
    private String confirmarContrasena;

    /**
     * Valida que las contraseñas coincidan
     */
    @AssertTrue(message = "Las contraseñas no coinciden")
    public boolean isContrasenaValida() {
        return nuevaContrasena != null && nuevaContrasena.equals(confirmarContrasena);
    }
}

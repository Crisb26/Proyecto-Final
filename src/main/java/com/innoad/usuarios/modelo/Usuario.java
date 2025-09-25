package com.innoad.usuarios.modelo;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonIgnore;
import java.time.LocalDateTime;

/**
 * Entidad Usuario para el sistema InnoAd
 * 
 * Esta clase representa un usuario del sistema y contiene toda la información
 * necesaria para la autenticación, autorización y gestión de usuarios.
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Implementar validaciones personalizadas (ej: formato de email colombiano)
 * 2. Agregar campos adicionales según necesidades (teléfono, foto, etc.)
 * 3. Implementar métodos de utilidad (isAccountNonExpired, etc.)
 * 4. Configurar relaciones con otras entidades si es necesario
 * 5. Agregar anotaciones de auditoría
 * 
 * @author Equipo SENA ADSO
 */
@Entity
@Table(name = "usuarios")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Usuario {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_usuario")
    private Long idUsuario;

    @NotBlank(message = "El nombre es obligatorio")
    @Size(min = 2, max = 50, message = "El nombre debe tener entre 2 y 50 caracteres")
    @Column(nullable = false, length = 50)
    private String nombre;

    @NotBlank(message = "El correo es obligatorio")
    @Email(message = "Debe ser un correo válido")
    @Size(max = 100, message = "El correo no puede exceder 100 caracteres")
    @Column(nullable = false, unique = true, length = 100)
    private String correo;

    @JsonIgnore
    @NotBlank(message = "La contraseña es obligatoria")
    @Size(min = 8, message = "La contraseña debe tener al menos 8 caracteres")
    @Column(nullable = false)
    private String contrasena;

    @NotNull(message = "El rol es obligatorio")
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "id_rol", nullable = false)
    private Rol rol;

    @Column(nullable = false)
    private Boolean activo = true;

    @Column(name = "ultimo_acceso")
    private LocalDateTime ultimoAcceso;

    @Column(name = "intentos_login")
    private Integer intentosLogin = 0;

    @Column(name = "bloqueado_hasta")
    private LocalDateTime bloqueadoHasta;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(name = "updated_at")
    private LocalDateTime updatedAt = LocalDateTime.now();

    // Métodos de utilidad

    /**
     * Verifica si el usuario está bloqueado por exceso de intentos de login
     * TODO: Implementar lógica de bloqueo temporal
     */
    public boolean estaBloqueado() {
        if (bloqueadoHasta == null) {
            return false;
        }
        return LocalDateTime.now().isBefore(bloqueadoHasta);
    }

    /**
     * Reinicia el contador de intentos de login fallidos
     * TODO: Llamar este método cuando el login sea exitoso
     */
    public void reiniciarIntentosLogin() {
        this.intentosLogin = 0;
        this.bloqueadoHasta = null;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Incrementa el contador de intentos de login fallidos
     * TODO: Implementar lógica de bloqueo después de X intentos
     */
    public void incrementarIntentosLogin() {
        this.intentosLogin++;
        this.updatedAt = LocalDateTime.now();

        // TODO: Implementar bloqueo temporal después de 5 intentos
        if (this.intentosLogin >= 5) {
            this.bloqueadoHasta = LocalDateTime.now().plusMinutes(15);
        }
    }

    /**
     * Actualiza la fecha del último acceso
     * TODO: Llamar este método en cada login exitoso
     */
    public void actualizarUltimoAcceso() {
        this.ultimoAcceso = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}

package com.innoad.usuarios.modelo;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

/**
 * Entidad para tokens de recuperación de contraseña
 * 
 * Esta clase maneja los tokens únicos y seguros para la recuperación
 * de contraseñas olvidadas por parte de los usuarios.
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Implementar generación segura de tokens
 * 2. Configurar tiempo de expiración personalizable
 * 3. Agregar sistema de limpieza de tokens expirados
 * 4. Implementar validaciones de uso único
 * 5. Integrar con servicio de envío de emails
 * 
 * @author Equipo SENA ADSO
 */
@Entity
@Table(name = "password_reset_tokens")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PasswordResetToken {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_token")
    private Long idToken;

    @Column(nullable = false, unique = true)
    private String token;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "usuario_id", nullable = false)
    private Usuario usuario;

    @Column(name = "expiry_date", nullable = false)
    private LocalDateTime expiryDate;

    @Column(nullable = false)
    private Boolean usado = false;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    /**
     * Verifica si el token ha expirado
     * TODO: Considerar diferentes tiempos de expiración según tipo de token
     */
    public boolean haExpirado() {
        return LocalDateTime.now().isAfter(expiryDate);
    }

    /**
     * Verifica si el token es válido para usar
     * TODO: Agregar validaciones adicionales de seguridad
     */
    public boolean esValido() {
        return !usado && !haExpirado();
    }

    /**
     * Marca el token como usado
     * TODO: Registrar información de uso (IP, fecha, etc.)
     */
    public void marcarComoUsado() {
        this.usado = true;
    }

    /**
     * Constructor para crear nuevo token
     * TODO: Mejorar generación de token con más entropía
     */
    public PasswordResetToken(String token, Usuario usuario, int horasExpiracion) {
        this.token = token;
        this.usuario = usuario;
        this.expiryDate = LocalDateTime.now().plusHours(horasExpiracion);
        this.usado = false;
        this.createdAt = LocalDateTime.now();
    }
}

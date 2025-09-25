package com.innoad.dispositivos.modelo;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

/**
 * Esta clase almacena toda la informacion necesaria para gestionar pantallas
 * remotas, incluyendo configuracion, estado de conexion y metricas.
 * 
 * TAREAS PARA EL QUE TOME ESTA PARTE:
 * 1. Implementar validaciones personalizadas para direcciones MAC
 * 2. Agregar campos para configuración avanzada (proxy, VPN, etc.)
 * 3. Implementar relaciones con contenido programado
 * 4. Crear metodos para calculo de estadisticas
 * 5. Agregar campos para geolocalizacion de dispositivos
 * 6. Implementar sistema de alertas por estado crítico
 */
@Entity
@Table(name = "dispositivos_raspberry")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class DispositivoRaspberry {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_dispositivo")
    private Long idDispositivo;

    @NotBlank(message = "El nombre del dispositivo es obligatorio")
    @Size(min = 3, max = 100, message = "El nombre debe tener entre 3 y 100 caracteres")
    @Column(nullable = false, length = 100)
    private String nombre;

    @NotBlank(message = "La dirección MAC es obligatoria")
    @Pattern(regexp = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", 
             message = "Formato de MAC address inválido")
    @Column(name = "mac_address", nullable = false, unique = true, length = 17)
    private String macAddress;

            @Pattern(regexp = "^(?:[0-9]{1,3}\\\\.){3}[0-9]{1,3}$|^$", 
                     message = "Formato de IP address inválido")
    @Column(name = "ip_address", length = 45)
    private String ipAddress;

    @NotBlank(message = "La ubicación es obligatoria")
    @Size(max = 200, message = "La ubicación no puede exceder 200 caracteres")
    @Column(nullable = false, length = 200)
    private String ubicacion;

    @Size(max = 500, message = "La descripción no puede exceder 500 caracteres")
    @Column(length = 500)
    private String descripcion;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private EstadoDispositivo estado = EstadoDispositivo.DESCONECTADO;

    @Column(name = "ultimo_heartbeat")
    private LocalDateTime ultimoHeartbeat;

    @Column(name = "fecha_registro", nullable = false)
    private LocalDateTime fechaRegistro = LocalDateTime.now();

    @Size(max = 50)
    @Column(name = "version_software", length = 50)
    private String versionSoftware;

    @Size(max = 20)
    @Column(name = "resolucion_pantalla", length = 20)
    private String resolucionPantalla;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private OrientacionPantalla orientacion = OrientacionPantalla.HORIZONTAL;

    @Min(value = 0, message = "El volumen debe ser entre 0 y 100")
    @Max(value = 100, message = "El volumen debe ser entre 0 y 100")
    @Column(name = "volumen_audio")
    private Integer volumenAudio = 50;

    @Min(value = 0, message = "El brillo debe ser entre 0 y 100")
    @Max(value = 100, message = "El brillo debe ser entre 0 y 100")
    @Column(name = "brillo_pantalla")
    private Integer brilloPantalla = 80;

    @Column(nullable = false)
    private Boolean activo = true;

    @NotNull(message = "El propietario es obligatorio")
    @Column(name = "propietario_id", nullable = false)
    private Long propietarioId;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(name = "updated_at")
    private LocalDateTime updatedAt = LocalDateTime.now();

    // Metodos de utilidad para el negocio

    /**
     * Verifica si el dispositivo esta online basado en el ultimo heartbeat
     */
    public boolean estaOnline() {
        if (ultimoHeartbeat == null) return false;
        return estado == EstadoDispositivo.CONECTADO && 
               ultimoHeartbeat.isAfter(LocalDateTime.now().minusMinutes(2));
    }

    /**
     * Actualiza el heartbeat y estado cuando se recibe señal del dispositivo
     */
    public void actualizarHeartbeat() {
        this.ultimoHeartbeat = LocalDateTime.now();
        if (this.estado == EstadoDispositivo.DESCONECTADO) {
            this.estado = EstadoDispositivo.CONECTADO;
        }
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Marca el dispositivo como desconectado
     */
    public void marcarDesconectado() {
        this.estado = EstadoDispositivo.DESCONECTADO;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Cambia el estado a reproduciendo contenido
     */
    public void marcarReproduciendo() {
        this.estado = EstadoDispositivo.REPRODUCIENDO;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Obtiene el tiempo transcurrido desde el ultimo heartbeat
     */
    public long getMinutosSinHeartbeat() {
        if (ultimoHeartbeat == null) return Long.MAX_VALUE;
        return java.time.Duration.between(ultimoHeartbeat, LocalDateTime.now()).toMinutes();
    }

    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}


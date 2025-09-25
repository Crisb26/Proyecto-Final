package com.innoad.dispositivos.repositorio;

import com.innoad.dispositivos.modelo.DispositivoRaspberry;
import com.innoad.dispositivos.modelo.EstadoDispositivo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * Repositorio para operaciones de base de datos con dispositivos Raspberry Pi
 * en esta se definiria consultas especializadas para gestion de dispositivos,
 * incluyendo busquedas por ubicacion, estado, y metricas de conectividad.
 * 
 * TAREAS PARA EL QUE SE ARRIESGUE A TOMAR ESTA PARTE:
 * 1. Implementar consultas geograficas para dispositivos cercanos
 * 2. Crear consultas para reportes de uso y estadisticas
 * 3. Agregar metodos para detectar dispositivos inactivos
 * 4. Implementar busquedas por metricas de rendimiento
 * 5. Crear consultas para alertas automaticas
 */
@Repository
public interface DispositivoRepositorio extends JpaRepository<DispositivoRaspberry, Long> {

    /**
     * Busca dispositivo por dirección MAC (unico identificador)
     * Metodo critico para identificacion en conexiones WebSocket
     */
    Optional<DispositivoRaspberry> findByMacAddress(String macAddress);

    /**
     * Busca dispositivos activos por propietario
     */
    List<DispositivoRaspberry> findByPropietarioIdAndActivoTrue(Long propietarioId);

    /**
     * Busca dispositivos por ubicación (búsqueda parcial)
     */
    List<DispositivoRaspberry> findByUbicacionContainingIgnoreCaseAndActivoTrue(String ubicacion);

    /**
     * Busca dispositivos por estado específico
     */
    List<DispositivoRaspberry> findByEstadoAndActivoTrue(EstadoDispositivo estado);

    /**
     * Busca dispositivos que no han enviado heartbeat recientemente
     */
    @Query("SELECT d FROM DispositivoRaspberry d WHERE d.activo = true AND " +
           "(d.ultimoHeartbeat IS NULL OR d.ultimoHeartbeat < :fechaLimite)")
    List<DispositivoRaspberry> findDispositivosSinHeartbeat(@Param("fechaLimite") LocalDateTime fechaLimite);

    /**
     * Busca dispositivos online (con heartbeat reciente)
     */
    @Query("SELECT d FROM DispositivoRaspberry d WHERE d.activo = true AND " +
           "d.estado = 'CONECTADO' AND d.ultimoHeartbeat > :fechaLimite")
    List<DispositivoRaspberry> findDispositivosOnline(@Param("fechaLimite") LocalDateTime fechaLimite);

    /**
     * Cuenta dispositivos por estado
     */
    long countByEstadoAndActivoTrue(EstadoDispositivo estado);

    /**
     * Busca dispositivos registrados en un período
     */
    @Query("SELECT d FROM DispositivoRaspberry d WHERE d.fechaRegistro BETWEEN :fechaInicio AND :fechaFin")
    List<DispositivoRaspberry> findDispositivosRegistradosEntreFechas(
        @Param("fechaInicio") LocalDateTime fechaInicio,
        @Param("fechaFin") LocalDateTime fechaFin
    );

    /**
     * Busca dispositivos por múltiples criterios
     */
    @Query("SELECT d FROM DispositivoRaspberry d WHERE " +
           "(:nombre IS NULL OR LOWER(d.nombre) LIKE LOWER(CONCAT('%', :nombre, '%'))) AND " +
           "(:ubicacion IS NULL OR LOWER(d.ubicacion) LIKE LOWER(CONCAT('%', :ubicacion, '%'))) AND " +
           "(:estado IS NULL OR d.estado = :estado) AND " +
           "(:propietarioId IS NULL OR d.propietarioId = :propietarioId) AND " +
           "d.activo = true")
    List<DispositivoRaspberry> findDispositivosPorCriterios(
        @Param("nombre") String nombre,
        @Param("ubicacion") String ubicacion,
        @Param("estado") EstadoDispositivo estado,
        @Param("propietarioId") Long propietarioId
    );

    /**
     * Verifica si existe dispositivo con MAC address
     */
    boolean existsByMacAddress(String macAddress);

    /**
     * Busca dispositivos con versión de software específica
     */
    List<DispositivoRaspberry> findByVersionSoftwareAndActivoTrue(String version);

    /**
     * Busca dispositivos que requieren actualización
     */
    @Query("SELECT d FROM DispositivoRaspberry d WHERE d.activo = true AND " +
           "(d.versionSoftware IS NULL OR d.versionSoftware != :versionActual)")
    List<DispositivoRaspberry> findDispositivosParaActualizar(@Param("versionActual") String versionActual);

    /**
     * Obtiene estadísticas básicas de dispositivos
     */
    @Query("SELECT " +
           "COUNT(*) as total, " +
           "SUM(CASE WHEN d.estado = 'CONECTADO' THEN 1 ELSE 0 END) as conectados, " +
           "SUM(CASE WHEN d.estado = 'DESCONECTADO' THEN 1 ELSE 0 END) as desconectados, " +
           "SUM(CASE WHEN d.estado = 'ERROR' THEN 1 ELSE 0 END) as conError " +
           "FROM DispositivoRaspberry d WHERE d.activo = true")
    Object[] getEstadisticasDispositivos();

    
       // Metodos adicionales pueden incluir:
    // - findDispositivosCercanos(latitud, longitud, radio)
    // - findDispositivosConMayorUso()
    // - findDispositivosPorRendimiento()
    // - etc.
}

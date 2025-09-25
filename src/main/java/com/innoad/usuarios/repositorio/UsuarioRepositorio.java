package com.innoad.usuarios.repositorio;

import com.innoad.usuarios.modelo.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * Repositorio para operaciones de base de datos con usuarios
 * 
 * Esta interfaz define métodos personalizados para consultas específicas
 * de usuarios, incluyendo búsquedas, filtros y operaciones especializadas.
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Implementar consultas personalizadas con @Query
 * 2. Agregar métodos de búsqueda por diferentes criterios
 * 3. Implementar paginación en las consultas complejas
 * 4. Crear índices de base de datos para optimizar consultas
 * 5. Agregar consultas para reportes y estadísticas
 * 
 * @author Equipo SENA ADSO
 */
@Repository
public interface UsuarioRepositorio extends JpaRepository<Usuario, Long> {

    /**
     * Busca un usuario por su correo electrónico
     * Método esencial para la autenticación
     */
    Optional<Usuario> findByCorreo(String correo);

    /**
     * Busca usuarios activos por correo
     * TODO: Usar para validar usuarios en login
     */
    Optional<Usuario> findByCorreoAndActivoTrue(String correo);

    /**
     * Busca usuarios por nombre (búsqueda parcial)
     * TODO: Implementar para funcionalidad de búsqueda en el frontend
     */
    List<Usuario> findByNombreContainingIgnoreCase(String nombre);

    /**
     * Busca usuarios activos por rol
     * TODO: Usar para listados filtrados por tipo de usuario
     */
    @Query("SELECT u FROM Usuario u WHERE u.rol.idRol = :rolId AND u.activo = true")
    List<Usuario> findUsuariosActivosPorRol(@Param("rolId") Long rolId);

    /**
     * Busca usuarios que no han accedido recientemente
     * TODO: Implementar para reportes de usuarios inactivos
     */
    @Query("SELECT u FROM Usuario u WHERE u.ultimoAcceso < :fecha OR u.ultimoAcceso IS NULL")
    List<Usuario> findUsuariosInactivosDesdeFecha(@Param("fecha") LocalDateTime fecha);

    /**
     * Cuenta usuarios por estado activo
     * TODO: Usar para dashboard con estadísticas
     */
    long countByActivoTrue();
    long countByActivoFalse();

    /**
     * Busca usuarios con intentos de login fallidos
     * TODO: Implementar para monitoreo de seguridad
     */
    @Query("SELECT u FROM Usuario u WHERE u.intentosLogin >= :intentos")
    List<Usuario> findUsuariosConIntentosLogin(@Param("intentos") Integer intentos);

    /**
     * Busca usuarios bloqueados
     * TODO: Usar para panel de administración
     */
    @Query("SELECT u FROM Usuario u WHERE u.bloqueadoHasta > :ahora")
    List<Usuario> findUsuariosBloqueados(@Param("ahora") LocalDateTime ahora);

    /**
     * Verifica si existe un usuario con el correo dado
     * TODO: Usar para validación en registro de nuevos usuarios
     */
    boolean existsByCorreo(String correo);

    /**
     * Busca usuarios creados en un rango de fechas
     * TODO: Implementar para reportes periódicos
     */
    @Query("SELECT u FROM Usuario u WHERE u.createdAt BETWEEN :fechaInicio AND :fechaFin")
    List<Usuario> findUsuariosCreadosEntreFechas(
        @Param("fechaInicio") LocalDateTime fechaInicio,
        @Param("fechaFin") LocalDateTime fechaFin
    );

    /**
     * Busca usuarios por múltiples criterios
     * TODO: Implementar para búsqueda avanzada
     */
    @Query("SELECT u FROM Usuario u WHERE " +
           "(:nombre IS NULL OR LOWER(u.nombre) LIKE LOWER(CONCAT('%', :nombre, '%'))) AND " +
           "(:correo IS NULL OR LOWER(u.correo) LIKE LOWER(CONCAT('%', :correo, '%'))) AND " +
           "(:rolId IS NULL OR u.rol.idRol = :rolId) AND " +
           "(:activo IS NULL OR u.activo = :activo)")
    List<Usuario> findUsuariosPorCriterios(
        @Param("nombre") String nombre,
        @Param("correo") String correo,
        @Param("rolId") Long rolId,
        @Param("activo") Boolean activo
    );

    // TODO: Agregar más consultas según necesidades del negocio:
    // - findTopUsuariosPorActividad()
    // - findUsuariosPorDepartamento() (si se agrega campo)
    // - findUsuariosConPermisoEspecifico()
    // - etc.
}

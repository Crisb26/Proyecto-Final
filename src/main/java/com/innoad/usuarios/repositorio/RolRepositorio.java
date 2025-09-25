package com.innoad.usuarios.repositorio;

import com.innoad.usuarios.modelo.Rol;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Repositorio para la entidad Rol
 */
@Repository
public interface RolRepositorio extends JpaRepository<Rol, Long> {
    // En el futuro agregar queries específicas si es necesario
}

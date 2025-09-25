package com.innoad.usuarios.modelo;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Entidad Rol para el sistema de permisos InnoAd
 * 
 * Esta clase define los diferentes roles que pueden tener los usuarios
 * en el sistema y sus respectivos permisos.
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Definir enumeración de permisos específicos por módulo
 * 2. Implementar sistema de herencia de permisos
 * 3. Crear roles predefinidos (ADMIN, MANAGER, EDITOR, VIEWER)
 * 4. Implementar validaciones de permisos en los controladores
 * 5. Agregar sistema de permisos granulares por funcionalidad
 * 
 * @author Equipo SENA ADSO
 */
@Entity
@Table(name = "roles")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Rol {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_rol")
    private Long idRol;

    @NotBlank(message = "El nombre del rol es obligatorio")
    @Size(min = 3, max = 50, message = "El nombre debe tener entre 3 y 50 caracteres")
    @Column(nullable = false, unique = true, length = 50)
    private String nombre;

    @Size(max = 255, message = "La descripción no puede exceder 255 caracteres")
    private String descripcion;

    @Column(nullable = false)
    private Boolean activo = true;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(name = "updated_at")
    private LocalDateTime updatedAt = LocalDateTime.now();

    @OneToMany(mappedBy = "rol", fetch = FetchType.LAZY)
    private List<Usuario> usuarios;

    // TODO: Agregar relación con tabla de permisos específicos
    // @ManyToMany
    // @JoinTable(
    //     name = "roles_permisos",
    //     joinColumns = @JoinColumn(name = "id_rol"),
    //     inverseJoinColumns = @JoinColumn(name = "id_permiso")
    // )
    // private List<Permiso> permisos;

    /**
     * Verifica si el rol es de administrador
     * TODO: Implementar lógica más robusta de verificación
     */
    public boolean esAdministrador() {
        return "ADMIN".equals(this.nombre) || "ADMINISTRADOR".equals(this.nombre);
    }

    /**
     * Verifica si el rol puede gestionar usuarios
     * TODO: Implementar verificación basada en permisos granulares
     */
    public boolean puedeGestionarUsuarios() {
        return esAdministrador() || "MANAGER".equals(this.nombre);
    }

    /**
     * Verifica si el rol puede crear campañas
     * TODO: Implementar sistema de permisos por módulo
     */
    public boolean puedeCrearCampanas() {
        return !("VIEWER".equals(this.nombre));
    }

    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}

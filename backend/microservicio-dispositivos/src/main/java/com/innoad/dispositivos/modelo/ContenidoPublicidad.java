package com.innoad.dispositivos.modelo;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

/**
 * esta clase la cree para almacenar el contenido multimedia que se envoiara a las pantallas
 * por ende representa archivos de imagen, video, paginas web o el contenido HTML
 * que se puede reproducir en los dispositivos Raspberry Pi, quienes son los encargados de dar la imagen en la pantalla.
 * 
 * TAREAS PARA QUIEN SE ENCARGUE DE ESTA PARTE:
 * 1. Implementar validaciones de tipo de archivo y tamaño
 * 2. Crear sistema de almacenamiento en cloud (AWS S3, o el que le parezca mas facil.)
 * 3. Implementar compresion automatica de archivos grandes y por ende pesados
 * 4. Agregar sistema de versionado de contenido
 * 5. Crear preview automatico para contenido web
 * 6. Implementar un sistema de checksums para verificar integridad
 */

@Entity
@Table(name = "contenido_publicidad")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ContenidoPublicidad {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_contenido")
    private Long idContenido;

    @NotBlank(message = "El nombre del contenido es obligatorio")
    @Size(min = 2, max = 200, message = "El nombre debe tener entre 2 y 200 caracteres")
    @Column(nullable = false, length = 200)
    private String nombre;

    @Size(max = 1000, message = "La descripción no puede exceder 1000 caracteres")
    @Column(length = 1000)
    private String descripcion;

    @NotNull(message = "El tipo de contenido es obligatorio")
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TipoContenido tipo;

    @Size(max = 500, message = "La URL no puede exceder 500 caracteres")
    @Column(name = "url_archivo", length = 500)
    private String urlArchivo;

    @Lob
    @Column(name = "contenido_html", columnDefinition = "TEXT")
    private String contenidoHtml;

    @Min(value = 1, message = "La duración debe ser al menos 1 segundo")
    @Max(value = 86400, message = "La duración no puede exceder 24 horas")
    @Column(name = "duracion_segundos")
    private Integer duracionSegundos = 30;

    @Min(value = 0, message = "El tamaño no puede ser negativo")
    @Column(name = "tamano_archivo")
    private Long tamanoArchivo;

    @Size(max = 64)
    @Column(length = 64)
    private String checksum;

    @Size(max = 20)
    @Column(length = 20)
    private String resolucion;

    @Column(nullable = false)
    private Boolean activo = true;

    @NotNull(message = "El creador del contenido es obligatorio")
    @Column(name = "creado_por", nullable = false)
    private Long creadoPor;

    @Column(name = "fecha_creacion", nullable = false)
    private LocalDateTime fechaCreacion = LocalDateTime.now();

    @Column(name = "fecha_modificacion")
    private LocalDateTime fechaModificacion = LocalDateTime.now();

    // Metodos de utilidad

    /**
     * Verifica si el contenido es multimedia (imagen o video)
     */
    public boolean esMultimedia() {
        return tipo == TipoContenido.IMAGEN || tipo == TipoContenido.VIDEO;
    }

    /**
     * Verifica si el contenido es web (HTML o URL)
     */
    public boolean esContenidoWeb() {
        return tipo == TipoContenido.WEB || tipo == TipoContenido.HTML;
    }

    /**
     * Obtiene la extension del archivo basada en el tipo
     */
    public String getExtensionArchivo() {
        switch (tipo) {
            case IMAGEN: return "jpg";
            case VIDEO: return "mp4";
            case HTML: return "html";
            case WEB: return "url";
            default: return "bin";
        }
    }

    /**
     * Calcula el tamaño en MB para mostrar en UI
     */
    public double getTamanoEnMB() {
        if (tamanoArchivo == null) return 0;
        return tamanoArchivo / (1024.0 * 1024.0);
    }

    /**
     * Verifica si el contenido necesita descarga (no es HTML y tiene URL)
     */
    public boolean requiereDescarga() {
        return urlArchivo != null && !urlArchivo.isEmpty() && tipo != TipoContenido.HTML;
    }

    @PreUpdate
    public void preUpdate() {
        this.fechaModificacion = LocalDateTime.now();
    }
}

/**
 * Enumeracion para tipos de contenido soportados
 */
enum TipoContenido {
    IMAGEN,    // JPG, PNG, GIF
    VIDEO,     // MP4, AVI, MOV
    WEB,       // URL externa
    HTML,      // Contenido HTML personalizado
    TEXTO      // Texto simple para pantallas basicas
}

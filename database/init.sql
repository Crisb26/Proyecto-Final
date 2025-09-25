-- InnoAd - Base de Datos Completa
-- Creación de base de datos y tablas para el sistema InnoAd
-- Incluye módulos: usuarios, campañas, reuniones, tareas, auditoría y dispositivos Raspberry Pi

CREATE DATABASE IF NOT EXISTS innoad 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

USE innoad;

-- ================================
-- MÓDULO DE USUARIOS Y ROLES
-- ================================

-- Tabla de roles del sistema
CREATE TABLE IF NOT EXISTS roles (
  id_rol INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  descripcion VARCHAR(255),
  activo BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabla de usuarios del sistema
CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  correo VARCHAR(100) NOT NULL UNIQUE,
  contrasena VARCHAR(255) NOT NULL,
  id_rol INT UNSIGNED NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  ultimo_acceso DATETIME NULL,
  intentos_login INT DEFAULT 0,
  bloqueado_hasta DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
) ENGINE=InnoDB;

-- Tokens de recuperación de contraseña
CREATE TABLE IF NOT EXISTS password_reset_tokens (
  id_token INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  token VARCHAR(255) NOT NULL UNIQUE,
  usuario_id INT UNSIGNED NOT NULL,
  expiry_date DATETIME NOT NULL,
  usado BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

-- ================================
-- MÓDULO DE CAMPAÑAS
-- ================================

-- Tabla de campañas publicitarias
CREATE TABLE IF NOT EXISTS campanas (
  id_campana INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  id_usuario INT UNSIGNED NOT NULL,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NOT NULL,
  estado ENUM('borrador','activa','pausada','finalizada') DEFAULT 'borrador',
  presupuesto DECIMAL(10,2) DEFAULT 0,
  plataforma VARCHAR(50) DEFAULT 'Google Ads',
  tipo_objetivo VARCHAR(50) DEFAULT 'conversiones',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

-- Tabla de anuncios dentro de campañas
CREATE TABLE IF NOT EXISTS anuncios (
  id_anuncio INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  contenido TEXT NOT NULL,
  id_campana INT UNSIGNED NOT NULL,
  tipo_contenido ENUM('texto','imagen','video','html') DEFAULT 'texto',
  fecha_publicacion DATETIME,
  estado ENUM('programado','publicado','pausado') DEFAULT 'programado',
  impresiones INT DEFAULT 0,
  clics INT DEFAULT 0,
  costo_total DECIMAL(10,2) DEFAULT 0,
  cpc_maximo DECIMAL(6,2) DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (id_campana) REFERENCES campanas(id_campana)
) ENGINE=InnoDB;

-- ================================
-- MÓDULO DE REUNIONES
-- ================================

-- Tabla de reuniones
CREATE TABLE IF NOT EXISTS reuniones (
  id_reunion INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  fecha DATE NOT NULL,
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL,
  motivo VARCHAR(250) NOT NULL,
  descripcion TEXT,
  ubicacion VARCHAR(200),
  estado ENUM('programada','en_curso','finalizada','cancelada') DEFAULT 'programada',
  organizador_id INT UNSIGNED NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (organizador_id) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

-- Tabla de relación reuniones-usuarios (asistencia)
CREATE TABLE IF NOT EXISTS reuniones_usuarios (
  id_reunion INT UNSIGNED NOT NULL,
  id_usuario INT UNSIGNED NOT NULL,
  PRIMARY KEY (id_reunion, id_usuario),
  asistencia ENUM('pendiente','confirmada','rechazada','ausente') DEFAULT 'pendiente',
  comentarios TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_reunion) REFERENCES reuniones(id_reunion),
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

-- ================================
-- MÓDULO DE TAREAS
-- ================================

-- Tabla de tareas del sistema Kanban
CREATE TABLE IF NOT EXISTS tareas (
  id_tarea INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL,
  descripcion TEXT NOT NULL,
  responsable INT UNSIGNED NOT NULL,
  asignado_por INT UNSIGNED NOT NULL,
  prioridad ENUM('baja','media','alta','critica') DEFAULT 'media',
  estado ENUM('pendiente','en_proceso','en_revision','finalizada','cancelada') DEFAULT 'pendiente',
  fecha_entrega DATE,
  horas_estimadas DECIMAL(5,2),
  horas_trabajadas DECIMAL(5,2) DEFAULT 0,
  porcentaje_completado INT DEFAULT 0,
  categoria VARCHAR(50),
  etiquetas JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (responsable) REFERENCES usuarios(id_usuario),
  FOREIGN KEY (asignado_por) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

-- ================================
-- MÓDULO DE AUDITORÍA
-- ================================

-- Tabla de auditoría del sistema
CREATE TABLE IF NOT EXISTS auditoria (
  id_log INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tabla_afectada VARCHAR(50) NOT NULL,
  accion VARCHAR(50) NOT NULL,
  registro_id INT UNSIGNED,
  detalles JSON,
  usuario_id INT UNSIGNED,
  ip_address VARCHAR(45),
  user_agent TEXT,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

-- ================================
-- MÓDULO RASPBERRY PI Y DISPOSITIVOS
-- ================================

-- Tabla de dispositivos Raspberry Pi
CREATE TABLE IF NOT EXISTS dispositivos_raspberry (
  id_dispositivo INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  mac_address VARCHAR(17) NOT NULL UNIQUE,
  ip_address VARCHAR(45),
  ubicacion VARCHAR(200) NOT NULL,
  descripcion TEXT,
  estado ENUM('conectado','desconectado','error','mantenimiento','reproduciendo') DEFAULT 'desconectado',
  ultimo_heartbeat DATETIME,
  fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
  version_software VARCHAR(50),
  resolucion_pantalla VARCHAR(20),
  orientacion ENUM('horizontal','vertical') DEFAULT 'horizontal',
  volumen_audio INT DEFAULT 50,
  brillo_pantalla INT DEFAULT 80,
  activo BOOLEAN DEFAULT TRUE,
  propietario_id INT UNSIGNED NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (propietario_id) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

-- Tabla de contenido para publicidad en pantallas
CREATE TABLE IF NOT EXISTS contenido_publicidad (
  id_contenido INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(200) NOT NULL,
  descripcion TEXT,
  tipo ENUM('imagen','video','web','html','texto') NOT NULL,
  url_archivo VARCHAR(500),
  contenido_html TEXT,
  duracion_segundos INT DEFAULT 30,
  tamano_archivo BIGINT,
  checksum VARCHAR(64),
  resolucion VARCHAR(20),
  activo BOOLEAN DEFAULT TRUE,
  creado_por INT UNSIGNED NOT NULL,
  fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
  fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (creado_por) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

-- Tabla de programación de contenido en dispositivos
CREATE TABLE IF NOT EXISTS programacion_contenido (
  id_programacion INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  dispositivo_id INT UNSIGNED NOT NULL,
  contenido_id INT UNSIGNED NOT NULL,
  fecha_inicio DATETIME NOT NULL,
  fecha_fin DATETIME NOT NULL,
  repetir_diariamente BOOLEAN DEFAULT FALSE,
  repetir_semanal BOOLEAN DEFAULT FALSE,
  dias_semana SET('lunes','martes','miercoles','jueves','viernes','sabado','domingo'),
  hora_inicio TIME,
  hora_fin TIME,
  prioridad INT DEFAULT 1,
  activo BOOLEAN DEFAULT TRUE,
  programado_por INT UNSIGNED NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (dispositivo_id) REFERENCES dispositivos_raspberry(id_dispositivo),
  FOREIGN KEY (contenido_id) REFERENCES contenido_publicidad(id_contenido),
  FOREIGN KEY (programado_por) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

-- Tabla de métricas de dispositivos
CREATE TABLE IF NOT EXISTS metricas_dispositivos (
  id_metrica INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  dispositivo_id INT UNSIGNED NOT NULL,
  cpu_usage DECIMAL(5,2),
  memoria_total BIGINT,
  memoria_usada BIGINT,
  disco_total BIGINT,
  disco_usado BIGINT,
  temperatura_cpu DECIMAL(4,1),
  estado_red ENUM('excelente','buena','regular','mala'),
  velocidad_descarga DECIMAL(8,2),
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (dispositivo_id) REFERENCES dispositivos_raspberry(id_dispositivo)
) ENGINE=InnoDB;

-- ================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ================================

-- Índices para usuarios
CREATE INDEX idx_usuario_correo ON usuarios(correo);
CREATE INDEX idx_usuario_activo ON usuarios(activo);
CREATE INDEX idx_usuario_rol ON usuarios(id_rol);

-- Índices para campañas
CREATE INDEX idx_campana_nombre ON campanas(nombre);
CREATE INDEX idx_campana_estado ON campanas(estado);
CREATE INDEX idx_campana_usuario ON campanas(id_usuario);
CREATE INDEX idx_campana_fechas ON campanas(fecha_inicio, fecha_fin);

-- Índices para reuniones
CREATE INDEX idx_reunion_fecha ON reuniones(fecha);
CREATE INDEX idx_reunion_estado ON reuniones(estado);
CREATE INDEX idx_reunion_organizador ON reuniones(organizador_id);

-- Índices para tareas
CREATE INDEX idx_tarea_responsable ON tareas(responsable);
CREATE INDEX idx_tarea_estado ON tareas(estado);
CREATE INDEX idx_tarea_fecha_entrega ON tareas(fecha_entrega);

-- Índices para dispositivos
CREATE INDEX idx_dispositivo_mac ON dispositivos_raspberry(mac_address);
CREATE INDEX idx_dispositivo_estado ON dispositivos_raspberry(estado);
CREATE INDEX idx_dispositivo_ubicacion ON dispositivos_raspberry(ubicacion);
CREATE INDEX idx_dispositivo_ultimo_heartbeat ON dispositivos_raspberry(ultimo_heartbeat);

-- Índices para auditoría
CREATE INDEX idx_auditoria_tabla ON auditoria(tabla_afectada);
CREATE INDEX idx_auditoria_fecha ON auditoria(fecha);
CREATE INDEX idx_auditoria_usuario ON auditoria(usuario_id);

-- ================================
-- DATOS INICIALES
-- ================================

-- Roles del sistema
INSERT INTO roles (nombre, descripcion) VALUES 
('ADMIN', 'Administrador del sistema con todos los permisos'),
('MANAGER', 'Gerente con permisos de gestión de campañas y equipos'),
('EDITOR', 'Editor de contenido y campañas'),
('VIEWER', 'Solo visualización de información');

-- Usuario administrador inicial (contraseña: admin123)
INSERT INTO usuarios (nombre, correo, contrasena, id_rol) VALUES 
('Administrador', 'admin@innoad.com', '$2a$10$8K1p/a1Zy4K19.oYkVwYk.sRwDf9hVx9qZk5.GjEp2QbHN5.3ZJ.', 1);

-- Contenido de ejemplo
INSERT INTO contenido_publicidad (nombre, descripcion, tipo, duracion_segundos, activo, creado_por) VALUES
('Bienvenida InnoAd', 'Mensaje de bienvenida al sistema', 'texto', 10, TRUE, 1),
('Logo Corporativo', 'Logo de la empresa', 'imagen', 15, TRUE, 1);

-- Configuración inicial completada

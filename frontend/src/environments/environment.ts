/**
 * Configuración de entorno para desarrollo local
 * 
 * Este archivo contiene las configuraciones específicas para el entorno
 * de desarrollo local. No debe contener datos sensibles en producción.
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Configurar URLs de APIs según el entorno local
 * 2. Agregar configuraciones para servicios externos
 * 3. Configurar WebSocket para dispositivos Raspberry Pi
 * 4. Establecer configuraciones de debug y logging
 * 
 * @author Equipo SENA ADSO
 */

export const environment = {
  production: false,
  name: 'development',

  // URLs de APIs - Backend Local
  apiUrls: {
    usuarios: 'http://localhost:8081/api/usuarios',
    campanas: 'http://localhost:8082/api/campanas', 
    reuniones: 'http://localhost:8083/api/reuniones',
    tareas: 'http://localhost:8084/api/tareas',
    auditoria: 'http://localhost:8085/api/auditoria',
    dispositivos: 'http://localhost:8086/api/dispositivos',
    ia: 'http://localhost:5000/api/ia'
  },

  // WebSocket para dispositivos Raspberry Pi
  websocket: {
    dispositivos: 'ws://localhost:8086/websocket/raspberry',
    notificaciones: 'ws://localhost:8081/websocket/notifications'
  },

  // Configuración de autenticación
  auth: {
    tokenKey: 'innoad_token',
    refreshTokenKey: 'innoad_refresh_token',
    tokenExpiration: 24 * 60 * 60 * 1000, // 24 horas
    autoRefresh: true
  },

  // Configuración de la aplicación
  app: {
    name: 'InnoAd',
    version: '1.0.0',
    defaultLanguage: 'es',
    supportedLanguages: ['es', 'en'],
    pageSize: 10,
    maxFileSize: 10 * 1024 * 1024, // 10MB
    allowedFileTypes: ['image/jpeg', 'image/png', 'video/mp4', 'text/html']
  },

  // Configuración de logging
  logging: {
    level: 'debug',
    enableConsoleLog: true,
    enableRemoteLog: false,
    logEndpoint: null
  },

  // Configuración de features (para desarrollo)
  features: {
    enableDevTools: true,
    enableMockData: false,
    enableBetaFeatures: true,
    enableAnalytics: false
  },

  // Configuración de terceros
  external: {
    googleMapsApiKey: '',
    analyticsKey: '',
    sentryDsn: ''
  }
};

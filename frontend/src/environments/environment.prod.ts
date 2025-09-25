/**
 * Configuración de entorno para producción
 * 
 * Este archivo contiene las configuraciones para el entorno de producción.
 * Se debe usar con variables de entorno seguras.
 * 
 * @author Equipo SENA ADSO
 */

export const environment = {
  production: true,
  name: 'production',

  // URLs de APIs - Producción (Railway)
  apiUrls: {
    usuarios: 'https://innoad-usuarios.railway.app/api/usuarios',
    campanas: 'https://innoad-campanas.railway.app/api/campanas', 
    reuniones: 'https://innoad-reuniones.railway.app/api/reuniones',
    tareas: 'https://innoad-tareas.railway.app/api/tareas',
    auditoria: 'https://innoad-auditoria.railway.app/api/auditoria',
    dispositivos: 'https://innoad-dispositivos.railway.app/api/dispositivos',
    ia: 'https://innoad-ia.railway.app/api/ia'
  },

  // WebSocket para dispositivos Raspberry Pi
  websocket: {
    dispositivos: 'wss://innoad-dispositivos.railway.app/websocket/raspberry',
    notificaciones: 'wss://innoad-usuarios.railway.app/websocket/notifications'
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
    level: 'warn',
    enableConsoleLog: false,
    enableRemoteLog: true,
    logEndpoint: 'https://innoad-auditoria.railway.app/api/logs'
  },

  // Configuración de features
  features: {
    enableDevTools: false,
    enableMockData: false,
    enableBetaFeatures: false,
    enableAnalytics: true
  },

  // Configuración de terceros
  external: {
    googleMapsApiKey: '',
    analyticsKey: '',
    sentryDsn: ''
  }
};

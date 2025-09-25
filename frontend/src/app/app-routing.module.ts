import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

/**
 * Configuración de rutas principales para InnoAd
 * 
 * Este módulo define las rutas de la aplicación usando lazy loading
 * para optimizar la carga inicial y mejorar el rendimiento.
 * 
 * TAREAS PARA EL EQUIPO:
 * 1. Implementar guards de autenticación para rutas protegidas
 * 2. Agregar guards de permisos por rol de usuario
 * 3. Implementar resolvers para cargar datos antes de mostrar componentes
 * 4. Configurar redirects para rutas no encontradas
 * 5. Agregar rutas para páginas de error (403, 404, 500)
 * 
 * @author Equipo SENA ADSO
 */

const routes: Routes = [
  // Ruta por defecto - redirige al dashboard
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },

  // Dashboard principal
  {
    path: 'dashboard',
    loadChildren: () => import('./features/dashboard/dashboard.module').then(m => m.DashboardModule),
    // TODO: Agregar guard de autenticación
    // canActivate: [AuthGuard]
  },

  // Autenticación (login, registro, recuperar contraseña)
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.module').then(m => m.AuthModule)
  },

  // Gestión de usuarios
  {
    path: 'usuarios',
    loadChildren: () => import('./features/usuarios/usuarios.module').then(m => m.UsuariosModule),
    // TODO: Agregar guard de permisos
    // canActivate: [AuthGuard, RoleGuard],
    // data: { expectedRole: ['ADMIN', 'MANAGER'] }
  },

  // Gestión de campañas publicitarias
  {
    path: 'campanas',
    loadChildren: () => import('./features/campanas/campanas.module').then(m => m.CampanasModule),
    // canActivate: [AuthGuard]
  },

  // Gestión de dispositivos Raspberry Pi
  {
    path: 'dispositivos',
    loadChildren: () => import('./features/dispositivos/dispositivos.module').then(m => m.DispositivosModule),
    // canActivate: [AuthGuard]
  },

  // Gestión de reuniones
  {
    path: 'reuniones',
    loadChildren: () => import('./features/reuniones/reuniones.module').then(m => m.ReunionesModule),
    // canActivate: [AuthGuard]
  },

  // Sistema de tareas (Kanban)
  {
    path: 'tareas',
    loadChildren: () => import('./features/tareas/tareas.module').then(m => m.TareasModule),
    // canActivate: [AuthGuard]
  },

  // Auditoría del sistema
  {
    path: 'auditoria',
    loadChildren: () => import('./features/auditoria/auditoria.module').then(m => m.AuditoriaModule),
    // canActivate: [AuthGuard, RoleGuard],
    // data: { expectedRole: ['ADMIN'] }
  },

  // Análisis con IA
  {
    path: 'analytics',
    loadChildren: () => import('./features/analytics/analytics.module').then(m => m.AnalyticsModule),
    // canActivate: [AuthGuard]
  },

  // Configuraciones del sistema
  {
    path: 'configuracion',
    loadChildren: () => import('./features/configuracion/configuracion.module').then(m => m.ConfiguracionModule),
    // canActivate: [AuthGuard]
  },

  // TODO: Rutas de error
  // {
  //   path: 'error',
  //   loadChildren: () => import('./features/error/error.module').then(m => m.ErrorModule)
  // },

  // Ruta wildcard - debe ir al final
  {
    path: '**',
    redirectTo: '/dashboard'
    // TODO: Cambiar por página 404 personalizada
    // redirectTo: '/error/404'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    // Habilitar tracing para debugging (solo desarrollo)
    enableTracing: false,

    // Estrategia de reutilización de rutas
    onSameUrlNavigation: 'reload',

    // Scrolling behavior
    scrollPositionRestoration: 'top',

    // Preloading strategy para lazy loading
    preloadingStrategy: 'PreloadAllModules' // TODO: Implementar estrategia personalizada
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }

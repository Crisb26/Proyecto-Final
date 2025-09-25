import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

// Angular Material
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatBadgeModule } from '@angular/material/badge';

// Layout Components
import { MainLayoutComponent } from './main-layout/main-layout.component';
import { HeaderComponent } from './header/header.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { FooterComponent } from './footer/footer.component';

/**
 * Módulo de Layout para InnoAd
 * 
 * Este módulo contiene todos los componentes de estructura de la aplicación:
 * - Layout principal
 * - Header con navegación
 * - Sidebar con menú
 * - Footer
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Implementar menú responsive para dispositivos móviles
 * 2. Agregar breadcrumbs de navegación
 * 3. Implementar notificaciones en tiempo real en el header
 * 4. Crear componente de búsqueda global
 * 5. Agregar indicadores de estado de conexión con Raspberry Pi
 * 
 * @author Equipo SENA ADSO
 */
@NgModule({
  declarations: [
    MainLayoutComponent,
    HeaderComponent,
    SidebarComponent,
    FooterComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    TranslateModule,

    // Angular Material
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatSidenavModule,
    MatListModule,
    MatMenuModule,
    MatBadgeModule
  ],
  exports: [
    MainLayoutComponent,
    HeaderComponent,
    SidebarComponent,
    FooterComponent
  ]
})
export class LayoutModule { }

import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';

/**
 * Componente de layout principal para InnoAd
 * 
 * Este componente gestiona la estructura general de la aplicación:
 * - Sidebar colapsible
 * - Header fijo
 * - Área de contenido principal
 * - Footer
 * - Responsividad para diferentes tamaños de pantalla
 * 
 * TAREAS PARA EL EQUIPO:
 * 1. Implementar estado persistente del sidebar
 * 2. Agregar animaciones suaves para transiciones
 * 3. Implementar tema claro/oscuro
 * 4. Agregar indicadores de carga global
 * 5. Implementar breadcrumbs automáticos
 * 
 * @author Equipo SENA ADSO
 */
@Component({
  selector: 'app-main-layout',
  templateUrl: './main-layout.component.html',
  styleUrls: ['./main-layout.component.scss']
})
export class MainLayoutComponent implements OnInit {

  @ViewChild('sidenav') sidenav!: MatSidenav;

  isHandset$ = this.breakpointObserver.observe(Breakpoints.Handset);
  sidenavMode: 'over' | 'side' = 'side';
  sidenavOpened = true;

  constructor(
    private breakpointObserver: BreakpointObserver
  ) {}

  ngOnInit(): void {
    // Configurar responsividad del sidebar
    this.isHandset$.subscribe(result => {
      if (result.matches) {
        this.sidenavMode = 'over';
        this.sidenavOpened = false;
      } else {
        this.sidenavMode = 'side';
        this.sidenavOpened = true;
      }
    });

    // TODO: Cargar estado persistente del sidebar desde localStorage
    this.loadSidebarState();
  }

  /**
   * Alterna el estado del sidebar
   */
  toggleSidenav(): void {
    this.sidenav.toggle();

    // TODO: Persistir estado en localStorage
    this.saveSidebarState();
  }

  /**
   * Carga el estado persistente del sidebar
   * TODO: Implementar persistencia en localStorage
   */
  private loadSidebarState(): void {
    // const savedState = localStorage.getItem('sidebarState');
    // if (savedState) {
    //   this.sidenavOpened = JSON.parse(savedState);
    // }
  }

  /**
   * Guarda el estado del sidebar
   * TODO: Implementar persistencia en localStorage
   */
  private saveSidebarState(): void {
    // localStorage.setItem('sidebarState', JSON.stringify(this.sidenav.opened));
  }
}

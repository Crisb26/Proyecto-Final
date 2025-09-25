import { Component, OnInit } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

/**
 * Componente principal de la aplicacion InnoAd
 * 
 * Este componente es el punto de entrada de la aplicación y se encarga de:
 * - Configuración inicial del idioma
 * - Inicialización de servicios globales
 * - Gestión del estado general de la aplicación
 * 
 * TAREAS:
 * 1. Implementar detección automática de idioma del navegador
 * 2. Configurar tema dinámico (claro/oscuro)
 * 3. Agregar manejo global de errores
 * 4. Implementar sistema de notificaciones globales
 * 5. Configurar analytics y métricas
 * 
 * @author Equipo SENA ADSO
 */
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'InnoAd - Gestión de Campañas Publicitarias';

  constructor(
    private translate: TranslateService
  ) {
    // Configuracion inical de idiomas
    this.translate.addLangs(['es', 'en']);
    this.translate.setDefaultLang('es');
  }

  ngOnInit(): void {
    // detectar idioma del navegador
    const browserLang = this.translate.getBrowserLang();
    const languageToUse = browserLang?.match(/es|en/) ? browserLang : 'es';

    this.translate.use(languageToUse);

    // inicializar servicios globales
    this.initializeApp();
  }

  private initializeApp(): void {
    // - Verificar autenticación
    // - Cargar configuración del usuario
    // - Inicializar conexión WebSocket para dispositivos
    // - Configurar interceptores

    console.log('🚀 InnoAd Frontend iniciado correctamente');
  }
}

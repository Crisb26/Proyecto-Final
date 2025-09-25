import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

// Routing
import { AppRoutingModule } from './app-routing.module';

// Translate
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';

// Angular Material
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatDialogModule } from '@angular/material/dialog';
import { MatSnackBarModule } from '@angular/material/snack-bar';

// Third party
import { ToastrModule } from 'ngx-toastr';
import { NgxLoadingModule } from 'ngx-loading';

// App Components
import { AppComponent } from './app.component';
import { LayoutModule } from './layout/layout.module';

/**
 * Módulo principal de la aplicación InnoAd
 * 
 * Este módulo configura toda la aplicación Angular incluyendo:
 * - Módulos de Angular Material para UI
 * - Sistema de internacionalización (i18n)
 * - Configuración HTTP y formularios
 * - Librerías de terceros (Toastr, Loading, etc.)
 * 
 * TAREAS PARA EL EQUIPO DE DESARROLLO:
 * 1. Configurar tema personalizado de Angular Material
 * 2. Agregar más idiomas al sistema i18n
 * 3. Configurar interceptores HTTP para autenticación
 * 4. Implementar lazy loading para módulos de funcionalidades
 * 5. Agregar configuración PWA si es necesario
 * 6. Configurar service worker para cache offline
 * 
 * @author Equipo SENA ADSO
 */

// Factory function for translate loader
export function HttpLoaderFactory(http: HttpClient): TranslateHttpLoader {
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    AppRoutingModule,
    LayoutModule,

    // Translate Module
    TranslateModule.forRoot({
      defaultLanguage: 'es',
      loader: {
        provide: TranslateLoader,
        useFactory: HttpLoaderFactory,
        deps: [HttpClient]
      }
    }),

    // Angular Material Modules
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatSidenavModule,
    MatListModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatTableModule,
    MatPaginatorModule,
    MatDialogModule,
    MatSnackBarModule,

    // Third Party Modules
    ToastrModule.forRoot({
      timeOut: 3000,
      positionClass: 'toast-top-right',
      preventDuplicates: true,
      progressBar: true
    }),

    NgxLoadingModule.forRoot({
      animationType: 'circle',
      backdropBackgroundColour: 'rgba(0,0,0,0.1)',
      primaryColour: '#3f51b5',
      secondaryColour: '#ff4081',
      tertiaryColour: '#ffffff'
    })
  ],
  providers: [
    // TODO: Agregar interceptores HTTP aquí
    // {
    //   provide: HTTP_INTERCEPTORS,
    //   useClass: AuthInterceptor,
    //   multi: true
    // }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

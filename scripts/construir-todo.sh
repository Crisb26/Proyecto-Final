#!/bin/bash

# InnoAd - Script para construir todo el proyecto
# Compila backend, frontend y prepara distribución

echo "🏗️  Construyendo InnoAd - Proyecto Completo"
echo "=========================================="

# Variables
BUILD_DIR="dist"
DATE=$(date +"%Y%m%d_%H%M%S")

# Limpiar build anterior
echo "🧹 Limpiando builds anteriores..."
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# Construir Backend - Microservicio Usuarios
echo "🔧 Construyendo Backend - Usuarios..."
cd backend/microservicio-usuarios
mvn clean package -DskipTests
if [ $? -eq 0 ]; then
    echo "✅ Backend Usuarios construido exitosamente"
    cp target/*.jar ../../$BUILD_DIR/usuarios-service.jar
else
    echo "❌ Error construyendo Backend Usuarios"
    exit 1
fi
cd ../..

# Construir Backend - Microservicio Dispositivos
echo "📺 Construyendo Backend - Dispositivos..."
cd backend/microservicio-dispositivos
mvn clean package -DskipTests
if [ $? -eq 0 ]; then
    echo "✅ Backend Dispositivos construido exitosamente"
    cp target/*.jar ../../$BUILD_DIR/dispositivos-service.jar
else
    echo "❌ Error construyendo Backend Dispositivos"
    exit 1
fi
cd ../..

# Construir Frontend Angular
echo "🎨 Construyendo Frontend Angular..."
cd frontend
npm ci
npm run build:prod
if [ $? -eq 0 ]; then
    echo "✅ Frontend construido exitosamente"
    cp -r dist/innoad-frontend/* ../$BUILD_DIR/frontend/
    mkdir -p ../$BUILD_DIR/frontend
    cp -r dist/innoad-frontend/* ../$BUILD_DIR/frontend/
else
    echo "❌ Error construyendo Frontend"
    exit 1
fi
cd ..

# Preparar Servicios IA
echo "🤖 Preparando Servicios IA..."
cp -r python-ia/* $BUILD_DIR/ia-services/
mkdir -p $BUILD_DIR/ia-services
cp -r python-ia/* $BUILD_DIR/ia-services/

# Preparar Cliente Raspberry Pi
echo "📺 Preparando Cliente Raspberry Pi..."
mkdir -p $BUILD_DIR/raspberry-cliente
cp -r raspberry-cliente/* $BUILD_DIR/raspberry-cliente/

# Generar archivo de versión
echo "📋 Generando información de build..."
cat > $BUILD_DIR/BUILD_INFO.txt << EOF
InnoAd - Información de Build
============================
Fecha: $(date)
Versión: 1.0.0
Build ID: $DATE
Commit: $(git rev-parse HEAD 2>/dev/null || echo "No Git")

Componentes:
- Backend Usuarios: ✅ usuarios-service.jar
- Backend Dispositivos: ✅ dispositivos-service.jar  
- Frontend Angular: ✅ frontend/
- Servicios IA: ✅ ia-services/
- Cliente Raspberry: ✅ raspberry-cliente/

Instrucciones de Despliegue:
1. Subir .jar files a Railway
2. Configurar variables de entorno
3. Desplegar frontend como static site
4. Instalar cliente en Raspberry Pi

Desarrollado por: Equipo SENA ADSO
EOF

# Crear archivo de despliegue
echo "📦 Creando paquete de distribución..."
cd $BUILD_DIR
tar -czf "../innoad-release-${DATE}.tar.gz" *
cd ..

echo ""
echo "🎉 ¡Build completado exitosamente!"
echo "=================================="
echo "📦 Archivo de distribución: innoad-release-${DATE}.tar.gz"
echo "📁 Archivos en: $BUILD_DIR/"
echo "📋 Info de build: $BUILD_DIR/BUILD_INFO.txt"
echo ""
echo "🚀 Siguiente paso: ./scripts/desplegar-railway.sh"

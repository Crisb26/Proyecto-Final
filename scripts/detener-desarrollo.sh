#!/bin/bash

# InnoAd - Script para detener servicios de desarrollo

echo "🛑 Deteniendo InnoAd - Servicios de Desarrollo"
echo "============================================="

# Detener procesos Java (Spring Boot)
echo "🔧 Deteniendo servicios Backend..."
pkill -f "spring-boot:run"
pkill -f "java.*innoad"

# Detener procesos Node.js (Angular)
echo "🎨 Deteniendo Frontend Angular..."
pkill -f "ng serve"
pkill -f "node.*angular"

# Detener servicios Python (IA)
echo "🤖 Deteniendo Servicios IA..."
pkill -f "python.*api_ia.py"
pkill -f "flask"

# Limpiar puertos específicos si están ocupados
echo "🔌 Liberando puertos..."
lsof -ti:4200 | xargs -r kill -9  # Angular
lsof -ti:8081 | xargs -r kill -9  # Backend Usuarios
lsof -ti:8086 | xargs -r kill -9  # Backend Dispositivos
lsof -ti:5000 | xargs -r kill -9  # IA Services

# Cerrar terminales abiertas por el script de inicio
echo "🖥️  Cerrando terminales..."
pkill -f "gnome-terminal.*Backend"
pkill -f "gnome-terminal.*Frontend"
pkill -f "gnome-terminal.*IA-Services"

# Limpiar archivos temporales
echo "🧹 Limpiando archivos temporales..."
find . -name "*.pid" -delete
find . -name "*.log" -size +10M -delete  # Solo logs muy grandes

echo ""
echo "✅ Todos los servicios InnoAd han sido detenidos"
echo "💡 Para reiniciar: ./scripts/iniciar-desarrollo.sh"

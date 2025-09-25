#!/bin/bash

# InnoAd - Script de inicio para desarrollo
# Este script inicia todos los servicios necesarios para desarrollo local

echo "🚀 Iniciando InnoAd - Desarrollo Local"
echo "=================================="

# Verificar prerrequisitos
echo "📋 Verificando prerrequisitos..."

# Verificar Java
if ! command -v java &> /dev/null; then
    echo "❌ Java 17 no encontrado. Instalar desde: https://adoptium.net/"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no encontrado. Instalar desde: https://nodejs.org/"
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.9+ no encontrado. Instalar desde: https://python.org/"
    exit 1
fi

echo "✅ Prerrequisitos verificados"

# Configurar variables de entorno
if [ ! -f .env ]; then
    echo "📝 Configurando variables de entorno..."
    cp config/env/.env.desarrollo .env
    echo "⚠️  IMPORTANTE: Editar .env con tus credenciales de Railway MySQL"
    echo "   - DATABASE_PASSWORD=tu_password_railway"
    echo "   - Otros parámetros según necesidad"
fi

# Crear directorios necesarios
mkdir -p logs
mkdir -p uploads
mkdir -p python-ia/logs
mkdir -p raspberry-cliente/logs

echo "📁 Directorios creados"

# Iniciar servicios en paralelo
echo "🔄 Iniciando servicios..."

# Backend - Microservicio Usuarios
echo "🔧 Iniciando Backend - Usuarios (Puerto 8081)..."
cd backend/microservicio-usuarios
gnome-terminal --tab --title="Backend-Usuarios" -- bash -c "
    echo 'Iniciando Microservicio Usuarios...'; 
    mvn clean compile;
    mvn spring-boot:run;
    exec bash"
cd ../..

# Backend - Microservicio Dispositivos (Raspberry Pi)
echo "📺 Iniciando Backend - Dispositivos (Puerto 8086)..."
cd backend/microservicio-dispositivos
gnome-terminal --tab --title="Backend-Dispositivos" -- bash -c "
    echo 'Iniciando Microservicio Dispositivos...'; 
    mvn clean compile;
    mvn spring-boot:run;
    exec bash"
cd ../..

# Servicios de IA
echo "🤖 Iniciando Servicios IA (Puerto 5000)..."
cd python-ia
gnome-terminal --tab --title="IA-Services" -- bash -c "
    echo 'Iniciando Servicios de IA...';
    if [ ! -d 'venv' ]; then
        python3 -m venv venv;
    fi;
    source venv/bin/activate;
    pip install -r requirements.txt;
    python services/api_ia.py;
    exec bash"
cd ..

# Frontend Angular
echo "🎨 Iniciando Frontend Angular (Puerto 4200)..."
cd frontend
gnome-terminal --tab --title="Frontend-Angular" -- bash -c "
    echo 'Iniciando Frontend Angular...';
    if [ ! -d 'node_modules' ]; then
        npm install;
    fi;
    ng serve --host 0.0.0.0 --port 4200;
    exec bash"
cd ..

# Esperar un momento para que se inicien los servicios
echo "⏳ Esperando inicio de servicios (30 segundos)..."
sleep 30

echo ""
echo "🎉 InnoAd iniciado correctamente!"
echo "================================"
echo "📱 Frontend:           http://localhost:4200"
echo "🔧 API Usuarios:       http://localhost:8081/api/usuarios"
echo "📺 API Dispositivos:   http://localhost:8086/api/dispositivos" 
echo "🤖 Servicios IA:       http://localhost:5000/health"
echo "📊 Documentación API:  http://localhost:8081/swagger-ui.html"
echo ""
echo "📝 Para detener todos los servicios:"
echo "   ./scripts/detener-desarrollo.sh"
echo ""
echo "🔍 Para ver logs:"
echo "   tail -f logs/*.log"
echo ""
echo "✨ ¡Desarrollo exitoso! El equipo puede comenzar a trabajar."

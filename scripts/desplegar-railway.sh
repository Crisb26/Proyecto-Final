#!/bin/bash

# InnoAd - Script de despliegue en Railway
# Despliega todos los servicios en Railway automáticamente

echo "🚂 Desplegando InnoAd en Railway"
echo "==============================="

# Verificar Railway CLI
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI no encontrado"
    echo "💡 Instalar con: npm install -g @railway/cli"
    echo "💡 Luego autenticarse: railway login"
    exit 1
fi

# Verificar autenticación
railway auth
if [ $? -ne 0 ]; then
    echo "❌ No autenticado en Railway"
    echo "💡 Ejecutar: railway login"
    exit 1
fi

echo "✅ Railway CLI configurado"

# Desplegar Microservicio Usuarios
echo "🔧 Desplegando Backend - Usuarios..."
cd backend/microservicio-usuarios
railway up --service innoad-usuarios
if [ $? -eq 0 ]; then
    echo "✅ Backend Usuarios desplegado"
else
    echo "❌ Error desplegando Backend Usuarios"
fi
cd ../..

# Desplegar Microservicio Dispositivos
echo "📺 Desplegando Backend - Dispositivos..."
cd backend/microservicio-dispositivos
railway up --service innoad-dispositivos
if [ $? -eq 0 ]; then
    echo "✅ Backend Dispositivos desplegado"
else
    echo "❌ Error desplegando Backend Dispositivos"
fi
cd ../..

# Desplegar Servicios IA
echo "🤖 Desplegando Servicios IA..."
cd python-ia
railway up --service innoad-ia
if [ $? -eq 0 ]; then
    echo "✅ Servicios IA desplegados"
else
    echo "❌ Error desplegando Servicios IA"
fi
cd ..

# Desplegar Frontend
echo "🎨 Desplegando Frontend..."
cd frontend
npm run build:railway
railway up --service innoad-frontend
if [ $? -eq 0 ]; then
    echo "✅ Frontend desplegado"
else
    echo "❌ Error desplegando Frontend"
fi
cd ..

echo ""
echo "🎉 ¡Despliegue completado!"
echo "========================"
echo "🔗 URLs de servicios (verificar en Railway Dashboard):"
echo "   Frontend: https://innoad-frontend.railway.app"
echo "   API Usuarios: https://innoad-usuarios.railway.app"
echo "   API Dispositivos: https://innoad-dispositivos.railway.app"
echo "   Servicios IA: https://innoad-ia.railway.app"
echo ""
echo "🔧 Configurar variables de entorno en Railway:"
echo "   DATABASE_URL, JWT_SECRET, etc."
echo ""
echo "📱 Cliente Raspberry Pi:"
echo "   Descargar desde: raspberry-cliente/"
echo "   Configurar INNOAD_SERVER con URL de dispositivos"

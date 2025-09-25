#!/bin/bash

# InnoAd Cliente Raspberry Pi - Script de Instalación
# Este script configura e instala el cliente InnoAd en un Raspberry Pi

set -e  # Salir si cualquier comando falla

echo "🥧 InnoAd - Instalación en Raspberry Pi"
echo "======================================"

# Variables de configuración
INSTALL_DIR="/opt/innoad"
SERVICE_NAME="innoad-cliente"
PYTHON_VENV="$INSTALL_DIR/venv"

# Verificar que se ejecuta como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script debe ejecutarse como root"
    echo "💡 Ejecutar: sudo ./install.sh"
    exit 1
fi

# Función para mostrar mensajes
log_info() {
    echo "ℹ️  $1"
}

log_success() {
    echo "✅ $1"
}

log_error() {
    echo "❌ $1"
}

# Actualizar sistema
log_info "Actualizando sistema..."
apt update
apt upgrade -y
log_success "Sistema actualizado"

# Instalar dependencias del sistema
log_info "Instalando dependencias del sistema..."
apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    feh \
    omxplayer \
    chromium-browser \
    alsa-utils \
    git \
    curl \
    supervisor

log_success "Dependencias instaladas"

# Crear usuario innoad si no existe
if ! id "pi" &>/dev/null; then
    log_info "Creando usuario pi..."
    useradd -r -s /bin/bash -d $INSTALL_DIR pi
    log_success "Usuario pi creado"
fi

# Crear directorio de instalación
log_info "Creando directorios de instalación..."
mkdir -p $INSTALL_DIR
mkdir -p $INSTALL_DIR/logs
mkdir -p $INSTALL_DIR/content
mkdir -p $INSTALL_DIR/config

# Copiar archivos del cliente
log_info "Copiando archivos del cliente..."
cp main.py $INSTALL_DIR/
cp requirements.txt $INSTALL_DIR/
cp config/client.conf $INSTALL_DIR/config/
cp innoad-cliente.service /etc/systemd/system/

# Cambiar propietario de archivos
chown -R pi:pi $INSTALL_DIR
chmod +x $INSTALL_DIR/main.py

log_success "Archivos copiados"

# Crear entorno virtual Python
log_info "Creando entorno virtual Python..."
sudo -u pi python3 -m venv $PYTHON_VENV
sudo -u pi $PYTHON_VENV/bin/pip install -r $INSTALL_DIR/requirements.txt
log_success "Entorno Python configurado"

# Configurar servicio systemd
log_info "Configurando servicio systemd..."
systemctl daemon-reload
systemctl enable $SERVICE_NAME
log_success "Servicio configurado"

# Configurar permisos especiales
log_info "Configurando permisos especiales..."

# Permitir control de brillo sin sudo
echo 'SUBSYSTEM=="backlight", ACTION=="add", RUN+="/bin/chgrp video /sys/class/backlight/%k/brightness", RUN+="/bin/chmod g+w /sys/class/backlight/%k/brightness"' > /etc/udev/rules.d/99-backlight.rules

# Agregar usuario pi a grupos necesarios
usermod -a -G audio,video,gpio pi

log_success "Permisos configurados"

# Configurar arranque automático
log_info "Configurando arranque automático..."

# Habilitar GPU para reproducción de video
if ! grep -q "gpu_mem=128" /boot/config.txt; then
    echo "gpu_mem=128" >> /boot/config.txt
fi

# Configurar resolución de pantalla
if ! grep -q "hdmi_force_hotplug=1" /boot/config.txt; then
    echo "hdmi_force_hotplug=1" >> /boot/config.txt
fi

log_success "Configuración de arranque actualizada"

# Mostrar información de configuración
echo ""
echo "🎉 Instalación completada exitosamente!"
echo "======================================"
echo ""
echo "📝 Próximos pasos:"
echo "1. Configurar URL del servidor en:"
echo "   $INSTALL_DIR/config/client.conf"
echo ""
echo "2. O configurar variable de entorno:"
echo "   sudo systemctl edit $SERVICE_NAME"
echo "   [Service]"
echo "   Environment=INNOAD_SERVER=ws://tu-servidor:8086/websocket/raspberry"
echo ""
echo "3. Iniciar el servicio:"
echo "   sudo systemctl start $SERVICE_NAME"
echo ""
echo "4. Ver logs en tiempo real:"
echo "   sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "5. Verificar estado:"
echo "   sudo systemctl status $SERVICE_NAME"
echo ""
echo "🔧 Comandos útiles:"
echo "   sudo systemctl start $SERVICE_NAME    # Iniciar"
echo "   sudo systemctl stop $SERVICE_NAME     # Detener" 
echo "   sudo systemctl restart $SERVICE_NAME  # Reiniciar"
echo "   sudo systemctl disable $SERVICE_NAME  # Deshabilitar"
echo ""
echo "📍 Directorios importantes:"
echo "   Cliente: $INSTALL_DIR"
echo "   Logs: $INSTALL_DIR/logs"
echo "   Contenido: $INSTALL_DIR/content"
echo "   Configuración: $INSTALL_DIR/config"
echo ""
echo "✨ ¡Tu Raspberry Pi está listo para InnoAd!"

# Preguntar si iniciar el servicio ahora
read -p "¿Deseas iniciar el servicio ahora? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl start $SERVICE_NAME
    log_success "Servicio iniciado"
    echo "📊 Ver logs: sudo journalctl -u $SERVICE_NAME -f"
fi

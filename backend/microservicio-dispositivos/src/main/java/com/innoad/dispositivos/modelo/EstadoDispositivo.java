package com.innoad.dispositivos.modelo;

/**
 * Estado del dispositivo Raspberry.
 * Añadido publico para que pueda ser referenciado desde repositorios y servicios.
 */
public enum EstadoDispositivo {
    CONECTADO,
    DESCONECTADO,
    ERROR,
    MANTENIMIENTO,
    REPRODUCIENDO,
    ACTUALIZANDO,
    PENDIENTE
}

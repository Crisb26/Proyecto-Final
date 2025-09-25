# -*- coding: utf-8 -*-
"""
Utilidad de logging centralizada para servicios de IA
=====================================================

Este módulo proporciona un sistema de logging unificado y configurable
para todos los componentes de los servicios de IA.

TAREAS PARA EL EQUIPO DE DESARROLLO:
1. Implementar logging estructurado con JSON
2. Agregar integración con sistemas de monitoreo (ELK, Prometheus)
3. Implementar niveles de logging dinámicos
4. Crear filtros personalizados para logs sensibles
5. Agregar rotación automática de logs por tamaño y fecha

Autor: Equipo SENA ADSO
"""

import logging
import logging.config
import os
from pathlib import Path
from typing import Optional

from config.configuracion import LOGGING_CONFIG, PATHS

# ========================================
# CONFIGURACIÓN DEL LOGGER
# ========================================

def setup_logging(config_dict: dict = None):
    """
    Configura el sistema de logging usando la configuración proporcionada

    Args:
        config_dict: Configuración personalizada de logging
    """
    if config_dict is None:
        config_dict = LOGGING_CONFIG

    # Asegurar que el directorio de logs existe
    PATHS['logs'].mkdir(parents=True, exist_ok=True)

    # Configurar logging
    logging.config.dictConfig(config_dict)

def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Obtiene un logger configurado con el nombre especificado

    Args:
        name: Nombre del logger (generalmente __name__ del módulo)
        level: Nivel de logging opcional

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)

    if level:
        numeric_level = getattr(logging, level.upper(), None)
        if isinstance(numeric_level, int):
            logger.setLevel(numeric_level)

    return logger

# ========================================
# FILTROS PERSONALIZADOS
# ========================================

class SensitiveDataFilter(logging.Filter):
    """
    Filtro para remover datos sensibles de los logs

    TODO: Implementar filtrado de contraseñas, tokens, etc.
    """

    def __init__(self):
        super().__init__()
        self.sensitive_patterns = [
            'password', 'token', 'secret', 'key', 'auth'
        ]

    def filter(self, record):
        # TODO: Implementar filtrado de datos sensibles
        # Ejemplo básico - mejorar con regex más robustos
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            for pattern in self.sensitive_patterns:
                if pattern in record.msg.lower():
                    record.msg = record.msg.replace(record.msg, '[FILTERED]')

        return True

class ModelPerformanceFilter(logging.Filter):
    """
    Filtro especializado para logs de rendimiento de modelos
    """

    def filter(self, record):
        # Solo permitir logs relacionados con modelos si están en nivel INFO o superior
        if hasattr(record, 'funcName'):
            model_functions = ['train_model', 'predict', 'evaluate_model']
            if any(func in record.funcName for func in model_functions):
                return record.levelno >= logging.INFO

        return True

# ========================================
# FUNCIONES DE UTILIDAD
# ========================================

def log_model_metrics(logger: logging.Logger, model_name: str, metrics: dict):
    """
    Registra métricas de modelo de forma estructurada

    Args:
        logger: Logger a utilizar
        model_name: Nombre del modelo
        metrics: Diccionario con métricas
    """
    logger.info(f"Model Performance - {model_name}")
    for metric_name, value in metrics.items():
        logger.info(f"  {metric_name}: {value:.4f}")

def log_prediction_request(logger: logging.Logger, request_data: dict, prediction_time: float):
    """
    Registra información sobre requests de predicción

    Args:
        logger: Logger a utilizar
        request_data: Datos de la solicitud
        prediction_time: Tiempo de predicción en ms
    """
    logger.info(f"Prediction Request - Time: {prediction_time:.2f}ms")
    logger.debug(f"Request data keys: {list(request_data.keys())}")

def log_training_progress(logger: logging.Logger, model_name: str, epoch: int, loss: float):
    """
    Registra progreso de entrenamiento

    Args:
        logger: Logger a utilizar
        model_name: Nombre del modelo
        epoch: Número de época
        loss: Valor de pérdida
    """
    logger.info(f"Training {model_name} - Epoch {epoch}, Loss: {loss:.6f}")

def log_error_with_context(logger: logging.Logger, error: Exception, context: dict = None):
    """
    Registra error con contexto adicional

    Args:
        logger: Logger a utilizar
        error: Excepción capturada
        context: Contexto adicional
    """
    logger.error(f"Error: {str(error)}")
    if context:
        logger.error(f"Context: {context}")
    logger.exception("Full traceback:")

# ========================================
# CONFIGURACIÓN AUTOMÁTICA
# ========================================

# Configurar logging automáticamente al importar
setup_logging()

# Crear logger por defecto para el módulo
default_logger = get_logger(__name__)
default_logger.info("Sistema de logging inicializado correctamente")

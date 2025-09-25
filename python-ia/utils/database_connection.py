# -*- coding: utf-8 -*-
"""
Utilidad de conexión a base de datos para servicios de IA
========================================================

Este módulo maneja la conexión con la base de datos MySQL de InnoAd,
proporcionando métodos para ejecutar consultas y extraer datos.

TAREAS PARA EL EQUIPO DE DESARROLLO:
1. Implementar pool de conexiones robusto
2. Agregar retry logic para conexiones perdidas
3. Implementar cache de consultas frecuentes
4. Crear métodos específicos para cada tipo de análisis
5. Agregar métricas de rendimiento de consultas

Autor: Equipo SENA ADSO
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging
from typing import Optional, Dict, Any, List
import time

from config.configuracion import get_database_url, DATABASE_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

class DatabaseConnection:
    """
    Clase para manejar conexiones y consultas a la base de datos
    """

    def __init__(self):
        self.engine = None
        self.connection_string = get_database_url()
        self._initialize_engine()

    def _initialize_engine(self):
        """
        Inicializa el engine de SQLAlchemy con pool de conexiones
        """
        try:
            self.engine = create_engine(
                self.connection_string,
                poolclass=QueuePool,
                pool_size=DATABASE_CONFIG['pool_size'],
                max_overflow=DATABASE_CONFIG['max_overflow'],
                pool_timeout=DATABASE_CONFIG['pool_timeout'],
                pool_recycle=DATABASE_CONFIG['pool_recycle'],
                echo=False  # Cambiar a True para debugging SQL
            )

            # Probar conexión
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            logger.info("✅ Conexión a base de datos inicializada correctamente")

        except Exception as e:
            logger.error(f"❌ Error inicializando conexión a base de datos: {e}")
            raise

    def is_connected(self) -> bool:
        """
        Verifica si la conexión a la base de datos está activa
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except:
            return False

    @contextmanager
    def get_connection(self):
        """
        Context manager para obtener conexión de base de datos
        """
        connection = None
        try:
            connection = self.engine.connect()
            yield connection
        finally:
            if connection:
                connection.close()

    def execute_query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL y retorna un DataFrame

        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta

        Returns:
            DataFrame con los resultados
        """
        start_time = time.time()

        try:
            with self.get_connection() as conn:
                df = pd.read_sql(text(query), conn, params=params)

            execution_time = (time.time() - start_time) * 1000
            logger.debug(f"Consulta ejecutada en {execution_time:.2f}ms - {len(df)} filas")

            return df

        except Exception as e:
            logger.error(f"Error ejecutando consulta: {e}")
            logger.error(f"Query: {query}")
            if params:
                logger.error(f"Params: {params}")
            raise

    def get_campaigns_data(self, days_back: int = 90) -> pd.DataFrame:
        """
        Obtiene datos de campañas para análisis

        TODO: Optimizar consulta con índices apropiados
        """
        query = """
        SELECT 
            c.id_campana,
            c.nombre,
            c.presupuesto,
            c.fecha_inicio,
            c.fecha_fin,
            c.estado,
            c.plataforma,
            c.tipo_objetivo,
            DATEDIFF(c.fecha_fin, c.fecha_inicio) as duracion_dias,
            COUNT(a.id_anuncio) as total_anuncios,
            COALESCE(SUM(a.impresiones), 0) as total_impresiones,
            COALESCE(SUM(a.clics), 0) as total_clics,
            COALESCE(SUM(a.costo_total), 0) as costo_total,
            COALESCE(AVG(a.cpc_maximo), 0) as cpc_promedio,
            CASE 
                WHEN SUM(a.impresiones) > 0 
                THEN (SUM(a.clics) / SUM(a.impresiones)) * 100 
                ELSE 0 
            END as ctr,
            CASE 
                WHEN SUM(a.costo_total) > 0 
                THEN ((SUM(a.clics) * 10 - SUM(a.costo_total)) / SUM(a.costo_total)) * 100
                ELSE 0 
            END as roi
        FROM campanas c
        LEFT JOIN anuncios a ON c.id_campana = a.id_campana
        WHERE c.created_at >= DATE_SUB(NOW(), INTERVAL %s DAY)
        GROUP BY c.id_campana
        HAVING total_anuncios > 0
        ORDER BY c.created_at DESC
        """

        return self.execute_query(query, (days_back,))

    def get_devices_metrics(self, days_back: int = 30) -> pd.DataFrame:
        """
        Obtiene métricas de dispositivos Raspberry Pi

        TODO: Implementar cuando esté disponible tabla de métricas
        """
        query = """
        SELECT 
            d.id_dispositivo,
            d.nombre,
            d.ubicacion,
            d.estado,
            d.ultimo_heartbeat,
            COUNT(pc.id_programacion) as contenido_programado,
            TIMESTAMPDIFF(HOUR, d.ultimo_heartbeat, NOW()) as horas_sin_heartbeat
        FROM dispositivos_raspberry d
        LEFT JOIN programacion_contenido pc ON d.id_dispositivo = pc.dispositivo_id
        WHERE d.activo = 1
        AND d.fecha_registro >= DATE_SUB(NOW(), INTERVAL %s DAY)
        GROUP BY d.id_dispositivo
        ORDER BY d.ultimo_heartbeat DESC
        """

        return self.execute_query(query, (days_back,))

    def get_content_performance(self) -> pd.DataFrame:
        """
        Obtiene datos de rendimiento de contenido
        """
        query = """
        SELECT 
            cp.id_contenido,
            cp.nombre,
            cp.tipo,
            cp.duracion_segundos,
            cp.tamano_archivo,
            COUNT(pc.id_programacion) as veces_programado,
            COUNT(DISTINCT pc.dispositivo_id) as dispositivos_unicos
        FROM contenido_publicidad cp
        LEFT JOIN programacion_contenido pc ON cp.id_contenido = pc.contenido_id
        WHERE cp.activo = 1
        GROUP BY cp.id_contenido
        ORDER BY veces_programado DESC
        """

        return self.execute_query(query)

    def insert_prediction_log(self, prediction_data: Dict[str, Any]) -> int:
        """
        Registra una predicción en la base de datos para auditoría

        TODO: Crear tabla de logs de predicciones
        """
        # Por ahora, solo logging
        logger.info(f"Predicción realizada: {prediction_data}")
        return 1

    def get_model_performance_history(self, model_name: str) -> pd.DataFrame:
        """
        Obtiene historial de rendimiento de un modelo específico

        TODO: Implementar tabla de métricas de modelos
        """
        # Placeholder - implementar cuando esté disponible la tabla
        return pd.DataFrame()

    def close(self):
        """
        Cierra la conexión a la base de datos
        """
        if self.engine:
            self.engine.dispose()
            logger.info("Conexión a base de datos cerrada")

    def __del__(self):
        """
        Destructor para asegurar cierre de conexión
        """
        self.close()

# ========================================
# FUNCIONES DE UTILIDAD
# ========================================

def test_database_connection() -> bool:
    """
    Prueba la conexión a la base de datos
    """
    try:
        db = DatabaseConnection()
        result = db.is_connected()
        db.close()
        return result
    except Exception as e:
        logger.error(f"Error probando conexión: {e}")
        return False

def get_table_info(table_name: str) -> pd.DataFrame:
    """
    Obtiene información sobre las columnas de una tabla
    """
    db = DatabaseConnection()
    query = f"DESCRIBE {table_name}"
    try:
        return db.execute_query(query)
    except Exception as e:
        logger.error(f"Error obteniendo info de tabla {table_name}: {e}")
        return pd.DataFrame()
    finally:
        db.close()

# Instancia global para reutilización
_global_db_instance = None

def get_database_instance() -> DatabaseConnection:
    """
    Obtiene instancia singleton de conexión a base de datos
    """
    global _global_db_instance

    if _global_db_instance is None:
        _global_db_instance = DatabaseConnection()

    return _global_db_instance

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API de Servicios de Inteligencia Artificial para InnoAd
=======================================================

Esta API proporciona servicios de IA para el análisis predictivo de campañas,
optimización de anuncios y recomendaciones automáticas.

Servicios incluidos:
- Análisis predictivo de ROI de campañas
- Recomendaciones de optimización
- Predicción de CTR y conversiones
- Clustering de audiencias
- Análisis de sentiment de contenido

TAREAS PARA EL EQUIPO DE DESARROLLO:
1. Entrenar modelos con datos reales de campañas
2. Implementar sistema de evaluación de modelos
3. Crear endpoints para análisis en tiempo real
4. Agregar cache de predicciones
5. Implementar sistema de métricas y monitoreo
6. Crear sistema de reentrenamiento automático

Autor: Equipo SENA ADSO
Versión: 1.0.0
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import sys
from datetime import datetime
import traceback
import numpy as np
import pandas as pd

# Agregar el directorio padre al path para importar módulos locales
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.configuracion import get_config
from models.analizador_campanas import AnalizadorCampanas
from models.predictor_rendimiento import PredictorRendimiento
from models.optimizador_anuncios import OptimizadorAnuncios
from utils.logger import get_logger
from utils.database_connection import DatabaseConnection

# ========================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ========================================

app = Flask(__name__)
CORS(app, origins=['http://localhost:4200', 'https://*.railway.app'])

# Configurar logging
logger = get_logger(__name__)

# Cargar configuración
config = get_config()
app.config.update(config.get('api', {}))

# ========================================
# INICIALIZACIÓN DE SERVICIOS DE IA
# ========================================

# Variables globales para servicios de IA
analizador_campanas = None
predictor_rendimiento = None
optimizador_anuncios = None
db_connection = None

def inicializar_servicios_ia():
    """
    Inicializa todos los servicios de IA al arrancar la aplicación

    TODO: Implementar lazy loading de modelos para mejorar tiempo de inicio
    TODO: Agregar verificación de modelos entrenados
    """
    global analizador_campanas, predictor_rendimiento, optimizador_anuncios, db_connection

    try:
        logger.info("🚀 Inicializando servicios de IA...")

        # Inicializar conexión a base de datos
        db_connection = DatabaseConnection()

        # Inicializar analizador de campañas
        analizador_campanas = AnalizadorCampanas()
        logger.info("✅ Analizador de campañas inicializado")

        # Inicializar predictor de rendimiento
        predictor_rendimiento = PredictorRendimiento()
        logger.info("✅ Predictor de rendimiento inicializado")

        # Inicializar optimizador de anuncios
        optimizador_anuncios = OptimizadorAnuncios()
        logger.info("✅ Optimizador de anuncios inicializado")

        logger.info("🎉 Todos los servicios de IA inicializados correctamente")

    except Exception as e:
        logger.error(f"❌ Error inicializando servicios de IA: {e}")
        logger.error(traceback.format_exc())
        raise

# ========================================
# ENDPOINTS DE SALUD Y INFORMACIÓN
# ========================================

@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificación de salud del servicio
    """
    try:
        # Verificar estado de servicios críticos
        estado_servicios = {
            'analizador_campanas': analizador_campanas is not None,
            'predictor_rendimiento': predictor_rendimiento is not None,
            'optimizador_anuncios': optimizador_anuncios is not None,
            'base_datos': db_connection is not None and db_connection.is_connected()
        }

        todos_ok = all(estado_servicios.values())

        return jsonify({
            'status': 'healthy' if todos_ok else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'services': estado_servicios,
            'uptime': 'TODO: implementar cálculo de uptime'
        }), 200 if todos_ok else 503

    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503

@app.route('/api/ia/info', methods=['GET'])
def info_servicios():
    """
    Información detallada sobre los servicios de IA disponibles
    """
    return jsonify({
        'servicios': {
            'analisis_campanas': {
                'descripcion': 'Análisis predictivo de rendimiento de campañas',
                'endpoints': ['/api/ia/analizar-campana', '/api/ia/predecir-roi'],
                'version': '1.0.0'
            },
            'prediccion_rendimiento': {
                'descripcion': 'Predicción de CTR, CPC y conversiones',
                'endpoints': ['/api/ia/predecir-ctr', '/api/ia/predecir-conversiones'],
                'version': '1.0.0'
            },
            'optimizacion_anuncios': {
                'descripcion': 'Recomendaciones de optimización automática',
                'endpoints': ['/api/ia/optimizar-anuncio', '/api/ia/recomendar-mejoras'],
                'version': '1.0.0'
            }
        },
        'modelo_info': {
            'algoritmos': ['RandomForest', 'XGBoost', 'LightGBM'],
            'features_principales': ['presupuesto', 'duracion', 'audiencia_tamaño', 'cpc_objetivo'],
            'metricas_evaluacion': ['MAE', 'RMSE', 'R²', 'Accuracy']
        }
    })

# ========================================
# ENDPOINTS DE ANÁLISIS DE CAMPAÑAS
# ========================================

@app.route('/api/ia/analizar-campana', methods=['POST'])
def analizar_campana():
    """
    Analiza una campaña específica y proporciona insights

    TODO: Validar formato de datos de entrada
    TODO: Implementar cache de resultados
    """
    try:
        datos = request.get_json()
        campana_id = datos.get('campana_id')

        if not campana_id:
            return jsonify({'error': 'ID de campaña requerido'}), 400

        logger.info(f"Analizando campaña ID: {campana_id}")

        # Obtener análisis de la campaña
        resultado = analizador_campanas.analizar_campana(campana_id)

        return jsonify({
            'campana_id': campana_id,
            'analisis': resultado,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"Error analizando campaña: {e}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': str(e),
            'status': 'error'
        }), 500

@app.route('/api/ia/predecir-roi', methods=['POST'])
def predecir_roi():
    """
    Predice el ROI de una campaña basado en sus parámetros

    TODO: Validar rangos de valores de entrada
    TODO: Agregar intervalos de confianza en las predicciones
    """
    try:
        datos = request.get_json()

        # Validar campos requeridos
        campos_requeridos = ['presupuesto', 'duracion_dias', 'plataforma', 'tipo_objetivo']
        campos_faltantes = [campo for campo in campos_requeridos if campo not in datos]

        if campos_faltantes:
            return jsonify({
                'error': f'Campos requeridos faltantes: {", ".join(campos_faltantes)}'
            }), 400

        logger.info(f"Prediciendo ROI para campaña: {datos.get('nombre', 'Sin nombre')}")

        # Realizar predicción
        prediccion = analizador_campanas.predecir_roi(datos)

        return jsonify({
            'prediccion': prediccion,
            'confianza': prediccion.get('confianza', 0.85),
            'recomendaciones': prediccion.get('recomendaciones', []),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"Error prediciendo ROI: {e}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': str(e),
            'status': 'error'
        }), 500

@app.route('/api/ia/entrenar-modelo', methods=['POST'])
def entrenar_modelo():
    """
    Entrena o reentrena los modelos con nuevos datos

    TODO: Implementar entrenamiento asíncrono para modelos grandes
    TODO: Agregar validación de calidad de datos de entrenamiento
    """
    try:
        datos = request.get_json()
        tipo_modelo = datos.get('tipo_modelo', 'todos')
        forzar_reentrenamiento = datos.get('forzar', False)

        logger.info(f"Iniciando entrenamiento de modelo: {tipo_modelo}")

        resultados = {}

        if tipo_modelo in ['campanas', 'todos']:
            metricas = analizador_campanas.entrenar_modelo()
            resultados['campanas'] = metricas

        if tipo_modelo in ['rendimiento', 'todos']:
            metricas = predictor_rendimiento.entrenar_modelo()
            resultados['rendimiento'] = metricas

        if tipo_modelo in ['optimizacion', 'todos']:
            metricas = optimizador_anuncios.entrenar_modelo()
            resultados['optimizacion'] = metricas

        return jsonify({
            'resultados': resultados,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"Error entrenando modelo: {e}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': str(e),
            'status': 'error'
        }), 500

# ========================================
# ENDPOINTS DE PREDICCIÓN DE RENDIMIENTO
# ========================================

@app.route('/api/ia/predecir-ctr', methods=['POST'])
def predecir_ctr():
    """
    Predice el Click-Through Rate (CTR) de un anuncio
    """
    try:
        datos = request.get_json()

        prediccion = predictor_rendimiento.predecir_ctr(datos)

        return jsonify({
            'ctr_predicho': prediccion['ctr'],
            'rango_confianza': prediccion.get('rango', {}),
            'factores_clave': prediccion.get('factores', []),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"Error prediciendo CTR: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/ia/predecir-conversiones', methods=['POST'])
def predecir_conversiones():
    """
    Predice el número de conversiones esperadas
    """
    try:
        datos = request.get_json()

        prediccion = predictor_rendimiento.predecir_conversiones(datos)

        return jsonify({
            'conversiones_predichas': prediccion['conversiones'],
            'tasa_conversion': prediccion.get('tasa', 0),
            'valor_estimado': prediccion.get('valor', 0),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"Error prediciendo conversiones: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

# ========================================
# ENDPOINTS DE OPTIMIZACIÓN
# ========================================

@app.route('/api/ia/optimizar-anuncio', methods=['POST'])
def optimizar_anuncio():
    """
    Proporciona recomendaciones de optimización para un anuncio
    """
    try:
        datos = request.get_json()
        anuncio_id = datos.get('anuncio_id')

        if not anuncio_id:
            return jsonify({'error': 'ID de anuncio requerido'}), 400

        recomendaciones = optimizador_anuncios.optimizar_anuncio(anuncio_id)

        return jsonify({
            'anuncio_id': anuncio_id,
            'recomendaciones': recomendaciones,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"Error optimizando anuncio: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/ia/recomendar-mejoras', methods=['POST'])
def recomendar_mejoras():
    """
    Genera recomendaciones generales de mejora para campañas
    """
    try:
        datos = request.get_json()
        campana_ids = datos.get('campana_ids', [])

        mejoras = optimizador_anuncios.recomendar_mejoras_generales(campana_ids)

        return jsonify({
            'mejoras': mejoras,
            'prioridad': mejoras.get('prioridad', 'media'),
            'impacto_estimado': mejoras.get('impacto', 0),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"Error generando recomendaciones: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

# ========================================
# ENDPOINTS DE ANÁLISIS AVANZADO
# ========================================

@app.route('/api/ia/analisis-audiencia', methods=['POST'])
def analisis_audiencia():
    """
    Realiza clustering y análisis de audiencias

    TODO: Implementar algoritmos de segmentación avanzada
    """
    try:
        datos = request.get_json()

        resultado = analizador_campanas.analizar_audiencia(datos)

        return jsonify({
            'segmentos': resultado.get('segmentos', []),
            'insights': resultado.get('insights', []),
            'recomendaciones_targeting': resultado.get('recomendaciones', []),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"Error analizando audiencia: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

# ========================================
# MANEJO DE ERRORES GLOBAL
# ========================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint no encontrado',
        'message': 'La ruta solicitada no existe',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Error interno del servidor: {error}")
    return jsonify({
        'error': 'Error interno del servidor',
        'message': 'Ha ocurrido un error inesperado',
        'status': 'error'
    }), 500

# ========================================
# FUNCIÓN PRINCIPAL
# ========================================

def main():
    """
    Función principal para ejecutar la API
    """
    try:
        # Inicializar servicios de IA
        inicializar_servicios_ia()

        # Configurar puerto y host
        port = int(os.getenv('PORT', config['api']['port']))
        host = config['api']['host']
        debug = config['api']['debug']

        logger.info(f"🚀 Iniciando API de IA en {host}:{port}")
        logger.info(f"🔧 Modo debug: {debug}")
        logger.info(f"📊 Servicios disponibles: Análisis, Predicción, Optimización")

        # Ejecutar aplicación Flask
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )

    except Exception as e:
        logger.error(f"❌ Error iniciando aplicación: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()

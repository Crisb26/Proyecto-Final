# -*- coding: utf-8 -*-
"""
Configuración centralizada para servicios de IA de InnoAd
=========================================================

Este módulo contiene toda la configuración necesaria para los servicios
de inteligencia artificial, incluyendo modelos, base de datos, APIs y logging.

TAREAS PARA EL EQUIPO DE DESARROLLO:
1. Configurar parámetros óptimos de modelos ML
2. Agregar configuración para diferentes entornos
3. Implementar configuración dinámica desde base de datos
4. Configurar parámetros de cache y optimización
5. Agregar configuración para servicios externos (AWS, etc.)

Autor: Equipo SENA ADSO
Versión: 1.0.0
"""

import os
from pathlib import Path
from typing import Dict, Any

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent.parent.absolute()

# ========================================
# CONFIGURACIÓN DE BASE DE DATOS
# ========================================

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'innoad'),
    'charset': 'utf8mb4',
    'pool_size': 10,
    'max_overflow': 20,
    'pool_timeout': 30,
    'pool_recycle': 3600
}

# ========================================
# CONFIGURACIÓN DE CONEXIÓN CON BACKEND
# ========================================

BACKEND_CONFIG = {
    'usuarios_url': os.getenv('BACKEND_USUARIOS_URL', 'http://localhost:8081/api'),
    'campanas_url': os.getenv('BACKEND_CAMPANAS_URL', 'http://localhost:8082/api'),
    'dispositivos_url': os.getenv('BACKEND_DISPOSITIVOS_URL', 'http://localhost:8086/api'),
    'timeout': 30,
    'retry_attempts': 3,
    'retry_delay': 1,
    'verify_ssl': True
}

# ========================================
# CONFIGURACIÓN DE MODELOS DE IA
# ========================================

MODEL_CONFIG = {
    'analisis_campanas': {
        'algoritmo': 'random_forest',
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'n_jobs': -1,
        'cross_validation_folds': 5
    },
    'prediccion_rendimiento': {
        'algoritmo': 'xgboost',
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 100,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': 42,
        'early_stopping_rounds': 10
    },
    'optimizacion_anuncios': {
        'algoritmo': 'lightgbm',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0,
        'random_state': 42
    },
    'clustering_audiencia': {
        'algoritmo': 'kmeans',
        'n_clusters': 5,
        'random_state': 42,
        'max_iter': 300,
        'n_init': 10
    }
}

# ========================================
# CONFIGURACIÓN DE PROCESAMIENTO DE DATOS
# ========================================

DATA_CONFIG = {
    'batch_size': 1000,
    'max_records_per_query': 10000,
    'cache_ttl': 3600,  # 1 hora en segundos
    'feature_window_days': 90,
    'min_campaign_data_points': 10,
    'outlier_threshold': 3.0,  # Desviaciones estándar
    'missing_value_threshold': 0.3,  # 30% máximo de valores faltantes
    'correlation_threshold': 0.95,  # Para eliminar características correlacionadas
}

# ========================================
# CONFIGURACIÓN DE APIs
# ========================================

API_CONFIG = {
    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 5000)),
    'debug': os.getenv('FLASK_ENV', 'production') != 'production',
    'threaded': True,
    'max_content_length': 16 * 1024 * 1024,  # 16MB
    'jsonify_prettyprint_regular': False
}

# ========================================
# CONFIGURACIÓN DE LOGGING
# ========================================

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        },
        'simple': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': str(BASE_DIR / 'logs' / 'ia_service.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'sklearn': {
            'level': 'WARNING'
        },
        'xgboost': {
            'level': 'WARNING'
        }
    }
}

# ========================================
# CONFIGURACIÓN DE CACHE
# ========================================

CACHE_CONFIG = {
    'type': 'memory',  # memory, redis, file
    'ttl': 3600,
    'max_size': 1000,
    'redis_host': os.getenv('REDIS_HOST', 'localhost'),
    'redis_port': int(os.getenv('REDIS_PORT', 6379)),
    'redis_db': int(os.getenv('REDIS_DB', 0))
}

# ========================================
# CONFIGURACIÓN DE MÉTRICAS
# ========================================

METRICS_CONFIG = {
    'enable_metrics': True,
    'metrics_port': int(os.getenv('METRICS_PORT', 9090)),
    'model_performance_threshold': {
        'mae': 0.1,
        'rmse': 0.15,
        'r2_score': 0.8,
        'accuracy': 0.85
    },
    'alert_thresholds': {
        'prediction_time_ms': 1000,
        'training_time_hours': 2,
        'memory_usage_gb': 4
    }
}

# ========================================
# RUTAS DE ARCHIVOS
# ========================================

PATHS = {
    'models': BASE_DIR / 'models',
    'trained_models': BASE_DIR / 'models' / 'trained',
    'data': BASE_DIR / 'data',
    'processed_data': BASE_DIR / 'data' / 'processed',
    'logs': BASE_DIR / 'logs',
    'temp': BASE_DIR / 'temp',
    'exports': BASE_DIR / 'exports',
    'notebooks': BASE_DIR / 'notebooks'
}

# Crear directorios si no existen
for path in PATHS.values():
    path.mkdir(parents=True, exist_ok=True)

# ========================================
# CONFIGURACIÓN POR ENTORNO
# ========================================

ENVIRONMENT_CONFIG = {
    'development': {
        'debug': True,
        'log_level': 'DEBUG',
        'cache_ttl': 300,  # 5 minutos para desarrollo
        'enable_mock_data': True
    },
    'testing': {
        'debug': False,
        'log_level': 'INFO',
        'database': 'innoad_test',
        'cache_ttl': 60,
        'enable_mock_data': True
    },
    'production': {
        'debug': False,
        'log_level': 'INFO',
        'cache_ttl': 3600,
        'enable_mock_data': False,
        'enable_metrics': True
    }
}

# ========================================
# FUNCIONES DE CONFIGURACIÓN
# ========================================

def get_config(section: str = None) -> Dict[str, Any]:
    """
    Obtiene configuración específica o toda la configuración

    Args:
        section: Sección específica de configuración a obtener

    Returns:
        Dict con la configuración solicitada
    """
    config = {
        'database': DATABASE_CONFIG,
        'backend': BACKEND_CONFIG,
        'models': MODEL_CONFIG,
        'data': DATA_CONFIG,
        'api': API_CONFIG,
        'logging': LOGGING_CONFIG,
        'cache': CACHE_CONFIG,
        'metrics': METRICS_CONFIG,
        'paths': PATHS
    }

    # Aplicar configuración específica del entorno
    env = os.getenv('FLASK_ENV', 'production')
    if env in ENVIRONMENT_CONFIG:
        env_config = ENVIRONMENT_CONFIG[env]
        # Merge configuración del entorno
        for key, value in env_config.items():
            if key in config:
                if isinstance(config[key], dict) and isinstance(value, dict):
                    config[key].update(value)
                else:
                    config[key] = value

    if section:
        return config.get(section, {})

    return config

def get_database_url() -> str:
    """
    Construye URL de conexión a la base de datos
    """
    config = DATABASE_CONFIG
    return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset={config['charset']}"

def get_model_config(model_name: str) -> Dict[str, Any]:
    """
    Obtiene configuración específica de un modelo

    Args:
        model_name: Nombre del modelo

    Returns:
        Dict con configuración del modelo
    """
    return MODEL_CONFIG.get(model_name, {})

# ========================================
# VALIDACIÓN DE CONFIGURACIÓN
# ========================================

def validate_config():
    """
    Valida que la configuración sea correcta

    TODO: Implementar validaciones más robustas
    """
    required_env_vars = ['DB_HOST', 'DB_PASSWORD']

    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(f"Variables de entorno faltantes: {', '.join(missing_vars)}")

    return True

# Validar configuración al importar
try:
    validate_config()
except ValueError as e:
    print(f"⚠️ Advertencia de configuración: {e}")

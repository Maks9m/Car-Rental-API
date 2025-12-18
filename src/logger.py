import logging
import time
import functools
import inspect

from src.config import config

# --- Налаштування логера ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(config.APP_NAME)

# --- Декоратор ---
def log_execution(func):
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        func_name = func.__name__
        _log_start(func_name, args, kwargs)
        
        try:
            result = await func(*args, **kwargs)
            _log_end(func_name, start_time, result)
            return result
        except Exception as e:
            _log_error(func_name, e)
            raise e

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        func_name = func.__name__
        _log_start(func_name, args, kwargs)

        try:
            result = func(*args, **kwargs)
            _log_end(func_name, start_time, result)
            return result
        except Exception as e:
            _log_error(func_name, e)
            raise e

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

# --- Private Helpers ---

def _serialize(data, depth=0, max_depth=3):
    """
    Перетворює дані з захистом від нескінченної рекурсії.
    max_depth=3 означає, що ми заглибимось максимум на 3 рівні вкладеності.
    """
    # 0. Захист від рекурсії
    if depth > max_depth:
        return "..."
    
    # 1. Якщо це список -> рекурсивно обробляємо елементи
    if isinstance(data, list):
        return [_serialize(item, depth + 1, max_depth) for item in data]
    
    # 2. Якщо це Pydantic модель
    if hasattr(data, "model_dump"):
        return _serialize(data.model_dump(), depth, max_depth)
    if hasattr(data, "dict"): 
        return _serialize(data.dict(), depth, max_depth)
        
    # 3. Якщо це SQLAlchemy модель (або інший клас)
    if hasattr(data, "__dict__"):
        obj_dict = data.__dict__.copy()
        obj_dict.pop("_sa_instance_state", None)
        # Передаємо той самий depth, бо ми просто перетворили об'єкт на dict поточного рівня
        return _serialize(obj_dict, depth, max_depth)

    # 4. Якщо це словник
    if isinstance(data, dict):
        return {
            k: _serialize(v, depth + 1, max_depth) 
            for k, v in data.items()
        }

    # 5. Дати та час -> у рядок
    if hasattr(data, "isoformat"):
        return data.isoformat()
    
    # 6. Enum
    if hasattr(data, "value"):
        return data.value

    return data

def _filter_sensitive_data(data):
    """Ховає паролі"""
    SENSITIVE_KEYS = {'password', 'token', 'access_token', 'secret', 'password_hash', 'authorization'}
    
    if isinstance(data, dict):
        return {
            k: ("***" if str(k).lower() in SENSITIVE_KEYS else _filter_sensitive_data(v)) 
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [_filter_sensitive_data(item) for item in data]
    else:
        return data

def _log_start(func_name, args, kwargs):
    # Серіалізуємо вхідні дані
    safe_args = _serialize(list(args))
    safe_kwargs = _filter_sensitive_data(_serialize(kwargs))
    
    args_str = str(safe_args)
    if len(args_str) > 500: 
        args_str = args_str[:500] + "... [truncated]"

    logger.info(f"▶ START '{func_name}' | Args: {args_str} | Kwargs: {safe_kwargs}")

def _log_end(func_name, start_time, result):
    duration = time.time() - start_time
    
    # 1. Серіалізуємо з обмеженням глибини
    serialized_result = _serialize(result)
    
    # 2. Ховаємо паролі
    safe_result = _filter_sensitive_data(serialized_result)
    
    result_str = str(safe_result)
    
    # Обрізаємо занадто довгі відповіді
    if len(result_str) > 1000:
        result_str = result_str[:1000] + " ... [truncated]"
    
    logger.info(f"✅ END '{func_name}' ({duration:.4f}s) | Result: {result_str}")

def _log_error(func_name, error):
    logger.error(f"❌ ERROR '{func_name}': {str(error)}")
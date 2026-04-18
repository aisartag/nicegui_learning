# from core.settings import SettingPaths
from core.logging.logger_settings import LoggerSettings
from core.settings import SettingPaths




def bootstrap() -> bool:
    print('bootstrap senza guard ui')

    logger = LoggerSettings().setup()
    logger.info(f"Inizio bootstrap logging: {logger.name}")

    
    
    try:
        SettingPaths.validate_environment()
    except Exception as e:
        logger.error(f"Errore nella validazione delle cartelle: {e}")   
        return False
    
    return True
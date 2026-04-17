# from core.settings import SettingPaths
from core.logging.logger_settings import LoggerSettings




def bootstrap() -> bool:
    print('bootstrap senza guard ui')

    logger = LoggerSettings().setup()
    logger.info(f"Inizio bootstrap logging: {logger.name}")

    return True
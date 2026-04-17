from core.settings import SettingPaths
from core.logger.logset import LoggerSettings

def bootstrap() -> bool:
    print('bootstrap senza guard ui')

    logger = LoggerSettings().setup()
    logger.info("Inizio bootstrap")


    if not SettingPaths.CONFIG_FILE.exists():
        # Se manca, lo creiamo vuoto o lanciamo errore
        # ProjectPaths.setup_folders()
        logger.error(f"ERRORE CRITICO: Config file: {SettingPaths.CONFIG_FILE} non trovato.")
        # print(f"ERRORE CRITICO: Config file: {SettingPaths.CONFIG_FILE} non trovato.")
        return False
    
    try:
        SettingPaths().validate_environment()
    except Exception as e:
        logger.error(e.args[0])
        return False




    return True
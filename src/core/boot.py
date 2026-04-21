from core.paths import ProjectPaths
from core.log_loader import setup_logging



def bootstrap() -> bool:

    error = ProjectPaths.ensure_dirs()
    if error:
       print(error)
       return False

    error =setup_logging()
    if error:
       print(error)
       return False

    return True

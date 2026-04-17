from pathlib import Path


class SettingPaths:
    # Percorsi base (Calcolati rispetto a questo file)
    ROOT = Path(__file__).resolve().parent.parent.parent

    SRC = ROOT / "src"
    ASSETS = ROOT / "assets"
    CONFIG_FILE = ROOT / "config.json"
  
    # File critici che DEVONO esserci
    REQUIRED_FILES = [CONFIG_FILE, ASSETS / "logo.png"]

    @classmethod
    def validate_environment(cls):
        """Verifica la presenza di cartelle e file critici."""
        for folder in [cls.ASSETS]:
            if not folder.exists():
                raise FileNotFoundError(f"Cartella '{folder.name}' non trovata")
    
    @classmethod
    def get_asset(cls, filename: str) -> str:
        """Ritorna il percorso stringa per NiceGUI."""
        target = cls.ASSETS / filename
        return str(target) if target.exists() else ""
              
       

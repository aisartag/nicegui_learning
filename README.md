# Posizione delle risorse

## ASSETS risorsa interna
get_internal_path(relative_path: str):
		"""la posizione delle risorse interne dipende se siamo in ambiente native o in ambiente web"""
		if hasattr(sys, '_MEIPASS'):
			return Path(sys._MEIPASS) / relative_path  # type: ignore
		return Path(__file__).parent / relative_path

## logs risorsa esterna



# Installer
1. Inno Setup (Il più consigliato per Python/NiceGUI) Sito ufficiale: jrsoftware.org/isinfo.php
2. PyInstaller Bundle OS (Opzione base)
3. Advanced Installer (Interfaccia Grafica Moderna) Sito ufficiale: advancedinstaller.com
4. NSIS (Nullsoft Scriptable Install System)


pyinstaller --name "DarkSight" --onedir --windowed -p "src" --add-data="app/assets;assets" app/run_native.py 
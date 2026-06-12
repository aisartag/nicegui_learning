# Usa l'immagine ufficiale di uv basata su Python slim
FROM ghcr.io/astral-sh/uv:python3.14-alpine

# Imposta la cartella di lavoro nel container
WORKDIR /nicegui_learning

# Abilita l'ottimizzazione del caching dei layer di Docker per uv
ENV UV_COMPILE_BYTECODE=1

# Copia solo i file di configurazione per sfruttare la cache di Docker
COPY pyproject.toml uv.lock ./

# Installa le dipendenze SENZA installare il progetto corrente e senza dev dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copia il resto del codice della tua applicazione
COPY app ./app/

# IMPORTANTE: Aggiungi --no-sync per impedire a uv run di reinstallare i dev packages all'avvio
CMD ["uv", "run", "--no-sync", "app/run_web.py"]
 
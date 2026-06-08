# Appunti su docker
docker compose --env-file .env.docker up   # avvia il docker-compose

docker exec -it nicegui_learning_db_container psql -U user -d nicegui_learning_db  # per entrare in psql
 
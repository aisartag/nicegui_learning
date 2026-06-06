# DA NON FARE ASSOLUTAMENTE IN NICEGUI
# def mio_layout_sincrono():
#     # Questo distrugge l'Event Loop globale di NiceGUI e solleva un RuntimeError!
#     user = asyncio.run(db.get_user(user_id))


# import asyncio

# def mio_layout_sincrono():
#     try:
#         # Recupera l'event loop già attivo di NiceGUI
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         # Se non c'è un loop attivo (raro in NiceGUI, ma protettivo)
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#     # Esegue la funzione async bloccando il thread SOLO per questa operazione sincrona
#     # Nota: in contesti ad alto traffico può rallentare, ma è tecnicamente corretto
#     user_state = loop.run_until_complete(self.user_repo.get_user_by_id(user_id))
#     return user_state

# from asgiref.sync import async_to_sync

# def mio_layout_sincrono():
#     # Trasforma temporaneamente la tua funzione async in una sincrona callable
#     fetch_user_sync = async_to_sync(self.user_repo.get_user_by_id)

#     # La chiami normalmente senza await
#     user_state = fetch_user_sync(user_id)
#     return user_state

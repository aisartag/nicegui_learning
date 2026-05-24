# services/crypto_service.py
import bcrypt


class CryptoService:
	@staticmethod
	def hash_password(password: str) -> str:
		"""Genera un hash sicuro usando direttamente la libreria bcrypt."""
		# 1. Convertiamo la stringa della password in byte
		password_bytes = password.encode('utf-8')

		# 2. Generiamo il salt e creiamo l'hash
		salt = bcrypt.gensalt()
		hashed_bytes = bcrypt.hashpw(password_bytes, salt)

		# 3. Trasformiamo l'hash finale in stringa per salvarlo nel DB
		return hashed_bytes.decode('utf-8')

	@staticmethod
	def verify_password(plain_password: str, hashed_password: str) -> bool:
		"""Verifica se la password in chiaro corrisponde all'hash memorizzato."""
		try:
			# Convertiamo sia la password in chiaro sia l'hash in byte
			plain_bytes = plain_password.encode('utf-8')
			hashed_bytes = hashed_password.encode('utf-8')

			# La libreria controlla internamente la corrispondenza
			return bcrypt.checkpw(plain_bytes, hashed_bytes)
		except Exception:
			return False

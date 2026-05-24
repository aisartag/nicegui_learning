from database.engine import Base
from models.profile import Profile
from models.user import User

# In questo modo, quando qualcuno scriverà "import models",
# Python leggerà questo file e caricherà sia User che Profile nella Base.

# Spiega a Ruff (e a Python) cosa è disponibile per l'esterno
__all__ = ['Base', 'User', 'Profile']

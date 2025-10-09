"""
Repository Implementation: Memory User Repository
Implementación que guarda usuarios en memoria (sesión).
"""

from typing import Dict, Optional
from src.domain.entities import User
from src.domain.repositories import UserRepository


class MemoryUserRepository(UserRepository):
    """
    Implementación del UserRepository que guarda en memoria.

    Esta implementación mantiene los usuarios en un diccionario
    en memoria. Los datos se pierden al reiniciar la aplicación.

    Útil para: desarrollo, testing, sesiones temporales.
    Para producción: usar implementación con base de datos real.
    """

    def __init__(self):
        """Inicializa el repositorio con diccionario vacío."""
        self._users: Dict[str, User] = {}
        print("✅ Memory User Repository initialized")

    def save(self, user: User) -> User:
        """
        Guardar un usuario.

        Args:
            user: Usuario a guardar

        Returns:
            User: Usuario guardado
        """
        self._users[user.user_id] = user
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        """
        Buscar usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            Optional[User]: Usuario encontrado o None
        """
        return self._users.get(user_id)

    def update(self, user: User) -> User:
        """
        Actualizar un usuario.

        Args:
            user: Usuario con datos actualizados

        Returns:
            User: Usuario actualizado

        Raises:
            ValueError: Si el usuario no existe
        """
        if user.user_id not in self._users:
            raise ValueError(f"User {user.user_id} not found")

        self._users[user.user_id] = user
        return user

    def delete(self, user_id: str) -> bool:
        """
        Eliminar un usuario.

        Args:
            user_id: ID del usuario a eliminar

        Returns:
            bool: True si fue eliminado, False si no existía
        """
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def exists(self, user_id: str) -> bool:
        """
        Verificar si un usuario existe.

        Args:
            user_id: ID del usuario

        Returns:
            bool: True si existe, False si no
        """
        return user_id in self._users

    def clear(self) -> None:
        """Limpiar todos los usuarios (útil para testing)."""
        self._users.clear()

    def count(self) -> int:
        """Contar usuarios almacenados."""
        return len(self._users)
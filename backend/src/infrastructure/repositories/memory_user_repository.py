"""
Repository Implementation: Memory User Repository
Implementacion que guarda usuarios en memoria (sesion).
"""

from typing import Dict, Optional
from src.domain.entities import User
from src.domain.repositories import UserRepository


class MemoryUserRepository(UserRepository):
    """
    Implementacion del UserRepository que guarda en memoria.
    Los datos se pierden al reiniciar la aplicacion.
    """

    def __init__(self):
        self._users: Dict[str, User] = {}
        print("Memory User Repository initialized")

    def save(self, user: User) -> User:
        self._users[user.user_id] = user
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def update(self, user: User) -> User:
        if user.user_id not in self._users:
            raise ValueError(f"User {user.user_id} not found")
        self._users[user.user_id] = user
        return user

    def delete(self, user_id: str) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def exists(self, user_id: str) -> bool:
        return user_id in self._users

    def clear(self) -> None:
        self._users.clear()

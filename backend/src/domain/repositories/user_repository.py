"""
Repository Interface: User Repository
Define el contrato para acceso a datos de usuarios.
"""

from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities import User


class UserRepository(ABC):
    """Interface del Repository de Usuarios."""

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def exists(self, user_id: str) -> bool:
        pass
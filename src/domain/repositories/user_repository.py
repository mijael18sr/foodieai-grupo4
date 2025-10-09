"""
Repository Interface: User Repository
Define el contrato para acceso a datos de usuarios.
"""

from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities import User


class UserRepository(ABC):
    """
    Interface del Repository de Usuarios.

    Define operaciones CRUD básicas para usuarios.
    En este sistema, los usuarios son temporales (sesión),
    pero la interface permite escalar a persistencia real.
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """
        Guardar un usuario.

        Args:
            user: Usuario a guardar

        Returns:
            User: Usuario guardado
        """
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        """
        Buscar usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            Optional[User]: Usuario encontrado o None
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """
        Actualizar un usuario.

        Args:
            user: Usuario con datos actualizados

        Returns:
            User: Usuario actualizado
        """
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """
        Eliminar un usuario.

        Args:
            user_id: ID del usuario a eliminar

        Returns:
            bool: True si fue eliminado, False si no existía
        """
        pass

    @abstractmethod
    def exists(self, user_id: str) -> bool:
        """
        Verificar si un usuario existe.

        Args:
            user_id: ID del usuario

        Returns:
            bool: True si existe, False si no
        """
        pass
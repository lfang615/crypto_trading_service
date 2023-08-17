from abc import ABC, abstractmethod
from typing import Optional, TypeVar

T = TypeVar("T")

class BaseRepository(ABC):

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def update(self, id: str, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass

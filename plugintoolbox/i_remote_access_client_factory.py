from abc import ABC, abstractmethod

from .i_remote_access_client import IRemoteAccessClient


class IRemoteAccessClientFactory(ABC):
    @abstractmethod
    def create(self, **kwargs) -> IRemoteAccessClient:
        pass

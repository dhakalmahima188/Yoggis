from abc import ABC
from storages.backends.azure_storage import AzureStorage
import os


class AzureMediaStorage(AzureStorage, ABC):
    account_name = 'hackaweek'
    account_key = '**'
    azure_container = 'media'
    expiration_secs = None

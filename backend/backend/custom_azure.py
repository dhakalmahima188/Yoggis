from abc import ABC
from storages.backends.azure_storage import AzureStorage
import os


class AzureMediaStorage(AzureStorage, ABC):
    account_name = 'hackaweek'
    account_key = '3SMBil+xGbnxM5a7cWxelN8XdYUX+BQPunsvO3msaObuko/HueBz0V/sjLe7qEE+hIkaIix355k/+AStM5mNvg=='
    azure_container = 'media'
    expiration_secs = None
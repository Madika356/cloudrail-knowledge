from typing import Optional, List

from cloudrail.knowledge.context.azure.azure_resources.app_service.azure_ftps_state import FtpsState
from cloudrail.knowledge.context.azure.azure_resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.azure_resources.constants.azure_resource_type import AzureResourceType


class AzureAppServiceConfig(AzureResource):
    """
        Attributes:
            name: The name of the AppService to which this config belongs
            ftps_state: The FTPS state defined in this config. Either AllAllowed, FTPSOnly or Disabled
    """
    def __init__(self, subscription_id: str, resource_group_name: str, location: str, name: str, ftps_state: FtpsState) -> None:
        super().__init__(subscription_id, resource_group_name, location,
                         'App Service Config', AzureResourceType.NONE)
        self.name: str = name
        self.ftps_state: FtpsState = ftps_state
        self.with_aliases(name)

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return False

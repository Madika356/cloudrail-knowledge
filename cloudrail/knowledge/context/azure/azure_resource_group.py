from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureResourceGroup(AzureResource):
    """
        Attributes:
            resource_group_id: Resource group ID.
    """

    def __init__(self, resource_group_id: str) -> None:
        super().__init__(AzureResourceType.AZURERM_RESOURCE_GROUP)
        self.resource_group_id: str = resource_group_id

    def get_keys(self) -> List[str]:
        return [self.resource_group_id]

    def get_id(self) -> str:
        return self.resource_group_id

    def get_name(self) -> str:
        return self.resource_group_name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass  # todo

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return True

from typing import List

from cloudrail.knowledge.context.aws.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class DirectoryService(NetworkEntity):

    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 directory_id: str,
                 vpc_id: str,
                 directory_type: str,
                 vpc_config: NetworkConfiguration):
        super().__init__(name, account, region, AwsServiceName.AWS_DIRECTORY_SERVICE_DIRECTORY)
        self.name: str = name
        self.directory_id: str = directory_id
        self.vpc_id: str = vpc_id
        self.directory_type: str = directory_type
        self.vpc_config: NetworkConfiguration = vpc_config
        self.arn: str = f'arn:aws:clouddirectory:{self.region}:{self.account}:directory/{self.directory_id}'
        self.security_group_controller: SecurityGroup = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_id(self) -> str:
        return self.directory_id

    def get_arn(self) -> str:
        return self.arn

    def get_name(self) -> str:
        return self.name

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [NetworkConfiguration(self.vpc_config.assign_public_ip, self.vpc_config.security_groups_ids, self.vpc_config.subnet_list_ids)]

    def get_cloud_resource_url(self) -> str:
        return '{0}directoryservicev2/home?region={1}#!/directories/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.directory_id)

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Directory'
        else:
            return 'Directories'

    @property
    def is_tagable(self) -> bool:
        return True

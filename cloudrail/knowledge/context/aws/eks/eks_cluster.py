from typing import List, Optional

from cloudrail.knowledge.context.aws.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity


class EksCluster(NetworkEntity, INetworkConfiguration):
    def __init__(self,
                 name: str,
                 arn: str,
                 role_arn: str,
                 endpoint: str,
                 security_group_ids: List[str],
                 cluster_security_group_id: Optional[str],
                 subnet_ids: List[str],
                 endpoint_public_access: bool,
                 endpoint_private_access: bool,
                 public_access_cidrs: List[str],
                 account: str,
                 region: str):
        super().__init__(name, account, region, AwsServiceName.AWS_EKS_CLUSTER)
        self.cluster_security_group_id: Optional[str] = cluster_security_group_id
        self.public_access_cidrs: List[str] = public_access_cidrs
        self.endpoint_private_access: bool = endpoint_private_access
        self.endpoint_public_access: bool = endpoint_public_access
        self.role_arn: str = role_arn
        self.arn: str = arn
        self.endpoint: str = endpoint
        security_groups = security_group_ids
        if cluster_security_group_id:
            security_groups.append(cluster_security_group_id)
        self._network_configuration: NetworkConfiguration = NetworkConfiguration(endpoint_public_access, security_groups, subnet_ids)
        self.port: int = 443

        self.security_group_allowing_public_access: Optional[SecurityGroup] = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_id(self) -> str:
        return self.arn

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [self._network_configuration]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'EKS cluster'
        else:
            return 'EKS clusters'

    def get_cloud_resource_url(self) -> str:
        return '{0}eks/home?region={1}#/clusters/{2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.name)

    def get_arn(self) -> str:
        return self.arn

    @property
    def is_tagable(self) -> bool:
        return True

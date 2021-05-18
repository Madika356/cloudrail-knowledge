from typing import List, Optional

from cloudrail.knowledge.context.aws.indirect_public_connection_data import IndirectPublicConnectionData
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.es.elastic_search_domain_policy import ElasticSearchDomainPolicy
from cloudrail.knowledge.context.aws.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity


class ElasticSearchDomain(NetworkEntity, INetworkConfiguration):

    def __init__(self,
                 domain_id: str,
                 domain_name: str,
                 arn: str,
                 enforce_https: bool,
                 subnet_ids: Optional[List[str]],
                 security_group_ids: Optional[List[str]],
                 encrypt_at_rest_state: bool,
                 encrypt_node_to_node_state: bool,
                 account: str,
                 region: str):
        """
        `ElasticSearch Domain` can either be `Publicly Accessible` and not in any VPC, or it can be `Publicly In-Accessible` if its in a VPC.
        Subsequently, if an `ElasticSearch Domain` does not belong to a subnet then it means it is can only be accessed from within the VPC.
        """
        self.encrypt_at_rest_state: bool = encrypt_at_rest_state
        self.encrypt_node_to_node_state: bool = encrypt_node_to_node_state

        super().__init__(domain_name, account, region, AwsServiceName.AWS_ELASTIC_SEARCH_DOMAIN)
        self.domain_id: str = domain_id
        self.arn: str = arn
        self._network_configuration: NetworkConfiguration = NetworkConfiguration(False, security_group_ids, subnet_ids)
        self.is_public: bool = subnet_ids is None
        self.is_in_vpc: bool = not self.is_public
        self.ports: List[int] = [443]
        if not enforce_https:
            self.ports.append(80)
        self.policy: ElasticSearchDomainPolicy = None

        self.indirect_public_connection_data: Optional[IndirectPublicConnectionData] = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_id(self) -> str:
        return self.domain_id

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [self._network_configuration]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ElasticSearch Domain'
        else:
            return 'ElasticSearch Domains'

    def get_cloud_resource_url(self) -> str:
        return '{0}es/home?region={1}#domain:resource={2};action=dashboard' \
            .format(self.AWS_CONSOLE_URL, self.region, self.name)

    @property
    def is_tagable(self) -> bool:
        return True

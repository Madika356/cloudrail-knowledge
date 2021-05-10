from typing import List, Dict, Optional

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.utils.connection_utils import ConnectionData, get_allowing_indirect_public_access_on_ports
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class IndirectPublicAccessElasticSearchRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'indirect_public_access_elastic_search_rule'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for es_domain in [es for es in env_context.elastic_search_domains if es.is_in_vpc]:
            violation_data: Optional[ConnectionData] = get_allowing_indirect_public_access_on_ports(es_domain, es_domain.ports)
            if violation_data:
                issues.append(
                    Issue(
                        f"~Internet~. "
                        f"Instance `{violation_data.target_instance.owner.get_friendly_name()}"
                        f"` resides in subnet(s) that are routable to internet gateway. "
                        f"Instance has public IP address. "
                        f"Instance accepts incoming traffic on port 443. "
                        f"~Instance `{violation_data.target_instance.owner.get_friendly_name()}`~. "
                        f"{es_domain.get_type()} `{es_domain.get_friendly_name()}` is on Vpc "
                        f"`{es_domain.network_resource.vpc.get_friendly_name()}`. "
                        f"{es_domain.get_type()} is not publically accessible and "
                        f"uses subnets `{', '.join([x.get_friendly_name() for x in es_domain.network_resource.subnets])}`. "
                        f"{es_domain.get_type()} resides in same subnet as Instance"
                        f"`{violation_data.target_instance.owner.get_friendly_name()}`. "
                        f"{es_domain.get_type()} uses Network ACL's "
                        f"`{', '.join([x.network_acl.get_friendly_name() for x in es_domain.network_resource.subnets])}`. "
                        f"{es_domain.get_type()} is indirectly accessible from instance "
                        f"`{violation_data.target_instance.owner.get_friendly_name()}`. "
                        f"~{es_domain.get_type()} `{es_domain.get_friendly_name()}`~"
                        , es_domain, violation_data.security_group))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.elastic_search_domains)

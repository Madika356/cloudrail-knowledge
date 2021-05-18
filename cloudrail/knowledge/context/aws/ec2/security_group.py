import copy
from typing import List, Set

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.ec2.security_group_rule import SecurityGroupRule, SecurityGroupRulePropertyType
from cloudrail.knowledge.utils.range_util import get_range_numbers_overlap
from cloudrail.knowledge.utils.utils import get_overlap_cidr


class SecurityGroup(AwsResource):

    def __init__(self, security_group_id: str, region: str, account: str,
                 name: str, vpc_id: str, is_default: bool, has_description: bool):
        super().__init__(account, region, AwsServiceName.AWS_SECURITY_GROUP)
        self.security_group_id: str = security_group_id
        self.name: str = name
        self.vpc_id: str = vpc_id
        self.inbound_permissions: List[SecurityGroupRule] = []
        self.outbound_permissions: List[SecurityGroupRule] = []
        self.is_default = is_default
        self.vpc: 'Vpc' = None
        self.aliases.add(security_group_id)
        self.has_description: bool = has_description
        self.used_by: Set[AwsResource] = set()

    def get_keys(self) -> List[str]:
        return [self.security_group_id]

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.security_group_id

    def get_arn(self) -> str:
        pass

    def get_extra_data(self) -> str:
        vpc_id = 'vpc_id: {}'.format(self.vpc_id) if self.vpc_id else ''
        is_default = 'is_default: {}'.format(self.is_default) if self.is_default else ''

        return ', '.join([vpc_id, is_default])

    @staticmethod
    def get_rule_matches(sg_rules1: List[SecurityGroupRule], sg_rules2: List[SecurityGroupRule]) -> List[SecurityGroupRule]:
        rules: List[SecurityGroupRule] = []
        for rule1 in sg_rules1:
            for rule2 in sg_rules2:
                if rule1.is_match(rule2):
                    copy_rule: SecurityGroupRule = copy.deepcopy(rule1)
                    from_port, to_port = get_range_numbers_overlap(rule1.get_ports_range(), rule2.get_ports_range())
                    if from_port != -1 and to_port != -1:
                        copy_rule.from_port = from_port
                        copy_rule.to_port = to_port
                        if rule1.property_type == SecurityGroupRulePropertyType.IP_RANGES:
                            for ip_net in get_overlap_cidr(rule1.property_value, rule2.property_value).iter_cidrs():
                                c_rule: SecurityGroupRule = copy.deepcopy(copy_rule)
                                c_rule.property_value = str(ip_net)
                                rules.append(c_rule)
                        else:
                            rules.append(copy_rule)
        return rules

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Security group'
        else:
            return 'Security groups'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#SecurityGroup:groupId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.security_group_id)

    @property
    def is_tagable(self) -> bool:
        return True

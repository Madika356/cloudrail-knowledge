from typing import List
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class CloudHsmV2Hsm(AwsResource):

    def __init__(self,
                 cluster_id: str,
                 hsm_id: str,
                 subnet_id: str,
                 availability_zone: str,
                 hsm_state: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_CLOUDHSM_V_2_HSM)
        self.cluster_id: str = cluster_id
        self.hsm_id: str = hsm_id
        self.subnet_id: str = subnet_id
        self.hsm_state: str = hsm_state
        self.availability_zone: str = availability_zone

    def get_keys(self) -> List[str]:
        return [self.hsm_id]

    def get_id(self) -> str:
        return self.hsm_id

    def get_arn(self) -> str:
        pass

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudHSM'
        else:
            return 'CloudHSMs'

    def get_cloud_resource_url(self) -> str:
        return '{0}cloudhsm/home?region={1}#/clusters/{2}/'\
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_id)

    @property
    def is_tagable(self) -> bool:
        return False

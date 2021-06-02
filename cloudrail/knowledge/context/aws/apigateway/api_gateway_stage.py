from typing import List
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class ApiGatewayStage(AwsResource):
    """
        Attributes:
            api_gw_id: The ID of the REST API Gateway.
            stage_name: The name of the stage.
            xray_tracing_enabled: An indication if active tracing with X-ray is enabled.
    """
    def __init__(self,
                 account:str,
                 region: str,
                 api_gw_id: str,
                 stage_name: str,
                 xray_tracing_enabled: bool):
        super().__init__(account, region, AwsServiceName.AWS_API_GATEWAY_STAGE)
        self.api_gw_id: str = api_gw_id
        self.stage_name: str = stage_name
        self.xray_tracing_enabled: bool = xray_tracing_enabled

    def get_keys(self) -> List[str]:
        return [self.api_gw_id]

    def get_id(self) -> str:
        return self.api_gw_id

    def get_name(self) -> str:
        return self.stage_name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API stage'
        else:
            return 'API stages'

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}apigateway/home?region={1}#/apis/{2}/stages/{3}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.api_gw_id, self.stage_name)

    @property
    def is_tagable(self) -> bool:
        return True
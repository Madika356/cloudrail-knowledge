from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.webapp.azure_ftps_state import FtpsState
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AppServiceFtpsRequiredRule(AzureBaseRule):
    def get_id(self) -> str:
        return 'non_car_azure_app_service_ftps_required'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for app_service in env_context.app_services:
            if app_service.ftps_state == FtpsState.ALL_ALLOWED:
                issues.append(
                    Issue(
                        f'~{app_service.get_type()}~. '
                        f'The web app `{app_service.get_friendly_name()}` is not enforcing FTPS only or does not have FTP disabled',
                        app_service,
                        app_service))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.app_services)

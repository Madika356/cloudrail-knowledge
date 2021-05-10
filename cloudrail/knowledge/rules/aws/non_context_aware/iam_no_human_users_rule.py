from typing import Dict, List
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class IamNoHumanUsersRule(AwsBaseRule):

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues_list: List[Issue] = []
        for user in env_context.users:
            if any(user.name == login_profile.name and user.account == login_profile.account for login_profile in env_context.users_login_profile):
                issues_list.append(Issue(f'The {user.get_type()} `{user.get_friendly_name()}` has console access, '
                                         f'and so is considered human', user, user))
        return issues_list

    def get_id(self) -> str:
        return "non_car_iam_no_human_users"

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.users)

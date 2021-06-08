from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureS3BucketObjectsEncryptedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'not_car_s3_bucket_object_encrypt_at_rest'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for s3_bucket_object in env_context.s3_bucket_objects:
            if not s3_bucket_object.encrypted and not s3_bucket_object.owning_bucket.is_inbound_public():
                issues.append(
                    Issue(
                        f'The {s3_bucket_object.get_type()} `{s3_bucket_object.get_friendly_name()}` '
                        f'is not set to be encrypted at rest', s3_bucket_object, s3_bucket_object))

        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.s3_bucket_objects)

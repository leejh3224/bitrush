import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration


def init_sentry():
    sentry_sdk.init(
        dsn="https://f2b6cfd094824b53aa911ddf7a191231@o1078939.ingest.sentry.io/6083450",
        integrations=[AwsLambdaIntegration()],
        traces_sample_rate=1.0
    )


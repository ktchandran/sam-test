import connexion
import awsgi
import boto3
import os


def post_greeting() -> str:
    # client = boto3.client('appconfig')
    # res = client.get_configuration(
    #     ClientConfigurationVersion='0',
    #     Application='MyTestApplication',
    #     Environment='DevEnvironment',
    #     Configuration='DevConfig',
    #     ClientId='dev'
    # )
    # config = res['Content'].read()
    # return json.loads(config.decode("utf-8"))
    return f"{os.environ.get('APP_ENV')} environment"

def post_greeting2() -> str:
    return 'Hello, world2'

app = connexion.FlaskApp(__name__)
app.add_api('openapi.yaml', arguments={'title': 'Hello World Example'})
# app.run()
def lambda_handler(event, context):
    return awsgi.response(app.app, event, context)

from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_lambda, 
    aws_iot, 
    aws_iam
)
from constructs import Construct

class IoTTriggerLambdaDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.build_lambda()
        self.create_IoT_rule()
        self.configure_lambda_permission()

    def build_lambda(self):
        self.lambda_function = aws_lambda.Function(
            scope=self, 
            id="IoTTriggeredLambda", 
            function_name="IoTTriggeredLambda", 
            code=aws_lambda.Code.from_asset(
                path="lib"
            ), 
            handler="handler.lambda_handler", 
            runtime=aws_lambda.Runtime.PYTHON_3_12
        )
        self.lambda_function.apply_removal_policy(RemovalPolicy.DESTROY)
        
    def create_IoT_rule(self):
        self.iot_rule = aws_iot.CfnTopicRule(
            scope=self, 
            id="IOTTriggerLambdaDemoRule",
            rule_name="IOTTriggerLambdaDemoRule",
            topic_rule_payload=aws_iot.CfnTopicRule.TopicRulePayloadProperty(
                actions = [aws_iot.CfnTopicRule.ActionProperty(
                    lambda_ = aws_iot.CfnTopicRule.LambdaActionProperty(
                        function_arn=self.lambda_function.function_arn
                    )
                )], 
                sql="SELECT topic(2) as region, * FROM 'temperature/#' WHERE temperature > 35",
                aws_iot_sql_version = "2016-03-23", 
                rule_disabled=False
            )
        )
        self.iot_rule.apply_removal_policy(RemovalPolicy.DESTROY)
        
        
    def configure_lambda_permission(self):
        self.lambda_function.add_permission(
            scope=self,
            id="IOTTriggerLambdaDemoRulePermission", 
            principal=aws_iam.ServicePrincipal("iot.amazonaws.com"),
            source_arn=self.iot_rule.attr_arn,
            action="lambda:InvokeFunction"
        )
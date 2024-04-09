import aws_cdk as core
import aws_cdk.assertions as assertions

from io_t_trigger_lambda_demo.io_t_trigger_lambda_demo_stack import IoTTriggerLambdaDemoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in io_t_trigger_lambda_demo/io_t_trigger_lambda_demo_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = IoTTriggerLambdaDemoStack(app, "io-t-trigger-lambda-demo")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

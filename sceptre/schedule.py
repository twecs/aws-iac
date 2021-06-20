import json


def sceptre_handler(
        sceptre_user_data,
    ):
    function_input = {
        'amount': sceptre_user_data['wise']['amount'],
        'amount_side': sceptre_user_data['wise']['amount_side'],
        'reference': sceptre_user_data['wise']['reference'],
        'source_currency': sceptre_user_data['wise']['source_currency'],
        'target_currency': sceptre_user_data['wise']['target_currency'],
    }

    function_input_str = json.dumps(
        obj=function_input,
        indent=None,
    )

    template = {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Description': 'twecs Wise currency exchange schedule',
        'Parameters': {
            'FunctionArn': {
                'Description': 'ARN of the Lambda function to invoke.',
                'Type': 'String',
            },
            'ScheduleExpression': {
                'Description': 'EventBridge rule schedule expression.',
                'Type': 'String',
            },
            'State': {
                'AllowedValues': [
                    'DISABLED',
                    'ENABLED',
                ],
                'Description': 'Whether to schedule currency exchanges.',
                'Type': 'String',
            },
        },
        'Resources': {
            'Permission': {
                'Properties': {
                    'Action': 'lambda:InvokeFunction',
                    'FunctionName': {
                        'Ref': 'FunctionArn',
                    },
                    'Principal': 'events.amazonaws.com',
                    'SourceArn': {
                        'Fn::GetAtt': [
                            'Rule',
                            'Arn',
                        ],
                    },
                },
                'Type': 'AWS::Lambda::Permission',
            },
            'Rule': {
                'Properties': {
                    'ScheduleExpression': {
                        'Ref': 'ScheduleExpression',
                    },
                    'State': {
                        'Ref': 'State',
                    },
                    'Targets': [
                        {
                            'Arn': {
                                'Ref': 'FunctionArn',
                            },
                            'Id': 'function',
                            'Input': function_input_str,
                        },
                    ],
                },
                'Type': 'AWS::Events::Rule',
            },
        },
    }

    template_str = json.dumps(
        obj=template,
        indent=None,
    )

    return template_str

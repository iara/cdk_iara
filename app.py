#!/usr/bin/env python3
import os
from typing_extensions import runtime

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_kms as kms
from aws_cdk import aws_sqs as sqs
from aws_cdk import aws_s3_notifications as notifications
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as sns_sub
import aws_cdk.aws_lambda as lambda_    
from aws_cdk.aws_lambda_python import PythonFunction


import sys
sys.path.insert(0, 'lambdas')

from lambdas.tota import *


from cdk_iara.cdk_iara_stack import CdkIaraStack


app = core.App()
stack = CdkIaraStack(app, "CdkIaraStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=core.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

key_kms = kms.Key(stack, "chave_ada").from_key_arn(stack,"ada-key-kms","arn:aws:kms:us-east-1:729557758924:key/619eee2d-09f1-4858-8872-fbc0e9b9b32c")
s3_bucket1 = s3.Bucket(stack, "bucket_benoit_id", bucket_name="benoit-leao", encryption_key=key_kms)
sqs_ada = sqs.Queue(stack,"sql-maleao",  queue_name="filaada") 

notification_sqs = notifications.SqsDestination(sqs_ada)

s3_bucket1.add_event_notification(s3.EventType.OBJECT_CREATED, notification_sqs)

# s3_bucket1.add_event_notification(x, y, z)

PythonFunction(stack, "pyALeo", entry="lambdas", 
                index="tota.py", 
                handler="main", 
                runtime=lambda_.Runtime.PYTHON_3_6
                )

#s3_bucket2 = s3.Bucket(stack, "bucket_aleo_id", bucket_name="aleo-leao", encryption_key=key_kms)

#sns_notify = sns.Topic(stack, "sns-aleo", topic_name="chazinho-da-leo")

#notification_sns = notifications.SnsDestination(sns_notify)

#s3_bucket2.add_event_notification(s3.EventType.OBJECT_CREATED, notification_sns)

#subinscricao_iara = sns_sub.EmailSubscription("iaramirandaprates@gmail.com")
#sns_notify.add_subscription(subinscricao_iara)


app.synth()

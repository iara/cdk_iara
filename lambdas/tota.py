import boto3
import botocore
import json
def download_file_lambda(s3, bucketname, filename):
    try:
        s3.Bucket(bucketname).download_file(filename, '/tmp/' + filename)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def n_guests(filepath, quantity):
    header = 1
    with open(filepath, 'r') as reader:
            line = reader.readline()
            while line != '':  # The EOF char is an empty string
                line = reader.readline()
                quantity = quantity + 1
    quantity = quantity - header
    return quantity


def create_topic(name):
    sns = boto3.resource("sns")
    topic = sns.create_topic(Name=name)
    return topic


def subscribe(topic, protocol, endpoint):
    subscription = topic.subscribe(Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
    return subscription


def publish_message(topic, message):
    response = topic.publish(Message=message)
    message_id = response['MessageId']
    return message_id


def main(event, context):
    print("ENTRANDO NO LAMDA BOTO")
    sqs = boto3.resource('sqs')
    sns = boto3.client('sns')

    queue = sqs.get_queue_by_name(QueueName='filaada')

    # Process messages by printing out body and optional author name
    for message in queue.receive_messages(MessageAttributeNames=['Author']):
        dicionary = json.loads('{0}'.format(message.body))
        
        file_name = dicionary["Records"][0]["s3"]["object"]["key"]
        bucket_name = dicionary["Records"][0]["s3"]["bucket"]["name"]

        s3_resource = boto3.resource('s3')

        download_file_lambda(s3_resource, bucket_name, file_name)

        guests = n_guests('/tmp/' + file_name, 0)
        print(guests)

        topic = create_topic("chazinho-da-leo")

        email = "iaramirandaprates@gmail.com"
        email_sub = subscribe(topic, "email", email)

        print(email_sub.attributes["PendingConfirmation"])

        publish_message(topic, "Leo, seu chazinho terao " + str(guests) + " convidados! Prepare as xicaras.")
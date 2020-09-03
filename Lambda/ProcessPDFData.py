# python code
# Requires Boto3-layer-1.14

import boto3
from botocore.exceptions import ClientError
import csv
import os

s3 = boto3.client('s3')
s3_client = boto3.client("s3")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomerData')
clientC = boto3.client('comprehend')

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_file_name = event['Records'][0]['s3']['object']['key']
    resp = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)
    data = resp['Body'].read().decode("utf-8")
    customer = data.split("\n")
    for cus in customer:
        cus_data = cus.split(",")
        try:
            if cus_data[1] == "Salutation: " or cus_data[3] == "Name: " or cus_data[5] == "NRIC: " or cus_data[7] == "Address: " or cus_data[9] == "Contact: " or cus_data[11] == "Date of Birth: " or cus_data[13] == "Reason":
                CustomerEmail =  cus_data[1] 
                SENDER = "lies.everywhr@gmail.com"
                RECIPIENT = CustomerEmail
                #CONFIGURATION_SET = "ConfigSet"
                AWS_REGION = "ap-southeast-1"
                SUBJECT = "Appeal Rejection"
                BODY_TEXT = ("We are sorry to inform you that your appeal has been rejected. Reason: Missing details. Please submit another form via the bot with a completed form. Thank You!"
                            )
                BODY_HTML = """<html>
                <head></head>
                <body>
                  <p>We are sorry to inform you that your appeal has been rejected. Reason: Missing details. Please submit another form via the bot with a completed form. Thank You!</p>
                </body>
                </html>
                            """            
                CHARSET = "UTF-8"
                client = boto3.client('ses',region_name=AWS_REGION)
                try:
                    #Provide the contents of the email.
                    response = client.send_email(
                        Destination={
                            'ToAddresses': [
                                RECIPIENT,
                            ],
                        },
                        Message={
                            'Body': {
                                'Html': {
                                    'Charset': CHARSET,
                                    'Data': BODY_HTML,
                                },
                                'Text': {
                                    'Charset': CHARSET,
                                    'Data': BODY_TEXT,
                                },
                            },
                            'Subject': {
                                'Charset': CHARSET,
                                'Data': SUBJECT,
                            },
                        },
                        Source=SENDER,
                        # If you are not using a configuration set, comment or delete the
                        # following line
                        #ConfigurationSetName=CONFIGURATION_SET,
                    )
                # Display an error if something goes wrong.	
                except ClientError as e:
                    print(e.response['Error']['Message'])
                else:
                    print("Email sent! Message ID:"),
                    print(response['MessageId'])
                
            elif cus_data[16] in (None,""):
                CustomerEmail =  cus_data[1] 
                SENDER = "lies.everywhr@gmail.com"
                RECIPIENT = CustomerEmail
                #CONFIGURATION_SET = "ConfigSet"
                AWS_REGION = "ap-southeast-1"
                SUBJECT = "Appeal Rejection"
                BODY_TEXT = ("We are sorry to inform you that your appeal has been rejected. Reason: Missing Reason. Please submit another form via the bot with a completed form. Thank You!"
                            )
                BODY_HTML = """<html>
                <head></head>
                <body>
                  <p>We are sorry to inform you that your appeal has been rejected. Reason: Missing Reason. Please submit another form via the bot with a completed form. Thank You!</p>
                </body>
                </html>
                            """            
                CHARSET = "UTF-8"
                client = boto3.client('ses',region_name=AWS_REGION)
                try:
                    #Provide the contents of the email.
                    response = client.send_email(
                        Destination={
                            'ToAddresses': [
                                RECIPIENT,
                            ],
                        },
                        Message={
                            'Body': {
                                'Html': {
                                    'Charset': CHARSET,
                                    'Data': BODY_HTML,
                                },
                                'Text': {
                                    'Charset': CHARSET,
                                    'Data': BODY_TEXT,
                                },
                            },
                            'Subject': {
                                'Charset': CHARSET,
                                'Data': SUBJECT,
                            },
                        },
                        Source=SENDER,
                        # If you are not using a configuration set, comment or delete the
                        # following line
                        #ConfigurationSetName=CONFIGURATION_SET,
                    )
                # Display an error if something goes wrong.	
                except ClientError as e:
                    print(e.response['Error']['Message'])
                else:
                    print("Email sent! Message ID:"),
                    print(response['MessageId'])
                
            else:
                if cus_data[17] in (None, ""):
                    F = cus_data[16] 
                    
                elif cus_data[18] in (None, ""):
                    F = cus_data[16] + cus_data[17]  
                    
                elif cus_data[19] in (None, ""):
                    F = cus_data[16] + cus_data[17] + cus_data[18]
                    
                elif cus_data[20] in (None, ""):
                    F = cus_data[16] + cus_data[17] + cus_data[18] + cus_data[19]
                    
                else:
                    F = cus_data[16] + cus_data[17] + cus_data[18] + cus_data[19] + cus_data[20]    
    
                responses = clientC.classify_document(
                    Text = F,
                    EndpointArn='<EndPointARN>'
                )
                #print(responses)
                for item in responses["Classes"]:
                    if item['Name'] == 'Approved':
                        a = item['Score']
                        print(a)
                    if item['Name'] == 'Rejected':
                        b = item['Score']
                        print(b)
                if a >= 0.8:
                            result = "Approved"
                            NRIC = cus_data[7]
                            NAME = cus_data[5]
                            CustomerEmail =  cus_data[1]
                            SENDER = "lies.everywhr@gmail.com"
                            RECIPIENT1 = CustomerEmail
                            RECIPIENT2 = "dstworstsubject@gmail.com"
                            #CONFIGURATION_SET = "ConfigSet"
                            AWS_REGION = "ap-southeast-1"
                            SUBJECT = "Appeal approved for " + NAME + ',' + NRIC
                            BODY_TEXT = ("We have reviewed your appeal to request for a waiver for late payment. We would like to inform that your appeal is successful. The finance department should contact you shortly regarding the refund procedures"
                                        )
                            BODY_HTML = """<html>
                            <head></head>
                            <body>
                              <p>We have reviewed your appeal to request for a waiver for late payment. 
                              We would like to inform that your appeal is successful. The finance department should contact you shortly regarding the refund procedures</p>
                            </body>
                            </html>
                                        """            
                            CHARSET = "UTF-8"
                            client = boto3.client('ses',region_name=AWS_REGION)
                            try:
                                #Provide the contents of the email.
                                response = client.send_email(
                                    Destination={
                                        'ToAddresses': [
                                            RECIPIENT1,
                                            RECIPIENT2,
                                        ],
                                    },
                                    Message={
                                        'Body': {
                                            'Html': {
                                                'Charset': CHARSET,
                                                'Data': BODY_HTML,
                                            },
                                            'Text': {
                                                'Charset': CHARSET,
                                                'Data': BODY_TEXT,
                                            },
                                        },
                                        'Subject': {
                                            'Charset': CHARSET,
                                            'Data': SUBJECT,
                                        },
                                    },
                                    Source=SENDER,
                                    # If you are not using a configuration set, comment or delete the
                                    # following line
                                    #ConfigurationSetName=CONFIGURATION_SET,
                                )
                            # Display an error if something goes wrong.	
                            except ClientError as e:
                                print(e.response['Error']['Message'])
                            else:
                                print("Email sent! Message ID:"),
                                print(response['MessageId'])

                elif b >= 0.8:
                            result = "Rejected"
                            NRIC = cus_data[7]
                            NAME = cus_data[5]
                            CustomerEmail =  cus_data[1]
                            SENDER = "lies.everywhr@gmail.com"
                            RECIPIENT1 = CustomerEmail
                            #CONFIGURATION_SET = "ConfigSet"
                            AWS_REGION = "ap-southeast-1"
                            SUBJECT = "Appeal rejected for " + NAME + ',' + NRIC
                            BODY_TEXT = ("We have reviewed your appeal to request for a waiver for late payment. We have reviewed your appeal and regret to inform that your appeal is unsuccessful."
                                        )
                            BODY_HTML = """<html>
                            <head></head>
                            <body>
                              <p>We have reviewed your appeal to request for a waiver for late payment. 
                              We have reviewed your appeal and regret to inform that your appeal is unsuccessful.</p>
                            </body>
                            </html>
                                        """            
                            CHARSET = "UTF-8"
                            client = boto3.client('ses',region_name=AWS_REGION)
                            try:
                                #Provide the contents of the email.
                                response = client.send_email(
                                    Destination={
                                        'ToAddresses': [
                                            RECIPIENT1,
                                        ],
                                    },
                                    Message={
                                        'Body': {
                                            'Html': {
                                                'Charset': CHARSET,
                                                'Data': BODY_HTML,
                                            },
                                            'Text': {
                                                'Charset': CHARSET,
                                                'Data': BODY_TEXT,
                                            },
                                        },
                                        'Subject': {
                                            'Charset': CHARSET,
                                            'Data': SUBJECT,
                                        },
                                    },
                                    Source=SENDER,
                                    # If you are not using a configuration set, comment or delete the
                                    # following line
                                    #ConfigurationSetName=CONFIGURATION_SET,
                                )
                            # Display an error if something goes wrong.	
                            except ClientError as e:
                                print(e.response['Error']['Message'])
                            else:
                                print("Email sent! Message ID:"),
                                print(response['MessageId'])
                                
                elif a < 0.8 and b < 0.8:
                            result = "In Review"
                            NRIC = cus_data[7]
                            NAME = cus_data[5]
                            CustomerEmail =  cus_data[1]
                            SENDER = "lies.everywhr@gmail.com"
                            RECIPIENT1 = CustomerEmail
                            RECIPIENT2 = "dstworstsubject@gmail.com"
                            #CONFIGURATION_SET = "ConfigSet"
                            AWS_REGION = "ap-southeast-1"
                            SUBJECT = "Appeal in review for " + NAME + ',' + NRIC
                            BODY_TEXT = ("We have reviewed your appeal to request for a waiver for late payment. Your waiver status will be forwarded to the relevant parties for futher review. You will be informed of the status and next steps in due time"
                                        )
                            BODY_HTML = """<html>
                            <head></head>
                            <body>
                              <p>"We have reviewed your appeal to request for a waiver for late payment. 
                              Your waiver status will be forwarded to the relevant parties for futher review. You will be informed of the status and next steps in due time"</p>
                            </body>
                            </html>
                                        """            
                            CHARSET = "UTF-8"
                            client = boto3.client('ses',region_name=AWS_REGION)
                            try:
                                #Provide the contents of the email.
                                response = client.send_email(
                                    Destination={
                                        'ToAddresses': [
                                            RECIPIENT1,
                                            RECIPIENT2,
                                        ],
                                    },
                                    Message={
                                        'Body': {
                                            'Html': {
                                                'Charset': CHARSET,
                                                'Data': BODY_HTML,
                                            },
                                            'Text': {
                                                'Charset': CHARSET,
                                                'Data': BODY_TEXT,
                                            },
                                        },
                                        'Subject': {
                                            'Charset': CHARSET,
                                            'Data': SUBJECT,
                                        },
                                    },
                                    Source=SENDER,
                                    # If you are not using a configuration set, comment or delete the
                                    # following line
                                    #ConfigurationSetName=CONFIGURATION_SET,
                                )
                            # Display an error if something goes wrong.	
                            except ClientError as e:
                                print(e.response['Error']['Message'])
                            else:
                                print("Email sent! Message ID:"),
                                print(response['MessageId'])
                                
                table.put_item(
                    Item = {
                        "Salutation" : cus_data[3],
                        "Name" : cus_data[5],
                        "NRIC" : cus_data[7],
                        "Address" : cus_data[9],
                        "Contact" : cus_data[11],
                        "Email" : cus_data[1],
                        "Date of Birth" : cus_data[13],
                        "Reason" : F,
                        "Result" : result 
                    }
                    )
 
        except Exception as e:
            print("EOF")

# SuppBot
AWS Services to address ACRA's pain points for Live Smart Singapore Hackathon 2020

## Contents
1. Description
2. Architecture of Solution
2. Setup and Explanation
3. Results
4. Built with:
5. Credits and Contact

## 1. Description
Front end hosted by AWS Amplify consist of 3 sections. SuppBot, Instructions and Upload Button. Customers can interact with SuppBot to have their enquiries addressed or booking an apppointment with ACRA. The customers details and appointment date will be stored into database for future used. The customer can upload the filled form via the upload button.
<img src="/Images/WebApp.PNG" alt="Web App" width="1000"/>
The form would then be processed on the backend using various AWS services. The outcome of the process would determine the email that would be sent out to the customer, meanwhile the customer data are also being stored into a seperate database from before.

## 2. Architecture of Solution
<img src="/Images/Archi.PNG" alt="Archi" width="1000"/>

## 3. Setup and Explanation
#### Front End
###### Pre-requistes
Follow the instructions in this link: https://docs.amplify.aws/start/getting-started/installation/q/integration/react

###### Setup steps
Our front end is created using **Amplify with the React JS framework**. Amplify acts as the hosting and the cloud provider. 
To start, we will  initialize a react app using
```
npx create-react-app App Name
```
Execting this code will initialize and create a react web application on your local machine. To run the default application, in the directory created, run:
```
npm start
```

Next up, we will initialize amplify with our newly created **react app**. To do so, run :
```
amplify init
```
and configure using the default parameters. This will create a **backend folder** and **aws-exports.js** that will link your project to any apis added.

Once amplify is added to your react application, you will then need to create a github repo to push the folder there. Run these commands: 
```
git init
git remote add origin git@github.com:username/reponame.git
git add .
git commit -m “initial commit”
git push origin master
```

After which, you will need to link the github repo to amplify. You can do this via the amplify console and connect your github account to this. From here on out, any commits changed to the git hub repo will automatically trigger the aws access key in github and it will rebuild in the cloud to update your webpage.
To push changes to the react app to github, simply do:
```
git add .
git commit -m "Changes made"
git push origin master
```

Individually, the create react app package comes with some standard js files.
These include **App.js** and **Index.js**.
- **App.js** is the main js file for our front end react webapp. It renders the components displayed on the amplify domain.
- **Index.js** is the 'rulemaker' and defines the parameters for app.js

To add apis to our react application using Amplify, will will use the command line interface(CLI):  
```
amplify add <api>
```

The APIs we used are **Storage**, **Interactions**, **Auth** and **XR**.
- **Storage** configures the S3 bucket linked with the same aws console account to link with amplify
- **Interactions** Configures Lex chatbot with Amplify allowing access and interactions with the chatbot
- **Auth** Configures AWS cognito to manage authenticated and unauthenticated access to the webapplication
- **XR** Used for sumerian for a more 'futeristic' chatbot feel with a host and scene.

#### Back End
###### Pre-requsites
Attach Boto3-layer-1.14 to every lambda function

###### Setup steps
Our backend mainly consists of lambda functions. So let us create the first lambda function that is responsible for calling textract for data extraction. This lambda function is triggered by the upload of a **.pdf** file into an **S3 Bucket**. As we are analysing PDFs, asynchronous application is required. Thus **SNS** must be employed to determine if this task has been completed. Follow the steps below to setup **Lambda**, **S3 Trigger** and **SNS Policy**

 1. Create a lambda function and copy the code from FindPDFData
 2. Create a trigger using the S3 bucket created by the front end. Ensure that suffix is **.pdf**
    
    <img src="/Images/FirstTrigger.PNG" alt="1stTrigger" width="500"/>
 
 3. Create a SNS policy
 4. Replace SNSTopicARN in the lambda code with the SNS policy ARN created
 5. Create an IAM role for SNS full access using lambda service and add SNS Full Access. Edit trust relationship from 'lambda.amazonaws.com' to 'textract.amazonaws.com'
    
    <p float="left">
    <img src="/Images/SNS.PNG" alt="SNS" width="400"/>
    <img src="/Images/SNSs.PNG" alt="SNS" width="400"/>
    <img src="/Images/Trust.PNG" alt="Trust" width="400"/>
    </p>
    
 6. Replace RoleARN in the lambda code with the IAM Role ARN created
 7. Attach S3 and textract full access to this function's Role in IAM
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
The second lambda function is responsible for getting the data extracted by textract in the first lambda function. It is triggered by SNS that was sent out by the first lambda function upon completion of task. This function will then retrieve the data and store it into **.csv** file in a different **S3 Bucket**. Follow the steps below to setup **Lambda**, **SNS Trigger** and **S3 Bucket**.
 
 8. Create another lambda function and copy the code from GetPDFData.
 9. Create a trigger using SNS created in step 4
 
    <img src="/Images/SNSTrigger.PNG" alt="SNSTrigger" width="500"/>
 
 10. Create a new bucket with no public access.
 11. Replace <bucketname> in the line 58 of code with the bucket name created in step 10
 12. Attach S3 and textract full access to this function's Role in IAM
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
The third and final lambda function serves as a decision maker, sending of emails and storing of data into a database. This function will check the CSV file to classify if the form is void or non void. If the form void, an email will be automatically sent to the customer in regards to a *void form* via **SES**. Else if the form is *non void*, it will begin processing of the reasoning via **Amazon Comprehend**. 
 
**Amazon Comprehend** will output 1 of 3 outcomes based on confidence level. The 3 outcomes are mainly 'Approved' for valid reasoning, 'Rejected' for invalid reasoning and 'In Review' if Amazon comprehend is not confident of either outcome (< 80%). Afterwards, an email will be automatically sent to the customer and/or respective incharges in regards to the outcome of the appeal via **SES**. Meanwhile, the customer data is also being stored into **DynamoDB** for future use. Follow the steps below to setup **Lambda**, **SES**, **Comprehend** and **DynamoDB**.
 
 13. Create another lambda function and copy the code from ProcessPDFData
 14. Create a trigger using the S3 bucket created in step 10. Ensure that suffix is **.csv**
     
     <img src="/Images/SecondTrigger.PNG" alt="2ndTrigger" width="500"/>
     
 15. Create a DynamoDB table with the name 'CustomerData' and primary key as 'NRIC'
 16. Create an IAM policy using JSON policy editor and paste this code in:
     ```javascript
     {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ses:SendEmail",
                    "ses:SendRawEmail"
                ],
                "Resource": "*"
            }
        ]
     }
     ```
 17. Verify the email address that will be used via SES
 18. Replaced all the sender's email in the code to the email that was verified in step 17
 19. Create a bucket, download the **train.csv** and place it in the bucket
 20. Navigate to comprehend and train a custom classifier. Select the input bucket that contains train.csv.
 21. Start training. Once completed, create an endpoint.
 22. Replace EndPointARN in line 151 of the code with the ARN created in step 21
 23. Attach S3, textract, comprehend full access as well as IAM policy created in step 16 to this function's Role in IAM

## 4. Results
Interact with SuppBot to address any enquries. Feel free to book an appointment using Suppbot. To view appointment datas from company POV, navigate to DynamoDB and select the table "AppointmentData". 

Upload a form through AWS Amplify, give it a few minutes for the form to be processed. Afterwards an email should be sent to you regarding the outcome. To view the customer's data, navigate to DynamoDB and select the table "CustomerData".

## 5. Built with:
- Amplify
- Cognito
- Lex
- S3 
- Lambda
- Textract
- SNS
- Comprehend
- SES
- DynamoDB

## 6. Credits and Contact
Feel free to contact us regarding any questions

>Front End
>>Gaanesh: dstworstsubject@gmail.com

>Back End
>>Ian: ianlim0309@gmail.com

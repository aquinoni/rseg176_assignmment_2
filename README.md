# Assignment 2
## RSEG176 Cloud Computing

These are the files used in the lambda functions for our second assignment.
Each folder represents a single function and ould be zipped and uploaded to aws lambda. 

They are executed in the following sequence:

1. detectS3andLoad 
1. cleanSalesData
1. generateBranchSalesReport
1. generatePaymentTypeSalesReport
1. generateProductBranchSalesReport
1. generateProductPaymentSalesReport
1. generateProductSalesReport
1. globalSalesData

On error the following is executed
1. sendFailureEmail

The following is a utility lambda to create new company users
1. createNewCompanyUser

With the Exception of detectS3andLoad and createNewCompanyUser each function in the sequence is triggered 
by the success of the previous function. They pass the company name and original event
through each execution in order to make sure they can be used for any company or csv.

If there is an exception during any stage of the pipeline the data is passed to the 
sendFailureEmail lambda for processing and alerting. Some useful information is pulled form the event and then a message is published to an SNS topic that will notify users by email or SMS.

detectS3andLoad is triggered by detecting a csv loaded in the company's directory in the sales_record_in folder 

createNewCompanyUser is triggered manually and passed a json with a list of users. The user objects include the user name and a temporary password. The lambda will create the user, attach group policy, create their folders in the S3 bucket, and require the user reset their password on first login.

This project is built on Python3.7 and requires the following libraries
1. Boto3 for S3 Management - https://aws.amazon.com/sdk-for-python/
1. psycopg2 for Redshift - https://www.psycopg.org/docs/

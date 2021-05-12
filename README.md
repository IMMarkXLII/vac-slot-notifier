# vac-slot-notifier

Steps to make this work:

1. Create a lambda function in AWS and replace the default lambda_function with the one provided here.
2. Create an SNS topic with a subscription, I chose email as protocol because that is free. You can choose SMS or http as well.
3. Create a trigger, I chose AWS eventbridge with a fixed timely rate of 5 minutes. 

Once this is done, deploy the lambda. It will keep polling the cowin api for a slot for 18+ for the pincode(default is 262524) and send you an email(or sms depending on your SNS subscription).


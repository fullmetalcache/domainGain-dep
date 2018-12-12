# domainGain
Helps with finding and registering categorized domains so that you can assume the categorization of the domain. This is very useful for bypassing web-proxy filters and evading other network detections.

This tool will query multiple sources to find domains that have recently expired, determine the categorization for the domains (if any), verify that the domains can still be registered, and will display pricing information for the domains. If you obtain the optional and free NameSilo Payment ID (not to be confused with the NameSilo API Key) then you can also have the script register a domain for you and have it set the DNS A-record to a host of your choosing.

To use this tool, you will need to sign up for a few, free API-Keys. The API Keys can be obtained from the following sites:

K9 License for Categorization Checking: http://www1.k9webprotection.com/

NameSilo API Key for Verifying Domain Availablity: https://www.namesilo.com

Please note that if you would like to use the registration feature of this script, you will also need to obtain a NameSilo Payment ID. The NameSilo Payment ID is provided to you once they have verified a payment method of yours, which can be done by uploading a picture of your credit/check/debit card for them to review. Note that this is completely optional and you don't have to use this feature; you can just Ctrl-C out of the program after it displays the domain names, categorizations, and prices.

After you obtain the API keys, open up the domainGain.py file and place the API keys into the appropriate fields that are towards the top of the script. Please let me know if you have trouble finding where to put the API keys.

After you've updated the domainGain.py file with your API keys, just run the script as follows:

python domainGain.py

Enjoy and please let me know if you run into any issues!

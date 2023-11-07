# currencyConverter

This application is a currency Converter. It's still hardcoded so it will only convert from CHF to USD or from USD to CHF. 

To test it you can use PostMan. 
1. Navigate to PostMan and paste the URL which is given when you run the code.
2. Change the CRUD function to "POST"
3. The URL should be: "YOURURL/convert"
4. Send the JSON with the test data in the body. Example:
   {
    "amounts": [10, 20, 50],
    "from_currency": "aud", 
     "to_currency" : "JYP"
   }
5. Send the request. It should deliver the total sum converted in the currency you would like. 

# iot_systemintegration_api_gateway
Assignment 2 in the course IoT 
System Integration at KYH IoT-developer program.

Authors:  
Ali Chehade  
Simon Martinsson  
  
### Get the Locksmith project going localy.  
The Flask server with API and MQTT client is started by running **main.py**.  
This will also start the Locksmith client GUI. If you do not have the APISIX server running  
the GUI will not work (so you can close it if you want).  

Documentation for the API-endpoint is found on ***http://localhost:5050***

#### Try outs  
Test the API server and MQTT klient by starting the simulated project on 
Wokwi ([Link](https://wokwi.com/projects/383852780985853953 "Embedded device simulated on Wokwi"))  

After compiling the WokWi projcet and seeing that it connects to wifi. 
You can now start sending codes to the MQTT broker.  
Door ID of the embedded device is set on row 171 in the code. 
This determines which codes are valid to open the door. 
There's only two test users in the database each with a unique code.  
Below are the valid test codes listed and which door they open: 

*Door ID 1* valid codes: **4321**  
*Door ID 2* valid codes: **1234**  
*Door ID 3* valid codes: **1234**, **4321**




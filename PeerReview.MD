# Peer Review Assignment (From Distributed Computing) 
by Bowen Song and Anish Gupta

 This is a peer review assignment for the Alzheimers-Application
 (https://github.com/scbhatia/Alzheimers-Application)
## User Story Review
The patient user story is very understandable and reasonable. It covers almost all aspect of the application, However, not as much on the developer and care giver side.

I feel, by reading the developer user story, I am not standing in the shoes of a developer, but still as a patient or care giver. In addition, the developer side of user story is not capturing all features stated in patient and care giver sides. This may result in some feature mismatches in the final delivered application.  

## System Architecture Review
If a link can be provided to the system diagram on the Github would be very helpful. 

The actual system architecture on the final presentation slide is very hard to read. It would be very helpful if it is a DAG with component groupings: Such as Database group, UI group, patient side, and care giver side. In addition, some color label would be nice.

Content wise, the system architecture failed to deliver the relation between components. There are only double headed arrows everywhere without any explanation. 
## Data flow
The data flow of the application is hidden in the System Architecture diagram. Application front-end draws user information from registration, and sending it to server to stare in MongoDB. Every requests from either patients or the care givers are going through the same process to log or retrieve data from MongoDB. The scheduled message notification is sent from server when scanning though MongoDB. All of requests and messages are handled by Twilio.

## Error handling 
There are json parsing to detect error messages. For GPS [location error](https://github.com/scbhatia/Alzheimers-Application/blob/master/Backend/AlzCare/server.js#L278) the request return is parsed to capture error message. However, error messages are shown instead of been taking cared of. There is no further action other than the message showing "something went wrong". The same type of error handling are placed for all other handled error places such as database fetching errors, message sending errors, and etc. 

There are some Unit test available which also derived some good results. This is very good for app development. I do suggest using AWS auto application testing for more rigorous unit tests. 

## Conclusion
This is a useable application with some good features involved such as GPS tracing and Message notification. However, while I am testing, if the silence is one, there is no Notification available. This could be a problem for Alzheimer application. There are some ways to get around that during application setup which should be a feature from the application to enable notification while on silence.  
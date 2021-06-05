# ur_sql_message_logger
Application for capturing log messages from UR cobot ang logging them into sql database

Code written in Python 3.8. 
Messags from UR captured using TCP/IP socket connection. Byte stream decoded as described in UR documentation:
https://www.universal-robots.com/articles/ur/interface-communication/remote-control-via-tcpip/

For capturing log messages connection with Primary Client Interface is used. 

As SQL server, MS SQL Server Express 2019 is used. For sending queries to server, 'pyodbc' library is used.  

In develop branch there is currently support for GUI deveoping. PyQt5 is used.

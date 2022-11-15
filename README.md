# Keylogger Detector
An application that alerts users to kill/shut down applications attempting to send out 
information through popular SMTP servers.

## How It Works
This project focuses on combating keylogger software by monitoring all running applications, 
targeting those attempting to communicate through popular SMTP ports for Gmail, Yahoo, ATT, 
Microsoft, and AOL on Windows machines. 

Once the software has targeted an application that is communicating through specific SMTP ports, 
the process will be paused, and the user will be notified of the potential threat. Then, the 
user will be asked if this process should be added to a trusted whitelist to continue running 
as normal or kill the process immediately and be added to a blacklist so that any other time this 
process is detected it will be automatically terminated.

## Monitored SMTP Ports
| **SMTP Ports** | **E-mail Service**    |
|----------------|-----------------------|
| 587            | Gmail, Microsoft, AOL |
| 465            | Yahoo, Live           |
| 2525           | Other                 |

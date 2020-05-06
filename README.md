# atlassian-ip-range-security-group-updater
In the event you are using a private Bitbucket instance and Atlassian Cloud JIRA you may need to whitelist the Atlassian IP ranges. This script reads the Atlassian IP range and updates an AWS security group accordingly. 

This can be plugged into a Lambda, and the requests.zip includes the requests module which needs to be added as a Layer.

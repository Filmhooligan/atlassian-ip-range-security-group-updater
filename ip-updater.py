import boto3
import json
import re
import requests

url = 'https://ip-ranges.atlassian.com'
security_group_id = "<your_security_group>"
port = 443

def lambda_handler(event, context):

	response = requests.get(url)

	if response.status_code != 200:
		print('Status:', response.status_code, 'Problem with the request. Exiting.')
		exit()

	data = response.json()
	items = data['items']

	# Create boto session
	ec2 = boto3.resource('ec2')
	SG = ec2.SecurityGroup(security_group_id)
	
	# Remove existing rules so old addresses are removed and only current ones are used
	SG.revoke_ingress(IpPermissions=SG.ip_permissions)
	
	# IPv6 list, based on searching for the colon in IPv6 addresses
	for ip_address in items:
		if re.search(":", ip_address['cidr']) is not None:
			IPstring = ip_address['cidr']
			print(IPstring)
			SG.authorize_ingress(IpPermissions=[{'IpProtocol':'tcp','Ipv6Ranges': [{'CidrIpv6':(IPstring), 'Description':'Generated from https://ip-ranges.atlassian.com/'}],'FromPort':(port),'ToPort':(port)}])
		
	# IPv4 addresses
	for ip_address in items:
		if re.search(":", ip_address['cidr']) is None:
			IPstring = ip_address['cidr']
			print(IPstring) 
			SG.authorize_ingress(IpPermissions=[{'IpProtocol':'tcp','IpRanges': [{ 'CidrIp':(IPstring), 'Description':'Generated from https://ip-ranges.atlassian.com/'}],'FromPort':(port),'ToPort':(port)}])

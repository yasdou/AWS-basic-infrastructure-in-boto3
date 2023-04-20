import boto3

region = 'us-west-2'

ec2 = boto3.client('ec2', region_name=region) 

vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
ec2.create_tags(Resources=[vpc['Vpc']['VpcId']], Tags=[{'Key': 'Name', 'Value': 'boto3'}])

ig = ec2.create_internet_gateway()
ec2.attach_internet_gateway(InternetGatewayId=ig['InternetGateway']['InternetGatewayId'], VpcId=vpc['Vpc']['VpcId'])

sg = ec2.create_security_group(Description='boto3SG', GroupName='boto3SG', VpcId=vpc['Vpc']['VpcId'])
ec2.authorize_security_group_ingress(GroupId=sg['GroupId'], IpPermissions=[{'FromPort': 22, 'IpProtocol': 'tcp', 'IpRanges': [{'CidrIp': '0.0.0.0/0',},], 'ToPort': 22, },],)
print("Secouritygroup: " + sg['GroupId'])
privsubnet = ec2.create_subnet(TagSpecifications=[{'ResourceType': 'subnet', 'Tags': [{'Key': 'Name', 'Value': 'boto3subnet',},],},], CidrBlock='10.0.1.0/24', AvailabilityZone=region+"a", VpcId=vpc['Vpc']['VpcId'])
print("Private Subnet AZ: " + privsubnet['Subnet']['AvailabilityZone'])
ec2 = boto3.resource('ec2', region_name='us-west-2')
instance = ec2.create_instances(ImageId="ami-0747e613a2a1ff483", InstanceType="t2.micro", SubnetId=privsubnet['Subnet']['SubnetId'], SecurityGroupIds=[sg['GroupId'] ,], KeyName="vockey", MinCount=1, MaxCount=1, TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'boto3instance'},]},],)
print(instance)
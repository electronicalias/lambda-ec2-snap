import boto3
import logging

logging.getLogger().setLevel(logging.DEBUG)


def lambda_handler(event, context):
    
    pname = event['Product']
    rname = event['Region']
    
    ec2 = boto3.client('ec2', rname)
    ecsnap = boto3.resource('ec2', rname)
    
    def create_snap(vol_id):
        data = ec2.create_snapshot(
            VolumeId=vol_id,
            Description='This is a test'
        )
        return data['SnapshotId']
    
    def tag_snap(snap_id):
        snapshot = ecsnap.Snapshot(snap_id)
        tag = snapshot.create_tags(
            Tags=[
                {
                    'Key': 'Name',
                    'Value': pname + '-something'
                },
            ]
        )

    reservations = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag-value', 
                'Values': [pname],
            },
        ])['Reservations']
        
    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    for instance in instances:
        print instance
        for dev in instance['BlockDeviceMappings']:
            Name = dev['DeviceName']
            if '/dev/xvda' in Name:
                print "InstanceId: %s \nVolumeName: %s\nDriveLetter: E" % (
                    instance['InstanceId'], Name)
                snapid = create_snap(dev['Ebs']['VolumeId'])
                tag_snap(snapid)
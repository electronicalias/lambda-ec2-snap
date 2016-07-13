import boto3
import logging
import datetime
import collections
from datetime import datetime

logging.getLogger().setLevel(logging.DEBUG)


def lambda_handler(event, context):

    dtstamp = datetime.today()
    dstamp = dtstamp.date()

    pname = event['Product']
    rname = event['Region']
    period = event['Period']
    
    ec2 = boto3.client('ec2', rname)
    ecsnap = boto3.resource('ec2', rname)

    to_tag = collections.defaultdict(list)
    
    def create_snap(vol_id):
        data = ec2.create_snapshot(
            VolumeId=vol_id,
            Description='This is a test'
        )
        return data['SnapshotId']
    
    def tag_snap(snap_id, disk_id, instance_id, retention_days):
        delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
        delete_fmt = delete_date.strftime('%Y-%m-%d')
        snapshot = ecsnap.Snapshot(snap_id)
        tag = snapshot.create_tags(
            Tags=[
                {
                    'Key': 'Name',
                    'Value': str(dstamp) + '-' + period + '-' + instance_id
                },
                {
                    'Key': 'Date',
                    'Value': str(dstamp)
                },
                {
                    'Key': 'Device',
                    'Value': disk_id
                },
                {
                    'Key': 'InstanceId',
                    'Value': instance_id
                },
                {
                    'Key': 'DeleteOn',
                    'Value': delete_fmt
                },
            ]
        )

    if 'All' in pname:
        reservations = ec2.describe_instances(
            )['Reservations']
    else:
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

        try:
            retention_days = [
                int(t.get('Value')) for t in instance['Tags']
                if t['Key'] == 'Retention'][0]
        except IndexError:
            retention_days = 7

        for dev in instance['BlockDeviceMappings']:
            Name = dev['DeviceName']
            print "InstanceId: %s \nVolumeName: %s" % (
                instance['InstanceId'], Name)

            snapid = create_snap(dev['Ebs']['VolumeId'])

            tag_snap(snapid, Name, instance['InstanceId'], retention_days)
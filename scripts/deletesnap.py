import boto3
import datetime

ec = boto3.client('ec2')

def lambda_handler(event, context):

    delete_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag-key', 'Values': ['DeleteOn']},
        {'Name': 'tag-value', 'Values': [delete_on]},
    ]

    ec = boto3.client('ec2')
    account_ids = [event['Account']]
    snapshot_response = ec.describe_snapshots(
    	OwnerIds=account_ids, 
    	Filters=[
        {
            'Name': 'tag:DeleteOn',
            'Values': [
                delete_on,
            ]
        },
    ]
    )

    for snap in snapshot_response['Snapshots']:
        print "Deleting snapshot %s" % snap['SnapshotId']
        ec.delete_snapshot(SnapshotId=snap['SnapshotId'])
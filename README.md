# lambda-ec2-snap
This CloudFormation Template creates a Labmda Function and Event that will search EC2 in the Region it is installed and make snapshots of all Volumes for an instance that has the correct tags specified.

# Pre-requisites
- An account in AWS IAM with permissions to create resources in EC2, Lambda, CloudFormation and S3
- Alternatively a login to an EC2 Host that has an IAM Role applied that has these permissions

# Usage
To use this correctly, make sure you tag your instances with a Product tag, that has a value for the role/product. This particular CloudFormation stack will ask for the Product and expect to find instances tagged as such. Additionally, you need to package the file in the scripts directory into a zipfile called snapper.zip, this should be uploaded to a bucket of your choice and then you can specify the bucket and key in the template

1. Tag instances correctly with a Product tag (CAPS sensitive) and give it a name.
2. Create a bucket in your account where you want to carry out the snapshots
3. Clone the repository and create a Zip File;
       a) cd path/to/files/scripts/
       b) zip snapper.zip *
4. Copy the zip to your S3 Bucket
       a) aws s3 cp snapper.zip s3://yourbucket/snapper.zip
5. Run the snapbackups.template and fill in the product name (note you can specify ALL if you want it to back up ALL the EC2 instances that have the "Product" tag specified, irrespective of the value. Also give the s3 link.


The Template will create all of the required

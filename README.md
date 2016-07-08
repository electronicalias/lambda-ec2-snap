# lambda-ec2-snap
This CloudFormation Template creates a Labmda Function and Event that will search EC2 in the Region it is installed and make snapshots of all Volumes.

# Usage
To use this correctly, make sure you tag your instances with a Product tag, that has a value for the role/product. This particular CloudFormation stack will ask for the Product and expect to find instances tagged as such. Additionally, you need to package the file in the scripts directory into a zipfile called snapper.zip, this should be uploaded to a bucket of your choice and then you can specify the bucket and key in the template

# ToDo
Currently the name of every snapshot will just be the Product and '-something' appended to the end (see the tagging function in the script). I plan to add a date feature so this can be used to take daily/monthly snapshots which would be date stamped.

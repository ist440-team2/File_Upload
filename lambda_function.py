import boto3
import urllib2
import urlparse
import os
import json
import datetime

s3 = boto3.resource('s3')

def lambda_handler(event, context):

    bucket = "ist440grp2-images"
    fileurl = event['fileurl'];
    username = event['username'];
    id = event['id'];
    email = event['email']
    m_data= {'username': username, 'email': email, 'id': id}
    a = urlparse.urlparse(fileurl)
    Key=os.path.basename(a.path);
    email = event['email'];
    imagepull = urllib2.Request(fileurl, headers={'User-Agent': "Magic Browser"})
    image=urllib2.urlopen(fileurl)
    s3.Bucket(bucket).put_object(Key=Key, Body=image.read(), ACL='public-read', ContentType='image/png', Metadata=m_data)
    x = datetime.datetime.now().isoformat()
    data = {
        'userId': username,
        'jobId': id,
        'createdDate': x,
        'status': "QUEUED",
        "uploadedImageInfo": {"bucket": bucket, "key": Key}
        }
    req = urllib2.Request('https://l08fl95wj9.execute-api.us-east-1.amazonaws.com/test/jobs/start/')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    
    
    return {"location": "https://sites.psu.edu/group2ist440/check-status/" +"?id="+username}
    #return fileurl + username + id + email;

import os
import boto
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser

aws_access_key = os.getenv('aws_access_key', 'default')
aws_secret_key = os.getenv('aws_secret_key', 'default')
bucket_name = "insight-naveen-rebot"
folder_name = "raw/"
file_name = "stackexchange-posts-sample.xml"
conn = boto.connect_s3(aws_access_key, aws_secret_key)

bucket = conn.get_bucket(bucket_name)
key = bucket.get_key(folder_name + file_name)

data = key.get_contents_as_string()

posts = ET.fromstring(data)
rows = {}

class PostsBodyParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.recording = 0
        self.codes = ''
    def handle_starttag(self, tag, attrs):
        if tag != 'code':
            return
        if self.recording:
            self.recording += 1
        self.recording = 1
    def handle_endtag(self, tag):
        if tag != 'code':
            return
        if self.recording:
            self.recording -= 1
    def handle_data(self, data):
        if self.recording:
            self.codes += "<code>" + data + "</code>"

def process_row(row):
    _id = row.attrib['Id']
    rows[_id] = row.attrib
    parser = PostsBodyParser()
    parser.feed(row.attrib['Body'])
    rows[_id]['snippets'] = parser.codes
        
for row in posts:
    process_row(row)



print rows['4']['snippets']

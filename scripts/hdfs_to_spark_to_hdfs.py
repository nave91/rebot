from pyspark import SparkContext, SparkConf

folder_name = "raw/"
out_folder_name = "output/"
file_name = "Posts.xml"
hdfs = "ec2-52-8-194-49.us-west-1.compute.amazonaws.com:9000"

def jsoner(row):
    header = ['id','posttypeid','score','answer','body','snippets']
    header_map = ['Id','PostTypeId','Score','AcceptedAnswerId','Body','snippets']
    out = {}
    for ind, h in enumerate(header_map):
        if h == 'AcceptedAnswerId':
            if h in row.keys():
                out[header[ind]] = row[h]
            else:
                out[header[ind]] = 'NULL'
            continue
        out[header[ind]] = row[h]
    import json
    return json.dumps(out)

def load_row(row):
    from HTMLParser import HTMLParser
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
    new_row = {}
    for key,value in row.attrib.items():
        new_row[key] = value
    parser = PostsBodyParser()
    parser.feed(new_row['Body'])
    new_row['snippets'] = parser.codes
    return jsoner(new_row)


def fetch_line(line):
    if line[-2] == '/':
        import xml.etree.ElementTree as ET
        row = ET.fromstring(line.encode('UTF-8'))
        return load_row(row)


conf = SparkConf().setAppName("ESTest")
sc = SparkContext(conf=conf)


file = sc.textFile("hdfs://"+hdfs+"/"+folder_name+file_name)

lines = file.map(lambda line: fetch_line(line))
lines.collect()
lines.saveAsTextFile("hdfs://"+hdfs+"/"+out_folder_name+'jsons')

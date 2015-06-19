from pyspark import SparkContext, SparkConf

folder_name = "input/"
out_folder_name = "json/"
#file_name = "stackexchange-posts-sample.xml"
file_name = "Posts.xml"
hdfs = "ec2-52-8-214-93.us-west-1.compute.amazonaws.com:9000"

def jsoner(dic):
    import json
    return json.dumps(dic)

def dicter(row):
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
    return out

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
    return dicter(new_row)


def fetch_line(line):
    if line[-2] == '/':
        import xml.etree.ElementTree as ET
        row = ET.fromstring(line.encode('UTF-8'))
        return load_row(row)


conf = SparkConf().setAppName("ESTest")
sc = SparkContext(conf=conf)


file = sc.textFile("hdfs://"+hdfs+"/"+folder_name+file_name)

lines = file.map(lambda line: fetch_line(line))\
            .filter(lambda dic: dic is not None)\
            .filter(lambda dic: dic['posttypeid'] == '1')\
            .map(lambda d: jsoner(d))

lines.saveAsTextFile("hdfs://"+hdfs+"/"+out_folder_name+'middles')

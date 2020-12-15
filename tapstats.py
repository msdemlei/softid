import sys
from urllib import request
from urllib.error import URLError
import pyvo

opener = request.build_opener()
opener.addheaders = [
	("User-Agent", "tapstats/1.0 (IVOA-monitor {}) python-urllib/{}".format(
		"http://ivoa.net/documents/softid/",
		request.__version__))]

stats = {}
for svc_rec in pyvo.registry.search(servicetype="tap"):
    try:
        res = opener.open(
            svc_rec.access_url+"/capabilities",
            timeout=10)
        server_software = str(res.info()["server"])
    except URLError as msg:
        # dead server
        server_software = "BROKEN: %r"%msg
    stats[server_software] = stats.get(server_software, 0)+1

print("\n".join("{:70s} | {:4d}".format(*i) 
    for i in sorted(stats.items(), key=lambda i: -i[1])))

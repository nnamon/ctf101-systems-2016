#!/usr/bin/python

import sys
from itsdangerous import URLSafeSerializer
import subprocess
import hashlib
import os
from os.path import splitext

"""
# whoami
www-data
# ls -la
total 348
drwxr-xr-x  2 snekuser snekuser   4096 Apr  9 18:10 .
drwxr-xr-x 80 root     root       4096 Apr  9 18:13 ..
-r-sr-sr-x  1 snekuser snekuser   7560 Apr  9 18:10 read_file
-r--------  1 snekuser snekuser  24961 Apr  9 14:39 snek.jpg
-r--------  1 snekuser snekuser   7118 Apr  9 12:47 snek1.jpg
-r--------  1 snekuser snekuser  35242 Apr  9 12:47 snek2.jpg
-r--------  1 snekuser snekuser  50713 Apr  9 12:47 snek3.jpg
-r--------  1 snekuser snekuser 173542 Apr  9 12:47 snek4.jpg
-r--------  1 snekuser snekuser  18784 Apr  9 12:48 snek5.jpg
-r--------  1 snekuser snekuser   9418 Apr  9 13:47 snek_flag.png
-r-xr-xr-x  1 snekuser snekuser   1819 Apr  9 17:43 straya.py
"""

def main():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    action = sys.argv[1]
    secret_key = sys.argv[2]

    if action == "generate":
        filename = sys.argv[3]
        basename = filename.split(".")[-2]
        extension = filename.split(".")[-1]
        digest = hashlib.sha512(secret_key + basename).hexdigest()
        des = URLSafeSerializer(digest)
        credentials = {'filename': filename.encode("base64"),
                       'ext': extension,
                       'length': len(filename),
                       'signature': digest}
        print des.dumps(credentials, salt="donttread")
        return

    signed_serial = sys.argv[3]

    result = URLSafeSerializer("").loads_unsafe(signed_serial)

    img = "snek.jpg"

    try:
        if result[1]:
            signature = result[1]['signature']
            extension = result[1]['ext']
            filename  = result[1]['filename'].decode("base64")
            length    = result[1]['length']
            if len(filename) == length and len(extension) == 3:
                basename = filename.split(".")[-2]
                digest = hashlib.sha512(secret_key + splitext(filename)[0]).hexdigest()
                if digest == signature:
                    des = URLSafeSerializer(digest)
                    des.loads(signed_serial, salt="donttread")
                    img = "%s.%s" % (basename, extension)
    except:
        pass

    proc = subprocess.Popen(["./read_file", img], stdout=subprocess.PIPE)
    imgo = proc.stdout.read().encode("base64").replace("\n", "")
    output = '<img src="data:image/png;base64,%s" alt="i am %s" />' % (imgo, img)
    print output

if __name__ == "__main__":
    main()

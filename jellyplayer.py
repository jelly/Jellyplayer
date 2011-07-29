#!/usr/bin/python2 

import json
from subprocess import call

def parseData(streams):
    try:
        fsock = open(streams, "r")
        try:
            data = json.load(fsock)
        finally:
            fsock.close()
    except IOError:
        print "no json file"

    return data



def playVideo(stream):
    if "rtmp" in stream:
        # parse RTMP
        stream_list = stream.split(" ")
        swfurl = ""
        playpath = ""
        url = "" 
        pageurl = ""
        tcurl = ""
        for a,b in enumerate(stream_list): 
            if "rtmp" in b:
                url = b
            if "tcUrl" in b:
                tcurl = " -t " + b.replace("tcUrl=","")
            if "playpath" in b:
                playpath = " -y " + b.replace("playpath=","")
            if "Playpath" in b:
                playpath = " -W " + b.replace("Playpath=","")
            if "swfUrl" in b:
                swfurl = " -W " + b.replace("swfUrl=","")
            if "pageUrl" in b:
                pageurl = " -p " + b.replace("pageUrl=","")

        rtmpdump = "rtmpdump -r " + url + playpath + swfurl + pageurl
        if "live=true" in stream_list:
            rtmpdump += " -v "
        rtmpdump += " | mplayer -cache 2000 -"
        print rtmpdump
        call(rtmpdump, shell=True)
        
    else:
        if "http" in stream:
            call("mplayer -cache 2000 -playlist " + stream, shell=True)
        else:
            call("mplayer -cache 2000 " + stream, shell=True)

def mainloop(data):
    bar = 1

    while(bar != 0):

        foo = 1
        for d in data:
            print "%i. %s " % (foo,d['title'])
            foo += 1

        print "press '0' for quit"
        bar=input('Please enter a value:')
        if bar != 0:
            foo = 1
            for d in data:
                if foo == bar:
                    playVideo(d['stream'])
                foo += 1



if __name__ == "__main__":
    mainloop(parseData('streams.json'))

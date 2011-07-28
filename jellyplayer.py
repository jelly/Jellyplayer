from xml.dom import minidom
import urwid

from subprocess import call

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def parseXML(xmlFile):
    """
    Parse the xml
    """
 
    dom = minidom.parse('XBMC-Streams.xml')
    channellist = {}
    channels = dom.getElementsByTagName("item")
    for channel in channels:
        title = channel.getElementsByTagName("title")[0]
        url = channel.getElementsByTagName("link")[0]

        channellist[getText(title.childNodes)] = getText(url.childNodes)
        
        #print  getText(title.childNodes) + " " + getText(url.childNodes)
    return channellist

def playVideo(video):
    video_list = video.split(" ")
    url = video_list[0] # -r
    playpath = video_list[1].replace("playpath=","") # -y
    swfurl = video_list[2].replace("swfUrl=","") # -W

    rtmpdump = "rtmpdump -r " + url + " -y " + playpath + " -W " + swfurl 
    if "live=true" in video_list:
        rtmpdump += " -v "
    rtmpdump += " | mplayer -cache 2000 -"
    #os.system(rtmpdump)
    call(rtmpdump, shell=True)




if __name__ == "__main__":
    channellist  = parseXML("XBMC-Streams.xml")

    bar = 1 
    while bar != 0:
        foo = 1
        for i in channellist:
            print "%i. %s" % (foo, i)
            foo += 1

        print "press '0' for quit"
        bar=input('Please enter a value:')

        if bar != 0:
            foo = 1
            for i in channellist:
                if foo == bar:
                        playVideo(channellist[i])
                foo += 1


    #bbc = channellist["BBC News"]
    #playVideo(bbc)



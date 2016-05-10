import urllib2

url = "https://r7---sn-hju7en7e.googlevideo.com/videoplayback?id=f70b9937ac00b0b4&itag=22&source=picasa&begin=0&requiressl=yes&mm=30&mn=sn-hju7en7e&ms=nxu&mv=m&pl=24&mime=video/mp4&lmt=1415352439160936&mt=1462807547&ip=88.201.58.172&ipbits=8&expire=1462836506&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,mime,lmt&signature=1C40444EA84858E10507815930AE53E17D2556CB.71263A37A658DBC1443C0445AD17BC7ACE5BBB1A&key=ck2"

def download_file(url, file_name = "a.mp4"):
    try:
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
    except:
        return False
    finally:
        f.close()

    return True

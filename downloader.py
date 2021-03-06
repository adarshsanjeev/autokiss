import urllib2

def download_file(url, file_name="a.mp4", proxy = None):
    """
    Function to download a file, given url, and save it as file_name
    """
    
    proxy = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

    f = open(file_name, 'wb')
    u = urllib2.urlopen(url)
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        download_buffer = u.read(block_sz)
        if not download_buffer:
            break

        file_size_dl += len(download_buffer)
        f.write(download_buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()

    return True

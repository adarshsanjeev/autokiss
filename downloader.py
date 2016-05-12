import urllib2

def download_file(url, file_name="a.mp4"):
    """
    Function to download a file, given url, and save it as file_name
    """
    try:
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
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
    except:
        return False
    finally:
        f.close()

    return True

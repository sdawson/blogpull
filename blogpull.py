from gdata import service
from BeautifulSoup import BeautifulStoneSoup
from urlparse import urlparse
import gdata
import atom
import sys, time, os, errno

def pullFeed(blogger_service, uri, dirname):
  # Only create the requested directory if it doesn't already exist
  try:
    os.makedirs(dirname)
  except OSError, e:
    if e.errno != errno.EEXIST:
      raise

  feed = blogger_service.GetFeed(uri)
  for entry in feed.entry:
    saveToFile(entry, dirname)
  feed = blogger_service.GetNext(feed)
  f = open(''.join([dirname, 'feedinfo']), 'w')
  f.write(str(feed.title) + "\n")
  f.write(str(feed.author) + "\n")
  f.write(str(feed.id) + "\n")
  while feed is not None:
    for entry in feed.entry:
      saveToFile(entry, dirname)
    feed = blogger_service.GetNext(feed)
    time.sleep(3)

def saveToFile(entry, dirname):
  filename = os.path.join(dirname, entry.published.text)
  if not os.path.exists(filename):
    print "writing", filename
    f = open(filename, 'w')
    f.write(str(entry.title))
    f.write("\n")
    f.write(str(entry.published))
    f.write("\n")
    f.write('<content>' + str(entry.content.text) + '</content>')
    f.write("\n")
    print "\t" + str(entry.title.text)
    f.close()
  else:
    print "skipping", filename, "(already exists)"
    return

# Takes all downloaded posts and creates local copies
# of the referenced images.
def sourceLocalImages(dirname, url):
  netloc = urlparse(url).netloc
  # Writes to temp file in case of large files
  for file in os.listdir(dirname):
    f = open(os.path.join(dirname, file), 'r')
    print "opening:", file
    contentSoup = BeautifulStoneSoup(f.read())
    f.close()
    imgTags = contentSoup.findAll('img')
    for tag in imgTags:
      # removes images referencing the blog itself
      if netloc and netloc in tag['src']:
        print "extracting:", tag
        tag.extract()
        continue
      else:
        print "orig tag src:", tag['src']
        print "will replace image ref here"
    tempfile = '.'.join([file, "tmp"])
    print "tempfile name:", tempfile
    ftemp = open(os.path.join(dirname, tempfile), 'w')
    ftemp.write(contentSoup.prettify())
    ftemp.close()
    os.rename(os.path.join(dirname, tempfile), os.path.join(dirname, file))

def getUrl(filename):
  f = open(filename, 'r')
  url = f.readline().rstrip()
  f.close()
  return ''.join([url, "/feeds/posts/default"])

def usage():
  print "Usage: python blogpull.py outputdirname"

def main():
  if len(sys.argv[1:]) != 2:
    usage()
    sys.exit(1)
  blogger_service = service.GDataService()
  url = getUrl(sys.argv[1])
  outputdir = sys.argv[2]
  pullFeed(blogger_service, url, outputdir)
  sourceLocalImages(outputdir, url)

if __name__ == '__main__':
  main()

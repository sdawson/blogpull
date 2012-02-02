from gdata import service
from BeautifulSoup import BeautifulStoneSoup
from urlparse import urlparse, urlsplit
from os.path import basename
import gdata, atom, mimetypes
import sys, time, os, errno, urllib
import urllib2

def pullFeed(blogger_service, uri, dirname):
  # Only create the requested directory if it doesn't already exist
  try:
    os.makedirs(dirname)
  except OSError, e:
    if e.errno != errno.EEXIST:
      raise

  feed = blogger_service.GetFeed(uri)
  f = open(os.path.join(dirname, 'feedinfo'), 'w')
  f.write(str(feed.title) + "\n")
  f.write(str(feed.author) + "\n")
  f.write(str(feed.id) + "\n")
  f.close()
  for entry in feed.entry:
    saveToFile(entry, dirname)
  feed = blogger_service.GetNext(feed)
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
  # Writes to temp file in case of large files
  for file in os.listdir(dirname):
    f = open(os.path.join(dirname, file), 'r')
    print "opening:", file
    contentSoup = BeautifulStoneSoup(f.read())
    f.close()
    replaceImageTags(contentSoup, dirname, url)
    tempfile = '.'.join([file, "tmp"])
    print "tempfile name:", tempfile
    ftemp = open(os.path.join(dirname, tempfile), 'w')
    ftemp.write(contentSoup.prettify())
    ftemp.close()
    os.rename(os.path.join(dirname, tempfile), os.path.join(dirname, file))

# Replaces image tags contained in a link
# with local copies of the images
def replaceImageTags(contentSoup, dirname, url):
  netloc = urlparse(url).netloc
  # Replace links to images
  for link in contentSoup.findAll('a'):
    (predType, _) =  mimetypes.guess_type(link['href'])
    if predType in ('image/png', 'image/jpeg', 'image/gif'):
      print "+++DOWNLOADING AHREF:", link['href']
      filename = download(dirname, link['href'])
      link['href'] = filename
  # Replace image tags
  imgTags = contentSoup.findAll('img')
  for tag in imgTags:
    # removes images sourced from within the blog
    if netloc and netloc in tag['src']:
      tag.extract()
      continue
    else:
      print "+++DOWNLOADING:", tag['src']
      filename = download(dirname, tag['src'])
      tag['src'] = filename

def urlToName(url):
  return basename(urlsplit(url)[2])

# Returns the filename of the downloaded file relative
# to the final directory (as given by dirname)
def download(dirname, url, localFileName = None):
  localName = urlToName(url)
  req = urllib2.Request(url)
  r = urllib2.urlopen(req)
  if r.info().has_key('Content-Disposition'):
    # If the response has a Content-Disposition the filename is taken from it
    localName = r.info()['Content-Disposition'].split('filename=')[1]
    if localName[0] == "" or localName[0] == "'":
      localName = localName[1:-1]
    elif r.url != url:
      # A redirection occured, so take that filename from the final url
      localName = urlToName(r.url)
    if localFileName:
      # Save the file under the user-specified name
      localName = localFileName
    f = open(os.path.join(dirname, localName), 'wb')
    f.write(r.read())
    f.close()
  return localName

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

from gdata import service
import gdata
import atom
import sys, time, os, errno

def runningPostTitlePrint(blogger_service, uri, dirname):
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
  while feed is not None:
    print "looping\n"
    for entry in feed.entry:
      saveToFile(entry, dirname)
    feed = blogger_service.GetNext(feed)
    time.sleep(10)

def saveToFile(entry, dirname):
  filename = os.path.join(dirname, entry.published.text)
  if not os.path.exists(filename):
    print "writing", filename
    f = open(filename, 'w')
    f.write(str(entry.title.text))
    f.write("\n")
    f.write(str(entry.published.text))
    f.write("\n")
    f.write(str(entry.content.text))
    f.write("\n")
    print "\t" + str(entry.title.text)
    f.close()
  else:
    return

def usage():
  print "Usage: python blogpull.py outputdirname"

def getUrl(filename):
  f = open(filename, 'r')
  url = f.readline().rstrip()
  f.close
  return ''.join([url, "/feeds/posts/default"])

def main():
  print len(sys.argv[1:])
  if len(sys.argv[1:]) != 2:
    usage()
    sys.exit(1)
  blogger_service = service.GDataService()
  #PrintAllPosts(blogger_service)
  print "argv[1]: ", sys.argv[1]
  url = getUrl(sys.argv[1])
  outputfile = sys.argv[2]
  runningPostTitlePrint(blogger_service, url, outputfile)

if __name__ == '__main__':
  main()

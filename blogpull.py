from gdata import service
import gdata
import atom
import sys, time, os

def PrintAllPosts(blogger_service):
  feed = blogger_service.GetFeed('http://theeyechild.blogspot.com/feeds/posts/default')

  print feed.title.text
  for entry in feed.entry:
    print "\t" + str(entry.title.text)
    #print "\t" + entry.content.text
  print
  new_feed = blogger_service.GetNext(feed)
  for entry in new_feed.entry:
    print "\t" + str(entry.title.text)
  print

def runningPostTitlePrint(blogger_service, uri, dirname):
  os.makedirs(dirname)
  #f = open(dirname, 'w')
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
  #f.close()

def saveToFile(entry, dirname):
  filename = os.path.join(dirname, entry.published.text)
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

def usage():
  print "Usage: python bloggerreg.py outputdirname"

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

from gdata import service
import gdata
import atom
import sys
import time

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

def runningPostTitlePrint(blogger_service, uri, filename):
  f = open(filename, 'w')
  feed = blogger_service.GetFeed(uri)

  for entry in feed.entry:
    print "writing", entry.title.text
    f.write(str(entry.title.text))
    f.write("\n")
    f.write(str(entry.published.text))
    f.write("\n")
    f.write(str(entry.content.text))
    f.write("\n\n")
  feed = blogger_service.GetNext(feed)
  while feed is not None:
    print "looping\n"
    for entry in feed.entry:
      print "\t" + str(entry.title.text)
    feed = blogger_service.GetNext(feed)
    time.sleep(10)
  f.close()

def usage():
  print "Usage: python bloggerreg.py filename"

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

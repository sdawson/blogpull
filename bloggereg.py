from gdata import service
import gdata
import atom
import sys

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
  f.close()

def usage():
  print "Usage: python pbloggerreg.py filename"

def getUrl(filename):
  f = open(filename, 'r')
  url = f.readline()
  f.close
  return ''.join([url, "/feeds/posts/default"])

def main():
  print len(sys.argv[1:])
  if len(sys.argv[1:]) != 1:
    usage()
    sys.exit(1)
  blogger_service = service.GDataService()
  #PrintAllPosts(blogger_service)
  print "argv[1]: ", sys.argv[1]
  url = getUrl(sys.argv[1])
  runningPostTitlePrint(blogger_service, url, "eyechildtest2")

if __name__ == '__main__':
  main()

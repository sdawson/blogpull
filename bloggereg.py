from gdata import service
import gdata
import atom

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

def runningPostTitlePrint(blogger_service, uri):
  f = open("eyechildtest1", 'w')
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

def main():
  blogger_service = service.GDataService()
  #PrintAllPosts(blogger_service)
  runningPostTitlePrint(blogger_service, 'http://theeyechild.blogspot.com/feeds/posts/default')

if __name__ == '__main__':
  main()

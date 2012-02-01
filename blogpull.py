from gdata import service
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
    f.write(str(entry.content))
    f.write("\n")
    print "\t" + str(entry.title.text)
    f.close()
  else:
    return

def usage():
  print "Usage: python blogpull.py outputdirname"

def main():
  print len(sys.argv[1:])
  if len(sys.argv[1:]) != 2:
    usage()
    sys.exit(1)
  blogger_service = service.GDataService()
  outputfile = sys.argv[2]
  pullFeed(blogger_service, url, outputfile)

if __name__ == '__main__':
  main()

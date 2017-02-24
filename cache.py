def make_caches(no_caches, csize):
  return [Cache(i, csize) for i in range(no_caches)]

class CacheOverflowException(Exception):

  def __init__(self, message):
    super(CacheOverflowException, self).__init__(message)


class Cache(object):
  def __init__(self, id, csize):
    self.id = id
    self.maxsize = csize
    self.vids = []
    self.size = 0

  def add(self, video):
    #print "space left: {} video size: {} outcome: {}".format(self.left(), video.size, self.left() < video.size)
    if self.left() < video.size:
      raise CacheOverflowException("Trying to add video to cache that doesn't have enough space!!!")
    self.vids.append(video)
    self.size += video.size
    video.cache.append(self)

  def remove(self, video):
    self.vids.remove(video)
    self.size -= video.size
    video.cache.remove(self)

  def getvids(self):
    return self.vids

  def left(self):
    return self.maxsize - self.size

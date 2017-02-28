import numpy as np
import video

def make_caches(no_caches, csize):
  return [Cache(i, csize) for i in range(no_caches)]

class CacheOverflowException(Exception):

  def __init__(self, message):
    super(CacheOverflowException, self).__init__(message)


class Cache(object):
  def __init__(self, id, csize):
    self.id = int(id)
    self.maxsize = csize
    self.vids = np.array([], dtype = video.Video)
    self.size = 0
    self.eps = []

  def add(self, video):
    if self.left() < video.size:
      raise CacheOverflowException("Trying to add video to cache that doesn't have enough space!!!")
    self.vids = np.append(self.vids, [video])
    self.size += video.size
    video.cache = np.append(video.cache, [self])
    for r in video.reqs:
      r.minlat = min(r.minlat, r.getlat(self.id))

  def remove(self, video):
    self.vids.remove(video)
    self.size -= video.size
    np.setdiff1d(video.cache, [self])
    for r in video.reqs:
      r.put_ep(r.ep)

  def getvids(self):
    return self.vids

  def left(self):
    return self.maxsize - self.size

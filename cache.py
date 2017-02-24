def make_caches(no_caches, csize):
  return [Cache(csize) for i in range(no_caches)]

class Cache(object):
  def __init__(self, csize):
    self.maxsize = csize
    self.vids = []
    self.size = 0

  def add_video(self, video):
    self.vids.append(video)
    self.size += video.size

  def remove_video(self, video):
    self.vids.remove(video)
    self.size -= video.size

  def get_video(self):
    return self.vids

  def left(self):
    return self.maxsize - self.size

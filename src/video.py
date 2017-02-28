import numpy as np
import cache
import request

class Video(object):
  def __init__(self, _id, _size):
    self.size = _size
    self.id = _id
    self.cache = np.array([], dtype = cache.Cache)
    self.reqs = np.array([], dtype = request.Request)

  def spv(self, c):
    total = 0
    for r in self.reqs:
      total += r.score_if_slow(c)
    return total

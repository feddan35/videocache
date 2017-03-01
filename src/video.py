import numpy as np
import cache
import request

class Video(object):
  def __init__(self, _id, _size):
    self.size = _size
    self.id = _id
    self.cache = np.array([], dtype = cache.Cache)
    self.reqs = np.array([], dtype = request.Request)
    self.posscache = set([])

  def spv(self, c):
    total = 0
    for r in self.reqs:
      total += r.score_if(c.id)
    return total

  def spvdiff(self, c):
    total = 0
    for r in self.reqs:
      total += r.score_diff_if(c.id)
    return total

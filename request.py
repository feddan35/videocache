import numpy as np

def make_requests(requests, dc):
  _requests = np.zeros(len(requests), dtype = Request)
  for i, r in enumerate(requests):
    _r = Request(dc.videos[r[0]], r[1])
    _requests[i] = _r
    dc.videos[r[0]].reqs = np.append(dc.videos[r[0]].reqs, [_r])
  return _requests

class Request(object):
  def __init__(self, vid, no):
    self.vid = vid
    self.no = no
    self.ep = None
    self.minlat = None

  def put_ep(self, ep):
    self.ep = ep
    self.minlat = ep.dclat

    for c in self.vid.cache:
      try:
        if self.ep.lats[c.id] < self.minlat:
          self.minlat = self.ep.lats[c.id]
      except KeyError:
        pass

  def getlat(self, cid):
    try:
      return self.ep.lats[cid]
    except KeyError:
      return self.ep.dclat

  def score_if(self, cid):
    try:
      lat = min(self.minlat, self.ep.lats[cid])
    except KeyError:
      lat = self.minlat
    return self.no * (self.ep.dclat - lat)

  def score_if_slow(self, cache):
    _min = self.ep.dclat
    for i in self.vid.cache:
      _min = min(_min, self.ep.lats[i.id]) if i.id in self.ep.lats.keys() else _min
    if cache.id in self.ep.lats.keys():
      return self.no * (self.ep.dclat - min(_min, self.ep.lats[cache.id]))
    else:
      return self.no * (self.ep.dclat - _min)

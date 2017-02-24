def make_requests(requests, dc):
  _requests = []
  for r in requests:
    _r = Request(dc.videos[r[0]], r[1])
    _requests.append(_r)
    dc.videos[r[0]].reqs.append(_r)
  return _requests

class Request(object):
  def __init__(self, vid, no):
    self.vid = vid
    self.no = no
    self.ep = None

  def score_if(self, cache):
    return self.no * (self.ep.dclat - min(map(lambda x: self.ep.lats[x.id] if x.id in self.ep.lats.keys() else 0, list(set(self.vid.cache + [cache])))))

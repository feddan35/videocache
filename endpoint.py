import request

def make_eps(dc_lats, ep_cache_lts, reqs, dc):
  eps = []
  n = len(dc_lats)
  for i in range(n):
    epcachelats = {}
    for data in ep_cache_lts[i]:
      epcachelats[data[0]] = data[1]
    _reqs = request.make_requests(reqs[i], dc)
    _e = Endpoint(epcachelats, dc_lats[i], _reqs)
    for r in _e.reqs:
      r.ep = _e
    eps.append(_e)
    
  return eps

class Endpoint(object):
  def __init__(self, latencies, dclat, reqs):
    self.lats = latencies
    self.dclat = dclat
    self.reqs = reqs

if __name__ == "__main__":
  print map(lambda x: x.lats, make_eps([1, 2], [[[1, 2], [2, 3]], [[0, 1], [0, 0]]], [[[1, 2],[2, 3]], [[0, 1], [0, 0]]]))

import request
import numpy as np

def make_eps(dc_lats, ep_cache_lts, reqs, dc, caches):
  n = len(dc_lats)
  eps = np.zeros(n, dtype = Endpoint)

  for i in range(n):
    epcachelats = {}
    for data in ep_cache_lts[i]:
      epcachelats[data[0]] = data[1]
    _reqs = request.make_requests(reqs[i], dc)
    _e = Endpoint(epcachelats, dc_lats[i], _reqs, i)
    for cacheid in _e.lats.keys():
      caches[cacheid].eps.append(_e)
    for r in _e.reqs:
      r.put_ep(_e)
    eps[i] = _e
  return eps

class Endpoint(object):
  def __init__(self, latencies, dclat, reqs, id):
    self.lats = latencies
    self.dclat = dclat
    self.reqs = reqs
    self.id = id

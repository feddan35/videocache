import request
import numpy as np

def make_eps(dc_lats, ep_cache_lts, reqs, dc):
  n = len(dc_lats)
  eps = np.zeros(n, dtype = Endpoint)

  for i in range(n):
    epcachelats = {}
    for data in ep_cache_lts[i]:
      epcachelats[data[0]] = data[1]
    _reqs = request.make_requests(reqs[i], dc)
    _e = Endpoint(epcachelats, dc_lats[i], _reqs)
    for r in _e.reqs:
      r.put_ep(_e)
    eps[i] = _e
  return eps

class Endpoint(object):
  def __init__(self, latencies, dclat, reqs):
    self.lats = latencies
    self.dclat = dclat
    self.reqs = reqs

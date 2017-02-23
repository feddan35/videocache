def make_eps(dc_lats, ep_cache_lts, reqs):
  eps = []
  n = len(dc_lats)
  for i in range(n):
    epcachelats = {}
    for data in ep_cache_lts[i]:
      epcachelats[data[0]] = data[1]
    eps.apend((epcachelats, dc_lats[i], 

class Endpoint(object):
  def __init__(self, latencies, dclat, reqs):
    self.lat = {}
    for latency in latencies:
      

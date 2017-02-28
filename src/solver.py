from time import time
from collections import deque

def score(req, ep):
  if len(req.vid.cache) == 0:
    return 0
  return req.no * (ep.dclat - min(map(lambda x: ep.lats[x.id] if x.id in ep.lats.keys() else 0, req.vid.cache)))

def tscore(endpoints, mode = 'ms'):
  tscore = 0
  rn = 0
  for ep in endpoints:
    for r in ep.reqs:
      tscore += score(r, ep)
      rn     += r.no
  return tscore * 1000 if mode == 'mic' else (tscore * 1000) / rn if mode == 'com' else tscore

def solve_random(caches, datacentre, endpoints):
  import random
  from cache import CacheOverflowException
  videos = datacentre.videos
  for c in caches:
    has_space = True
    while has_space:
      vid = random.choice(videos)
      try:
        c.add(vid)
      except CacheOverflowException:
        has_space = False
  return tscore(endpoints, 'com')

def byNoOfPossibleEPs(c): # heuristic 1
  return len(c.eps)

def byValuePerSize(c): # heuristic 2
  return lambda v: float(v.spv(c)) / float(v.size)

def solve(caches, datacentre, endpoints):
  caches.sort(key = byNoOfPossibleEPs)

  for i, c in enumerate(caches):
    t1 = time()

    datacentre.videos.sort(key = byValuePerSize(c), reverse = True)

    sizs = map(lambda x: x.size, datacentre.videos)
    csiz = caches[0].maxsize

    t2 = time()

    vids2add = max_knapsack(sizs, csiz)
    for v in vids2add:
      c.add(datacentre.videos[v])

    t3 = time()

    print "Cache {}/{} finished with times {}s prep + {}s knapsack".format(i, len(caches), t2 - t1, t3 - t2)
  return tscore(endpoints, 'com')

def max_knapsack(sizs, csiz):
  size = 0
  ret = []
  q = deque(zip(sizs, range(len(sizs))))
  while len(q) > 0:
    curr_elem = q.popleft()
    if curr_elem[0] > (csiz - size):
      continue
    else:
      ret.append(curr_elem[1])
      size += curr_elem[0]
  return ret

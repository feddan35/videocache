from memoized import memoized
from time import time
import numpy as np

MODE_MIL = 'ms'
MODE_MIC = 'us'
MODE_COM = 'com'
MODES = [MODE_MIL, MODE_MIC, MODE_COM]

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
  return tscore * 1000 if mode == MODES[1] else (tscore * 1000) / rn if mode == MODES[2] else tscore

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

def solve_bl_rec_ks(caches, datacentre, endpoints):
  for c in caches:
    vals = map(lambda x: x.spv(c.id), datacentre.videos)
    sizs = map(lambda x: x.size, datacentre.videos)
    csiz = caches[0].maxsize
    nvid = len(datacentre.videos)
    scor, to_add = rec_knapsack(zip(vals, sizs, range(len(vals))), csiz)
    for v in to_add:
      c.add(datacentre.videos[v[2]])
  return tscore(endpoints, 'com')

def get_values(vids):
  vals = np.zeros(vids.size)

def solve_bl_ks(caches, datacentre, endpoints):
  t1 = time()
  for c in caches:
    t3 = time()
    vals = np.zeros(datacentre.videos.size) #datacentre.getvals(c.id) #map(lambda x: x.spv(c.id), datacentre.videos)
    for x in xrange(datacentre.videos.size):
      vals[x] = datacentre.videos[x].spv(c)
    sizs = map(lambda x: x.size, datacentre.videos)
    csiz = caches[0].maxsize
    t4 = time()
    to_add = max_knapsack(vals, sizs, csiz)
    for i in to_add:
      c.add(datacentre.videos[i])
    t5 = time()
    print "Cache {}/{} {:.10f}ms".format(c.id, len(caches), (t4 - t3) * 1000)
    print "Knapsack {:.10f}ms".format((t5-t4)*1000)
  t2 = time()
  print "madagaskar {:.10f}s".format(t2 - t1)
  return tscore(endpoints, 'com')

def rec_knapsack(items, maxweight):
    
    @memoized
    def bestvalue(i, j):
        if i == 0: return 0
        value, weight, _ = items[i - 1]
        if weight > j:
            return bestvalue(i - 1, j)
        else:
            return max(bestvalue(i - 1, j),
                       bestvalue(i - 1, j - weight) + value)

    j = maxweight
    result = []
    for i in xrange(len(items), 0, -1):
        if bestvalue(i, j) != bestvalue(i - 1, j):
            result.append(items[i - 1])
            j -= items[i - 1][1]
    result.reverse()
    return bestvalue(len(items), maxweight), result

def max_knapsack(vals, sizs, csiz):
  dp = np.zeros((vals.size + 1, csiz + 1))
  
  for i in xrange(1, vals.size + 1):
    for s in xrange(1, csiz + 1):
      if sizs[i-1] > s:
        dp[i, s] = dp[i-1, s]
      else:
        dp[i, s] = max(dp[i-1, s],
                       dp[i-1, s-sizs[i-1]] + vals[i-1])

  result = []
  y = csiz
  for x in range(len(vals), 0, -1):
    added = dp[x, y] != dp[x-1, y]
    if added:
      result.append(x-1)
      y -= sizs[x-1]
  return result

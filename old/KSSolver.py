from memoized import memoized
from time import time
import numpy as np
from collections import deque


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

def byNoOfPossibleEPs(c): # heuristic 1
  return len(c.eps)

def byValuePerSize(c):
  return lambda v: float(v.spv(c)) / float(v.size)

def solve_ks_h1(caches, datacentre, endpoints):
  caches.sort(key = byNoOfPossibleEPs)
  return solve_bl_ks(caches, datacentre, endpoints)

def solve_ks_h2(caches, datacentre, endpoints):
  caches.sort(key = byNoOfPossibleEPs)
  
  for i, c in enumerate(caches):
    t1 = time()

    datacentre.videos.sort(key = byValuePerSize(c), reverse = True)

    sizs = map(lambda x: x.size, datacentre.videos)
    csiz = caches[0].maxsize

    t2 = time()

    vids2add = max_knapsack_al(sizs, csiz)
    for v in vids2add:
      c.add(datacentre.videos[v])

    t3 = time()

    print "Cache {}/{} finished with times {}s prep + {}s knapsack".format(i, len(caches), t2 - t1, t3 - t2)
  return tscore(endpoints, 'com')

def solve_bl_ks(caches, datacentre, endpoints):
  for l, c in enumerate(caches):
    t3 = time()

    vals = [0] * len(datacentre.videos)
    for x in xrange(len(datacentre.videos)):
      vals[x] = datacentre.videos[x].spv(c)
    sizs = map(lambda x: x.size, datacentre.videos)
    csiz = caches[0].maxsize

    t4 = time()

    to_add = max_knapsack5(vals, sizs, csiz)
    for i in to_add:
      c.add(datacentre.videos[i])

    t5 = time()

    print "Cache {}/{} {:.6f}s".format(l, len(caches), (t4 - t3))
    print "Knapsack {:.6f}s".format((t5-t4))
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

def dp_knapsack(vals, sizs, csiz):
  dp = np.zeros((len(vals) + 1, csiz + 1))
  
  for i in xrange(1, len(vals) + 1):
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

def max_knapsack_al(sizs, csiz):
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
  

def max_knapsack(vals, sizs, csiz):
  dpv = [0] * (csiz + 1)
  dpl = [[]] * (csiz + 1)
  for ccsize in xrange(1, csiz + 1):
    for x in xrange(len(vals)):
      if ccsize < sizs[x] or dpv[ccsize - 1] >= dpv[ccsize - sizs[x]] + vals[x]:
        dpv[ccsize] = dpv[ccsize - 1]
        dpl[ccsize] = dpl[ccsize - 1]
      else:
        dpv[ccsize] = dpv[ccsize - sizs[x]] + vals[x]
        dpl[ccsize] = dpl[ccsize - sizs[x]] + [x]
  return dpl[-1]

def max_knapsack2(vals, sizs, csiz):
  dpv = [0] * (csiz + 1)
  dpl = [[]] * (csiz + 1)
  for ccsize in xrange(1, csiz + 1):
    for x in xrange(len(vals)):
      if ccsize < sizs[x] or dpv[ccsize - 1] >= dpv[ccsize - sizs[x]] + vals[x]:
        dpv[ccsize] = dpv[ccsize - 1]
        dpl[ccsize] = dpl[ccsize - 1]
      else:
        dpv[ccsize] = dpv[ccsize - sizs[x]] + vals[x]
        dpl[ccsize] = dpl[ccsize - sizs[x]] + [x]
  return dpl[-1]

def max_knapsack3(vals, sizs, csiz):
  dp = [[0, []]] * (csiz + 1)
  for ccsize in xrange(1, csiz + 1):
    _max = dp[ccsize - 1]
    for x in xrange(len(vals)):
      if ccsize < sizs[x] or (ccsize >= sizs[x] and x in dp[ccsize - sizs[x]][1]):
        continue
      if dp[ccsize - sizs[x]][0] + vals[x] > _max[0]:
        _max = [dp[ccsize - sizs[x]][0] + vals[x], dp[ccsize - sizs[x]][1] + [x]]
    if dp[ccsize - 1][0] >= _max[0]:
      dp[ccsize] = dp[ccsize - 1]
    else:
      dp[ccsize] = _max
  return dp[-1][1]

def max_knapsack4(vals, sizs, csiz):
  dp = [(0, [])] * (csiz + 1)
  for ccsize in xrange(1, csiz + 1):
    _max = dp[ccsize - 1]
    for x in xrange(len(vals)):
      if ccsize < sizs[x] or x in dp[ccsize - sizs[x]][1]:
        continue
      if dp[ccsize - sizs[x]][0] + vals[x] > _max[0]:
        _max = (dp[ccsize - sizs[x]][0] + vals[x], dp[ccsize - sizs[x]][1] + [x])
    if dp[ccsize - 1][0] >= _max[0]:
      dp[ccsize] = dp[ccsize - 1]
    else:
      dp[ccsize] = _max
  return dp[-1][1]

import copy
def max_knapsack5(vals, sizs, csiz):
  dp = [(0, [False] * len(vals))] * (csiz + 1)
  for ccsize in xrange(1, csiz + 1):
    _max = dp[ccsize - 1][0]
    _maxx = -1
    for x in xrange(len(vals)):
      if ccsize < sizs[x] or dp[ccsize - sizs[x]][1][x]:
        continue
      if dp[ccsize - sizs[x]][0] + vals[x] > _max:
        _max = dp[ccsize - sizs[x]][0] + vals[x]
        _maxx = x
    if dp[ccsize - 1][0] >= _max:
      dp[ccsize] = dp[ccsize - 1]
    else:
      dp[ccsize] = (_max, copy.copy(dp[ccsize - sizs[_maxx]][1]))
      dp[ccsize][1][_maxx] = True
  return [x for x in range(len(dp[-1][1])) if dp[-1][1][x]]

def max_knapsack6(vals, sizs, csiz):
  dp = [(0, [False] * len(vals))] * (csiz + 1)
  for ccsize in xrange(1, csiz + 1):
    _maxx = -1
    for x in xrange(len(vals)):
      if ccsize < sizs[x] or dp[ccsize - sizs[x]][1][x]:
        continue
      if dp[ccsize - sizs[x]][0] + vals[x] > dp[ccsize - sizs[_maxx]][0] + vals[_maxx]:
        _maxx = x
    if _maxx == -1 or dp[ccsize - 1][0] >= dp[ccsize - sizs[_maxx]][0] + vals[_maxx]:
      dp[ccsize] = dp[ccsize - 1]
    else:
      dp[ccsize] = (dp[ccsize - sizs[_maxx]][0] + vals[_maxx], copy.copy(dp[ccsize - sizs[_maxx]][1]))
      dp[ccsize][1][_maxx] = True
  return dp[-1][1]

def solve_benchmark(caches, datacentre, endpoints):
    c = caches[0]
    vals = [0] * datacentre.videos.size
    for x in xrange(datacentre.videos.size):
      vals[x] = datacentre.videos[x].spv(c)
    sizs = map(lambda x: x.size, datacentre.videos)
    csiz = caches[0].maxsize
    
    fs = [dp_knapsack, max_knapsack3]

    for f in range(2):
      t1 = time()
      for i in range(100):
        fs[f](vals, sizs, csiz)
      t2 = time()
      print "{} took {:.6f}s".format(fs[f].__name__, t2 - t1)

    print dp_knapsack(vals, sizs, csiz)
    print max_knapsack3(vals, sizs, csiz)
    print sorted(dp_knapsack(vals, sizs, csiz)) == sorted(max_knapsack3(vals, sizs, csiz))

def solve_bench(no_videos, no_caches, cache_size):
  vals = list(np.random.choice(range(1000), no_videos, replace=True))
  sizs = list(np.random.choice(range(1000), no_videos, replace=True))
  
  fs = [dp_knapsack, max_knapsack3, max_knapsack4, max_knapsack5, max_knapsack6]

  for f in [0, 3, 4]:
    t1 = time()
    fs[f](vals, sizs, cache_size)
    t2 = time()
    print "{} ({}, {}) took {:.6f}s".format(fs[f].__name__, no_videos, cache_size, t2-t1)

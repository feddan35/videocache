from memoized import memoized
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

def solve_bl_ks(caches, datacentre, endpoints):
  for c in caches:
    vals = map(lambda x: sum(map(lambda req: req.score_if(c), x.reqs)), datacentre.videos)
    sizs = map(lambda x: x.size, datacentre.videos)
    csiz = caches[0].maxsize
    nvid = len(datacentre.videos)
    scor, to_add = knapsack(zip(vals, sizs, range(len(vals))), csiz)
    for v in to_add:
      c.add(datacentre.videos[v[2]])
  return tscore(endpoints, 'com')

def knapsack(items, maxweight):
    
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

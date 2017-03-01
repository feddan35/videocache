from time import time
from collections import deque
import operator
from cache import CacheOverflowException
import copy

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

def flatten(l):
  return [item for sublist in l for item in sublist]

def byValuePerSize(c): # heuristic 2
  def byVPSfunc(v):
    if v.posscache == []:
      import code; code.interact(local=locals())
    return (float(v.spvdiff(c)) / float(v.size)) / float(len(v.posscache) + 1)
  return byVPSfunc

def solve(caches, datacentre, endpoints):
  caches.sort(key = byNoOfPossibleEPs, reverse=True)

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

def solve_parallel(cs, datacentre, endpoints):
  orig_videos = []
  for c in cs:
    orig_videos.append([v for v in datacentre.videos if any(map(lambda x: c.id in x.ep.lats, v.reqs))])
  t1 = time()
  caches = copy.copy(cs)
  csizes = [caches[0].maxsize] * len(caches)
  qs = [[]] * len(caches)
  maxs = [0] * len(caches)
  while len(caches) > 0:
    vid = [0] * len(caches)
    maxs = [0] * len(caches)
    print "Sorting..."
    for i, c in enumerate(caches):
      qs[i] = sorted(orig_videos[i], key = byValuePerSize(c), reverse = True)
      maxs[i] = qs[i][vid[i]]
    finished = False
    while not finished:
      print "Recalculating..."
      cid = max(enumerate(maxs), key=operator.itemgetter(1))[0]
      if caches[cid].left() >= qs[cid][vid[cid]].size:
        print "Adding {} to {}".format(qs[cid][vid[cid]].id, caches[cid].id)
        caches[cid].add(qs[cid][vid[cid]])
        finished = True
        break
      else:
        print "Video {} doesn't fit...".format(qs[cid][vid[cid]].id)
        vid[cid] += 1
        if vid[cid] >= len(orig_videos[cid]):
          print "Cache {} is full!".format(caches[cid].id)
          del caches[cid]
          del orig_videos[cid]
          finished = True
        else:
          maxs[cid] = qs[cid][vid[cid]]
    print [x.left() for x in caches]
  t2 = time()
  print "Finished with time: {:.6f}s".format(t2 - t1)
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

class max_q(object):

  def maxqnode_val(n):
    return n.value
  
  def __init__(self, maxsize, granularity):
    self.start = None
    self.index = {}
    self.g = granularity
    for i in range(0, maxsize, granularity):
      self.index[i] = []

  def push(self, value):
    if self.start is None:
      self.start = maxq_node(value)
    else:
      new_node = maxq_node(value)
      new_node.next = self.start
      self.start.previous = new_node
      self.start = new_node
      self.index[value/g].append(self.start)
      self.index[value/g].sort(key=maxqnode_val)

  def pop(self, value):
    if self.start is None:
      return None
    else:
      old_start = self.start
      self.start.next.previous = None
      self.start = self.start.next
      self.index[old_start.value/self.g].remove(old_start)
      return old_start.value

  def relocate(self, node, value):
    self.index[node.value/self.g].remove(node.value)
    self.index[value/self.g].append(node)
    node.value = value
    if node.value < node.next.value or node.next is None:
      return
    else:
      if node == self.start:
        self.start = self.start.next
        self.start.previous = None
      while True:
        i = node.value/self.g
        
        


class maxq_node(object):

  def __init__(self, value):
    self.value = value
    self.next = None
    self.previous = None

  

if __name__ == "__main__":
  import sys, parser, endpoint, cache
  from datacentre import Datacentre
  #sys.setrecursionlimit(100000)
  filename = sys.argv[1]
  no_vids, no_eps, no_reqs, no_caches, csize, dc_lats, vidsizes, ep_cache_lts, reqs = parser.parse(filename)

  if no_vids != len(vidsizes):
    print "The virtual number of videos is different to the declared number of videos!!!"

  if no_eps != len(dc_lats):
    print "The virtual number of endpoints is different from the declared number of endpoints!!!"

  dc = Datacentre(vidsizes)  
  eps = endpoint.make_eps(dc_lats, ep_cache_lts, reqs, dc)
  cs = cache.make_caches(no_caches, csize)

  import KSSolver
  print KSSolver.solve_random(cs, dc, eps)

  dc = Datacentre(vidsizes)
  eps = endpoint.make_eps(dc_lats, ep_cache_lts, reqs, dc)
  cs = cache.make_caches(no_caches, csize)

  print KSSolver.solve_bl_ks(cs, dc, eps)


  #import code; code.interact(local=locals())

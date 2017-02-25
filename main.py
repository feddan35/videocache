if __name__ == "__main__":
  import sys, parser, endpoint, cache
  from datacentre import Datacentre
  from time import time
  
  filename = sys.argv[1]
  t1 = time()
  no_vids, no_eps, no_reqs, no_caches, csize, dc_lats, vidsizes, ep_cache_lts, reqs = parser.parse(filename)
  t2 = time()
  print "parser took {:.10f}ms".format((t2 - t1)*1000)

  if no_vids != len(vidsizes):
    print "The virtual number of videos is different to the declared number of videos!!!"

  if no_eps != len(dc_lats):
    print "The virtual number of endpoints is different from the declared number of endpoints!!!"

  dc = Datacentre(vidsizes)  
  eps = endpoint.make_eps(dc_lats, ep_cache_lts, reqs, dc)
  cs = cache.make_caches(no_caches, csize)

  import KSSolver
  #print KSSolver.solve_random(cs, dc, eps)

  #dc = Datacentre(vidsizes)
  #eps = endpoint.make_eps(dc_lats, ep_cache_lts, reqs, dc)
  #cs = cache.make_caches(no_caches, csize)

  print KSSolver.solve_bl_ks(cs, dc, eps)


  import code; code.interact(local=locals())

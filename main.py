if __name__ == "__main__":
  import sys, parser
  from datacentre import Datacentre
  filename = sys.argv[1]
  no_vids, no_eps, no_reqs, no_caches, csize, dc_lats, vidsizes, ep_cache_lts, reqs = parser.parse(filename)

  if no_vids != len(vidsizes):
    print "The virtual number of videos is different to the declared number of videos!!!"

  if no_eps != len(dc_lats):
    print "The virtual number of endpoints is different from the declared number of endpoints!!!"

  if no_reqs != len(reqs):
    print "The virtual number of requests is different from the declared number of requests!!!"

  dc = Datacentre(vidsizes)  
  eps = endpoint.make_eps(dc_lats, ep_cache_lts, reqs)
  #cs = cache.make_caches(no_caches, csize)

  print map(lambda x: "{} {}\n".format(x.id, x.size),dc.videos)
  

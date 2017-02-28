if __name__ == "__main__":
  import sys, os, zipfile
  from time import time

  import src.parser as parser
  import src.serializer as serializer
  import src.endpoint as endpoint
  import src.cache as cache
  import src.datacentre as datacentre
  import src.solver as solver

  for f in ['me_at_the_zoo', 'trending_today', 'videos_worth_spreading', 'kittens']:

    filenamein = 'input/' + f + '.in'
    t1 = time()
    no_vids, no_eps, no_reqs, no_caches, csize, dc_lats, vidsizes, ep_cache_lts, reqs = parser.parse(filenamein)
    t2 = time()
    print "parsing {} took {:.3f}s".format(filenamein, t2 - t1)

    dc = datacentre.Datacentre(vidsizes)
    cs = cache.make_caches(no_caches, csize)
    eps = endpoint.make_eps(dc_lats, ep_cache_lts, reqs, dc, cs)

    print solver.solve(cs, dc, eps)

    filenameout = 'output/' + f + '.out'
    serializer.serialize(cs, filenameout)

  zipf = zipfile.ZipFile('output/submission.zip', 'w', zipfile.ZIP_DEFLATED)
  for file in os.listdir('.'):
    if file[-3:] == '.py':
      zipf.write(file)
  zipf.close()

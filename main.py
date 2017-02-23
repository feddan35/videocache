if __name__ == "__main__":
  import sys, parser
  filename = sys.argv[1]
  no_vids, no_eps, no_reqs, no_caches, csize, dc_lats, vidsizes, ep_cache_lts, reqs = parser.parse(filename)

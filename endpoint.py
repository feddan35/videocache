class Endpoint(object):
  def __init__(self, latencies):
    self.lat = {}
    for latency in latencies:
      

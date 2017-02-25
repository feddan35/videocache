from video import Video
import numpy as np

class Datacentre(object):
  def __init__(self, videos):
    self.videos = np.zeros(len(videos), dtype = Video)
    for i, size in enumerate(videos):
      self.videos[i] = Video(i, size)

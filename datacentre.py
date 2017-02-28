from video import Video
import numpy as np

class Datacentre(object):
  def __init__(self, videos):
    self.videos = []
    for i, size in enumerate(videos):
      self.videos.append(Video(i, size))

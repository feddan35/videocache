from video import Video

class Datacentre(object):
  def __init__(self, videos):
    self.videos = []
    id = 0
    for video_size in videos:
      self.videos.append(Video(id, video_size))
    

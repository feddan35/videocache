def serialize(caches, filepath):
  with open(filepath, 'w') as f:
    f.write(str(len(caches)))
    f.write('\n')
    for c in caches:
      f.write(str(c.id) + " ")
      f.write(" ".join(map(lambda x: str(x.id), c.vids)))
      f.write('\n')

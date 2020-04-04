scores = []

def get_high_scores(current_score):
  return

with open('scores.txt') as f:
  for points in f:
    points = points.strip()
    points = int(points)
    scores.append(points)
    scores.sort(reverse=True)
    if scores is < 10:
      print(scores)
      else:
        print[0:10]

    


  

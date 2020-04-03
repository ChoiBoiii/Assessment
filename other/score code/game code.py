print('how many of each enermy do you want??')
numenemy1 = input('number of enemy lvl 1 units: ')
print('you have selected', numenemy1, 'lvl 1 units')
numenemy2 = input('number of enemy lvl 2 units: ')
print('you have selected', numenemy2, 'lvl 2 units')
numenemy3 = input('number of enemy lvl 3 units: ')
print('you have selected', numenemy3, 'lvl 3 units')
numboss = input('number of enemy BOSS units: ')
print('you have selected', numboss, 'BOSS units')

numenemy1 = int(numenemy1)
numenemy2 = int(numenemy2)
numenemy3 = int(numenemy3)
numboss = int(numboss)

boss = 1000
enemy1 = 100
enemy2 = 200
enemy3 = 300

stuff_to_write_to_file = ""

with open('file.txt') as f:
  for points in f:
    points = points.strip()
    points = int(points)
    points += boss * numboss
    points += enemy1 * numenemy1
    points += enemy2 * numenemy2
    points += enemy3 * numenemy3
    stuff_to_write_to_file = stuff_to_write_to_file + str(points)+"\n"
    break
    
print('your total score is: ', points)

with open('file.txt', 'w') as f:
  f.write(stuff_to_write_to_file)

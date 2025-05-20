import imageio.v2 as imageio
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
from matplotlib.colors import ListedColormap
from math import *
from time import *

def count_alives(land, n, m):
    res = 0
    for i in range(n-1, n+2):
        for j in range(m-1, m+2):
            if i >= len(land) and j >= len(land):
                if land[0, 0] == 1:  
                    res+=1 
            elif i >= len(land):
                if land[0, j] == 1:
                    res+=1 
            elif j >= len(land):
                if land[i, 0] == 1:
                    res+=1
            elif i == n and j == m:
                pass
            else:
                if land[i, j] == 1:
                    res+=1
                        
    return res

def count_predators(land, n, m):
    res = 0
    for i in range(n-1, n+2):
        for j in range(m-1, m+2):
            if i >= len(land) and j >= len(land):
                if land[0, 0] == 2:  
                    res+=1 
            elif i >= len(land):
                if land[0, j] == 2:
                    res+=1 
            elif j >= len(land):
                if land[i, 0] == 2:
                    res+=1
            elif i == n and j == m:
                pass
            else:
                if land[i, j] == 2:
                    res+=1
                        
    return res

f = open('images/start', 'r')
n = len(list(f.readline().split()))
land = np.empty((n, n))
f.close()

f = open('images/start', 'r')

for i in range(len(land)):
    land[i] = np.array([list(f.readline().split(" "))])

f.close()

plt.ion()
fig, ax = plt.subplots(figsize=(9, 9), dpi=120)
colors = ['white', 'black', 'red']
cmap_custom = ListedColormap(colors)
plt.show()
frames = []
frame_id = 0
os.makedirs("frames", exist_ok=True)

while(True):
    new_land = np.zeros((len(land), len(land)))
    for i in range(len(land)):
        for j in range(len(land[i])):
            if land[i, j] == 1 and (count_alives(land, i, j) < 2 or count_alives(land, i, j) > 3):
                new_land[i, j] = 0
            elif land[i, j] == 0 and count_alives(land, i, j) == 3:
                new_land[i, j] = 1
            elif land[i, j] == 0 and count_alives(land, i, j) >=1 and count_predators(land, i, j)>=2:
                new_land[i, j] = 2 
            elif land[i, j] == 2 and count_alives(land, i, j) == 0:
                new_land[i, j] = 0
            else:
                new_land[i, j] = land[i, j]
    
    land = new_land

    if not((1 in land)) and not((2 in land)):
        f = open('images/end', 'r')
        n = len(list(f.readline().split()))
        f.close()

        end = np.empty((5, n))
        f = open('images/end', 'r')
        for i in range(5):
            end[i] = np.array([list(f.readline().split(" "))])
        f.close()

        ax.clear()
        ax.imshow(end, cmap='binary', vmin=0, vmax=1)
        ax.axis('off')
        
        fig.canvas.draw()
        fig.canvas.flush_events()
        final_frame = f"frames/frame_{frame_id:04d}.png"
        plt.savefig(final_frame)
        frames.append(imageio.imread(final_frame))
        sleep(2)
        break
    

    ax.clear()
    ax.imshow(land, cmap=cmap_custom, vmin=0, vmax=2)
    ax.axis('off')
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    filename = f"frames/frame_{frame_id:04d}.png"
    plt.savefig(filename)
    frames.append(imageio.imread(filename))
    frame_id += 1
    
    if frame_id == 50:
        f = open('images/end', 'r')
        n = len(list(f.readline().split()))
        f.close()

        end = np.empty((5, n))
        f = open('images/end', 'r')
        for i in range(5):
            end[i] = np.array([list(f.readline().split(" "))])
        f.close()

        ax.clear()
        ax.imshow(end, cmap='binary', vmin=0, vmax=1)
        ax.axis('off')
        
        fig.canvas.draw()
        fig.canvas.flush_events()
        final_frame = f"frames/frame_{frame_id:04d}.png"
        plt.savefig(final_frame)
        frames.append(imageio.imread(final_frame))
        sleep(2)
        break


    sleep(0.01)

imageio.mimsave("GIFs/game_of_life.gif", frames, duration=0.1)
for f in os.listdir("frames"):
    os.remove(os.path.join("frames", f))
os.rmdir("frames")
plt.close()

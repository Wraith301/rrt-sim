import pygame
import random
import sys
import numpy as np

class Node:
	def __init__(self,x,y,parent=None):
		self.x=x
		self.y=y
		self.parent=parent
pygame.init()

HEIGHT=512
WIDTH=512
clock=pygame.time.Clock()

tree=[]
path=[]

start = Node(20,20)
goal = Node(400,400)

tree.append(start)

def sample_closest(tree):
	xs=random.randint(0,WIDTH)
	ys=random.randint(0,HEIGHT)
	rho=20

	dist=sys.maxsize
	parent=None
	for node in tree:
		dist_node=(((node.x-xs)**2) + ((node.y-ys)**2))**0.5
		if dist_node<dist:
			dist=dist_node
			xn=node.x
			yn=node.y
			parent=node

	v=np.array([xs-xn,ys-yn])
	u_hat=v/np.linalg.norm(v)

	offset=rho*u_hat
	xf=xn+offset[0]
	yf=yn+offset[1]
	new_node=Node(xf,yf,parent)


	return new_node


def reconstruct(node):
	while node:
		path.append(node)
		node=node.parent


final_node=None
reconstruct(final_node)



screen = pygame.display.set_mode([512, 512])
screen.fill((0, 0, 0))

pygame.draw.circle(screen,(0,255,0),(start.x,start.y),6,width=0)
pygame.draw.circle(screen,(255,0,0),(goal.x,goal.y),6,width=0)

running = True
path_found=False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not path_found:
	    new_node=sample_closest(tree)
	    tree.append(new_node)
	    pygame.draw.circle(screen,(0,150,150),(new_node.x,new_node.y),3,width=0)
	    dist=((new_node.x-goal.x)**2 + (new_node.y-goal.y)**2)**0.5
	    if dist<30:
    		final_node=new_node
    		path_found=True
    else:
    	reconstruct(final_node)
    	pygame.draw.line(screen,(255,255,255), (goal.x,goal.y), (final_node.x,final_node.y), width=1)
    	for p in path:
    		pygame.draw.circle(screen,(0,0,255),(p.x,p.y),4,width=0)
    		pygame.draw.line(screen,(255,255,255), (p.x,p.y), ((p.parent.x,p.parent.y) if p.parent else (start.x,start.y)), width=1)

    pygame.display.update()
    clock.tick(10)
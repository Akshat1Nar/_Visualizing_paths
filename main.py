import math
import random
import sys
from collections import namedtuple
from math import sqrt
from collections import namedtuple
import pygame



#A named tuple to store dimension of various block drawn on screen
dimension = namedtuple('dimension',['height','width'])



#initializing pygame and it's window with resolution(800,600)
pygame.init()
screen=pygame.display.set_mode((800,600))
icon = pygame.image.load('./Png/icon.png')
pygame.display.set_icon(icon)




#It will work to store adjacent unblocked cells
#for this code f,g,h are of less importance..we can
cell= namedtuple('cell',['i_parent','j_parent','f','g','h'])
cell_ = namedtuple('cell_',['i','j'])
openList= namedtuple('openList',['value','i','j'])





'''  Class to evaluate the shortest path problem
     given a matrix of blocked elements, coordinates
     of source and destination; using A star Algorithm 
'''

class Graph():


	''' Initializing the attributes of class to be that of a matrix
		(row, col, matrix) and adding a traceback graph attribute to
		retrace the path from source to destination.
	'''
	def __init__(self,row,col,matrix):
		#self.ripples=[]
		self.row=row
		self.col=col
		self.matrix = matrix
		self.traceback_graph= ( [[cell(-1,-1,sys.float_info.max,sys.float_info.max,sys.float_info.max) 
										for _ in range(col)] for __ in range(row)] )
		self.path=[]
		self.closed_cells= [ [ False for _ in range(self.col)] for __ in range(self.row)]

		

	
	#Function to if given (r,c) is valid for a given matrix
	def check_valid(self,r,c):
		if( ((r<=-1 or r>=self.row) or (c<=-1 or c>=self.col)) ):
			return 0
		return 1


	#To check if a given block is unblocked or not
	def is_unblocked(self,r,c):
		if(self.matrix[r][c]==0):
			return 1
		return 0


	#To check if a given cell is destination or not
	def is_destination(self,r,c,dst):
		if(r==dst.i and c==dst.j):
			return 1
		return 0

	#A function to keep track of value of respective paths so as to choose
	#path with smallest value when at destination
	def calculateHValue(self,r,c,dest):
		return (sqrt( (r-dest.i)**2 + (c-dest.j)**2 )) 


	#A function to execute a given (r,c) for traceback_graph
	def execute_every(self,org_r,org_c,r,c,dst,Open_list__list,foundDest,help):


		if(self.check_valid(r,c) == 1):

			if(self.is_destination(r,c,dst)==1):

				

				self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(i_parent = org_r)
				self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(j_parent = org_c)

				
				self.tracepath(dst)
				foundDest = True
				return

			

			elif( self.closed_cells[r][c] == False and self.is_unblocked(r,c) == 1):
				
				self.closed_cells[r][c]=True

				gNew = self.traceback_graph[r][c].g + 1.0
				if(help==True):
					gNew+=0.414
				hNew = self.calculateHValue(r,c,dst)
				fNew = gNew+hNew


				if ( (self.traceback_graph[r][c].f == sys.float_info.max) or 
					(self.traceback_graph[r][c].f > fNew)):

					Open_list__list.append(openList(fNew,r,c))
					
					self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(f=fNew)
					self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(g=gNew)
					self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(h=hNew)
					self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(i_parent=org_r)
					self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(j_parent=org_c)
					


		return foundDest


	''' A function to traceback path given according to traceback array
		for the shortest point
	'''
	def tracepath(self,dst):

		if(len(self.path)!=0):
			return
		
		ro=dst.i
		co=dst.j

		while( (self.traceback_graph[ro][co].i_parent!=ro) or
					(self.traceback_graph[ro][co].j_parent!=co)):

			self.path.append(cell_(ro,co))
			temp_ro = self.traceback_graph[ro][co].i_parent
			temp_co = self.traceback_graph[ro][co].j_parent
			ro=temp_ro
			co=temp_co


		self.path.append(cell_(ro,co))
		return
		

	'''A gui function that uses the implimentation of Gui class in the same program
		to update colour of block every time a block is executed with execute_every
	'''
	def ripples(self,i,j):
		run.base()
		run.special_grid()
		run.color_column[j][i]=(255,0,0)
		run.base()
		run.special_grid()



	'''Driver function of this class which starts with a queue and processes every
	   block around it by pushing it into queue and then operating block around it.


	   example -----                  N-W   N  N-E
										 \	|  /
										  \	| /
	   								W-----block(6,7)-----E
	   									  /	| \
	   									 /	|  \
	   								   S-W	S   S-E


		It also updates the color of the processed blocks for visualization

	'''
	def aStarSearch(self,src,dst):

		if(self.check_valid(src.i,src.j)==0):
			return 0

		if(self.check_valid(dst.i,dst.j)==0):
			return 0

		if(self.is_unblocked(src.i,src.j)==0 or self.is_unblocked(dst.i,dst.j)==0 ):
			return 0

		if(src==dst):
			self.path.append(src)
			self.path.append(src)
			self.path.append(src)
			return self.path
		

		#Initaialising the parameters of starting node
		r= src.i 
		c=src.j
		self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(f=0.0)
		self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(g=0.0)
		self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(h=0.0)
		self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(i_parent=r)
		self.traceback_graph[r][c]=self.traceback_graph[r][c]._replace(j_parent=c)

		Open_list__list = []
		Open_list__list.append(openList(0.0,r,c))

		foundDest = False
		

		while(len(Open_list__list)!=0):


			
			element = Open_list__list.pop(0)
			r=element.i
			c=element.j
			run.run_clock()
			if(element.i!=src.i or element.j!=src.j):
				self.ripples(r,c)
			self.closed_cells[r][c] = True
			
			
			#############-----North-----#############
			foundDest = self.execute_every(r,c,r-1,c,dst,Open_list__list,foundDest,False)
			#############-----South-----#############
			if foundDest==False :
				foundDest = self.execute_every(r,c,r+1,c,dst,Open_list__list,foundDest,False)
			else:
				return	[self.path,self.ripples]
			#############-----East-----#############
			if foundDest==False :
				foundDest = self.execute_every(r,c,r,c+1,dst,Open_list__list,foundDest,False)
			else:
				return  [self.path,self.ripples]
			#############-----West-----#############
			if foundDest==False :
				foundDest = self.execute_every(r,c,r,c-1,dst,Open_list__list,foundDest,False)
			else:
				return  [self.path,self.ripples]
			#############-----North-East-----#############
			if foundDest==False :
				foundDest = self.execute_every(r,c,r-1,c+1,dst,Open_list__list,foundDest,True)
			else:
				return  [self.path,self.ripples]
			#############-----North-West-----#############
			if foundDest==False :
				foundDest = self.execute_every(r,c,r-1,c-1,dst,Open_list__list,foundDest,True)
			else:
				return  [self.path,self.ripples]
			#############-----South-East-----#############
			if foundDest==False :
				foundDest = self.execute_every(r,c,r+1,c+1,dst,Open_list__list,foundDest,True)
			else:
				return  [self.path,self.ripples]
			#############-----South-West-----#############
			if foundDest==False :
				foundDest = self.execute_every(r,c,r+1,c-1,dst,Open_list__list,foundDest,True)
			else:
				return  [self.path,self.ripples]


		if (foundDest== False):
			return 0

		






''' GUI interface for A-star Algorithm
	It involves drag select functonality for blocked elements
	It involves source select
	It involves destination select
	And a run button
'''
class Interface:

	def __init__(self):
		
		self.black= (0,0,0)
		self.width_column=15
		self.height_column=15
		self.margin=5
		self.list_column_left = []
		self.list_column_right = []

		#Two color column matrices to keep track of color of the grid displayed
		#and update is as the blocks are being processed
		self.color_column=[ [(255,255,255) for i in range(40)] for j in range(40)]
		self.color_column__=[ [(255,255,255) for i in range(40)] for j in range(40)]


		#Grid to store input matrix by setting all blocked elements to '1'
		self.grid = [[0 for i in range(40)] for j in range(40)]


		
		#storing icons for source,destination,play respectively
		self.src = pygame.transform.scale(pygame.image.load('./Png/source.png'), (30,30) )
		self.dst = pygame.transform.scale(pygame.image.load('./Png/dst.png'), (30,30) )
		self.play =pygame.transform.scale(pygame.image.load('./Png/play.png'), (50,50) )
		

		self.src_color=(255,255,255)
		self.dst_color=(255,255,255)
		self.play_color=(255,255,255)
		
		
		self.source_check=False
		self.destination_check=False
		self.play_check=False

		self.running = True
		self.drag=False

		self.destination=cell_(-1,-1)
		self.source=cell_(-1,-1)
		self.path=[]

		self.diamonds_points = []


		diamond_wid=8

		#This stores a diamond matrix which work as cuts for square matrix
		for i in range(37):
			for j in range(24):
				pos1=(59+(17*(i+1)+1*i),(64)+(17*(j+1)+1*j)) 
				pos2 = (pos1[0] - diamond_wid/2, pos1[1] + diamond_wid/2)
				pos3 = (pos1[0], pos1[1]+diamond_wid)
				pos4 = (pos2[0]+diamond_wid, pos2[1])
				self.diamonds_points.append( [pos1,pos2,pos3,pos4] )
		

	def check(self,pos):
		col=pos[0]
		row=pos[1]

		if  row>=10 and row<=40:
			if  col>=200 and col<=255:
				self.src_color=(255,255,77)
				self.base()
				self.special_grid()
				return 1

			if  col>=400 and col<=430:
				self.dst_color=(0,128,85)
				self.base()
				self.special_grid()
				return 2

			if  col>=600 and col<=630:
				self.play_color=(0,0,0)
				self.base()
				self.special_grid()
				return 3

		elif row>=70 and row <=(527) and col>=60 and col<=(747):
			return 4

		else:
			return 0


	def fill_grid(self,pos):
		pos = (pos[0]-60,pos[1]-70)
		row = pos[0] // (self.width_column+3)
		col = pos[1] // (self.height_column+3)
		self.grid[col][row] = 1
		self.color_column[row][col] = (112,11,55)


	def add_src(self):
		self.source_check=True
		temp_running = True

		while temp_running:
			for event in pygame.event.get():
				
				if event.type == pygame.MOUSEBUTTONDOWN:
					
					temp_running=False
					pos = pygame.mouse.get_pos()
					
					pos = (pos[0]-60,pos[1]-70)
					row = pos[0] // (self.width_column+3)
					col = pos[1] // (self.height_column+3)
					self.source=self.source._replace(j=row)
					self.source=self.source._replace(i=col)

					self.color_column[row][col]=self.src_color
					return

	def add_dst(self):
		self.destination_check=True
		temp_running = True

		while temp_running:
			for event in pygame.event.get():
				
				if event.type == pygame.MOUSEBUTTONDOWN:
					
					temp_running=False
					pos = pygame.mouse.get_pos()
					
					pos = (pos[0]-60,pos[1]-70)
					row = pos[0] // (self.width_column+3)
					col = pos[1] // (self.height_column+3)
					self.destination=self.destination._replace(j=row)
					self.destination=self.destination._replace(i=col)

					self.color_column[row][col]=self.dst_color
					return




	def playb(self):

		
		g=Graph(25,38,self.grid)
		self.path.append(g.aStarSearch(self.source,self.destination))

		if(self.path[0]==0):
			self.__init__()
			return



		help=self.path[0][0]
		
		help.pop(len(help)-1)

		while(len(help)!=1):

			temp=help.pop(len(help)-1)
			
			i=temp.i
			j=temp.j
			#self.color_picture[j][i] = True
			self.color_column[j][i]=(77,106,255)


	def base(self):
		screen.fill((0,4,26))
		pygame.draw.rect(screen,self.src_color,(200,10,30,30),0)
		screen.blit(self.src,(200,10))
		pygame.draw.rect(screen,self.dst_color,(400,10,30,30),0)
		screen.blit(self.dst,(400,10))
		pygame.draw.rect(screen,self.play_color,(600,10,30,30),0)
		screen.blit(self.play,(590,1))			
		rectangle = pygame.draw.rect(screen,self.black,(59,69,744-60,520-70),0)


	def special_grid(self):
		for i in range(37):
			for j in range(24):
				pygame.draw.polygon(screen,(77,106,255),self.diamonds_points[i*24+j*1],0)


		for i in range(38):
			for j in range(25):
				pygame.draw.rect(screen,self.color_column[i][j],
										(60+i*3+i*self.width_column,70+j*3+j*self.height_column,self.width_column,self.height_column),0)


	def run_clock(self):
		clock=pygame.time.Clock()
		clock.tick(60)
		pygame.display.set_caption("A* Interface :: FPS: %i " %clock.get_fps())
		pygame.display.update()



	'''Driver function for GUI interface
	   It sets the base screen, draws special grids,
	   takes input and then gets to work!
	'''
	def screen(self):

		

		while self.running:

			self.base()
			self.special_grid()
			
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					self.running=False


				elif event.type == pygame.MOUSEBUTTONDOWN:

					pos = pygame.mouse.get_pos()
					
					if(self.check(pos)==1): #area of source_select
						if(self.source_check==False):
								self.add_src()
					elif(self.check(pos)==2): #area of destination_select
						if(self.destination_check==False):
							self.add_dst()
					elif(self.check(pos)==3): #area of play_select
						if(self.play_check==False and self.source_check==True and self.destination_check==True):
							self.playb()
					elif(self.check(pos)==4): #area of grid
						self.fill_grid(pos)
						self.drag=True


				elif self.drag==True:
					if event.type !=pygame.MOUSEBUTTONUP:

						pos=pygame.mouse.get_pos()
						if(self.check(pos)==4):
							self.fill_grid(pos)
						else:
							self.drag=False
								
					else:
						self.drag=False
						
						
					


					
					
			self.run_clock()


#Creating instance of Interface class and running the driver function
run = Interface()
run.__init__()
run.screen()

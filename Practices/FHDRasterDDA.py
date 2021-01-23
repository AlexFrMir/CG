import array, time, threading
import random as rn
import math as mt
import numpy as np

class FHDRaster(object):
	"""docstring for FHDRasterBresenham"""
	def __init__(self, name, width, height, maxval):
		super(FHDRaster, self).__init__()
		# PPM Header
		self.name = name
		self.width = width
		self.height = height
		self.maxval = maxval
		self.ppm_header = f'P6 {self.width} {self.height} {self.maxval}\n'
		# PPM Image data (filled with black)
		self.image = array.array('B',[0, 0, 0] * self.width * self.height)

	def p(self,x1,y1,x2,y2):
		dx = x2 - x1
		dy = y2 - y1
		p = 2 * dy - dx
		return p
	
	def swap(self,v1,v2):
		temp = v1
		v1 = v2
		v2 = temp
		return v1,v2

	def drawline(self, x1, y1, x2, y2, r, g, b):
		print("Drawing line with points (", x1 , ",", y1, ") -> (", x2, ", ", y2, ")", end = " ")
		print("-> rgb (", r, ",", g, ",", b, ")")		
		if (x1>x2 or y1 > y2):
			x1,x2 = self.swap(x1,x2)
			y1,y2 = self.swap(y1,y2)
		p = self.p(x1,y1,x2,y2)
		swip_flag = False
		self.setpixel(x1, y1, r, g, b)
		self.setpixel(x2, y2, r, g, b)
		
		if p > 0:			
			#swip x and y 
			x1,y1 = self.swap(x1,y1)
			x2,y2 = self.swap(x2,y2)			 
			swip_flag = True

		if (x2 - x1) == 0 :
			m = 0
		else:
			m = (y2 - y1) / (x2 - x1)
		be = y1 - (m*x1)

		y = m * x1 + be
		if x1 == x2:
			for y in range(y1 + 1, y2):
				self.setpixel(abs(x1),abs(round(y)),r,g,b)
		else:	
			for x in range(x1 + 1, x2):
				y = y + m
				if swip_flag == False:
					self.setpixel(abs(x),abs(round(y)),r,g,b)
				else:
					self.setpixel(abs(round(y)), abs(x),r,g,b)
	
	def rotation_line(self,x1,y1,x2,y2,r,g,b,angle):
		X1 = x1 * mt.cos(angle) - y1 * mt.sin(angle)
		Y1 = x1 * mt.sin(angle) + y1 * mt.cos(angle)
		X2 = x2 * mt.cos(angle) - y2 * mt.sin(angle)
		Y2 = x2 * mt.sin(angle) + y2 * mt.cos(angle)
		self.drawline(abs(round(X1)),abs(round(Y1)),abs(round(X2)),abs(round(Y2)),r,g,b)
	
	def rotation_line_noabs(self,x1,y1,x2,y2,r,g,b,angle):
		X1 = x1 * mt.cos(angle) - y1 * mt.sin(angle)
		Y1 = x1 * mt.sin(angle) + y1 * mt.cos(angle)
		X2 = x2 * mt.cos(angle) - y2 * mt.sin(angle)
		Y2 = x2 * mt.sin(angle) + y2 * mt.cos(angle)
		self.drawline(round(X1),round(Y1),round(X2),round(Y2),r,g,b)
	
	def rotate_axe_x(self,x1,y1,x2,y2,r,g,b,angle):
		X1 = x1 * mt.cos(angle) - y1 * mt.sin(angle)
		Y2 = y2
		Y1 = y1
		X2 = x2 * mt.cos(angle) - y2 * mt.sin(angle)
		self.drawline(abs(round(X1)),abs(round(Y1)),abs(round(X2)),abs(round(Y2)),r,g,b)

	def rotate_axe_y(self,x1,y1,x2,y2,r,g,b,angle):
		X1 = x1 
		Y2 = x2 * mt.sin(angle) + y2 * mt.cos(angle)
		Y1 = x1 * mt.sin(angle) + y1 * mt.cos(angle)
		X2 = x2 
		self.drawline(abs(round(X1)),abs(round(Y1)),abs(round(X2)),abs(round(Y2)),r,g,b)	

	def rotation_point(self,x,y,r,g,b,angle):
		X = x * mt.cos(angle) - y * mt.sin(angle)
		Y = x * mt.sin(angle) + y * mt.cos(angle)
		self.setpixel(round(X),round(Y),r,g,b)

	def generate_random_lines(self,num_random): 
		threads = []
		for iterator in range(0,num_random):
			y1 = rn.randint(0,self.height-1)
			y2 = rn.randint(0,self.height-1)
			x1 = rn.randint(0,self.width-1)
			x2 = rn.randint(0,self.width-1)
			r = rn.randint(0,255)
			g = rn.randint(0,255)
			b = rn.randint(0,255)
			print(iterator,end=" ")
			t = threading.Thread(target=self.drawline(x1, y1, x2, y2, r, g, b))
			time.sleep(0.1)
			threads.append(t)
			t.start()
			
	def Projection(self,f):
		matrix = np.zeros([3,4])
		resoult = np.zeros(3)
		print(matrix)
		line = [120,200,2]
		print(line)
		line.append(1)
		print(line)

		for y in range(0,len(matrix)):
			for x in range(0,len(matrix[0])):
				if(y == x and x!=len(matrix)-1):
					matrix[x][y] = 1
				elif(y == x and x == len(matrix)-1):
					matrix[x][y] = 1 /  f
		matrix = matrix * line
		print(matrix)
		iterador = 0
		for row in matrix:
			for date in row:
				resoult[iterador] += date
			iterador +=1
		print(resoult)
		self.drawline(0,0,round(f*resoult[0]/resoult[2]),round(f*resoult[1]/resoult[2]),255,255,255)
		


	def setpixel(self, x, y, r, g, b):
		index = 3 * (y * self.width + x)
		self.image[index] = r
		self.image[index + 1] = g
		self.image[index + 2] = b
		with open(self.name + '.ppm', 'wb') as f:
			f.write(bytearray(self.ppm_header, 'ascii'))
			self.image.tofile(f)	
	

	def get_information(self):
		print("Name:\n\t", self.name)
		print("width:\n\t" ,self.width)
		print("height:\n\t" ,self.height)
		print("maxval:\n\t" ,self.maxval)
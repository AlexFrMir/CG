import os, time, threading
import numpy as np
from FHDRasterDDA2 import *
from wavefront2 import *

def points_distance(self,x1,y1,x2,y2):
	return mt.sqrt(mt.pow((x2-x1),2.0)+mt.pow((y2-y1),2.0))
        
def getting_scaling(obj,image,x_min,y_min,x_max,y_max):
	print(x_min,y_min,x_max,y_max)
	max = 0
	if x_min != 0:
		x_max += -x_min
		x_min += -x_min
	if y_min != 0:	
		y_max += -y_min
		y_min += -y_min

	print(x_min,y_min)
	print(x_max,y_max)
	if x_max-x_min < y_max-y_min:
		distance = y_max-y_min
		max = image.height
		d = y_max
	else:
		distance = x_max-x_min
		max = image.width
		d = x_max
	print(max)
	num = 0
	flag = False
	while num < max and flag is False:
		for vertice in obj.vertices:
			if vertice[0]*num >= image.height or vertice[1]*num >=image.width:
				flag = True
		num+=1
	return(num-1)


def scaling_image(image,obj):
	scale = 1
	minx = obj.min_x_coords()
	miny = obj.min_y_coords()
	maxx = obj.max_x_coords()
	maxy = obj.max_y_coords()
	flag = False
	while(flag is False):
		P1_1 = int(-(minx)+minx*scale)
		P1_2 = int((-miny+miny)*scale)
		P2_1 = int((-minx+maxx)*scale)
		P2_2 = int((-miny+maxy)*scale)
		if (P2_2 < image.width and P2_1 < image.height):
			scale = scale + 1
		else:
			flag = True
	
	return scale
	pass

def generate_random_images(num_images):
	threads = []
	for x in range(0,num_images):
		image = FHDRaster("Random"+ str(x), 2560, 1440, 3)
		t = threading.Thread(target = image.generate_random_lines(1))
		threads.append(t)
		print(x)
	print("end")
	t.start()

def printing_polygons(nuevo,obj,polygon):
	for poly in polygon:
		vertice1 = obj.vertices[poly[0]]
		vertice2 = obj.vertices[poly[1]]
		P1_1 = int(vertice1[0]*1000+nuevo.midwidth)
		P1_2 = int(vertice1[1]*1000+nuevo.midheight)
		P2_1 = int(vertice2[0]*1000+nuevo.midwidth)
		P2_2 = int(vertice2[1]*1000+nuevo.midheight)
		nuevo.drawline(P1_1,P1_2,P2_1,P2_2,255,255,255)
	pass

def printing_first_polygons(image,obj,polygons,scaling):
	x,y = obj.minimum_coords()
	for iterador in range (0,len(polygons)-1):
		#print(polygons[iterador])
		poly1 = polygons[iterador]
		poly2 = polygons[iterador+1]
		vertice1 = obj.vertices[poly1[0]]
		vertice2 = obj.vertices[poly2[0]]
		x1 = int(vertice1[0]*scaling+(1*(-x)*scaling))
		y1 = int(vertice1[1]*scaling+(1*(-y)*scaling))
		x2 = int(vertice2[0]*scaling+(1*(-x)*scaling))
		y2 = int(vertice2[1]*scaling+(1*(-y)*scaling))
		#image.drawline(x1,y1,x2,y2,255,255,255)
		image.rotation_line(x1,y1,x2,y2,255,255,255,180)

def printing_center_polygons(image,obj,polygons,rotating,x,y,scaling):
	
	for iterador in range (0,len(polygons)-1):
		#print(polygons[iterador])
		poly1 = polygons[iterador]
		poly2 = polygons[iterador+1]
		vertice1 = obj.vertices[poly1[0]]
		vertice2 = obj.vertices[poly2[0]]
		P1_1 = int((vertice1[0]+x)*scaling)+image.midheight 
		P1_2 = int((vertice1[1]+y)*scaling) + image.midwidth
		P1_3 = int((vertice1[2])*scaling)
		P2_1 = int((vertice2[0]+x)*scaling) +image.midheight
		P2_2 = int((vertice2[1]+y)*scaling) +image.midwidth
		P2_3 = int((vertice2[2])*scaling)
		#image.Rx(P1_1,P1_2,P1_3,P2_1,P2_2,P2_3,0,0,0,rotating)
		print(P1_1, P1_2)
		print(P2_1, P2_2)
		
		image.drawline(P1_1,P1_2,P2_1,P2_2,0,0,0)

def filling_matrix(matrix):
	for x in range(0,len(matrix)):
		for y in range(0,len(matrix[0])):
			if x == y:
				matrix[x][y] = 1

def main():
	#dimensions = np.ones(4)
	#print(dimensions)
	#Matrix_transform = np.zeros([4,4])
	#print(Matrix_transform)
	#filling_matrix(Matrix_transform)
	#print(Matrix_transform)
	angle = 100
	nuevo = FHDRaster("AngleRy" + str(angle), 1280, 720, 3)
	print(nuevo.width,nuevo.midwidth)
	print(nuevo.height,nuevo.midheight)
	nuevo.drawline(0,nuevo.midheight,nuevo.width-1,nuevo.midheight,0,0,255)
	nuevo.drawline(nuevo.midwidth,0,nuevo.midwidth,nuevo.height-1,0,0,255)
	obj = load_obj('Monkey.obj')
	scaling = 50
	miny = obj.min_y_coords()
	minx = obj.min_x_coords()

	scaling_image(nuevo,obj)

	for poly in obj.polygons:
		printing_center_polygons(nuevo,obj,poly,angle,-minx ,-miny,scaling_image(nuevo,obj))
	nuevo.close_file()


def D3_translation():
	pass

if __name__ == '__main__':
	
	main()
	#os.system('ffmpeg -framerate 1 -i images/another/*.ppm random.avi -y')
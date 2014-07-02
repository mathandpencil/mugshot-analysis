import os
import sys
import glob
import PIL
import re
import cv
import cv2

try:
	os.mkdir("cropped")
except:
	pass

def detect(img, cascade_fn='models/haarcascade_frontalface_alt.xml',
		   scaleFactor=1.2, minNeighbors=4, minSize=(10, 10),
		   flags=cv.CV_HAAR_SCALE_IMAGE):
 
	cascade = cv2.CascadeClassifier(cascade_fn)
	rects = cascade.detectMultiScale(img, scaleFactor=scaleFactor,
									 minNeighbors=minNeighbors,
									 minSize=minSize, flags=flags)
	if len(rects) == 0:
		return []
	rects[:, 2:] += rects[:, :2]
	return rects

def draw_rects(img, rects, color):
	for x1, y1, x2, y2 in rects:
		cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def get_face(image_path, index):
	""" use opencv to find the face in the image """
	try:
		img_color = cv2.imread(image_path)
		img_gray = img_color
		#img_gray = cv2.cvtColor(img_color, cv.CV_RGB2GRAY)
	except Exception, exc:
		print(exc)
		return None
		
	output_image = "cropped/%s" % image_path.split("/")[1]
		
	faces = detect(img_gray)
	for i, face in enumerate(faces):
		x1, y1, x2, y2 = face
		output_file = "%s_OUTPUT.jpg" %(image_path)
		x, y, dx, dy = face
		cropped = cv2.getRectSubPix(img_gray, (dx, dy), (x + dx / 2, y + dy / 2))
		grayscale = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
		resized = cv2.resize(img_color, (92, 112))
		
		cv2.imwrite(output_image, resized)
		print 'CROPPED %s: %s' % (index,output_image)



def run_face_detection():
	
	image_paths = glob.glob("mugshots/*")
	index = 1
	for image_path in image_paths:
		get_face(image_path, index)
		index += 1 
	
	
if __name__ == "__main__":
	run_face_detection()
# Run with the following
# python3.6 face_extract.py --image foto2.jpeg --prototxt deploy.prototxt 
# --model res10_300x300_ssd_iter_140000.caffemodel --confidence 0.2

# import the necessary packages
import numpy as np
import argparse
import cv2
import os
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-o", "--output", default=".", 
	help="path to save the resulting files")
args = vars(ap.parse_args())

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
image = cv2.imread(args["image"])
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
	(300, 300), (104.0, 177.0, 123.0))

# pass the blob through the network and obtain the detections and
# predictions
print("[INFO] computing object detections...")
net.setInput(blob)
detections = net.forward()
faces = []

# loop over the detections
for i in range(0, detections.shape[2]):
	# extract the confidence (i.e., probability) associated with the
	# prediction
	confidence = detections[0, 0, i, 2]

	# filter out weak detections by ensuring the `confidence` is
	# greater than the minimum confidence
	if confidence > args["confidence"]:
		# compute the (x, y)-coordinates of the bounding box for the
		# object
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
 
		# draw the bounding box of the face along with the associated
		# probability
		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		# extract face from image, sized at 50x50		
		faces.append(cv2.resize(cv2.cvtColor(image[startY:endY, startX:endX], cv2.COLOR_BGR2GRAY), (50,50)))
		# cv2.rectangle(image, (startX, startY), (endX, endY),
		# 	(0, 0, 255), 2)
		# cv2.putText(image, text, (startX, y),
		# 	cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

# print faces extracted from image
for i in range(0, len(faces)):
	cv2.imshow("Face x", faces[i])
	cv2.waitKey(0)


files_count = len(os.listdir(args["output"] + "/"))
print(datetime.timestamp)
# convert matrix to vector and save to a separated file
for i in range(files_count, files_count + len(faces)):
	np.save(args["output"] + "/v-face-" + str(i) + ".npy", faces[i - files_count].flatten())

	

# example how to load the data from a npy file
print(np.load(args["output"] + "/v-face-0.npy"))






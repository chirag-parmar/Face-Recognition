import json
import cv2
import os
import cognitive_face as cf

camera_port = 0
ramp_frames = 30
num_of_samples = 3
flag = 0

camera = cv2.VideoCapture(camera_port)

person_group_id = "YOUR_PERSON_GROUP_ID"
API_key = "YOUR_API_KEY"

cf.Key.set(API_key)

def get_image():
        retval, im = camera.read()
	return im

face_id = []

for i in range(1, num_of_samples + 1):
        file = "/home/pi/facerecog/database/test" + str(i) + ".jpg"
	for i in xrange(ramp_frames):
                temp = get_image()

        print("Taking image...")
        camera_capture = get_image()
	cv2.imwrite(file, camera_capture)
	result = cf.face.detect(open(file,'rb'))
	if len(result) > 0:
		face_id.append(result[0]['faceId'])
	os.system("rm " + file)

# only if face detected in front of the camera(atleast one out of three times) only then the image captured will be tested
if len(face_id)>0:
	res = cf.face.identify(face_id,person_group_id)
	for item in res:
		testdata = item['candidates']
		if len(testdata) > 0:
			confidence = float(testdata[0]['confidence'])
			if confidence > 0.6:
				flag = 1
				print("access granted")
				break;




import util
import json
import cv2

camera_port = 0
ramp_frames = 30
num_of_samples = 1

camera = cv2.VideoCapture(camera_port)
person_group_id = "YOUR_PERSON_GROUP_ID"
person_id = "YOUR_PERSON_ID"

def get_image():
        retval, im = camera.read()
	return im

def add_face(image, person_group_id, person_id, user_data=None,
             target_face=None):
    url = 'persongroups/{}/persons/{}/persistedFaces'.format(
        person_group_id, person_id)
    headers, data, json = util.parse_image(image)
    params = {
        'userData': user_data,
        'targetFace': target_face,
    }

    return util.request('POST', url, data=data,json=json,headers=headers, params=params)

def create(person_group_id, name, user_data=None):
    url = 'persongroups/{}/persons'.format(person_group_id)
    json = {
        'name': name,
        'userData': user_data,
    }

    return util.request('POST', url, json=json)


def delete(person_group_id, person_id):
    url = 'persongroups/{}/persons/{}'.format(person_group_id, person_id)

    return util.request('DELETE', url)


def delete_face(person_group_id, person_id, persisted_face_id):
    url = 'persongroups/{}/persons/{}/persistedFaces/{}'.format(
        person_group_id, person_id, persisted_face_id
    )

    return util.request('DELETE', url)


def get(person_group_id, person_id):
    url = 'persongroups/{}/persons/{}'.format(person_group_id, person_id)

    return util.request('GET', url)


def get_face(person_group_id, person_id, persisted_face_id):
    url = 'persongroups/{}/persons/{}/persistedFaces/{}'.format(
        person_group_id, person_id, persisted_face_id
    )

    return util.request('GET', url)


def lists(person_group_id):
    url = 'persongroups/{}/persons'.format(person_group_id)

    return util.request('GET', url)


def update(person_group_id, person_id, name=None, user_data=None):
    url = 'persongroups/{}/persons/{}'.format(person_group_id, person_id)
    json = {
        'name': name,
        'userData': user_data,
    }

    return util.request('PATCH', url, json=json)


def update_face(person_group_id, person_id, persisted_face_id, user_data=None):
    url = 'persongroups/{}/persons/{}/persistedFaces/{}'.format(
        person_group_id, person_id, persisted_face_id
    )
    json = {
        'userData': user_data,
    }

    return util.request('PATCH', url, json=json)

def train_data(person_group_id):
    url = 'persongroups/{}/train'.format(person_group_id)

    return util.request('POST', url)

persist_id = []

for i in range(1,num_of_samples + 1):
        dummy  = raw_input("Press enter to take a photo")
        file = "/home/pi/facerecog/database/YOUR_NAME" + str(i) + ".jpg"
        if dummy != "quit":
		for i in xrange(ramp_frames):
                	temp = get_image()

        	print("Taking image...")
        	camera_capture = get_image()
		cv2.imwrite(file, camera_capture)
	result = add_face(file, person_group_id, person_id, "USER_DEFINED_DATA")
	persist_id.append(result['persistedFaceId'])
	#result = delete_face(person_group_id, person_id,persist_id)
	print(result)

persist_file = open("./persist_ids.txt", 'w')
for item in persist_id:
	persist_file.write("%s\n" % item)

print("Training Data")
train_data(person_group_id)

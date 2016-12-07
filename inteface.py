import util
import json
import cv2
import os
from PIL import Image

camera_port = 0

camera = cv2.VideoCapture(camera_port)
person_group_id = "YOUR_PERSON_GROUP_ID"     #the interface supports face recognition on one person group only.

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

def take_image(ramp_frames,file):
	for i in xrange(ramp_frames):
		temp = get_image()

        print("Taking image...")
        camera_capture = get_image()
        cv2.imwrite(file, camera_capture)

while True:
	os.system("clear")
	print("Micrsoft Cognitive Face API")
	print("1)Add Person to group")
	print("2)Delete Person from group")
	print("3)List Persons in the group")
	print("4)Add Faces to a Person")
	print("5)Train Database")
	print("6)Quit")
	choice = input("Enter your choice (1,2,3,4,5,6)	:")
	if choice == 1:
		person_name = raw_input("Enter name of the person	:")
		res_add_person = create(person_group_id,person_name)
		if len(res_add_person['personId']) > 0:
			print("PERSON ADDED!")
		dummy = raw_input("press enter to continue") 
	elif choice == 2:
		found_delete_id = 0
		res_lists_person = lists(person_group_id) 
		person_name = raw_input("Enter the name of the person	:")
		for persons in res_lists_person:
			if persons['name'] == person_name:
				deleteID = persons['personId']
				found_delete_id = 1
		if found_delete_id == 1:
			delete(person_group_id,deleteID)
			print("PERSON DELETED!")
		elif found_delete_id == 0:
			print("PERSON NOT FOUND")
		dummy = raw_input("press enter to continue")
	elif choice == 3:
		res_lists_person = lists(person_group_id)
		for persons in res_lists_person:
			table_string = persons['name'] + '\t' + persons['personId'] + '\t' + str(len(persons['persistedFaceIds'])) + "Photos"
			print(table_string)
		dummy = raw_input("press enter to continue")
	elif choice == 4:
		found_add_id = 0
		person_name = raw_input("Enter the name of the person	:")
		res_lists_person = lists(person_group_id)
		for persons in  res_lists_person:
			if persons['name'] == person_name:
				person_add_ID = persons['personId']
				found_add_id = 1
		if found_add_id == 1:
			added = 0
			num_of_samples = input("Enter the number of samples	:")
			for i in range(1,num_of_samples+1):
				dummy = raw_input("Press enter to take a photo")
				filepath = "./database/" + person_name + str(i) + ".jpg"
				take_image(30,filepath)
				res_add_face = add_face(filepath, person_group_id, person_add_ID)
				if len(res_add_face['persistedFaceId']) > 0:
					print("FACE ADDED")
					added = added + 1
				#os.system("rm " + filepath)	#uncomment if you do not want to store the images
			print(str(added) + " of " + str(num_of_samples) + " faces added")   
		elif found_add_id == 0:
			print("PERSON NOT FOUND")
		dummy = raw_input("press enter to continue")
	elif choice == 5:
		flag = 0
		flag2 = 0
		res_lists_person = lists(person_group_id)
                for persons in res_lists_person:
                        if len(persons['persistedFaceIds']) >= 10:
				flag = flag + 1
			flag2 = flag2 + 1
                if flag == flag2:
			train_data(person_group_id)
			res_training = util.wait_for_training(person_group_id)
			print("Training " + res_training)
		elif flag != flag2:
			print("Every person should have atleast 10 photos")
                dummy = raw_input("press enter to continue")
	elif choice == 6:
		break
	elif choice == 7:
		break
	else:
		print("INVALID CHOICE")

del(camera)

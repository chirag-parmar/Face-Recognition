# Face-Recognition 
This project was aimed at providing an interface to Microsoft's Cognitive FaceAPI. The interface provides controls to add and delete persons to/from a person group, faces (photos) to/from a person's database. It also provides controls for training a group and testing data using a camera. OpenCV was used to interface the camera with the python sccript. This project was designed to be run on a Raspberry pi.

Instructions:

1) If you are cloning the repository very well, if not please make sure that util.py and the other scripts are in the same directory.

Observations:

1) Adding more photos increases the confidence value, no doubt, but also try to add photos using different lighting 

2) Camera capture on the raspberry pi lags a bit, it should not on a PC( didnt test yet on a PC).




NOTE: The person group ID and API key must be replaced in all python scripts.



YOUTUBE: https://youtu.be/1lfsdZZ1XqI <-- Video shows testing using a camera

REFERENCES: Huxuan Microsoft/Cognitive-Face-Python for util.py script that provides a very good interface to  make requests.

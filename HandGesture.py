import cv2
import time
import numpy as np
import HandTracker as ht
import math

# pycaw stuff
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



# Video Window Configurations
width_camera = 640
height_camera = 480


# id of videocapture set as 0 to work
cap = cv2.VideoCapture(0)


# Code for setting width = 3, and for height = 4
cap.set(3,width_camera)
cap.set(4,height_camera)


# To calculate Frames per second
prev_Time = 0

# Meat of the code
hand_detector = ht.handDetector(maxHands=1,detectionCon=0.75)

# Distance Code
def get_line_distance(x1,x2,y1,y2):

    x_squared = math.pow(x1-x2,2)
    y_squared = math.pow(y1-y2, 2)


    return math.sqrt(x_squared+y_squared)

# pycaw code(core audio windows)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
min_max_vol =  volume.GetVolumeRange() #max = 0, min -65 #returns a tuple
# volume.SetMasterVolumeLevel(-30.0, None)

minVol = min_max_vol[0]
maxVol = min_max_vol[1]

vol_bar = 400
vol_per = 0

while True:
    success,img = cap.read()
#     Using HandtrackerModule to detect hands
    hand_detector.findHands(img,draw=True)

    # Getting all 21 positions of the hand
    positions_list = hand_detector.findPosition(img, draw=False)

#     Working only if postions are detected
    if positions_list:
        # 4th value respresents tip of thumb and 8th represent tip of index

#         Getting index co-ordinates
        xi,yi = positions_list[8][1],positions_list[8][2]
#         Getting thumb co-ordinates
        xt,yt = positions_list[4][1],positions_list[4][2]
#         Creating circles around index and thumb
        cv2.circle(img, (xi, yi), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (xt, yt), 10, (255, 0, 0), cv2.FILLED)
#         line drawn from thumb to index
        cv2.line(img,(xi,yi),(xt,yt),(255,0,0),2)

        dist = get_line_distance(xi,xt,yi,yt)
        # print(dist)
#         Based on the distance wwe change volume(Using pycaw library)
#         min distance = 30,15,50
#         max_distance = 280
#         volume_range -65 -0
#     Using numpy to nomralize and equate min max distance to min max volume
#         Using numpys linear interpolation
        vol = np.interp(dist,[15,280],[minVol,maxVol])
        vol_bar = np.interp(dist,[15,280],[400,150])
        vol_per = np.interp(dist,[15,280],[0,100])
        volume.SetMasterVolumeLevel(vol, None)



    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f"vol:{int(vol_per)}%", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 0, 0), 2)

    #     FPS calculations and display
    current_Time = time.time()    
    fps = 1/(current_Time-prev_Time)    
    prev_Time = current_Time   
#     Takes image, content to print, location,font_style,scale,color,thickness
    cv2.putText(img,f"FPS:{int(fps)}",(40,40),cv2.FONT_HERSHEY_COMPLEX,0.75,(255,0,0),2)
    
    cv2.imshow("Img",img)
    cv2.waitKey(1)
    
    








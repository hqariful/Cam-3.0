import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# value = {
#     "L":50,
#     "cam_r":30,
#     "offset":0,
#     "profiles":[
#     {
#         'type':'outStroke',
#         'deg':np.deg2rad(100),
#         'motion':"const_a",
#         "pnt":100
#     },
#     {
#         'type':'dwell',
#         'deg':np.deg2rad(80),
#         'pnt':100
#     },
#     {
#         'type':'returnStroke',
#         'deg':np.deg2rad(100),
#         'motion':"const_a",
#         "pnt":100
#     },
#     {
#         'type':'dwell',
#         'deg':None,
#         'pnt':100
#     }
#     ]
# }




#making follower strand
def strand(value):
    prof = value["profiles"]    #short forming into prof


    #-------------------------loop for motion----------------------------------
    def make(i,prevAng):    #get previous angle to make harmony 
        L=value["L"]
        #--------DWELL-----------
        if i["type"] == "dwell":
            cord = np.zeros((2,i["pnt"]))
            if i['max']:
                cord[0,0:] = np.linspace(prevAng, i["deg"]+prevAng, i["pnt"])
                cord[1,0:] = L
                return cord
            cord[0,0:] = np.linspace(prevAng, i["deg"]+prevAng, i["pnt"])
            cord[1,0:] = 0
            return cord
            

        #   initializing cord and x variable
        cord = np.zeros((2, i["pnt"]))
        x = np.linspace(0, i["deg"],i["pnt"])
        cord[0,0:] = np.linspace(prevAng,i["deg"]+prevAng,i["pnt"])

            #-------CONSTANT VELOCITY:---------
        if i["motion"] == "const_v":
            print(i["deg"],i["motion"])
            if i["type"] == "outStroke":
                cord[1,0:] = L/i["deg"]*x
            else:
                cord[1,0:] = L - L/i["deg"]*x
            return cord

            #------CONSTANT ACCELERATION:-------
        elif i["motion"] == "const_a":
            #print(i["deg"],i["motion"])
            mul = 2 * L/i["deg"]**2
            if i["type"] == "outStroke":    #RISING
                cord[1,0:] = np.where(x < i["deg"]/2, mul*x**2, L*(1-2*(1-x/i["deg"])**2))
            else:                           #DIVING
                cord[1,0:] = np.where(x < i["deg"]/2, L*(1-2*(x/i["deg"])**2), 2*L*(1-x/i["deg"])**2)
            return cord
            #-------SIMPLE HARMONIC MOTION:-------
        elif i["motion"] == "shm":
            print(i["deg"],i["motion"])
            if i["type"] == "outStroke":
                cord[1,0:] = L/2-L/2*np.cos(np.pi/i["deg"]*x)
            else:
                cord[1,0:] = L/2+L/2*np.cos(np.pi/i["deg"]*x)
            return cord

    #------------------------------loop for types-----------------------------
    firstTime = True        #to initiate first follower strand
    prevAng = 0

    for i in prof:
        if firstTime:
            cord = make(i,prevAng)
            sum = np.copy(cord)
            #print("sum\n",sum,"\ncord\n",cord)
        else:
            cord = make(i,prevAng)
            sum = np.concatenate((sum, cord), axis=1)
            #print("\nsum\n",sum,"\ncord\n",cord)
        firstTime = False
        prevAng = prevAng + i["deg"]
    print(sum)
    return sum


#   MAKE RADIAL CAM PROFILE
def linToRadi(value,strand):
    row, col = np.shape(strand)
    rcord = np.zeros((2,col))
    t = np.linspace(0,np.deg2rad(360),col)
    rcord[0,0:] = (strand[1]+value["cam_r"])*np.cos(t)
    rcord[1,0:] = (strand[1]+value["cam_r"])*np.sin(t)
    return rcord
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.set_aspect('equal', adjustable='box')
    # plt.plot(rcord[0],rcord[1])
    # plt.show()

#   CALLING THE CALCULATION FOR FOLLOWER DISPLACEMENT
#   2ND PARAMETER DEFINES IF WE WANT CAM PROFILE OR FOLLOWER DISPLACEMENT 
#   >> TRUE MEANS CAM PROFILE
#strand(value,True)





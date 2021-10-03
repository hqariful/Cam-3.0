import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


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
            #print("firstTime")
            cord = make(i,prevAng)
            #print("\n  cord\n",cord)
            sum = np.copy(cord)
            #print("\n  sum\n",sum)
        else:
            cord = make(i,prevAng)
            #print("\n  cord\n",cord)
            sum = np.concatenate((sum, cord), axis=1)
            #print("\n  sum\n",sum)
        firstTime = False
        prevAng = prevAng + i["deg"]
    #   MAKE RADIAL CAM PROFILE
    row, col = np.shape(sum)
    buf = np.zeros((2,col))
    #   CALULATION OF OFFSET
    f = value["offset"]
    r = value["cam_r"]
    # adj = l + np.sqrt(r**2-f**2)
    # o_ang = np.arctan(f/(sum[1] + np.sqrt(r**2-f**2)))
    # (r+ay)^2 = f^2 + (sqrt(r^2-f^2)+l^2)^2    
    # where r+ay is the radius
    buf[0,0:] = (np.sqrt(f**2 + (sum[1] + np.sqrt(r**2-f**2))**2))*np.cos(sum[0]-np.arctan(f/(sum[1] + np.sqrt(r**2-f**2))))
    buf[1,0:] = (np.sqrt(f**2 + (sum[1] + np.sqrt(r**2-f**2))**2))*np.sin(sum[0]-np.arctan(f/(sum[1] + np.sqrt(r**2-f**2))))
    sum = np.concatenate((sum,buf),axis=0)
    return sum



    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.set_aspect('equal', adjustable='box')
    # plt.plot(rcord[0],rcord[1])
    # plt.show()

if __name__ == "__main__":
    value = {
        "L":20,
        "cam_r":50,
        "offset":10,
        "profiles":[
        {
            'type':'outStroke',
            'deg':np.deg2rad(30),
            'motion':'const_a',
            "pnt":50
        },
        {
            'type':'dwell',
            'deg':np.deg2rad(30),
            'pnt':20,
            'max':True
        },
        {
            'type':'returnStroke',
            'deg':np.deg2rad(50),
            'motion':'const_a',
            "pnt":50
        },
        {
            'type':'dwell',
            'deg':None,
            'pnt':20,
            'max':False
        }
        ]
    }
    out = value["profiles"][0]['deg']
    dw = value["profiles"][1]['deg']
    rtn = value["profiles"][2]['deg']
    value["profiles"][3]['deg'] = 2*np.pi - (out+dw+rtn)
    #print(value)
    #   CALLING THE CALCULATION FOR FOLLOWER DISPLACEMENT
    #   2ND PARAMETER DEFINES IF WE WANT CAM PROFILE OR FOLLOWER DISPLACEMENT 
    #   >> TRUE MEANS CAM PROFILE
    cord = strand(value)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(cord[2],cord[3])
    f = value['offset']
    of_ang = np.arcsin(f/value["cam_r"])
    #-------plotting angles mark----------
    r = value["cam_r"]+value["L"]
    ax.plot([0,r*np.cos(0-of_ang)],[0,r*np.sin(0-of_ang)],color='teal',ls='--') #angle 0
    ax.plot([0,r*np.cos(out-of_ang)],[0,r*np.sin(out-of_ang)],color='teal',ls='--') #angle between outstroke and 0
    ax.plot([0,r*np.cos(out+dw-of_ang)],[0,r*np.sin(out+dw-of_ang)],color='teal',ls='--') #angle between outstroke and dwell
    ax.plot([0,r*np.cos(out+dw+rtn-of_ang)],[0,r*np.sin(out+dw+rtn-of_ang)],color='teal',ls='--') #angle between dwell and rtnstroke
    ax.plot(value["cam_r"]*np.cos(np.linspace(0, 2*np.pi, 100)), value["cam_r"]*np.sin(np.linspace(0, 2*np.pi, 100)), color='r', linestyle='--')
    ax.plot(value["offset"]*np.cos(np.linspace(0, 2*np.pi, 100)), value["offset"]*np.sin(np.linspace(0, 2*np.pi, 100)), color='r', linestyle='--')
    ax.set_aspect('equal', adjustable='box')
    plt.show()





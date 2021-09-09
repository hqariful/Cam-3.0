import numpy as np
import matplotlib.pyplot as plt

from value import profiles, L, pnt, cam_r

cord = np.zeros((2,pnt))
#cord[0,0:] = np.arange(0,pnt,1)
cord[0,0:] = np.arange(0,np.radians(pnt),np.radians(1))

def const_acc (deg,type) -> int:
    if type == "outStroke":
        mul = 2*L/deg**2
        x = np.arange(0,deg,1)
        #y = np.where(x<deg/2,mul*x**2,L*(1-2*(1-x/deg)**2))
        r = np.where(x<deg/2,cam_r+mul*x**2,cam_r+L*(1-2*(1-x/deg)**2))
        return r
    elif type == "returnStroke":
        x = np.arange(0,deg,1)
        r = np.where(x<deg/2,cam_r+L*(1-2*(x/deg)**2),cam_r+2*L*(1-x/deg)**2)
        return r

def dwell(deg,h) -> int:
    return np.full((1,deg),h)

def run():
    start = 0
    height = 0
    for profile in profiles:
        if profile['type'] == 'dwell':
            cord[1,start:start+profile['deg']] = dwell(profile['deg'],height)
            start+=profile['deg']
        else:
            cord[1,start:start+profile['deg']] = const_acc(profile['deg'],profile['type'])
            start+=profile['deg']
            height = cord[1,start-1]
    cord[1,start:] = cam_r

"""def start():
    run()
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(cord[0,0:],cord[1])
    plt.show()"""
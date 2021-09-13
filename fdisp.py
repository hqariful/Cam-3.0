import numpy as np

def const_acc (deg,type,L) -> int:
    if type == "outStroke":
        mul = 2*L/deg**2
        x = np.arange(0,deg,1)
        y = np.where(x<deg/2,mul*x**2,L*(1-2*(1-x/deg)**2))
        #r = np.where(x<deg/2,cam_r+mul*x**2,cam_r+val["L"]*(1-2*(1-x/deg)**2))
        return y
    elif type == "returnStroke":
        x = np.arange(0,deg,1)
        y = np.where(x<deg/2,L*(1-2*(x/deg)**2),2*L*(1-x/deg)**2)
        return y

def dwell(deg,h) -> int:
    return np.full((1,deg),h)

def run(val):
    cord = np.zeros((2,val["pnt"]))
    cord[0,0:] = np.arange(0,val["pnt"],1)
    start = 0
    height = 0
    L = val["L"]
    for profile in val["profiles"]:
        if profile['type'] == 'dwell':
            cord[1,start:start+profile['deg']] = dwell(profile['deg'],height)
            start+=profile['deg']
        else:
            cord[1,start:start+profile['deg']] = const_acc(profile['deg'],profile['type'],L)
            start+=profile['deg']
            height = cord[1,start-1]
    cord[1,start:] = 0
    return cord[0,0:], cord[1]


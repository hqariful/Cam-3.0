import numpy as np
    

L = 50
profiles = [
    {
        'type':'outStroke',
        'deg':160
    },
    {
        'type':'dwell',
        'deg':60
    },
    {
        'type':'returnStroke',
        'deg':80
    }
]

pnt = 360


cord = np.zeros((2,pnt))
x = np.arange(0,pnt,1)
cord[0,0:]=x

def const_acc (deg,type) -> int:
    if type == "outStroke":
        mul = 2*L/deg**2
        x = np.arange(0,deg,1)
        y = np.where(x<deg/2,mul*x**2,L*(1-2*(1-x/deg)**2))
        #r = np.where(x<deg/2,cam_r+mul*x**2,cam_r+L*(1-2*(1-x/deg)**2))
        return y
    elif type == "returnStroke":
        x = np.arange(0,deg,1)
        y = np.where(x<deg/2,L*(1-2*(x/deg)**2),2*L*(1-x/deg)**2)
        return y

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
    cord[1,start:] = 0

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    run()
    plt.plot(cord[0,0:],cord[1])
    plt.show()
"""
plt.savefig('figures/save.png')"""
    


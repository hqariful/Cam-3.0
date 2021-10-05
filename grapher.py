from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

#----mode = > server or self
#----type = > linear or radial
def grapher(mode,type,cord,value):
    out = value["profiles"][0]['deg']
    dw = value["profiles"][1]['deg']
    rtn = value["profiles"][2]['deg']
    

    if mode == "self":
        if type == "linear":
            pass
        elif type == "radial":
            fig = Figure()
            ax = fig.subplots()
            ax.set_title("Cam profile")
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
            
    elif mode == "server":
        fig = Figure()
        ax = fig.subplots()
        ax.set_title("Cam profile")
        ax.plot(cord[2],cord[3])
        f = value['offset']
        of_ang = np.arcsin(f/value["cam_r"])
        #-------plotting angles mark----------
        r = value["cam_r"]+value["L"]
        ax.plot([0,r*np.cos(0-of_ang)],[0,r*np.sin(0-of_ang)],color='teal',ls='--') #angle 0
        ax.plot([0,r*np.cos(out-of_ang)],[0,r*np.sin(out-of_ang)],color='teal',ls='--') #angle between outstroke and 0
        ax.plot([0,r*np.cos(out+dw-of_ang)],[0,r*np.sin(out+dw-of_ang)],color='teal',ls='--') #angle between outstroke and dwell
        ax.plot([0,r*np.cos(out+dw+rtn-of_ang)],[0,r*np.sin(out+dw+rtn-of_ang)],color='teal',ls='--') #angle between dwell and rtnstroke
        ax.plot(value["cam_r"]*np.cos(np.linspace(0, 2*np.pi, 100)), value["cam_r"]*np.sin(np.linspace(0, 2*np.pi, 100)), color='r', linestyle='--') #base circle
        ax.plot(value["offset"]*np.cos(np.linspace(0, 2*np.pi, 100)), value["offset"]*np.sin(np.linspace(0, 2*np.pi, 100)), color='r', linestyle='--') #offset circle
        ax.set_aspect('equal', adjustable='box')

        fig2 = Figure()
        ax2 = fig2.subplots()
        ax2.set_title('Follower Displacement')
        ax2.set_xlabel('angle in degree')
        ax2.set_ylabel('Displacement')
        #--------ploting follower marks-----------
        ax2.axvline(x=value["profiles"][0]['deg'],ymin=0,ymax=value["L"],color='teal',ls='--')
        ax2.axvline(x=value["profiles"][0]['deg']+value["profiles"][1]['deg'],ymin=0,ymax=value["L"],color='teal',ls='--')
        ax2.plot(cord[0],cord[1],color='#ff7f0e')

        return fig, fig2
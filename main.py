import numpy as np
from plotter import disp_diag, radial_plot

global theta, r
# create angle variable from 0 to 360 degree
theta = np.linspace(0,360,360)
# similarly create radius variable with 0 unit
r = np.zeros(np.shape(theta))

def merger(outStroke,dwell,returnStroke,max_disp):
    r[0:outStroke.angle] = outStroke.outStroke(theta)
    r[outStroke.angle:outStroke.angle+dwell] = max_disp
    r[outStroke.angle+dwell:outStroke.angle+dwell+returnStroke.angle] = returnStroke.returnStroke(theta)
    return r

def main(outstroke,dwell,returnStroke,max_disp):
    r = merger(outstroke,dwell,returnStroke,max_disp)
    return theta, r

if __name__ == "__main__":
    from calculate import linear_tragectory as LT
    max_disp = 40
    dwell = 30
    rF = 20 # Offset Distance
    rB = 50 # Base Circle
    plot_rad_cam = True
    outStroke = LT.Constant_Acceleration(60,max_disp)
    returnStroke = LT.Constant_Acceleration(120,max_disp)
    theta, r = main(outStroke,dwell,returnStroke, max_disp)
    radial_plot(theta, r, rB, rF)
    # disp_diag(theta, r)
    # plt.savefig('new.png', dpi=200)
    # plt.show()
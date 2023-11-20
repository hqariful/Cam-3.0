from main import np

class Displacement():
    def __init__(self,angle,max_disp) -> None:
        self.angle = angle
        self.max_disp = max_disp

class Constant_Velocity(Displacement):
    def outStroke(self,theta):
        return theta[:self.angle]/self.angle*self.max_disp

    def returnStroke(self,theta):
        return self.max_disp - theta[:self.angle]/self.angle*self.max_disp


class Constant_Acceleration(Displacement):
    def __init__(self, angle, max_disp) -> None:
        super().__init__(angle, max_disp)
        self.m = 2*self.max_disp/self.angle**2

    def outStroke(self,theta):
        r = list()
        r[:int(self.angle/2)] = self.m*theta[:int(self.angle/2)]**2
        r[int(self.angle/2):self.angle] = self.max_disp - self.m*(theta[int(self.angle/2):self.angle]-self.angle)**2
        return r

    def returnStroke(self,theta):
        r = list()
        r[:int(self.angle/2)] = self.max_disp-self.m*theta[:int(self.angle/2)]**2
        r[int(self.angle/2):self.angle] = self.m*(theta[int(self.angle/2):self.angle]-self.angle)**2
        return r
    

class Simple_Harmonic(Displacement):
    def outStroke(self,theta):
        r = list()
        r[:self.angle] = self.max_disp/2 - (self.max_disp/2)*np.cos(theta[:self.angle]/self.angle*np.pi)
        return r

    def returnStroke(self,theta):
        r = list()
        r[:self.angle] = self.max_disp/2 + (self.max_disp/2)*np.cos(theta[:self.angle]/self.angle*np.pi)
        return r
    
    
class Cycloidal(Displacement):
    def outStroke(self,theta):
        rG = self.max_disp/(2*np.pi)
        r = list()
        r[:self.angle] = theta[:self.angle]/self.angle*self.max_disp - rG*np.sin(theta[:self.angle]/self.angle*2*np.pi)
        return r

    def returnStroke(self,theta):
        rG = self.max_disp/(2*np.pi)
        r = list()
        r[:self.angle] = self.max_disp - theta[:self.angle]/self.angle*self.max_disp + rG*np.sin(theta[:self.angle]/self.angle*2*np.pi)
        return r
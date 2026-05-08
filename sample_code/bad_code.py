"""Bad code example with poor practices."""


class xyz:
    def __init__(self,a):
        self.a=a
        self.b=[]
    
    def f(self):
        if self.a>0:
            if len(self.a)>5:
                if self.a[0]>100:
                    if self.a[1]<50:
                        if self.a[2]==25:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    
    def g(self,x,y,z):
        result=x+y*z
        return result

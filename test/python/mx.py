from casadi import *
import casadi as c
from numpy import *
import unittest
from types import *
from helpers import *

def checkarray(self,zr,zt,name):
    if len(zr.shape)==1 and (zt.shape[0]==1 or zt.shape[1]==1) and zr.shape[0]==zt.shape[1]*zt.shape[0]:
      zr=reshape(zr,(zt.shape));
    self.assertEqual(zt.shape[0],zr.shape[0],"%s dimension error. Got %s, expected %s" % (name,str(zt.shape),str(zr.shape)))
    self.assertEqual(len(zt.shape),len(zr.shape),"%s dimension error. Got %s, expected %s" % (name,str(zt.shape),str(zr.shape)))
    self.assertEqual(zt.shape[1],zr.shape[1],"%s dimension error. Got %s, expected %s" % (name,str(zt.shape),str(zr.shape)))
    for i in range(zr.shape[0]):
      for j in range(zr.shape[1]):
        self.assertAlmostEqual(zt[i,j],zr[i,j],10,"%s evaluation error. %s <-> %s" % (name, str(zt),str(zr)))

def checkMXoperations(self,ztf,zrf,name):
    x = MX("x",1,3)
    z=vertcat([x*(i+1) for i in range(8)])
    f = MXFunction([x],[ztf(z)])
    f.init()
    L=[1,2,3]
    f.setInput(L,0)
    f.evaluate()
    zt = f.output(0).toArray()
    zr = array([[L[0]*(i+1),L[1]*(i+1),L[2]*(i+1)] for i in range(8)])
    checkarray(self,zrf(zr),zt,name)
    return (zt,zrf(zr))

def checkMXoperations2(self,ztf,zrf,name):
    x = MX("x",3,1)
    z = horzcat([x*i for i in range(8)])
    f = MXFunction([x],[ztf(z)])
    f.init()
    L=[1,2,3]
    f.setInput(L,0)
    f.evaluate()
    zt = f.output(0).toArray()
    zr = array([[L[0]*i,L[1]*i,L[2]*i] for i in range(8)]).T
    checkarray(self,zrf(zr),zt,name)
    return zt

def checkMXoperations3(self,ztf,zrf,name):
    x = MX("x",3,1)
    p = horzcat([x[0,0],x[1,0],x[2,0]])
    z = vertcat([p*i for i in range(8)])
    f = MXFunction([x],[ztf(z)])
    f.init()
    L=[1,2,3]
    f.setInput(L,0)
    f.evaluate()
    zt = f.output(0).toArray()
    zr = array([[L[0]*i,L[1]*i,L[2]*i] for i in range(8)])
    checkarray(self,zrf(zr),zt,name)
    return (zt,zrf(zr))
    
class MXtests(casadiTestCase):

  def setUp(self):
    self.pool=FunctionPool()
    self.pool.append(lambda x: sqrt(x[0]),sqrt,"sqrt")
    self.pool.append(lambda x: sin(x[0]),sin,"sin")
    self.pool.append(lambda x: cos(x[0]),cos,"cos")
    self.pool.append(lambda x: tan(x[0]),tan,"tan")
    self.pool.append(lambda x: arctan(x[0]),arctan,"arctan")
    self.pool.append(lambda x: arcsin(x[0]),arcsin,"arcsin")
    self.pool.append(lambda x: arccos(x[0]),arccos,"arccos")
    self.pool.append(lambda x: exp(x[0]),exp,"exp")
    self.pool.append(lambda x: log(x[0]),log,"log")
    self.pool.append(lambda x: x[0]**0,lambda x : x**0,"x^0")
    self.pool.append(lambda x: x[0]**1,lambda x : x**1,"^1")
    self.pool.append(lambda x: x[0]**(-2),lambda x : x**(-2),"^-2")
    self.pool.append(lambda x: x[0]**(0.3),lambda x : x**(0.3),"^0.3")
    self.pool.append(lambda x: floor(x[0]),floor,"floor")
    self.pool.append(lambda x: ceil(x[0]),ceil,"ceil")
    self.pool2=FunctionPool()
    self.pool2.append(lambda x: sqrt(x[0]),sqrt,"sqrt")
    self.pool2.append(lambda x: sin(x[0]),sin,"sin")
    self.pool2.append(lambda x: tan(x[0]),tan,"tan")
    self.pool2.append(lambda x: arctan(x[0]),arctan,"arctan")
    self.pool2.append(lambda x: arcsin(x[0]),arcsin,"arcsin")
    self.pool2.append(lambda x: x[0]**1,lambda x : x**1,"^1")
    self.pool2.append(lambda x: x[0]**(0.3),lambda x : x**(0.3),"^0.3")
    self.pool2.append(lambda x: floor(x[0]),floor,"floor")
    self.pool2.append(lambda x: ceil(x[0]),ceil,"ceil")
    self.Jpool=FunctionPool()
    self.Jpool.append(lambda x: sqrt(x[0]),lambda x:diag(1/(2.0*sqrt(x))),"sqrt")
    self.Jpool.append(lambda x: sin(x[0]),lambda x:diag(cos(x)),"sin")
    self.Jpool.append(lambda x: cos(x[0]),lambda x:diag(-sin(x)),"cos")
    self.Jpool.append(lambda x: tan(x[0]),lambda x:diag(1.0/cos(x)**2),"tan")
    self.Jpool.append(lambda x: arctan(x[0]),lambda x:diag( 1.0/(x**2+1)),"arctan")
    self.Jpool.append(lambda x: arcsin(x[0]),lambda x:diag( 1.0/sqrt(1-x**2)),"arcsin")
    self.Jpool.append(lambda x: arccos(x[0]),lambda x: diag(-1.0/sqrt(1-x**2)),"arccos")
    self.Jpool.append(lambda x: exp(x[0]),lambda x: diag(exp(x)),"exp")
    self.Jpool.append(lambda x: log(x[0]),lambda x: diag(1.0/x),"log")
    self.Jpool.append(lambda x: x[0]**0,lambda x :diag(zeros(x.shape)),"x^0")
    self.Jpool.append(lambda x: x[0]**1,lambda x : diag(ones(x.shape)),"^1")
    self.Jpool.append(lambda x: x[0]**(-2),lambda x : diag(-2.0/x**3),"^-2")
    self.Jpool.append(lambda x: x[0]**(0.3),lambda x :diag( 0.3/x**0.7),"^0.3")
    self.matrixpool=FunctionPool()
    self.matrixpool.append(lambda x: norm_2(x[0]),linalg.norm,"norm_2")
    self.matrixbinarypool=FunctionPool()
    self.matrixbinarypool.append(lambda a: a[0]+a[1],lambda a: a[0]+a[1],"Matrix+Matrix")
    self.matrixbinarypool.append(lambda a: a[0]-a[1],lambda a: a[0]-a[1],"Matrix-Matrix")
    self.matrixbinarypool.append(lambda a: a[0]*a[1],lambda a: a[0]*a[1],"Matrix*Matrix")
    #self.matrixbinarypool.append(lambda a: inner_prod(a[0],trans(a[1])),lambda a: dot(a[0].T,a[1]),name="inner_prod(Matrix,Matrix)") 
    self.matrixbinarypool.append(lambda a: c.prod(a[0],trans(a[1])),lambda a: dot(a[0],a[1].T),"prod(Matrix,Matrix.T)")

  def test_indirection(self):
    self.message("MXFunction indirection")
    x=MX("x",2,1)
    y=MX("y",2,1)
    z=MX("z",2,1)
    
    xn = array([2.3,1.3])
    yn = array([7.3,4.6])
    zn = array([12,7.4])
    
    f=MXFunction([x,y,z],[x+2*y+3*z])
    f.init()
    self.message(":simple indirection")
    g=MXFunction([x,y,z],f.call([x,y,z]))
    g.init()
    g.input(0).set(xn)
    g.input(1).set(yn)
    g.input(2).set(zn)
    g.fwdSeed(0).set(xn) # okay, I'm just lazy comming up with more numbers
    g.fwdSeed(1).set(yn)
    g.fwdSeed(2).set(zn)
    g.evaluate(1,0)
    self.checkarray(g.output(),xn+2*yn+3*zn,"MXFunction indirection");
    self.checkarray(g.fwdSens(),array([52.9,32.7]),"MXFunction indirection");
    
    g=MXFunction([x,y,z],f.call([vertcat([x[0],x[1]]),y,z]))
    g.init()
    g.input(0).set(xn)
    g.input(1).set(yn)
    g.input(2).set(zn)
    g.fwdSeed(0).set(xn)
    g.fwdSeed(1).set(yn)
    g.fwdSeed(2).set(zn)
    g.evaluate(1,0)

    self.checkarray(g.output(),xn+2*yn+3*zn,"MXFunction indirection");
    self.checkarray(g.fwdSens(),array([52.9,32.7]),"MXFunction indirection");
    
    self.message(":double output flipover")
    h=MXFunction([x,y,z],f.call([vertcat([y[0],x[1]]),vertcat([x[0],y[1]]),z]))
    h.init()
    h=MXFunction([x,y,z],h.call([vertcat([y[0],x[1]]),vertcat([x[0],y[1]]),z]))
    # h should be identical to g now
    h.init()
    h.input(0).set(xn)
    h.input(1).set(yn)
    h.input(2).set(zn)
    h.fwdSeed(0).set(xn)
    h.fwdSeed(1).set(yn)
    h.fwdSeed(2).set(zn)
    h.evaluate(1,0)
    self.checkarray(h.output(),xn+2*yn+3*zn,"MXFunction indirection");
    self.checkarray(h.fwdSens(),array([52.9,32.7]),"MXFunction indirection");
    
    self.message(":double input flipover")
    h=MXFunction([x,y,z],f.call([y,x,z]))
    h.init()
    h=MXFunction([x,y,z],h.call([y,x,z]))
    h.init()
    h.input(0).set(xn)
    h.input(1).set(yn)
    h.input(2).set(zn)
    h.fwdSeed(0).set(xn)
    h.fwdSeed(1).set(yn)
    h.fwdSeed(2).set(zn)
    h.evaluate(1,0)
    self.checkarray(h.output(),xn+2*yn+3*zn,"MXFunction indirection");
    self.checkarray(h.fwdSens(),array([52.9,32.7]),"MXFunction indirection");
    
    return # the following co
    self.message(":uncomplete call")
    h=MXFunction([x,z],f.call([x,y,z]))
    h.init()
    h=MXFunction([x,y,z],h.call([x,z]))
    h.init()
    h.input(0).set(xn)
    h.input(1).set(yn)
    h.input(2).set(zn)
    h.fwdSeed(0).set(xn)
    h.fwdSeed(1).set(yn)
    h.fwdSeed(2).set(zn)
    h.evaluate(1,0)
    self.checkarray(h.output(),xn+2*yn+3*zn,"MXFunction indirection");
    self.checkarray(h.fwdSens(),array([52.9,32.7]),"MXFunction indirection");
    
  def test_MX1(self):
    self.message("MX constructor")
    x = MX("x",2,3)
    self.assertEqual(x.size1(),2,"MX fails to indicate its size1")
    self.assertEqual(x.size2(),3,"MX fails to indicate its size2")

  def test_MXvertcat(self):
    self.message("MX vertcat")
    x = MX("x",1,3)
    y = MX("y",1,3)
    z=vertcat((x,y))
    self.assertEqual(z.size1(),2,"MX fails to indicate its size1")
    self.assertEqual(z.size2(),3,"MX fails to indicate its size2")

  # Joel: NOTE this does not work properly
  #def test_MX2(self):
    #U = MX("U",10,2)
    #u = U.getRow(1) # NOTE: the correct syntax should be U[1,:], there is a workaround that allow this, but it is not yet supported in C++

  def test_MXfunction1(self):
    self.message("MXFunction single input, single output")
    # check if x->2*x
    # evaluates correctly for x=3
    x = MX("x")
    y = 2*x
    f = MXFunction([x],[y])
    self.assertEqual(f.getNumInputs(),1,"MXFunction fails to indicate correct number of inputs")
    self.assertEqual(f.getNumOutputs(),1,"MXFunction fails to indicate correct number of outputs")
    f.init()
    f.setInput(3,0);
    f.evaluate()
    yt = tuple(f.output())
    self.assertEqual(type(yt),TupleType,"Output of MXFunction is expected to be tuple of floats")
    self.assertEqual(len(yt),1,"Output of MXFunction was tuple of floats, as expected, but length is incorrect.")
    y=yt[0]
    self.assertEqual(type(y),float,"Output of MXFunction is expected to be tuple of floats")
    self.assertAlmostEqual(y, 2*3,10)

  def test_MXfunction2(self):
    self.message("MXFunction multi input, multi output")
      # check if [x,y]->[y+x,y*x]
    # evaluates correctly for x=3,y=7
    x = MX("x")
    y = MX("y")
    f = MXFunction([x,y],[x+y,y*x])
    self.assertEqual(f.getNumInputs(),2,"MXFunction fails to indicate correct number of inputs")
    self.assertEqual(f.getNumOutputs(),2,"MXFunction fails to indicate correct number of outputs")

    f.init()
    f.setInput(3,0);
    f.setInput(7,1);
    f.evaluate()
    zt1 = tuple(f.output(0))
    zt2 = tuple(f.output(1))
    self.assertEqual(type(zt1),TupleType,"Output of MXFunction is expected to be tuple of floats")
    self.assertEqual(type(zt2),TupleType,"Output of MXFunction is expected to be tuple of floats")
    self.assertEqual(len(zt1),1,"Output of MXFunction was tuple of floats, as expected, but length is incorrect.")
    self.assertEqual(len(zt2),1,"Output of MXFunction was tuple of floats, as expected, but length is incorrect.")
    z1=zt1[0]
    z2=zt2[0]
    self.assertEqual(type(z1),float,"Output of MXFunction is expected to be tuple of floats")
    self.assertEqual(type(z2),float,"Output of MXFunction is expected to be tuple of floats")
    self.assertAlmostEqual(z2, 21,10)
    self.assertAlmostEqual(z1, 10,10)      



  def test_MXfunction3(self):
    self.message("MXFunction single input, multi output (1)")
    # check if [x,y]->[y+x,y*x]
    # evaluates correctly for x=3,y=7
    # now with single input, multi output
    xy = MX("xy",2)
    f = MXFunction([xy],[xy[0]+xy[1],xy[0]*xy[1]])
    self.assertEqual(f.getNumInputs(),1,"MXFunction fails to indicate correct number of inputs")
    self.assertEqual(f.getNumOutputs(),2,"MXFunction fails to indicate correct number of outputs")
    f.init()
    f.setInput([3,7],0);
    f.evaluate()
    zt1 = tuple(f.output(0))
    zt2 = tuple(f.output(1))
    self.assertEqual(type(zt1),TupleType,"Output of MXFunction is expected to be tuple of floats")
    self.assertEqual(type(zt2),TupleType,"Output of MXFunction is expected to be tuple of floats")
    self.assertEqual(len(zt1),1,"Output of MXFunction was tuple of floats, as expected, but length is incorrect.")
    self.assertEqual(len(zt2),1,"Output of MXFunction was tuple of floats, as expected, but length is incorrect.")
    z1=zt1[0]
    z2=zt2[0]
    self.assertEqual(type(z1),float,"Output of MXFunction is expected to be tuple of floats")
    self.assertEqual(type(z2),float,"Output of MXFunction is expected to be tuple of floats")
    self.assertAlmostEqual(z2, 21,10)
    self.assertAlmostEqual(z1, 10,10)

  def test_MXfunction3b(self):
    self.message("MXFunction single input, multi output (2)")
    # check if [x,y]->[y+x,y*x]
    # evaluates correctly for x=3,y=7
    # now with single input, multi output
    xy = MX("xy",1,2)
    f = MXFunction([xy],[xy[0]+xy[1],xy[0]*xy[1]])
    self.assertEqual(f.getNumInputs(),1,"MXFunction fails to indicate correct number of inputs")
    self.assertEqual(f.getNumOutputs(),2,"MXFunction fails to indicate correct number of outputs")
    f.init()
    f.setInput([3,7],0);
    f.evaluate()
    zt1 = f.output(0).toArray()
    zt2 = f.output(1).toArray()
    
    self.assertEqual(type(zt1),ndarray,"Output of MXFunction is expected to be numpy.ndarray")
    self.assertEqual(zt1.shape[0],1,"Output of MXFunction is of wrong shape.")
    self.assertEqual(zt1.shape[1],1,"Output of MXFunction is of wrong shape.")
    
    self.assertEqual(type(zt2),ndarray,"Output of MXFunction is expected to be numpy.ndarray")
    self.assertEqual(zt2.shape[0],1,"Output of MXFunction is of wrong shape.")
    self.assertEqual(zt2.shape[1],1,"Output of MXFunction is of wrong shape.")
    
    z1=zt1[0,0]
    z2=zt2[0,0]
    self.assertEqual(type(z1),float64,"Output of MXFunction is expected to be numpy.ndarray of floats")
    self.assertEqual(type(z2),float64,"Output of MXFunction is expected to be numpy.ndarray of floats")
    self.assertAlmostEqual(z2, 21,10)
    self.assertAlmostEqual(z1, 10,10)

  def test_MXfunction4(self):
    self.message("MXFunction single input, single output , using vertcat")
    # check if [x,y]->[y+x,y*x]
    # evaluates correctly for x=3,y=7
    # now with single input, single output
    xy = MX("xy",2)
    z=vertcat([xy[0]+xy[1],xy[0]*xy[1]])
    f = MXFunction([xy],[z])
    self.assertEqual(f.getNumInputs(),1,"MXFunction fails to indicate correct number of inputs")
    self.assertEqual(f.getNumOutputs(),1,"MXFunction fails to indicate correct number of outputs")
    f.init()
    f.setInput([3,7],0);
    f.evaluate()
    zt=f.output(0).toArray()
    self.assertEqual(type(zt),ndarray,"Output of MXFunction is expected to be numpy.ndarray")
    self.assertEqual(zt.shape[0],2,"Output of MXFunction is of wrong shape.")
    self.assertEqual(zt.shape[1],1,"Output of MXFunction is of wrong shape.")
    z1=zt[0,0]
    z2=zt[1,0]
    self.assertEqual(type(z1),float64,"Output of MXFunction is expected to be numpy.ndarray of floats")
    self.assertEqual(type(z2),float64,"Output of MXFunction is expected to be numpy.ndarray of floats")
    self.assertAlmostEqual(z2, 21,10)
    self.assertAlmostEqual(z1, 10,10)

  def test_MXfunction5(self):
    self.message("MXFunction single input, single output , using horzcat")
    # check if [x,y]->[y+x,y*x]
    # evaluates correctly for x=3,y=7
    # now with single input, single output
    xy = MX("xy",2)
    z=horzcat([xy[0]+xy[1],xy[0]*xy[1]])
    f = MXFunction([xy],[z])
    self.assertEqual(f.getNumInputs(),1,"MXFunction fails to indicate correct number of inputs")
    self.assertEqual(f.getNumOutputs(),1,"MXFunction fails to indicate correct number of outputs")
    f.init()
    f.setInput([3,7],0);
    f.evaluate()
    zt = f.output(0).toArray()
    self.assertEqual(type(zt),ndarray,"Output of MXFunction is expected to be numpy.ndarray")
    self.assertEqual(zt.shape[0],1,"Output of MXFunction is of wrong shape.")
    self.assertEqual(zt.shape[1],2,"Output of MXFunction is of wrong shape.")
    z1=zt[0,0]
    z2=zt[0,1]
    self.assertEqual(type(z1),float64,"Output of MXFunction is expected to be numpy.ndarray of floats")
    self.assertEqual(type(z2),float64,"Output of MXFunction is expected to be numpy.ndarray of floats")
    self.assertAlmostEqual(z2, 21,10)
    self.assertAlmostEqual(z1, 10,10)
    
  def test_issue83(self):
    x=MX("x")
    y=MX("y")

    z = x + y

    f = MXFunction([x,y],[z])
    f.init()

    [fc] = f.call([MX(3),y])

    g = MXFunction([y],[fc])
    g.init()
    g.input().set([7])
    g.evaluate()

    self.assertAlmostEqual(g.output()[0],10,10,"issue #83")
    
    [fc] = f.call([x,MX(7)])

    g = MXFunction([x],[fc])
    g.init()
    g.input().set([3])
    g.evaluate()

    self.assertAlmostEqual(g.output()[0],10,10,"issue #83")
  
  #def test_MXslice(self):
    #x = MX("x",1,3)
    #z=x[:]
    #self.assertEqual(z.size1(),1,"Flatten returns MX of wrong dimension")
    #self.assertEqual(z.size2(),3,"Flatten returns MX of wrong dimension")
    #f = MXFunction([x],[z])
    #f.init()
    #L=[1,2,3]
    #f.setInput(L,0)
    #f.evaluate()
    #zt = f.output(0).toArray()
    
    #for i in range(3):
      #self.assertAlmostEqual(L[i], zt[i],10)
      
  #def test_MXslice(self):
    #x = MX("x",3,1)
    #z=x[:]
    #self.assertEqual(z.size1(),3,"Flatten returns MX of wrong dimension")
    #self.assertEqual(z.size2(),1,"Flatten returns MX of wrong dimension")
    #f = MXFunction([x],[z])
    #f.init()
    #L=[1,2,3]
    #f.setInput(L,0)
    #f.evaluate()
    #zt = f.output(0).toArray()
    
    #for i in range(3):
      #self.assertAlmostEqual(L[i], zt[i],10)
        
  def test_identitySX(self):
    self.message("identity SXFunction")
    x = SX("x")
    f = SXFunction([[x]],[[x]])
    f.init()
    f.setInput([3],0)
    f.evaluate()
    self.assertAlmostEqual(f.output(0)[0,0], 3,10)

  def test_identityMX(self):
    self.message("identity MXFunction")
    x = MX("x")
    f  = MXFunction([x],[x])
    f.init()
    f.setInput([3],0)
    f.evaluate()
    self.assertAlmostEqual(f.output(0)[0,0], 3,10)
    
  def test_MXorder(self):
    self.message("MXFunction order of non-zero elements")
    x = MX("x",2,3)
    f = MXFunction([x],[x+x])

    self.assertEqual(f.getNumInputs(),1,"MXFunction fails to indicate correct number of inputs")
    self.assertEqual(f.getNumOutputs(),1,"MXFunction fails to indicate correct number of outputs")
    f.init()
    L=[1,2,3,4,5,6]
    f.setInput(L,0)
    f.evaluate()
    zt = f.output(0).toArray()
    self.assertEqual(zt.shape[0],2,"Output of MXFunction is of wrong shape.")
    self.assertEqual(zt.shape[1],3,"Output of MXFunction is of wrong shape.")
      
    Lr=reshape(L,(2,3))
    for i in range(2):
      for j in range(3):
        self.assertAlmostEqual(Lr[i,j]*2, zt[i,j],10)
    
  def test_MXtrans(self):
    self.message("trans(MX)")
    x = MX("x",2,3)
    z=trans(x)
    self.assertEqual(z.size1(),3,"Flatten returns MX of wrong dimension")
    self.assertEqual(z.size2(),2,"Flatten returns MX of wrong dimension")
    f = MXFunction([x],[z])
    self.assertEqual(f.getNumInputs(),1,"MXFunction fails to indicate correct number of inputs")
    self.assertEqual(f.getNumOutputs(),1,"MXFunction fails to indicate correct number of outputs")
    f.init()
    L=[1,2,3,4,5,6]
    f.setInput(L,0)
    f.evaluate()
    zt = f.output(0).toArray()
    
    ztr=reshape(zt,(3,2))
    Lr=reshape(L,(2,3))
    for i in range(2):
      for j in range(3):
        self.assertAlmostEqual(Lr[i,j], ztr[j,i],10)
    
  def test_MXflatten(self):
    self.message("trans(MX)")
    x = MX("x",2,3)
    z=vec(x)
    self.assertEqual(z.size1(),6,"Flatten returns MX of wrong dimension")
    self.assertEqual(z.size2(),1,"Flatten returns MX of wrong dimension")
    f = MXFunction([x],[z])
    self.assertEqual(f.getNumInputs(),1,"MXFunction fails to indicate correct number of inputs")
    self.assertEqual(f.getNumOutputs(),1,"MXFunction fails to indicate correct number of outputs")
    f.init()
    L=[1,2,3,4,5,6]
    f.setInput(L,0)
    f.evaluate()
    zt = f.output(0).toArray()
    for i in range(len(L)):
      self.assertAlmostEqual(L[i], zt[i],10)
      
    
  def test_MXreshape(self):
    self.message("reshape(MX)")
    x = MX("x",2,3)
    z=c.reshape(x,(1,6))
    self.assertEqual(z.size1(),1,"Flatten returns MX of wrong dimension")
    self.assertEqual(z.size2(),6,"Flatten returns MX of wrong dimension")
    f = MXFunction([x],[z])
    self.assertEqual(f.getNumInputs(),1,"MXFunction fails to indicate correct number of inputs")
    self.assertEqual(f.getNumOutputs(),1,"MXFunction fails to indicate correct number of outputs")
    f.init()
    L=[1,2,3,4,5,6]
    f.setInput(L,0)
    f.evaluate()
    zt = f.output(0).toArray()
    for i in range(len(L)):
      self.assertAlmostEqual(L[i], zt[0,i],10)
  
  def test_MXcompose(self):
    self.message("compositions of flatten, trans, reshape with vertcat")
    checkMXoperations(self,lambda x: x,lambda x: x,'vertcat')
    checkMXoperations(self,lambda x: trans(x),lambda x: x.T,'trans(vertcat)')
    checkMXoperations(self,lambda x: trans(trans(x)),lambda x: x,'trans(trans(vertcat))')
    checkMXoperations(self,lambda x: vec(trans(x)),lambda x: reshape(x.T,(prod(x.shape),1)),'vec(trans(vertcat))')
    checkMXoperations(self,lambda x: trans(vec(x)),lambda x: reshape(x,(prod(x.shape),1)).T,'vec(trans(vertcat))')
    checkMXoperations(self,lambda x: c.reshape(x,(4,6)),lambda x: reshape(x,(4,6)),'reshape(vertcat)')
    checkMXoperations(self,lambda x: c.reshape(trans(x),(4,6)),lambda x: reshape(x.T,(4,6)),'reshape(trans(vertcat))') 
    checkMXoperations(self,lambda x: trans(c.reshape(x,(4,6))),lambda x: reshape(x,(4,6)).T,'trans(reshape(vertcat))') 

  def test_MXcompose2(self):
    self.message("compositions of flatten, trans, reshape with horzcat")
    checkMXoperations2(self,lambda x: x,lambda x: x,'horzcat')
    checkMXoperations2(self,lambda x: trans(x),lambda x: x.T,'trans(horzcat)')
    checkMXoperations2(self,lambda x: trans(trans(x)),lambda x: x,'trans(trans(horzcat))')
    checkMXoperations2(self,lambda x: vec(trans(x)),lambda x: reshape(x.T,(prod(x.shape),1)),'vec(trans(horzcat))')
    checkMXoperations2(self,lambda x: trans(vec(x)),lambda x: reshape(x,(prod(x.shape),1)).T,'vec(trans(horzcat))')
    checkMXoperations2(self,lambda x: c.reshape(x,(4,6)),lambda x: reshape(x,(4,6)),'reshape(horzcat)')
    checkMXoperations2(self,lambda x: c.reshape(trans(x),(4,6)),lambda x: reshape(x.T,(4,6)),'reshape(trans(horzcat))') 
    checkMXoperations2(self,lambda x: trans(c.reshape(x,(4,6))),lambda x: reshape(x,(4,6)).T,'trans(reshape(horzcat))') 

  def test_MXcompose3(self):
    self.message("compositions of flatten, trans, reshape with vertcat")
    checkMXoperations3(self,lambda x: x,lambda x: x,'snippet')
    checkMXoperations3(self,lambda x: trans(x),lambda x: x.T,'trans(snippet)')
    checkMXoperations3(self,lambda x: trans(trans(x)),lambda x: x,'trans(trans(snippet))')
    checkMXoperations3(self,lambda x: vec(trans(x)),lambda x: reshape(x.T,(prod(x.shape),1)),'vec(trans(snippet))')
    checkMXoperations3(self,lambda x: trans(vec(x)),lambda x: reshape(x,(prod(x.shape),1)).T,'vec(trans(snippet))')
    checkMXoperations3(self,lambda x: c.reshape(x,(4,6)),lambda x: reshape(x,(4,6)),'reshape(snippet)')
    checkMXoperations3(self,lambda x: c.reshape(trans(x),(4,6)),lambda x: reshape(x.T,(4,6)),'reshape(trans(snippet))') 
    checkMXoperations3(self,lambda x: trans(c.reshape(x,(4,6))),lambda x: reshape(x,(4,6)).T,'trans(reshape(snippet))') 

  def test_MXcompose4(self):
    self.message("compositions of horzcat + vertcat")
    checkMXoperations(self,lambda x: vertcat([x]),lambda x: x,'vertcat(vertcat)')
    checkMXoperations(self,lambda x: vertcat([x,x*2]),lambda x: vstack((x,x*2)),'vertcat(vertcat,vertcat)')
    checkMXoperations(self,lambda x: horzcat([x]),lambda x: x,'horzcat(vertcat)')
    checkMXoperations(self,lambda x: horzcat([x,x*2]),lambda x: hstack((x,x*2)),'horzcat(vertcat,vertcat)')
    
    checkMXoperations2(self,lambda x: vertcat([x]),lambda x: x,'vertcat(horzcat)')
    checkMXoperations2(self,lambda x: vertcat([x,x*2]),lambda x: vstack((x,x*2)),'vertcat(horzcat,horzcat)')
    checkMXoperations2(self,lambda x: horzcat([x]),lambda x: x,'horzcat(horzcat)')
    checkMXoperations2(self,lambda x: horzcat([x,x*2]),lambda x: hstack((x,x*2)),'horzcat(horzcat,horzcat)')
    
    checkMXoperations3(self,lambda x: vertcat([x]),lambda x: x,'vertcat(snippet)')
    checkMXoperations3(self,lambda x: vertcat([x,x*2]),lambda x: vstack((x,x*2)),'vertcat(snippet,snippet)')
    checkMXoperations3(self,lambda x: horzcat([x]),lambda x: x,'horzcat(snippet)')
    checkMXoperations3(self,lambda x: horzcat([x,x*2]),lambda x: hstack((x,x*2)),'horzcat(snippet,snippet)')
    
  def test_MXslicingnew(self):
    self.message("MX slicing")

    self.message(":dense")
    x = MX("x",3,2)
    x0=array([[0.738,0.2],[ 0.1,0.39 ],[0.99,0.999999]])
    self.numpyEvaluationCheck(lambda x:x[0][1,0],lambda x: x[1,0],[x],x0,'x[1,0]')
    self.numpyEvaluationCheck(lambda x:x[0][0,1],lambda x: x[0,1],[x],x0,'x[0,1]')
    self.numpyEvaluationCheck(lambda x:x[0][0,-1],lambda x: x[0,-1],[x],x0,'x[0,-1]')
    self.numpyEvaluationCheck(lambda x: x[0][:,0], lambda x: matrix(x)[:,0],[x],x0,name="x[:,0]")
    self.numpyEvaluationCheck(lambda x: x[0][:,1], lambda x: matrix(x)[:,1],[x],x0,name="x[:,1]")
    self.numpyEvaluationCheck(lambda x: x[0][1,:], lambda x: matrix(x)[1,:],[x],x0,name="x[1,:]")
    self.numpyEvaluationCheck(lambda x: x[0][0,:], lambda x: matrix(x)[0,:],[x],x0,name="x[0,:]")
    self.numpyEvaluationCheck(lambda x: x[0][-1,:], lambda x: matrix(x)[-1,:],[x],x0,name="x[-1,:]")
    self.numpyEvaluationCheck(lambda x: x[0][:,-2], lambda x: matrix(x)[:,-2],[x],x0,name="x[:,-2]")
    self.numpyEvaluationCheck(lambda x: x[0][0:-2,0:-1], lambda x: matrix(x)[0:-2,0:-1],[x],x0,name="x[0:-2,0:-1]")
    self.numpyEvaluationCheck(lambda x: x[0][0:2,0:2], lambda x: matrix(x)[0:2,0:2],[x],x0,name="x[0:2,0:2]")
    self.numpyEvaluationCheck(lambda x: x[0][[0,1],0:2], lambda x: matrix(x)[[0,1],0:2],[x],x0,name="x[[0,1],0:2]")
    self.numpyEvaluationCheck(lambda x: x[0][[0,2,3]], lambda x: matrix([x[0,0],x[1,0],x[1,1]]).T,[x],x0,name="x[[0,2,3]]")

    self.numpyEvaluationCheck(lambda x: x[0][1], lambda x: matrix(x.ravel()[1]).T,[x],x0,name="x[1] on dense matrix")
    self.numpyEvaluationCheck(lambda x: x[0][-1], lambda x: matrix(x.ravel()[-1]).T,[x],x0,name="x[-1] on dense matrix")
    #self.numpyEvaluationCheck(lambda x: x[[0,1],0:1],lambda x: x[[0,1],0:1],[x],x0,name='x[:,0:1]')
    #self.numpyEvaluationCheck(lambda x: x[0:1,[0,1]],lambda x: x[0:1,[0,1]],[x],x0,name='x[0:1,:]')
    
    self.message(":sparse")
      
    sp=CRSSparsity(3,4,[1,2,1],[0,2,2,3])
    x=MX("X",sp)
    sx0=[0.738,0.39,0.99]
    x0=DMatrix(3,4,[1,2,1],[0,2,2,3],[0.738,0.39,0.99]).toArray()
    self.numpyEvaluationCheck(lambda x: x[0][0,0], lambda x: matrix(x)[0,0],[x],x0,name="x[0,0]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][1,0], lambda x: matrix(x)[1,0],[x],x0,name="x[1,0]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][0,1], lambda x: matrix(x)[0,1],[x],x0,name="x[1,0]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][0,-1], lambda x: matrix(x)[0,-1],[x],x0,name="x[0,-1]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][:,0], lambda x: matrix(x)[:,0],[x],x0,name="x[:,0]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][:,1], lambda x: matrix(x)[:,1],[x],x0,name="x[:,1]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][1,:], lambda x: matrix(x)[1,:],[x],x0,name="x[1,:]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][0,:], lambda x: matrix(x)[0,:],[x],x0,name="x[0,:]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][-1,:], lambda x: matrix(x)[-1,:],[x],x0,name="x[-1,:]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][:,-2], lambda x: matrix(x)[:,-2],[x],x0,name="x[:,-2]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][0:-2,0:-1], lambda x: matrix(x)[0:-2,0:-1],[x],x0,name="x[0:-2,0:-1]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][0:2,0:2], lambda x: matrix(x)[0:2,0:2],[x],x0,name="x[0:2,0:2]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][[0,1],0:2], lambda x: matrix(x)[[0,1],0:2],[x],x0,name="x[[0,1],0:2]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][[2,1]], lambda x: matrix([x[2,1],x[0,2]]).T,[x],x0,name="x[[2,1]]")
    #self.numpyEvaluationCheck(lambda x: x[0][0:2], lambda x: matrix(x)[0:2,0],[x],x0,name="x[0:2] on dense matrix")
    self.numpyEvaluationCheck(lambda x: x[0][1], lambda x: matrix(sx0[1]).T,[x],x0,name="x[1]",setx0=[sx0])
    self.numpyEvaluationCheck(lambda x: x[0][-1], lambda x: matrix(sx0[-1]).T,[x],x0,name="x[-1]",setx0=[sx0])
    
  def test_getinputMX(self):
    self.message("outputMX/inputMX")
    x=MX("x",2,3)
    f = MXFunction([x],[3*x]) 
    g = MXFunction([f.inputMX()],[6*f.outputMX()]) 
    
    f.init()
    g.init()
    n=[1,2,3,4,5,6]
    f.setInput(n)
    f.evaluate()
    g.setInput(n)
    g.evaluate()
    checkarray(self,6*f.output().toArray(),g.output().toArray(),"slicing(trans)")
    
  def test_dict(self):
    self.message("Dictionary constructor for MXFunction")
    x=MX("x",2,2)
    y=MX("y",2,2)
    f = MXFunction({0: x,1:y},{'NUM':1,0: x+y})
    self.assertEqual(f.getNumInputs(),2)
    self.checkarray(f.inputMX(0).shape,(2,2),"dict")
    self.checkarray(f.inputMX(1).shape,(2,2),"dict")
    self.assertEqual(f.getNumOutputs(),1)
    self.checkarray(f.outputMX(0).shape,(2,2),"dict")
    
  def test_scalarMX(self):
      x=MX("x")
      x0=0.738
      self.numpyEvaluationCheckPool(self.pool,[x],x0,name="scalarMX")
      
  def test_MXJacobian(self):
    self.message("MX(1,1) unary operation, jacobian")
    self.Jpool=FunctionPool()
    self.message("SXMatrix(1,1) unary operation, jacobian")
    x=MX("x")
    x0=array([[0.738]])

    def fmod(f,x):
      J=Jacobian(f)
      J.setOption("ad_mode","forward")
      J.init()
      return J
      
    self.numpyEvaluationCheckPool(self.Jpool,[x],x0,name="MX unary operations, jacobian",fmod=fmod)
    
    def fmod(f,x):
      J=Jacobian(f)
      J.setOption("ad_mode","adjoint")
      J.init()
      return J
      
    self.numpyEvaluationCheckPool(self.Jpool,[x],x0,name="MX unary operations, jacobian",fmod=fmod)
    
  def test_MXJacobians(self):
      self.message("MX(3,1) unary operation, jacobian")
      x=MX("x",3,1)
      
      x0=array([0.738,0.9,0.3])

      def fmod(f,x):
        J=Jacobian(f)
        J.setOption("ad_mode","forward")
        J.init()
        return J
        
      self.numpyEvaluationCheckPool(self.Jpool,[x],x0,name="MX unary operations, jacobian",fmod=fmod)
      
      def fmod(f,x):
        J=Jacobian(f)
        J.setOption("ad_mode","adjoint")
        J.init()
        return J
        
      self.numpyEvaluationCheckPool(self.Jpool,[x],x0,name="MX unary operations, jacobian",fmod=fmod)

  def test_MXbinary(self):
      self.message("MX binary operations")
      x=MX("x",3,2)
      y=MX("x",3,2)
      x0=array([[0.738,0.2],[ 0.1,0.39 ],[0.99,0.999999]])
      y0=array([[1.738,0.6],[ 0.7,12 ],[0,-6]])
      self.numpyEvaluationCheckPool(self.matrixbinarypool,[x,y],[x0,y0],name="MX")

  def test_MXSparse(self):
      #return # not working
      self.message("MX unary operations, sparse")
      from scipy.sparse import csr_matrix
      
      sp=CRSSparsity(3,4,[1,2,1],[0,2,2,3])
      
      x=MX("x",sp)
      x0=DMatrix(3,4,[1,2,1],[0,2,2,3],[0.738,0.1,0.99]).toCsr_matrix()
      
      self.numpyEvaluationCheckPool(self.pool2,[x],array(x0.todense()),name="SXMatrix",setx0=x0)
      
  def test_MXbinarySparse(self):
      self.message("SXMatrix binary operations")
      spx=CRSSparsity(3,4,[1,2,1],[0,2,2,3])
      spy=CRSSparsity(3,4,[0,2,3],[0,2,2,3])
      xx=MX("x",spx)
      yy=MX("y",spy)
      x0=DMatrix(3,4,[1,2,1],[0,2,2,3],[0.738,0.1,0.99]).toCsr_matrix()
      y0=DMatrix(3,4,[0,2,3],[0,2,2,3],[1.738,0.7,-6]).toCsr_matrix()
      
      self.numpyEvaluationCheckPool(self.matrixbinarypool,[xx,yy],[array(x0.todense()),array(y0.todense())],name="SXMatrix",setx0=[x0,y0])

  def test_symbolcheck(self):
    self.message("Check if non-symbolic inputs are caught")
    self.assertRaises(RuntimeError, lambda : SXFunction([MX(0)],[MX("x")]))


  def test_unite(self):
    self.message("unite operation")
    import numpy
    numpy.random.seed(42)
    xn = numpy.random.random((3,4))
    x=MX(3,4)
    y=MX("x",3,4)
    z=unite(x,y)
    f = MXFunction([y],[z])
    f.init()
    f.input().set(xn)
    f.evaluate()
    self.checkarray(f.output(),xn,"unite dense")
 
    spx=CRSSparsity(3,4,[1,2,1],[0,2,2,3])
    spy=CRSSparsity(3,4,[0,2,2],[0,1,2,3])

    nx=DMatrix(spx,0)
    for k in range(nx.size()):
      nx[k]= numpy.random.rand()
    ny=DMatrix(spy,0)
    for k in range(nx.size()):
      ny[k]= numpy.random.rand()
      
    nxn = nx.toArray()
    nyn = ny.toArray()
    x=MX("x",spx)
    y=MX("y",spy)
    z=unite(x,y)

    f = MXFunction([x,y],[z])
    f.init()
    f.input(0).set(nx)
    f.input(1).set(ny)
    f.evaluate()
    self.checkarray(f.output(),nxn+nyn,"unite sparse")
     
  def test_subsass(self):
     self.message("Check subscripted assignment")
     x=MX("X",3,4)
     import numpy
     numpy.random.seed(42)
     xn = numpy.random.random((3,4))
     r = numpy.zeros((7,8))
     y=MX("Y",7,8)
     y[1:4,[2,4,6,7]]=x
     r[1:4,[2,4,6,7]]=xn
     fy = MXFunction([x],[y])
     fy.init()
     fy.input().set(xn)
     fy.evaluate()
     
     self.checkarray(fy.output(),r,"subscripted assigment")
     
     y=MX(7,8)
     #y[1:4,[2,4,6,7]]=x
     y.setSub([1,2,3],[2,4,6,7],x)
     r[1:4,[2,4,6,7]]=xn
     fy = MXFunction([x],[y])
     fy.init()
     fy.input().set(xn)
     fy.evaluate()
     self.checkarray(fy.output(),r,"subscripted assigment")
  
  def test_erase(self):
    self.message("Erase function")
    self.message(":dense")
    y=MX("Y",7,8)
    import numpy
    r=2*numpy.ones((7,8))
    r[1:4,[2,4,6,7]]=numpy.zeros((3,4))
    z = y *2
    z.erase([1,2,3],[2,4,6,7])
    f = MXFunction([y],[z])
    f.init()
    f.input().set([1]*56)
    e = f.output()
    self.checkarray(f.output(),e,"erase")
    self.message(":sparse")

  def test_mapping(self):
     self.message("Check mapping")
     x=MX("X",3,4)
     import numpy
     numpy.random.seed(42)
     xn = numpy.random.random((3,4))
     r = numpy.zeros((7,8))
     y=MX("Y",7,8)
     y[1:4,[2,4,6,7]]=x
     r[1:4,[2,4,6,7]]=xn
     fy = MXFunction([x],[y])
     fy.init()
     fy.input().set(xn)
     fy.evaluate()
     
     z = c.prod(y.T,y)
     zr = numpy.dot(r.T,r)
     
     f = MXFunction([x],[z])
     f.init()
     f.input().set(xn)
     f.evaluate()
     self.checkarray(f.output(),zr,"prod(mapping.T,mapping)")
     
     x=MX("X",3,1)
     numpy.random.seed(42)
     xn = numpy.random.random((3,1))
     r = numpy.zeros((7,1))
     y=MX("Y",7,1)
     y[1:4,0]=x
     r[1:4,[0]]=xn
     fy = MXFunction([x],[y])
     fy.init()
     fy.input().set(xn)
     fy.evaluate()
     
     z = c.prod(y.T,y)
     zr = numpy.dot(r.T,r)
     
     f = MXFunction([x],[z])
     f.init()
     f.input().set(xn)
     f.evaluate()
     self.checkarray(f.output(),zr,"prod(mapping.T,mapping)")
     
     J=Jacobian(f)
     for mode in ["forward","adjoint"]:
       J.setOption("ad_mode",mode)
       J.init()
       J.input().set(xn)
       J.evaluate()
       self.checkarray(J.output(),matrix(xn).T*2,"jacobian(prod(mapping.T,mapping))")
     
     x=MX("X",3,1)
     numpy.random.seed(42)
     xn = numpy.random.random((3,1))
     r = numpy.zeros((7,1))
     y=MX("Y",7,1)
     y[1:4,0]=x
     r[1:4,[0]]=xn
     fy = MXFunction([x],[y])
     fy.init()
     fy.input().set(xn)
     fy.evaluate()
     
     z = c.prod(y,y.T)
     zr = numpy.dot(r,r.T)
     
     f = MXFunction([x],[z[1:4,1]])
     f.init()
     f.input().set(xn)
     f.evaluate()
     
     J=Jacobian(f)
     J_ = array([[xn[0,0]*2,0,0],[xn[1,0],xn[0,0],0],[xn[2,0],0,xn[0,0]]])
     for mode in ["forward","adjoint"]:
       self.message(":" + mode)
       J.setOption("ad_mode",mode)
       J.init()
       J.input().set(xn)
       J.evaluate()
       print J.output().toArray()
       self.checkarray(J.output(),J_,"jacobian(prod(mapping.T,mapping))")
      
  def test_MXalgebraDense(self):
    self.message("Test some dense algebraic properties of matrices")
    # issue 96
    n = 3
    m = 4
    import numpy
    numpy.random.seed(42)
    A_ = numpy.random.random((m,n))
    A = MX("A",m,n)
    b_ = numpy.random.random((m,1))
    b = MX("b",m,1)
    C_ = numpy.random.random((m,m))
    C = MX("C",m,m)
    D_ = numpy.random.random((m,n))
    D = MX("D",m,n)
    e_ = numpy.random.random((m,1))
    e = MX("e",m,1)
    x_ = numpy.random.random((n,1))
    x = MX("x",n,1)
    
    Axb = casadi.prod(A,x)+b
    Dxe = casadi.prod(D,x)+e
    a = casadi.prod(casadi.prod(trans(Axb),C),Dxe)
    
    f = MXFunction([x,A,b,C,D,e],[a])
    f.init()
    f.input(0).set(x_)
    f.input(1).set(A_)
    f.input(2).set(b_)
    f.input(3).set(C_)
    f.input(4).set(D_)
    f.input(5).set(e_)
    f.evaluate()
    
    f_ = dot(dot((dot(A_,x_)+b_).T,C_),(dot(D_,x_)+e_))
    
    self.checkarray(f.output(),f_,"evaluation")
    
    
    J_ = dot(dot((dot(D_,x_)+e_).T,C_.T),A_) + dot(dot((dot(A_,x_)+b_).T,C_),D_)
    
    for mode in ["forward", "adjoint"]:
      J = Jacobian(f)
      J.setOption("ad_mode","forward")
      J.init()
      J.input(0).set(x_)
      J.input(1).set(A_)
      J.input(2).set(b_)
      J.input(3).set(C_)
      J.input(4).set(D_)
      J.input(5).set(e_)
      J.evaluate()
      
      self.checkarray(J.output(),J_,"evaluation")
      
  def test_MXalgebraSparse(self):
    self.message("Test some sparse algebraic properties of matrices")
    # issue 97
    n = 3
    m = 4
    import numpy
    numpy.random.seed(42)
    
    def randsparsity(m,n):
      sp = CRSSparsity(m,n)
      for i in range((n*m)/2):
        sp.getNZ(numpy.random.randint(m),numpy.random.randint(n))
      return sp
      
    def gentest(m,n):
      As = randsparsity(m,n)
      A_ = DMatrix(As)
      for k in range(As.size()):
        A_[k]= numpy.random.rand()
      A = MX("A",As)
      return (A_.toCsr_matrix(),A)
    
    (A_,A)=gentest(m,n)
    (b_,b)=gentest(m,1)
    (C_,C)=gentest(m,m)
    (D_,D)=gentest(m,n)
    (e_,e)=gentest(m,1)
    x_ = numpy.random.random((n,1))
    x = MX("x",n,1)
    
    Axb = casadi.prod(A,x)+b
    Dxe = casadi.prod(D,x)+e
    a = casadi.prod(casadi.prod(trans(Axb),C),Dxe)
    
    f = MXFunction([x,A,b,C,D,e],[a])
    f.init()
    f.input(0).set(x_)
    f.input(1).set(A_)
    f.input(2).set(b_)
    f.input(3).set(C_)
    f.input(4).set(D_)
    f.input(5).set(e_)
    f.evaluate()


    Axb_ = A_*x_+b_
    Dxe_ = D_*x_+e_
    
    f_ = Axb_.T*C_*Dxe_
    
    self.checkarray(f.output(),f_,"evaluation")
    

    J_ = (D_*x_+e_).T*C_.T*A_ + (A_*x_+b_).T*C_*D_
    
    for mode in ["forward", "adjoint"]:
      J = Jacobian(f)
      J.setOption("ad_mode","forward")
      J.init()
      J.input(0).set(x_)
      J.input(1).set(A_)
      J.input(2).set(b_)
      J.input(3).set(C_)
      J.input(4).set(D_)
      J.input(5).set(e_)
      J.evaluate()
      
      self.checkarray(J.output(),J_,"evaluation")
    
if __name__ == '__main__':
    unittest.main()


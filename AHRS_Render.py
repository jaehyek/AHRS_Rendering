from skinematics.sensors.xsens import XSens

data = XSens("data_xsens.txt")
length = data.totalSamples
hz = data.rate
quat = data.quat
print("hz :%s" %hz)
print("length :%s"% length)


from vpython import *
drag = False
def down(ev):
    global drag
    s.pos = scene.mouse.pos
    s.visible = True
    drag = True

def move(ev):
    global drag
    if not drag: return
    s.pos = scene.mouse.pos

def up(ev):
    global drag
    s.visible = False
    drag = False

scene.bind("mousedown", down)
scene.bind("mousemove", move)
scene.bind("mouseup", up)

scene.title = "A display of Quaternion"
scene.width = 800
scene.height = 700
#scene.range = 5
scene.background = color.gray(0.7)
scene.center = vector(0,0.5,0)
scene.forward = vector(0.7, -0.3,-1)

AxisX = arrow(pos=vector(0,0,0), axis=vector(5,0,0), color=color.green, shaftwidth=0.1)
AxisY = arrow(pos=vector(0,0,0), axis=vector(0,5,0), color=color.green, shaftwidth=0.1)
AxisZ = arrow(pos=vector(0,0,0), axis=vector(0,0,5), color=color.green, shaftwidth=0.1)
label(pos=vector(5,0,0), text='Axis_X',xoffset=40, height=16, color=color.yellow)
label(pos=vector(0,5,0), text='Axis_Y',xoffset=40, height=16, color=color.yellow)
label(pos=vector(0,0,5), text='Axis_Z',xoffset=40, height=16, color=color.yellow)

Objarrow = arrow(pos=vector(0,0,0), axis=vector(5,0,0), color=color.red, shaftwidth=0.4)
Objbox = box(pos=vector(0,-0.4,0), axis=vector(5,0,0), length=5, height=0.2, width=2, color=color.blue )

ObjIMU = compound([Objarrow, Objbox])
# ObjIMU.axis = vector(1,0,0)
# ObjIMU.pos = vector(0,0,0)

for i in range(length) :
    rate(hz)
    ObjIMU.rotate(angle=radians(quat[i][0]), axis=vector(quat[i][1], quat[i][2], quat[i][3]), origin=vector(0,0,0))
    # ObjIMU.rotate(angle=radians(90), axis=vector(0,1,0), origin=vector(0, 0, 0))










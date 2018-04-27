from skinematics.imus import IMU_Base
import numpy as np
import pandas as pd

class RBIOSense(IMU_Base):
    """Concrete class based on abstract base class IMU_Base """

    def get_data(self, in_file, in_data=None):
        '''Get the sampling rate, as well as the recorded data,
        and assign them to the corresponding attributes of "self".

        Parameters
        ----------
        in_file : string
                Filename of the data-file
        in_data : not used here

        Assigns
        -------
        - rate : rate
        - acc : acceleration
        - omega : angular_velocity
        - mag : mag_field_direction
        '''

        # Get the sampling rate from the second line in the file
        try:
            fh = open(in_file)
            fh.readline()
            line = fh.readline()
            rate = np.float(line.split(':')[1].split('H')[0])
            fh.close()

        except FileNotFoundError:
            print('{0} does not exist!'.format(in_file))
            return -1

        # Read the data
        data = pd.read_csv(in_file,
                           sep=',',
                           skiprows=4,
                           index_col=False)

        # Extract the columns that you want, and pass them on
        in_data = {'rate': rate,
                   'acc': data.filter(regex='Acc').values,
                   'omega': data.filter(regex='Gyr').values,
                   'mag': data.filter(regex='Mag').values}

        CONST_GYRO = 0.06097560975609756097560975609756
        CONST_ACC = 16384.0

        ##---------------------gyro calculate -------------------------
        listlist = []
        for listtemp in in_data["omega"] :
            listaa = [float(int.from_bytes((bytes.fromhex(aa)), byteorder='big', signed=True)) for aa in listtemp]
            ## convert to degree
            listlist.append([aa * CONST_GYRO for aa in listaa])

        in_data["omega"] = listlist

        ##---------------------gyro calculate -------------------------
        listlist = []
        for listtemp in in_data["acc"] :
            listaa = [float(int.from_bytes((bytes.fromhex(aa)), byteorder='big', signed=True)) for aa in listtemp]
            ## convert to degree
            listlist.append([aa / CONST_ACC for aa in listaa])

        in_data["acc"] = listlist

        ##---------------------mag calculate -------------------------
        listlist = []
        for listtemp in in_data["mag"]:
            listaa = [float(int.from_bytes((bytes.fromhex(aa)), byteorder='big', signed=True)) for aa in listtemp]
            ## convert to degree
            listlist.append(listaa)

        in_data["mag"] = listlist

        self._set_data(in_data)


data = RBIOSense("putty.log")
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

count = 0
for loop in range(3) :
    ObjIMU.axis = vector(5,0,0)
    ObjIMU.pos = vector(0, 0, 0)
    ObjIMU.up = vector(0, 5, 0)
    sleep(2)
    for i in range(length) :
        rate(hz)
        ObjIMU.rotate(angle=radians(quat[i][0]), axis=vector(quat[i][1], quat[i][2], quat[i][3]), origin=vector(0,0,0))
        # ObjIMU.rotate(angle=radians(90), axis=vector(0,1,0), origin=vector(0, 0, 0))
        count += 1
        # if count == 40 :
        #     break










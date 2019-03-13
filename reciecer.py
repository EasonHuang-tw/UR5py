import socket
import time
import struct
import binascii
import numpy
import math
from pygcode import Line
from pygcode import words

import matplotlib.pyplot as plt


recorder_x = 0.0
recorder_y = 0.0
last_recorder_x=0.0
last_recorder_y=0.0
'''
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)
ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
plt.show()
'''


home_x = 0.5
home_y = 0.02
home_z = 0.1
offset_x = 0
offset_y = 0
offset_z = 0

last_pose_x = 0.0
last_pose_y = 0.0
last_pose_z = 0.0


current_pose_x = 0.5
current_pose_y = 0.02
current_pose_z = 0.1
pose_list=[]





HOST2 = "192.168.50.50" # The remote host
PORT_30003 = 30003
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.settimeout(0.1)
s2.connect((HOST2, PORT_30003))
UR5_pose={}
outofcontrol=1
 


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.grid()




def throwinfo(waypoint,last_recorder_x,recorder_x,last_recorder_y,recorder_y):
	#plt.pause(0.00000000000001);
	#print(waypoint)
	if waypoint != "":
		ax.plot([last_recorder_x,recorder_x], [last_recorder_y,recorder_y], "y", linewidth='1', markersize=1)
		pose_list.append(waypoint)
	#UR5_pose = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#UR5_pose.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#UR5_pose.bind(('', PORT2)) # Bind to the port


#read gcode file
with open('/home/eason/桌面/UR5/dynami_0002.ngc', 'r') as fh:
	print('Open file')

	for line_text in fh.readlines():
		#print line_text,
		line = Line(line_text)
		#print(line)  # will print the line (with cosmetic changes)
		line.block.gcodes  # is your list of gcodes
		line.block.modal_params  # are all parameters not assigned to a gcode, assumed to be motion modal parameters
		line.block.words
		waypoint = ''
		if len(line.block.words) != 0:
			a = words.words2dict(line.block.words)

			if 'G' in a.keys():

				if a['G']==0:

					if 'X' in a.keys():
						offset_x = a.get('X',0)
						last_pose_x = offset_x
						#current_pose_x = current_pose_x + offset_x
					else :
						offset_x = last_pose_x
						#print('sfdgsafgasgfas')

					if 'Y' in a.keys():
						offset_y = a.get('Y',0)
						last_pose_y = offset_y
						#current_pose_y = current_pose_y+ offset_x
					else :
						offset_y =  last_pose_y
					if 'Z' in a.keys():
						offset_z = a.get('Z',0)
						last_pose_z = offset_z
					else :
						offset_z = last_pose_z

					waypoint='('+str(home_x+offset_x*0.001)+', '
					waypoint=waypoint+str(home_y+offset_y*0.001)+', '
					waypoint=waypoint+str(home_z+offset_z*0.001)+', 2.2, -2.2, 0)'

					last_recorder_x = recorder_x
					last_recorder_y = recorder_y
					recorder_x = home_x+offset_x*0.001
					recorder_y = home_y+offset_y*0.001
					
					throwinfo(waypoint,last_recorder_x,recorder_x,last_recorder_y,recorder_y)
					last_offset_X=offset_x
					last_offset_Y=offset_y

				if a['G']==1:
					#print ('G01')
					if 'X' in a.keys():
						offset_x = a.get('X',0)
						last_pose_x = offset_x
						#current_pose_x = current_pose_x + offset_x
					else :
						offset_x = last_pose_x
						#print('sfdgsafgasgfas')

					if 'Y' in a.keys():
						offset_y = a.get('Y',0)
						last_pose_y = offset_y
						#current_pose_y = current_pose_y+ offset_x
					else :
						offset_y =  last_pose_y
					if 'Z' in a.keys():
						offset_z = a.get('Z',0)
						last_pose_z = offset_z
					else :
						offset_z = last_pose_z

					waypoint='('+str(home_x+offset_x*0.001)+', '
					waypoint=waypoint+str(home_y+offset_y*0.001)+', '
					waypoint=waypoint+str(home_z+offset_z*0.001)+', 2.2, -2.2, 0)'
					last_recorder_x = recorder_x
					last_recorder_y = recorder_y
					recorder_x = home_x+offset_x*0.001
					recorder_y = home_y+offset_y*0.001

						
					throwinfo(waypoint,last_recorder_x,recorder_x,last_recorder_y,recorder_y)

					last_offset_X=offset_x
					last_offset_Y=offset_y

				if a['G']==2:
					start_X = last_offset_X
					start_Y = last_offset_Y
					circle_X = start_X + a['I']
					circle_Y = start_Y + a['J']
					end_X = a['X']
					end_Y = a['Y']
					radius=((a['I'])**2+(a['J'])**2)**(1/2)
					start_angle=numpy.angle((start_X-circle_X)+(start_Y-circle_Y)*1j,deg=True)
					if start_angle<0:
						start_angle=start_angle+360
					end_angle=numpy.angle((end_X-circle_X)+(end_Y-circle_Y)*1j,deg=True)
					if end_angle<0:
						end_angle=end_angle+360
					delta_angle=end_angle-start_angle
					if delta_angle>0:
						delta_angle=360-delta_angle
					elif delta_angle<0:
						delta_angle=-delta_angle
					arclength=delta_angle*radius*math.pi/180
					num_of_point=arclength*2
					per_delta_angle=delta_angle/num_of_point

					for num in range (int(num_of_point)):
						offset_x=circle_X+radius*math.cos((start_angle-num*per_delta_angle)*math.pi/180)
						offset_y=circle_Y+radius*math.sin((start_angle-num*per_delta_angle)*math.pi/180)
						if 'Z' in a.keys():
							offset_z = a.get('Z',0)
						else :
							offset_z = current_pose_z

						waypoint='('+str(home_x+offset_x*0.001)+', '
						waypoint=waypoint+str(home_y+offset_y*0.001)+', '
						waypoint=waypoint+str(home_z+offset_z*0.001)+', 2.2, -2.2, 0)'

						
						last_recorder_x = recorder_x
						last_recorder_y = recorder_y
						recorder_x = home_x+offset_x*0.001
						recorder_y = home_y+offset_y*0.001

						throwinfo(waypoint,last_recorder_x,recorder_x,last_recorder_y,recorder_y)
						last_offset_X=offset_x
						last_offset_Y=offset_y

					last_recorder_x = recorder_x
					last_recorder_y = recorder_y
					recorder_x = home_x+end_X*0.001
					recorder_y = home_y+end_Y*0.001
					last_offset_X=end_X
					last_offset_Y=end_Y
					throwinfo(waypoint,last_recorder_x,recorder_x,last_recorder_y,recorder_y)
					
					'''
					recorder_x = home_x+end_X*0.001
					recorder_y = home_y+end_Y*0.001
					throwinfo(waypoint,last_recorder_x,recorder_x,last_recorder_y,recorder_y)
					last_offset_X=offset_x
					last_offset_Y=offset_y
					'''
				if a['G']==3:
					#print ('G03')
					
					start_X = last_offset_X
					start_Y = last_offset_Y
					circle_X = start_X + a['I']
					circle_Y = start_Y + a['J']
					end_X = a['X']
					end_Y = a['Y']
					radius=((a['I'])**2+(a['J'])**2)**(1/2)
					start_angle=numpy.angle((start_X-circle_X)+(start_Y-circle_Y)*1j,deg=True)
					if start_angle<0:
						start_angle=start_angle+360
					end_angle=numpy.angle((end_X-circle_X)+(end_Y-circle_Y)*1j,deg=True)
					if end_angle<0:
						end_angle=end_angle+360
					delta_angle=end_angle-start_angle
					if delta_angle>0:
						delta_angle=delta_angle
					elif delta_angle<0:
						delta_angle=360+delta_angle
					arclength=delta_angle*radius*math.pi/180
					num_of_point=arclength*2
					per_delta_angle=delta_angle/num_of_point

					for num in range (int(num_of_point)):
						offset_x=circle_X+radius*math.cos((start_angle+num*per_delta_angle)*math.pi/180)
						offset_y=circle_Y+radius*math.sin((start_angle+num*per_delta_angle)*math.pi/180)
						if 'Z' in a.keys():
							offset_z = a.get('Z',0)
						else :
							offset_z = current_pose_z

						waypoint='('+str(home_x+offset_x*0.001)+', '
						waypoint=waypoint+str(home_y+offset_y*0.001)+', '
						waypoint=waypoint+str(home_z+offset_z*0.001)+', 2.2, -2.2, 0)'

						
						last_recorder_x = recorder_x
						last_recorder_y = recorder_y
						recorder_x = home_x+offset_x*0.001
						recorder_y = home_y+offset_y*0.001
						if a['Z']<-0.9:
							throwinfo(waypoint,last_recorder_x,recorder_x,last_recorder_y,recorder_y)
						last_offset_X=offset_x
						last_offset_Y=offset_y
					last_recorder_x = recorder_x
					last_recorder_y = recorder_y
					recorder_x = home_x+end_X*0.001
					recorder_y = home_y+end_Y*0.001
					last_offset_X=end_X
					last_offset_Y=end_Y
					throwinfo(waypoint,last_recorder_x,recorder_x,last_recorder_y,recorder_y)
					
		 
		if line.comment:
			line.comment.text  # your comment text
		if waypoint!='' :
			1
			#print(str(current_pose_x)+str("  ")+str(current_pose_y)+str("  ")+str(current_pose_z)+str("  "))
	
plt.pause(0.1)

print("Starting Program")

count = 0
home_status = 0
program_run = 0


while(True):

	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s2.settimeout(5)
	s2.connect((HOST2, PORT_30003))
	count = count+1


	packet_1 = s2.recv(4)
	packet_2 = s2.recv(8)
	packet_3 = s2.recv(48)
	packet_4 = s2.recv(48)
	packet_5 = s2.recv(48)
	packet_6 = s2.recv(48)
	packet_7 = s2.recv(48) 
	packet_8 = s2.recv(48)
	packet_9 = s2.recv(48)
	packet_10 = s2.recv(48)
	packet_11 = s2.recv(48)

	packet_12 = s2.recv(8)
	#packet_12 = binascii.hexlify(packet_12) #convert the data from \x hex notation to plain hex
	x = struct.unpack('!d', packet_12)[0]
	print("X = ", x * 1000)
	UR5_pose['X']=x;

	packet_13 = s2.recv(8)
	##packet_13 = binascii.hexlify(packet_13) #convert the data from \x hex notation to plain hex
	##y = str(packet_13)
	y = struct.unpack('!d', packet_13)[0]
	print("Y = ", y * 1000)
	UR5_pose['Y']=y;

	packet_14 = s2.recv(8)
	#packet_14 = packet_14.encode("hex") #convert the data from \x hex notation to plain hex
	#z = str(packet_14)
	z = struct.unpack('!d', packet_14)[0]
	print("Z = ", z * 1000)
	UR5_pose['Z']=z;


	packet_15 = s2.recv(8)
	#packet_15 = packet_15.encode("hex") #convert the data from \x hex notation to plain hex
	#Rx = str(packet_15)
	Rx = struct.unpack('!d', packet_15)[0]
	print("Rx = ", Rx)
	UR5_pose['Rx']=Rx;

	packet_16 = s2.recv(8)
	#packet_16 = packet_16.encode("hex") #convert the data from \x hex notation to plain hex
	#Ry = str(packet_16)
	Ry = struct.unpack('!d', packet_16)[0]
	print("Ry = ", Ry)
	UR5_pose['Ry']=Ry;

	packet_17 = s2.recv(8)
	#packet_17 = packet_17.encode("hex") #convert the data from \x hex notation to plain hex
	#Rz = str(packet_17)
	Rz = struct.unpack('!d', packet_17)[0]

	print("Rz = ", Rz)
	UR5_pose['Rz']=Rz;
	#time.sleep(0.1)
	s2.recv(48)
	s2.recv(48)
	s2.recv(48)
	s2.recv(48)
	s2.recv(8)
	s2.recv(48)
	s2.recv(8)
	s2.recv(8)
	s2.recv(8)
	s2.recv(48)
	s2.recv(8)
	s2.recv(48)
	s2.recv(24)
	s2.recv(48)
	s2.recv(8)
	s2.recv(8)
	s2.recv(8)
	s2.recv(8)
	s2.recv(8)
	s2.recv(8)
	s2.recv(8)
	s2.recv(48)
	s2.recv(8)
	s2.recv(8)
	s2.recv(24)
	s2.recv(24)

	print("count:",count)
	if count>=2:	
		ax.plot([last_X,UR5_pose['X']], [last_Y,UR5_pose['Y']], color =  "green", linewidth='2', markersize=2)
		plt.pause(0.05);
	print("X= ",UR5_pose['X'])
	last_X=UR5_pose['X']
	last_Y=UR5_pose['Y']
print("Program finish")

'''
while(True):
	print (outofcontrol)
	if outofcontrol==1:
		s2.close()
		s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s2.settimeout(0.1)
		s2.connect((HOST2, PORT_30003))
		outofcontrol=0
		print ("Im out of control and reconnected")
		time.sleep(1)
	UR5_POSE_UPDATE(s2)
	count = count+1

	print("count:",count)
	if count>=2:	
		ax.plot([last_X,UR5_pose['X']], [last_Y,UR5_pose['Y']], color =  "green", linewidth='1', markersize=3)
		plt.pause(0.05);
	print("X= ",UR5_pose['X'])
	last_X=UR5_pose['X']
	last_Y=UR5_pose['Y']
	time.sleep(0.2)
	a=0
	while a==0:
		try:
			s.settimeout(0.002)
			s.recv(8)
		except:
			a=1
	a=0
	s2.settimeout(0.1)

print("Program finish")
'''
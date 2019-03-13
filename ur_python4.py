import socket
import time
import numpy
import math
from pygcode import Line
from pygcode import words

import matplotlib.pyplot as plt

import time
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



HOST = "192.168.50.110" # The remote host
PORT = 30000 # The same port as used by the server

HOST2 = "192.168.50.50" # The remote host
PORT_30003 = 30003

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.grid()



def throwinfo(waypoint,last_recorder_x,recorder_x,last_recorder_y,recorder_y):
	#plt.pause(0.00000000000001);
	#print(waypoint)
	if waypoint != "":
		ax.plot([last_recorder_x,recorder_x], [last_recorder_y,recorder_y], 'r-', linewidth='1', markersize=3)
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
					num_of_point=arclength*3
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
					num_of_point=arclength*3
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

#UR5.listen(5) # Now wait for client connection.
#c, addr = UR5.accept() # Establish connection with client.
#time.sleep( 1 )
step = 0
for i in pose_list:
	print(step,'   ')
	print(i),
	step=step+1

print ("Number of waypoints" ,len(pose_list))
#print (pose_list)
print ("Start program")

print('========================================================================')


print ("Open socket")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT)) # Bind to the port
s.listen(5) # Now wait for client connection.
c, addr = s.accept() # Establish connection with client.
print('addr of connection  is', addr)

#starting to communicate with the client
count=0

try:
	msg = c.recv(1024)
	if msg.decode('utf-8') == "initialize" :
		strdatanum = '(' + str(len(pose_list))  + ')'
		print(strdatanum)
		send_msg = bytes(strdatanum, encoding="utf8")
		c.send(send_msg)   #send datanum
except socket.error as socketerror:
		print ("error")
pose_last = pose_list[len(pose_list)-1]
for i in range(9):
	pose_list.append(pose_last)

try:
	msg = c.recv(1024)
	while (count < len(pose_list)):

		if msg.decode('utf-8') == 'asking_for_data':

				print ("The count is:", count)
				v=pose_list[count]
				v=bytes(v, encoding='utf8')
				c.send(v)
				print(v),
				count = count+1
				time.sleep(0.01)
		msg = c.recv(1024)
except socket.error as socketerror:
 			print (count)
c.close()
s.close()
print ("Program finish")

'''

flag = false

if targetPos[2] > 0.1

flag = true

elif targetPos[2]<0.1 && flag == true < 0.1

flag = false
'''

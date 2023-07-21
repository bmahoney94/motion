from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

class Frame:
	""" Holds the geometry for the attachment points of actuators.	"""
	def __init__( self, radius = 1, theta_o = 90):

		# Radius of the attachment points from the centroid
		self.radius = radius
		
		# This is the 'zero' radius.  Actuator attachment points count outwards from here.
		self.theta_o = theta_o

		# Attachment points in local coordinate system.
		self._set_attachment_points()
	

	def _set_attachment_points( self):
		""" Assigns location for attachment points in local coordinate system."""
		self.attachment_points = []
		
		theta = self.theta_o

		for i in range( 0, 6):
			self.attachment_points.append( [ self.radius * np.cos( np.radians( theta)),
											 self.radius * np.sin( np.radians( theta)), 
											 0. ])

			theta = theta + 120

	def plot( self):
		""" Creates scatterplot to show attachment points in local coordinate system. """
		x = np.zeros( 6)
		y = np.zeros( 6)		
		z = np.zeros( 6)		
		
		for index, attachment_point in enumerate( self.attachment_points):
			x[ index], y[ index], z[ index]= attachment_point

		plt.scatter( x, y)
		plt.show()

class Leg:
	""" Holds the geometry of a leg, i.e. start and end points and length.

		Eventually, should handle the inner loop dynamics for extending and retracting
		the legs with the help of an actuator object as well.
	"""
	def __init__( self, base_position, top_position):
		self.base_position = base_position
		self.top_position = top_position
		self.length = self.get_length()

	def __repr__( self):
		return "Hello!"

	def get_length( self):
		ssum = 0.

		for index in range( 0, 3):
			ssum += (self.top_position[ index] - self.base_position[ index]) ** 2
		
		return np.sqrt( ssum)


class StewartPlatform:
	""" Holds both moving and fixed frames' geometry, as well as that of the legs.	"""	
	def __init__( self, base_frame, moving_frame):
		print( "Creating a stewart platform")
		assert( type( base_frame) == Frame)
		assert( type( moving_frame) == Frame)

		self.base_frame = base_frame
		self.moving_frame = moving_frame
	
		# Separation between centroid of each frame in an East-North-Up frame
		# A North-East-Down relative to the base frame would make more sense, but I think
		# the math is a little more annoying that way until I update how the frames are defined.
		self.mf_centroid = [ 0., 0., 1.]

		self.pitch_angle = 0.
		self.bank_angle  = 0.
		self.yaw_angle   = 0.
		
		self.legs = []

		for index in range( 0, 6):
			top_pos	= self.moving_frame.attachment_points[ index] + self.mf_centroid
			base_pos = self.base_frame.attachment_points[ index]
					
			new_leg = Leg( base_pos, top_pos)
					
			self.legs.append( new_leg)
			
			print( new_leg.get_length())

	def plot( self):
		self.base_frame.plot()
		self.moving_frame.plot()

if __name__ == '__main__':

	base_frame = Frame( 1.5, 90)
	pprint( base_frame.__dict__)
	base_frame.plot()

	moving_frame = Frame( 1.5, 30)
	pprint( moving_frame.__dict__)
	moving_frame.plot()	


	test_platform = StewartPlatform( base_frame, moving_frame )
	pprint( test_platform.__dict__)

	test_platform.plot()


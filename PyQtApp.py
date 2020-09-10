import sys, math, random, queue, threading
import pyautogui
import serial
import numpy	
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.QtGui import QPainter, QPen, QColor, QKeySequence, QMouseEvent
from PyQt5.QtCore import Qt, QTimer, QThread

WIDTH = 40
grid = []
intense = 80

xpos = 50
ypos = 50

class Cell():
	def __init__(self, i, j, intensity):
		self.i = i
		self.j = j
		self.walls = [1, 1, 1, 1]  # top, right, bottom, left
		self.intensity = intensity
		#print(intensity)
	def index(self, i, j, cols, rows):
		if (i < 0) or (j < 0) or (i > (cols - 1)) or (j > (rows - 1)):
			return None
		else:
			return i + j * cols

class PressurePoint():
	def __init__(self, i, j, intensity):
		self.i = i
		self.j = j
		self.intensity = intensity

class App(QWidget):
	def __init__(self):
		super().__init__()
		
		self.state = 0
		self.data = [0,0,0,0,0,0,0,0]
		self.databaseline = [0,0,0,0,0,0,0,0]
		self.dataout = [1,1,1,1,1,1,1,1] 
		self.first = 100
		self.ser = serial.Serial('COM4',timeout=5)
		self.ser.baudrate = 115200
		self.pressed = 0
		self.left = 0
		self.top = 0
		self.centerPressure = Cell(0,0,1)
		self.width = 1400
		self.height = 620
		self.color = 0
		self.point = (10,10)
		self.force = 80
		self.up = 0
		self.cols = math.floor(self.width / WIDTH)
		self.rows = math.floor(self.height / WIDTH)
		self.points = [[self.cols*1/8,self.rows/4],[self.cols*3/8,self.rows/4],[self.cols*5/8,self.rows/4],[self.cols*7/8,self.rows/4],\
		[self.cols*7/8,self.rows*3/4],[self.cols*5/8,self.rows*3/4],[self.cols*3/8,self.rows*3/4],[self.cols*1/8,self.rows*3/4]]
		self.active = False
		self.initui()
		self.init_cells(self.point, intense)

	def keyPressEvent(self, event):
		global intense
		if(event.text() == 'a'):
			intense = intense + 1
		if(event.text() == 'd'):
			intense = intense - 1

	def mousePressEvent (self, event):
		self.pressed = 0
	
	def mouseReleaseEvent(self, event):
		self.pressed = 0


	def findClosestPoint(self, i, j):
		
		closestDist = 100000
		
		if not self.points:
			return None
		closestPoint = self.points[0].copy()
		number = 0
		closestnumber = 0
		firstpoint = 1
		for p in self.points:
			if firstpoint == 1:
				closestPoint = p
				closestDist = math.sqrt((p[0] - i)**2 + (p[1] - j)**2)
				firstpoint = 0
			else:
				if (math.sqrt((p[0] - i)**2 + (p[1] - j)**2) < closestDist):
					closestPoint = p
					closestDist = math.sqrt((p[0] - i)**2 + (p[1] - j)**2)
					closestnumber = number
			number = number + 1
		# print(closestPoint.copy())
		return closestPoint.copy(), closestnumber



		return

	def init_cells(self, point, force):
		if not self.active:
			del grid[:]
			for j in range(self.rows):
				for i in range(self.cols):
					closestPoint, number = self.findClosestPoint(i,j)
					if closestPoint is None:
						cell = Cell(i, j, 0)
					else:
						cell = Cell(i, j, min(255 , 255- (int(math.sqrt(abs(closestPoint[0]-i)**2 + abs(closestPoint[1]-j)**2)*(100-self.dataout[number])))))
					grid.append(cell)
			QTimer.singleShot(1, self.go)

	def go(self):
		global xpos
		global ypos

		self.active = True

		current = grid[0]
		current.visited = 1
		current.currentCell = 1
		while True:
			self.update()
			while(self.ser.read() != b's'):
				pass
			tdata = self.ser.read(63)
			#print (type(tdata))
			
			charcounter = 0
			tempdata = []
			for character in tdata:
				if character != 32:
					tempdata.append(character)
				else:
					self.data[charcounter] = float(bytes(tempdata).decode("utf-8"))
					tempdata = []
					charcounter = charcounter + 1



			if(self.first > 0):
				self.databaseline = self.data.copy()
				self.first = self.first - 1
				print(self.databaseline)
				print(self.data)		
				print(self.point)
			else:
				self.dataout = [self.data[0]-self.databaseline[0],self.data[1]-self.databaseline[1],self.data[2]-self.databaseline[2],self.data[3]-self.databaseline[3], \
				self.data[4]-self.databaseline[4],self.data[5]-self.databaseline[5],self.data[6]-self.databaseline[6],self.data[7]-self.databaseline[7]]
				#self.databaseline = numpy.subtract(self.databaseline, numpy.multiply(numpy.subtract(self.databaseline,self.data),0.0));
				if sum(self.dataout):
					self.point = [(self.dataout[0]*self.cols*1/8+ self.dataout[1]*self.cols*3/8+ self.dataout[2]*self.cols*5/8+ self.dataout[3]*self.cols*7/8+ \
							   self.dataout[4]*self.cols*7/8+ self.dataout[5]*self.cols*5/8+ self.dataout[6]*self.cols*3/8+ self.dataout[7]*self.cols*1/8)/sum(numpy.absolute(self.dataout)), \
							   (self.dataout[0]*self.rows/8+ self.dataout[1]*self.rows/8+ self.dataout[2]*self.rows/8+ self.dataout[3]*self.rows/8+ \
							   self.dataout[4]*self.rows*7/8+ self.dataout[5]*self.rows*7/8+ self.dataout[6]*self.rows*7/8+ self.dataout[7]*self.rows*7/8)/sum(numpy.absolute(self.dataout))]

				self.centerPressure = Cell(int(self.point[0]),int(self.point[1]),sum(self.dataout))
				print(self.databaseline)
				print(self.data)		
				print(self.point)

				#print(self.dataout)
				#print(dataout)

			x , y = (pyautogui.position())
			xpos = int(x / WIDTH)
			ypos = int(y / WIDTH)
			QApplication.processEvents()
			#QThread.msleep(1)
			if(self.pressed):
				self.points.append([xpos,ypos])
			if(self.up == 0):
				self.color = self.color + 1
				if self.color == 255:
					 self.up = 1
			else:
				self.color = self.color - 1
				if self.color == 0:
					 self.up = 0
		self.active = False

	def initui(self):
		QShortcut(QKeySequence('F5'), self, self.init_cells)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.lightGray)
		self.setPalette(p)
		self.show()

	def paintEvent(self, e):
		
		# Draw full grid

		# for c in grid:
		# 	closestPoint, number = self.findClosestPoint(c.i,c.j)
		# 	if closestPoint is not None:
		# 		c.intensity = min(255 , 255- min(255 ,(int(math.sqrt(abs(closestPoint[0]-c.i)**2 + abs(closestPoint[1]-c.j)**2)*(100-abs(self.dataout[number])*4)))))
		# 	self.draw_cell_manual(c)
		# self.draw_cell_manual(self.centerPressure)

		for c in grid:
			if(sum(self.dataout)):
				c.intensity = min(255 , 255- min(255 ,(int(math.sqrt(abs(self.centerPressure.i-c.i)**2 + abs(self.centerPressure.j-c.j)**2)*(100-self.centerPressure.intensity)))))
			else:
				c.intensity = 0

			self.draw_cell_manual(c)
		
		self.draw_cell_manual(self.centerPressure)
		#print(self.centerPressure.i)
		#print(self.centerPressure.j)



	def draw_cell_manual(self, cell):
		x = cell.i * WIDTH
		y = cell.j * WIDTH
		# LINES
		qp = QPainter(self)
		qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
		if cell.walls[0]:  # top
			qp.drawLine(x    , y    , x + WIDTH, y)
		if cell.walls[1]:  # right
			qp.drawLine(x + WIDTH, y    , x + WIDTH, y + WIDTH)
		if cell.walls[2]:  # bottom
			qp.drawLine(x + WIDTH, y + WIDTH, x    , y + WIDTH)
		if cell.walls[3]:  # left
			qp.drawLine(x    , y + WIDTH, x    , y)
		forcecolor = intense / 100
		qp.setBrush(QColor(max(0,min(255,forcecolor*cell.intensity*4)), max(0,min(255,((1.0 - forcecolor) * cell.intensity*4))) , 0, 200))
		qp.drawRect(x, y, WIDTH, WIDTH)


	def draw_cell(self, cell):
		x = cell.i * WIDTH
		y = cell.j * WIDTH
		# LINES
		qp = QPainter(self)
		qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
		if cell.walls[0]:  # top
			qp.drawLine(x    , y    , x + WIDTH, y)
		if cell.walls[1]:  # right
			qp.drawLine(x + WIDTH, y    , x + WIDTH, y + WIDTH)
		if cell.walls[2]:  # bottom
			qp.drawLine(x + WIDTH, y + WIDTH, x    , y + WIDTH)
		if cell.walls[3]:  # left
			qp.drawLine(x    , y + WIDTH, x    , y)
		if cell.visited:
			if cell.currentCell:
				qp.setBrush(QColor(0, 0 , 255, 100))
			else:
				qp.setBrush(QColor(255, 0, 255, 100))
			qp.drawRect(x, y, WIDTH, WIDTH)



if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())


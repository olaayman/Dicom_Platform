############################ Importing The Necessary Libraries ############################
import sys
import pydicom as dicom 
import numpy as np
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import os


############################  AUTO-Connect with ui file ############################ 
ui,_ = loadUiType(os.path.join(os.path.dirname(__file__),'first_gui.ui'))

class Dicom_Viewer_App(QMainWindow , ui):
    def __init__(self , parent=None):
        super(Dicom_Viewer_App , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        ########## Global variables ##########
        self.data_set_path=""
        self.volume3d=""
        self.sliders_list = [self.AxialHorizontalSlider,
                            self.SagittalHorizontalSlider,
                            self.CoronalHorizontalSlider,
                            self.AxialVerticalSlider,
                            self.SagittalVerticalSlider,
                            self.CoronalVerticalSlider]
        self.startPoint = [0,0]
        self.endPoint = [512,512]
        self.obliqueLineEquation = []
        self.obliqueLine_slope = 1
            
        self.axialSlice = 117
        self.sagittalSlice = 117
        self.coronalSlice = 117

        self.pointsList = [[0,0],[0,0]]                     
        
        ########## Calling Functions ##########
        self.handle_buttons() ##### Connect Browse Button to Dicom Folder ##### 
        self.set_oblique_sliders() ##### Set Oblique Sliders Limits #####

        self.obliqueLineSlider.valueChanged.connect(self.viewing_planes) ##### Oblique Line Angle Movement Event #####
        self.obliqueLineSlopeSlider.valueChanged.connect(self.viewing_planes) ##### Oblique Line Slope Movement Event #####
        

        ##### Loop through sliders_list to update the slices with respect to sliders values #####
        for i, slider in enumerate(self.sliders_list):
          if i ==0:
            slider.valueChanged.connect(self.Axial_H_changed)
          if i ==3:
            slider.valueChanged.connect(self.Axial_V_changed)
          if i ==1:
            slider.valueChanged.connect(self.Sagittal_H_changed)
          if i ==4:  
            slider.valueChanged.connect(self.Sagittal_V_changed)
          if i ==2:  
            slider.valueChanged.connect(self.Coronal_H_changed)
          if i ==5:  
            slider.valueChanged.connect(self.Coronal_V_changed)
       
        ##### Setting up Label for Line Length measurement #######
        self.lineLength_label.setStyleSheet("border: 1px solid black;")

           
    def set_oblique_sliders(self):
        '''Setting Oblique Sliders Limitations'''
        self.obliqueLineSlopeSlider.setValue(0)
        self.obliqueLineSlopeSlider.setMinimum(-512)
        self.obliqueLineSlopeSlider.setMaximum(512)
        self.obliqueLineSlopeSlider.setTickInterval(1)

        self.obliqueLineSlider.setValue(0)
        self.obliqueLineSlider.setMinimum(-512)
        self.obliqueLineSlider.setMaximum(512)
        self.obliqueLineSlider.setTickInterval(1)
        
    def Axial_H_changed(self):
        '''Update Sagittal Slice with Respect to Axial Horizontal Slider'''
        self.sagittalSlice = self.AxialHorizontalSlider.value()
        self.viewing_planes()
        

    def Axial_V_changed(self):
        '''Update Coronal Slice with Respect to Axial Vertical Slider'''
        self.coronalSlice = -self.AxialVerticalSlider.value()
        self.viewing_planes()

    def Sagittal_H_changed(self):
        '''Update Coronal Slice with Respect to Sagittal Horizontal Slider'''
        self.coronalSlice = self.SagittalHorizontalSlider.value()
        self.viewing_planes()

    def Sagittal_V_changed(self):
        '''Update Axial Slice with Respect to Sagittal Vertical Slider'''
        self.axialSlice = -self.SagittalVerticalSlider.value()
        self.viewing_planes()

    def Coronal_H_changed(self):
        '''Update Sagittal Slice with Respect to Coronal Horizontal Slider'''
        self.sagittalSlice = self.CoronalHorizontalSlider.value()
        self.viewing_planes()

    def Coronal_V_changed(self):
        '''Update Axial Slice with Respect to Coronal Vertical Slider'''
        self.axialSlice = -self.CoronalVerticalSlider.value()
        self.viewing_planes()

    def Graphic_Scene(self,fig_width,fig_height,view,bool=True):
        '''Setting up a canvas to view an image in its graphics view'''
        scene= QGraphicsScene()
        figure = Figure(figsize=(fig_width/90, fig_height/90),dpi = 90)
        canvas = FigureCanvas(figure)
        axes = figure.add_subplot()
        scene.addWidget(canvas)
        # scene.addWidget(self.dial)
        view.setScene(scene)
        if bool ==True:
            figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
            axes.get_xaxis().set_visible(False)
            axes.get_yaxis().set_visible(False)
        else:
            axes.get_xaxis().set_visible(True)
            axes.get_yaxis().set_visible(True)
        self.show()
        return figure,axes


    def handle_buttons(self):
        '''Connect Browse Button with browse_dicom_folder function'''
        self.Browse_Button.clicked.connect(self.browse_dicom_folder)

    def browse_dicom_folder(self):
        '''Browse to get Dicom Folder'''
        #Getting folder path
        self.data_set_path = QFileDialog.getExistingDirectory(self,"Select Dicom Folder",directory='.')
        if (self.data_set_path == ""):
            return
        else:
           self.build_3d_volume()
           
        
          

    def build_3d_volume(self):
        '''Convert dicom image to 3d volume'''
        head_images = os.listdir(self.data_set_path)

        # Getting the images slices
        # Reading Dicom images/slices
        slices = [dicom.read_file(self.data_set_path + '/' + s, force= True) for s in head_images]


        # Initializing the 3-D mattrix
        img_shape = list(slices[0].pixel_array.shape)
        img_shape.append(len(slices))
        self.volume3d=np.zeros(img_shape)

        # Converting dicom image to 3D Mattrix
        for i,s in enumerate(slices):
            array2D=s.pixel_array
            self.volume3d[:,:,i]= array2D

        self.set_sliders_limits(self.sliders_list )
        # viewing planes
        self.viewing_planes()


    def set_sliders_limits(self, sliders):
        '''Declaring sliders limitations'''
        for i, slider in enumerate(sliders):
            # slider.setValue()
            if i > 2 :
                if i == 3:
                    slider.setMinimum(-self.volume3d.shape[1]+2)
                    slider.setMaximum(0)
                    slider.setTickInterval(1)
                    slider.setValue(-self.volume3d.shape[1]//2)
                else:
                    slider.setMinimum(-232)
                    slider.setMaximum(0)
                    slider.setTickInterval(1)
                    slider.setValue(-234//2)
            if i == 0:
                slider.setMinimum(0)
                slider.setMaximum(self.volume3d.shape[0]-2)
                slider.setTickInterval(1)
                slider.setValue(self.volume3d.shape[0]//2)
            if (i ==1 or i ==2):
                slider.setMinimum(0)
                slider.setTickInterval(1)
                slider.setMaximum(510)
                slider.setValue(256)
       


    def viewing_planes(self):
        '''Creating the planes figures and axes and plotting slices on them'''

        # Initialize figure and axis for every plane
        self.axial_figure, self.axial_axis = self.Graphic_Scene(210, 170, self.Axial_Plane)
        self.sagittal_figure, self.sagittal_axis = self.Graphic_Scene(210, 170, self.Sagittal_Plane)
        self.coronal_figure, self.coronal_axis = self.Graphic_Scene(210, 170, self.Coronal_Plane)

        # Plot a slice on every plane
        self.axial_axis.imshow((self.volume3d[:,:,self.axialSlice]), cmap="gray")
        self.sagittal_axis.imshow(np.rot90((self.volume3d[:,self.sagittalSlice,:])), cmap="gray")
        self.coronal_axis.imshow(np.rot90((self.volume3d[self.coronalSlice,:,:])), cmap="gray")
        
        # Calculate Oblique Line Slope
        if (self.obliqueLineSlopeSlider.value() > 0 and (512- self.startPoint[0]) > 0):
            self.obliqueLine_slope = ((512-self.obliqueLineSlopeSlider.value()- self.startPoint[1])/(512- self.startPoint[0]))
        elif (self.obliqueLineSlopeSlider.value() < 0 and (512+self.obliqueLineSlopeSlider.value()-self.startPoint[1]) > 0):
            self.obliqueLine_slope = ((512- self.startPoint[1])/(512+self.obliqueLineSlopeSlider.value()-self.startPoint[1]))

        if self.obliqueLineSlider.value() >= 0:
            self.startPoint = [self.obliqueLineSlider.value(), 0]
            if self.obliqueLineSlopeSlider.value() >= 0:
                self.endPoint = [512, self.obliqueLine_slope * (512 - self.startPoint[0])+self.startPoint[1]] 
            else:
                self.endPoint = [((512-self.startPoint[1]) / self.obliqueLine_slope)+self.startPoint[0], 512]
        elif self.obliqueLine_slope  != 0:
            self.startPoint = [0, -self.obliqueLineSlider.value()]
            if self.obliqueLineSlopeSlider.value() <= 0:
                self.endPoint = [((512-self.startPoint[1]) / self.obliqueLine_slope)+self.startPoint[0], 512]
            else:
                self.endPoint = [512, self.obliqueLine_slope * (512 - self.startPoint[0])+self.startPoint[1]] 


        # Draw Oblique Line 
        self.obliqueLine = self.axial_axis.axline(self.startPoint,slope=self.obliqueLine_slope)
        self.obliqueLine.set_visible(True)
        
        # Get Oblique Line Equation by 2 points
        self.obliqueLineEquation = self.lineFromPoints(self.startPoint, self.endPoint)
        self.createObliqueImage() # Create Oblique Slice

        # Display The Planes
        self.axial_axis.axhline(y = -self.AxialVerticalSlider.value(), color = 'b', label = 'axvline - full height')
        self.axial_axis.axvline(x = self.AxialHorizontalSlider.value(), color = 'b', label = 'axvline - full height')
        self.sagittal_axis.axhline(y = -self.SagittalVerticalSlider.value(), color = 'b', label = 'axvline - full height')
        self.sagittal_axis.axvline(x = self.SagittalHorizontalSlider.value(), color = 'b', label = 'axvline - full height')
        self.coronal_axis.axhline(y = -self.CoronalVerticalSlider.value(), color = 'b', label = 'axvline - full height')
        self.coronal_axis.axvline(x = self.CoronalHorizontalSlider.value(), color = 'b', label = 'axvline - full height') 

        
        self.axial_figure.canvas.mpl_connect('button_press_event', self.onclick) # Update Oblique Slice Event

        self.show()

    def onclick(self,event):     
        '''Update Obliques Lines in The Axial Plane'''
        self.obliqueLine.set_visible(False)
        self.obliqueLine_slope = ((event.ydata- self.startPoint[1])/(event.xdata- self.startPoint[0]))
        self.obliqueLine = self.axial_axis.axline(self.startPoint,slope=abs(self.obliqueLine_slope))
        self.obliqueLine.set_visible(True)
        self.axial_figure.canvas.draw_idle()
        self.axial_figure.canvas.flush_events()    

    def createObliqueImage(self):
        '''Create Oblique Slice'''
        Line_length = np.sqrt(pow(self.endPoint[0] -self.startPoint[0], 2) + pow(self.endPoint[1] -self.startPoint[1], 2))
        
        self.obliqueLineCoordinates = []
        for p in range(int(Line_length)):
            t= p / Line_length
            self.obliqueLineCoordinates.append([round((1-t)*self.startPoint[1] + t* self.endPoint[1]),round((1-t)*self.startPoint[0] + t* self.endPoint[0])])  
    
       

        self.obliqueLineCoordinates = np.array(self.obliqueLineCoordinates)
        self.obliqueSlice = []

        for z in range(self.volume3d.shape[2]):
            for i in range(len(self.obliqueLineCoordinates)):
                self.obliqueSlice.append(self.volume3d[self.obliqueLineCoordinates[i][0], self.obliqueLineCoordinates[i][1], z])

        width = int(len(self.obliqueSlice) / len(self.obliqueLineCoordinates))
        self.obliqueSlice = np.array(self.obliqueSlice)
        self.obliqueSlice = np.reshape(self.obliqueSlice, (width, len(self.obliqueLineCoordinates)))
        
        self.oblique_figure, self.oblique_axis = self.Graphic_Scene(210, 170, self.Diagonal_Plane)

        # Plot Oblique Slice
        self.oblique_axis.imshow(np.rot90(self.obliqueSlice.T), cmap="gray")

        # Plot Line on Oblique and calulate the distance
        self.oblique_figure.canvas.mpl_connect('button_press_event', self.onclickOblique)
        # self.oblique_axis.plot([self.pointsList[0][0],self.pointsList[1][0]],[self.pointsList[0][1],self.pointsList[1][1]])
        # self.oblique_figure.canvas.draw_idle()
        # self.oblique_figure.canvas.flush_events()
        # self.show() 
    
    def onclickOblique(self, event):
        print("point clicked ", [event.xdata, event.ydata])
        if len(self.pointsList) < 2:
            self.pointsList.append([event.xdata, event.ydata])
        else: 
            self.pointsList = []
            self.pointsList.append([event.xdata, event.ydata])
            self.oblique_axis.cla()
            self.oblique_axis.imshow(np.rot90(self.obliqueSlice.T), cmap="gray")
            #self.createObliqueImage()


        if len(self.pointsList) == 2:
            self.oblique_axis.plot([self.pointsList[0][0],self.pointsList[1][0]],[self.pointsList[0][1],self.pointsList[1][1]])
            self.oblique_figure.canvas.draw_idle()
            self.oblique_figure.canvas.flush_events()
            self.show() 
            lineLength = np.sqrt(pow(self.pointsList[1][0] -self.pointsList[0][0], 2) + pow(self.pointsList[1][1] - self.pointsList[0][1], 2))
            self.lineLength_label.setText("Length of the line = " + str(lineLength))

        #self.obliqueLine_slope = ((event.ydata- self.startPoint[1])/(event.xdata- self.startPoint[0]))


    def lineFromPoints(self,P, Q):
        '''Get Line Equation from 2 Points'''
        a = Q[1] - P[1]
        b = P[0] - Q[0]
        c = a*(P[0]) + b*(P[1])
    
        return [a,b,c]


if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Dicom_Viewer_App()
    window.show()
    app.exec_()
# Importing necessary libraries
import pydicom as dicom # For reading dicom image
import numpy as np # For working with arrays
import matplotlib.pyplot as plt # For plotting
import os # For reading files

# Getting the dicom image path
data_set_path = "./Head"
head_images = os.listdir(data_set_path)

# Getting the images slices
# Reading Dicom images/slices
slices = [dicom.read_file(data_set_path + '/' + s, force= True) for s in head_images]


# Initializing the 3-D mattrix
img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))
volume3d=np.zeros(img_shape)

# Converting dicom image to 3D Mattrix
for i,s in enumerate(slices):
    array2D=s.pixel_array
    volume3d[:,:,i]= array2D


# Initializing axis for the 3 planes
axial=plt.subplot(2,2,1)
plt.title("Axial") # from top to down 
sagital=plt.subplot(2,2,2)
plt.title("Sagital") # from side to side 
coronal=plt.subplot(2,2,3)
plt.title("Coronal") # from front to back


axial.imshow(volume3d[:,:,img_shape[2]//2]) # A axial is an X-Y plane, parallel to the ground, the head from the feet.
sagital.imshow(np.rot90(volume3d[:,img_shape[1]//2,:])) # A sagittal is a Y-Z plane, which separates left from right. 
coronal.imshow(np.rot90(volume3d[img_shape[0]//2,:,:])) # A coronal is an X-Z plane, the front from the back.

# Displaying axial slices planes
for z in range(volume3d.shape[2] ):           
    axial.cla()                          
    axial.imshow(volume3d[:,:,z])
    plt.pause(0.0001)  

# Displaying sagittal slices planes
for y in range(volume3d.shape[1]):           
    sagital.cla()                          
    sagital.imshow(np.rot90(volume3d[:,y,:]))
    plt.pause(0.0001)    

# Displaying coronal slices planes
for x in range(volume3d.shape[0]):           
    coronal.cla()                          
    coronal.imshow(np.rot90(volume3d[x,:,:]))
    plt.pause(0.0001)                        

print(array2D.shape)
print(volume3d.shape)    




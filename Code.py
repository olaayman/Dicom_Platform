import pydicom as dicom
import numpy as np
import matplotlib.pyplot as plt
import os

path = "./Head"
head_images = os.listdir(path)

slices = [dicom.read_file(path + '/' + s, force= True) for s in head_images]

slices = sorted(slices,key=lambda x:x.ImagePositionPatient[2])

# pixel_spacing = slices[0].PixelSpacing
# slices_thickess = slices[0].SliceThickness

# axial_aspect_ratio = pixel_spacing[1]/pixel_spacing[0]
# sagital_aspect_ratio = pixel_spacing[1]/slices_thickess
# coronal_aspect_ratio = slices_thickess/pixel_spacing[0]


img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))
volume3d=np.zeros(img_shape)

for i,s in enumerate(slices):
    array2D=s.pixel_array
    volume3d[:,:,i]= array2D


axial=plt.subplot(2,2,1)
plt.title("Axial")
sagital=plt.subplot(2,2,2)
plt.title("Sagital")
coronal=plt.subplot(2,2,3)
plt.title("Coronal")


axial.imshow(volume3d[:,:,img_shape[2]//2])
sagital.imshow(np.rot90(volume3d[:,img_shape[1]//2,:]))
coronal.imshow(np.rot90(volume3d[img_shape[0]//2,:,:]))
for z in range(volume3d.shape[2]):           
    axial.cla()                          
    axial.imshow(volume3d[:,:,z])
    plt.draw()
    plt.pause(0.01)  

for y in range(volume3d.shape[1]):           
    sagital.cla()                          
    sagital.imshow(np.rot90(volume3d[:,y,:]))
    plt.draw()
    plt.pause(0.01)    

for x in range(volume3d.shape[0]):           
    coronal.cla()                          
    coronal.imshow(np.rot90(volume3d[x,:,:]))
    plt.draw()
    plt.pause(0.01)                        

print(array2D.shape)
print(volume3d.shape)    



# # import matplotlib.pyplot as plt
# # import pydicom
# # import pydicom.data
  
# # # Full path of the DICOM file is passed in base
# # base = r"C:/Collage Materials\SENIOR-2 Year/Fall Semester 2022/Image Modalities/Project/VHF-Head/Head"
# # pass_dicom = "vhf.1505.dcm"  # file name is 1-12.dcm
  
# # # enter DICOM image name for pattern
# # # result is a list of 1 element
# # filename = pydicom.data.data_manager.get_files(base, pass_dicom)[0]
  
# # ds = pydicom.dcmread(filename)
  
# # plt.imshow(ds.pixel_array, cmap=plt.cm.bone)  # set the color map to bone
# # plt.show()



# import pydicom as dicom
# import numpy as np
# import matplotlib.pyplot as plt
# import os

# path = "C:/Collage Materials\SENIOR-2 Year/Fall Semester 2022/Image Modalities/Project/VHF-Head/Head"
# head_images = os.listdir(path)

# slices = [dicom.read_file(path + '/' + s, force= True) for s in head_images]

# slices = sorted(slices,key=lambda x:x.ImagePositionPatient[2])

# pixel_spacing = slices[0].PixelSpacing
# slices_thickess = slices[0].SliceThickness

# axial_aspect_ratio = pixel_spacing[1]/pixel_spacing[0]
# sagital_aspect_ratio = pixel_spacing[1]/slices_thickess
# coronal_aspect_ratio = slices_thickess/pixel_spacing[0]


# img_shape = list(slices[0].pixel_array.shape)
# img_shape.append(len(slices))
# volume3d=np.zeros(img_shape)


# for i,s in enumerate(slices):
#     array2D=s.pixel_array
#     volume3d[:,:,i]= array2D

# for i in range (1):
#   plt.imshow(volume3d[:,:,img_shape[2]//2])
#   plt.show()
#   plt.imshow(volume3d[:,img_shape[1]//2,:])
#   plt.show()
#   plt.imshow(volume3d[img_shape[0]//2,:,:].T)
#   plt.show()


# # axial=plt.subplot(2,2,1)
# # plt.title("Axial")
# # plt.imshow(volume3d[:,:,img_shape[2]//2])
# # axial.set_aspect(axial_aspect_ratio)

# # sagital=plt.subplot(2,2,2)
# # plt.title("Sagital")
# # plt.imshow(volume3d[:,img_shape[1]//2,:])
# # sagital.set_aspect(sagital_aspect_ratio)

# # coronal = plt.subplot(2,2,3)
# # plt.title("Coronal")
# # plt.imshow(volume3d[img_shape[0]//2,:,:].T)
# # coronal.set_aspect(coronal_aspect_ratio)


# plt.show()

# print(array2D.shape)
# print(volume3d.shape)    




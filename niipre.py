#!/usr/bin/python3
# 2018-10-30

# Vincent Koppelmans

# Read in Nifit image and display

# Packages
import nibabel as nb
import numpy as np
import os
import sys
from pathlib import Path
import matplotlib.pyplot

# Environment
home = str(Path.home())

# Set rounding
np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})

# Load in input file
iFile = sys.argv[1]
oFile=(str(os.path.basename(iFile).replace('.nii.gz','.png').replace('.nii','.png')))
image=nb.load(iFile)

# Load data
# 3D data
if image.header['dim'][0]==3:
    data=image.get_data()
    # 4D data
elif  image.header['dim'][0]==4:
    data=image.get_data()[:,:,:,0]

# Header
header=image.header
    
# Set NAN to 0
data[np.isnan(data)] = 0
    
# Plot main window
fig = matplotlib.pyplot.figure(
    facecolor='black',
    figsize=(5,4),
    dpi=200
)


# Set title
fig.canvas.set_window_title(oFile.replace('.png',''))
#matplotlib.pyplot.title(oFile.replace('.png',''))

# Spacing for Aspect Ratio
sX=header['pixdim'][1]
sY=header['pixdim'][2]
sZ=header['pixdim'][3]

# Sagittal
x=int(data.shape[0]/2)
a=fig.add_subplot(2,2,1)
imgplot = matplotlib.pyplot.imshow(
    np.rot90(data[x,:,:]),
    aspect=sZ/sY
)
imgplot.set_cmap('gray')
matplotlib.pyplot.axis('off')

# Coronal
y=int(data.shape[1]/2)
a=fig.add_subplot(2,2,2)
imgplot = matplotlib.pyplot.imshow(
    np.rot90(data[:,y,:]),
    aspect=sZ/sX
)
imgplot.set_cmap('gray')
matplotlib.pyplot.axis('off')

# Axial
z=int(data.shape[2]/2)
a=fig.add_subplot(2,2,3)
imgplot = matplotlib.pyplot.imshow(
    np.rot90(data[:,:,z]),
    aspect=sY/sX
)
imgplot.set_cmap('gray')
imgplot.axes.get_xaxis().set_ticks([])
imgplot.axes.get_yaxis().set_ticks([])
matplotlib.pyplot.ylabel(
    'R',
    {'color': 'red', 'fontsize': 10},
    rotation=0,
    labelpad = -2
)

# Textual information
# sform code
sform=np.round(image.get_sform(),decimals=2)
sform_txt=str(sform).replace('[',' ').replace(']',' ').replace(' ','   ').replace('   -','  -')

# qform code
qform=np.round(image.get_qform(),decimals=2)
qform_txt=str(qform).replace('[',' ').replace(']',' ').replace(' ','   ').replace('   -','  -')

# Dimensions
dims=str(data.shape).replace(', ',' x ').replace('(','').replace(')','')
dim=("Dimensions: "+dims)

# Spacing
spacing=("Spacing: "
         +str(np.round(sX, decimals=2))
         +" x "
         +str(np.round(sY, decimals=2))
         +" x "
         +str(np.round(sZ, decimals=2))
         +" mm"
)

# Data type
type=image.header.get_data_dtype()
type_str=("Data type: "+str(type))

# Volumes
volumes=("Volumes: "+str(image.header['dim'][4]))

# Range
min=np.round(np.amin(data), decimals=2)
max=np.round(np.amax(data), decimals=2)
range=("Range: "+str(min)+" - "+str(max))

text=(
    dim+"\n"
    +spacing+"\n"
    +volumes+"\n"
    +type_str+"\n"
    +range+"\n\n"
    +"sform code:\n"
    +sform_txt+"\n"
    +"\nqform code:\n"
    +qform_txt
)

# Plot text subplot
a=fig.add_subplot(2,2,4)
matplotlib.pyplot.text(
    0.15,
    0.95,
    text,
    horizontalalignment='left',
    verticalalignment='top',
    size=6,
    color='white',
)
matplotlib.pyplot.axis('off')


# Adjust whitespace
matplotlib.pyplot.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

# Display
#matplotlib.pyplot.show(block=False)
matplotlib.pyplot.show()


# Save
# fig.tight_layout(pad=0)
# matplotlib.pyplot.savefig(
#     home+"/"+oFile,
#     bbox_inches='tight',
#     facecolor=fig.get_facecolor(),
#     transparent=True
# )

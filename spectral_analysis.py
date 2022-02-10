# -*- coding: utf-8 -*-
import numpy
import pylab
from PIL import Image, ImageOps
import math


#importing the reference spectrum
im_ref = Image.open('led.JPG') #refernce spectrum (LED flash)
imref_g = ImageOps.grayscale(im_ref) #converts the LED spectrum to grayscale
 
#importing the exp spectrum
im_fing = Image.open('finger9.png') # Spectrum of the finger
im_fing_g = ImageOps.grayscale(im_fing) #coverts the finger spectrum to grayscale


gray_pixref=imref_g.load()
gray_pix_fing=im_fing_g.load()


#getting the sizes of the imgs (both spectra must be cropped to have the same width)

imref_width, imref_height=imref_g.size
imfing_width, imfing_height=im_fing_g.size

wl_offset=400.0 # wavelength start value for the spectra
wl_range=300.0 # wavelength range for the spectra
yref_bin=imref_height   # bin size for adding spectral intensity for each wavelength of ref
yfing_bin=imfing_height   # bin size for adding spectral intensity for each wavelength of exp

wl_p_pix=wl_range/imref_width

x_all=[]
y_all=[]

yref_all=[]


    
for i in range(0,imref_width):      
    xref_sum=0.0
    xfing_sum=0.0
    
    
    
    for j in range(0,yref_bin):   
        
              
            xref_sum+=gray_pixref[i,j] #provides the inetnsity of each pixel of the refernce spectra located at (i,j)
      
        
    for k in range(0,yfing_bin):   
        
              
            xfing_sum+=gray_pix_fing[i,k] #provides the inetnsity of each pixel of the finger spectrum located at (i,k)
          

    xref_sum=xref_sum/yref_bin #average intensity of a column of pixels (spectral line) of LED spectra
    
    yref_all.append(xref_sum)
    
    xfing_sum=xfing_sum/yfing_bin #average intensity of a column of pixels (spectral line) of finger spectra
    
    trans=xfing_sum/xref_sum #transmitted intensity of a given spectral line
    
    y_all.append(trans)
    
    x_all.append(i*wl_p_pix+wl_offset)
    

yref_all=numpy.array(yref_all,dtype='f')

y_max=max(y_all) #maximum absolute transmitted intensity value in the finger spectra

y_all=numpy.array(y_all,dtype='f')

index_max=numpy.where(y_all==max(y_all))  #returns the index with max intensity in finger spectrum array

index_max=numpy.array(index_max,dtype='i')

yref_max=yref_all[index_max[0]] #absolute intensity value in LED spectra of the wavelegth corresponding to index_max

y_normal=(y_all/yref_max)*100 #normlising the intensities in the finger spectrum (as a percentage)

index_max=index_max*wl_p_pix+wl_offset #returns the wavelength value with maximum transmittance


    
#pylab.plot(x_all, y_trans, c='red', linewidth=2.0)
cnt=0
while (cnt<=max(y_normal)):
        pylab.plot(index_max, [cnt], 'o',c='red')
        cnt=cnt+0.1
        

pylab.plot(x_all, y_normal, c='blue', linewidth=2.0)
pylab.xlabel('Wavelength (nm)', fontsize = 12)
pylab.ylabel('Normalised Transmitted Intensity', fontsize = 12)
pylab.title('Spectrum for SpO2= %', fontsize = 18,fontweight="bold")
pylab.annotate('Max-intensity wavelength=('+u"\u00B1"+'1) nm', xy=(index_max, max(y_normal)),xytext=(300, 0.20),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )
# =============================================================================
# pylab.savefig('Spectrum_abs.png',dpi=300)
# =============================================================================


import numpy as np
import scipy as sc
from scipy import ndimage
from scipy import misc

path = '../data/testing/'
lower_file = 'lower.JPG'
upper_file = 'upper.JPG'
split_file_template = '/strips/strip_{}.JPG'

print("Opening files...", end='')
lower = sc.ndimage.imread(path + lower_file)
upper = sc.ndimage.imread(path + upper_file)

sources = lower, upper
print("Done!")

print("Making a rainbow stripe for testing...", end='')
# Make a rainbow stripe for testing in just the upper image
# rgb cycle
# 100
# 110
# 010
# 011
# 001
# 101
n_rows = upper.shape[0]
n_div = 6
nd_rows = n_rows//n_div
slant = np.linspace(0, 255, num=nd_rows, endpoint=True)
high = 255*np.ones(nd_rows)
low = np.zeros(nd_rows) # accounts for odd length rows
low_odd = np.zeros(n_rows - (n_div-1)*nd_rows) # accounts for odd length rows
#           _         _
# channel =   \ _ _ /   
#             _ _
# channel = /     \ _ _
  #               _ _
# channel = _ _ /     \
channel = np.concatenate([high, slant[::-1], low, low_odd, slant[::1], high])


rgb = np.zeros((n_rows, 3))
rgb[:,0] = np.roll(channel, 0*nd_rows)
rgb[:,1] = np.roll(channel, 2*nd_rows)
rgb[:,2] = np.roll(channel, 4*nd_rows)

upper[:, 0:50, :] = rgb[:,np.newaxis,:]

print("Done!")

print("Splitting images...", end='')
strip_width = 45
strips = []
for source in sources:
    n_rows = source.shape[0]
    n_strips = n_rows // strip_width

    strips += np.array_split(source, n_strips, axis=0)


print("Done!")
print("{} strips created.".format(len(strips)))

print("Saving...", end='')
for id, strip in enumerate(strips):
    image = sc.misc.toimage(strip, channel_axis=2)
    sc.misc.imsave(path + split_file_template.format(id), image)
print("Done!")



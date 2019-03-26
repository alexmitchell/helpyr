import os
import re
import numpy as np
import scipy as sc
from scipy import ndimage
from scipy import misc

path = '../data/testing/'
source = path + 'strips/'
regex = re.compile


print("Opening files...", end='')
files = [f for f in os.listdir(source) if os.path.isfile(os.path.join(source,f))]
files_dict = {}
for name in files:
    image = sc.ndimage.imread(source + name)
    id = regex.findall(filename)
    files_dict
print("Done!")

"""
print(lower.shape, upper.shape)

upper[:, 0:50, :] = upper[:, 0:50, :]*0 + 255

print("Concatenating...", end='')
composite = np.concatenate([upper, lower], axis=0)
print("Done!")
print(composite.shape)

print("Saving...", end='')
image = sc.misc.toimage(composite, channel_axis=2)
sc.misc.imsave(composite_file, image)
print("Done!")
"""

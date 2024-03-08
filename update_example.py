# %% [markdown]
# ## Setup evnironment

# %%
import os
import numpy as np
import pandas as pd
import json
from skimage.io import imread

# %%
from psf import compute, plotPSF, plotAvg

# %% [markdown]
# ## Setup plotting

# %%
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
sns.set_context('paper', font_scale=2.0)
sns.set_style('ticks')

# %%
# from IPython.html.widgets import interactive
# from IPython.html.widgets import IntSliderWidget 
from ipywidgets import interact, fixed
import ipywidgets as widgets
from IPython.display import display

# %% [markdown]
# ## Define parameters

# %%
FOVumLat = 61.0
FOVpxLat = 512.0 # 512
pxPerUmLat = FOVpxLat/FOVumLat
pxPerUmAx = 2.0 # 2.0
wavelength = 970.0
NA = 0.6
windowUm = [12, 2, 2]
options = {'FOVumLat':FOVumLat, 'FOVpxLat':FOVpxLat, 'pxPerUmLat':FOVpxLat/FOVumLat, 'pxPerUmAx':pxPerUmAx, 'wavelength':970.0, 'NA':0.6, 'windowUm':windowUm}
options['thresh'] = .05

# %%
options

# %% [markdown]
# ## Get PSF

# %%
im = imread('./data/images.tif', plugin='tifffile')   

# %%
data, beads, maxima, centers, smoothed = compute(im, options)

# %%
PSF = pd.concat([x[0] for x in data])
PSF['Max'] = maxima
PSF = PSF.reset_index().drop(['index'],axis=1)
latProfile = [x[1] for x in data]
axProfile = [x[2] for x in data]

# %%
PSF

# %%
# print len(PSF)
# print PSF.mean()
# print PSF.std()
print(len(PSF))
print(PSF.mean())
print(PSF.std())

# %% [markdown]
# ## Plot max projection

# %%
plt.figure(figsize=(5,5));
plt.imshow(smoothed);
plt.plot(centers[:, 2], centers[:, 1], 'r.', ms=10);
plt.xlim([0, smoothed.shape[0]])
plt.ylim([smoothed.shape[1], 0])
plt.axis('off');

# %% [markdown]
# ## Plot max projection

# %%
beadInd = 1
average = beads[beadInd]

# %%
# plane = IntSliderWidget(min=0, max=average.shape[0]-1, step=1, value=average.shape[0]/2)
# interactive(plotAvg, i=plane)
interact(plotAvg, i=widgets.IntSlider(min=-(average.shape[0]-1), max=average.shape[0]-1, step=1, value=average.shape[0]/2), average = fixed(average));

# %% [markdown]
# ## Plot 2D slices

# %%
plt.imshow(average.mean(axis=0));
plt.axis('off');

# %%
plt.imshow(average.mean(axis=1), aspect = pxPerUmLat/pxPerUmAx);
plt.axis('off');

# %%
plt.imshow(average.mean(axis=2), aspect = pxPerUmLat/pxPerUmAx);
plt.axis('off');

# %% [markdown]
# ## Plotting

# %%
plotPSF(latProfile[beadInd][0],latProfile[beadInd][1],latProfile[beadInd][2],latProfile[beadInd][3],pxPerUmLat,PSF.Max.iloc[beadInd])

# %%
plotPSF(axProfile[beadInd][0],axProfile[beadInd][1],axProfile[beadInd][2],axProfile[beadInd][3],pxPerUmAx,PSF.Max.iloc[beadInd])



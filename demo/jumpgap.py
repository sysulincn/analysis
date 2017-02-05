'''
Created on 2017年1月29日

@author: linchengnan
'''
from matplotlib import pyplot as plt 
from matplotlib import scale as mscale 
from matplotlib import transforms as mtransforms 
from matplotlib import ticker as mticker 
import numpy as np 
 
class SegmentLocator(mticker.Locator): 
    def __init__(self, x, gap, nbins=5): 
        self.nbins = nbins 
        self.x = x 
        self.gap = gap 
        self.segments = [] 
        for segment in np.split(x, np.where(np.diff(x) > self.gap)[0]+1): 
            self.segments.append((segment[0], segment[-1])) 
             
    def __call__(self): 
        loc = [] 
        for vmin, vmax in self.segments: 
            nlocator = mticker.MaxNLocator(nbins=self.nbins) 
            loc.append(nlocator.bin_boundaries(vmin, vmax)) 
        locs = np.concatenate(loc) 
        return locs 
         
class SegmentTransform(mtransforms.Transform): 
   def __init__(self, x1, x2): 
       mtransforms.Transform.__init__(self) 
       self.x1 = x1 
       self.x2 = x2 
 
   def transform(self, a): 
       return np.interp(a, self.x1, self.x2) 
 
   def inverted(self): 
       return SegmentTransform(self.x2, self.x1) 
 
class SegmentScale(mscale.ScaleBase): 
   name = "segment" 
   def __init__(self, axis, **kwargs): 
       mscale.ScaleBase.__init__(self) 
       self.x1 = kwargs["x"] 
       self.gap = kwargs["gap"] 
       self.x2 = np.zeros_like(self.x1) 
       self.x2[1:] = np.diff(self.x1) 
       np.clip(self.x2[1:], 0, self.gap, self.x2[1:]) 
       np.cumsum(self.x2, out=self.x2) 
        
   def get_transform(self): 
       return SegmentTransform(self.x1, self.x2) 
 
   def set_default_locators_and_formatters(self, axis): 
       axis.set_major_locator(SegmentLocator(self.x1, self.gap)) 
 
mscale.register_scale(SegmentScale) 
 
x = np.r_[np.arange(0, 10, 0.1), np.arange(50, 70, 0.1), np.arange(100, 120, 0.1)] 
y = np.sin(x) 
 
pos = np.where(np.abs(np.diff(x))>1.0)[0]+1 
x2 = np.insert(x, pos, np.nan) 
y2 = np.insert(y, pos, np.nan) 
 
plt.plot(x2, y2) 
plt.xscale("segment", x=x, gap=2.0) 
plt.xlim(0, 120) 
ax = plt.gca() 
xlabels = ax.get_xticklabels() 
for label in xlabels: 
    label.set_rotation(45) 
plt.show()
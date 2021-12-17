import numpy as np
from PIL import Image

###########################
# USER EDITABLE CONSTANTS #
###########################

#How many iterations to do from the basic star.
ITERATIONS = 3

#How much to scale the input images.
SCALING = 0.25

#image files for kites and darts.
#make sure they're exactly the same size as kite_mask.png and dart_mask.png
KITE_IMAGE = "kite_mask.png"
DART_IMAGE = "dart_mask.png"

#where to save the image!
OUT_FILE = "example_generated_2.png"

###########################

PHI = np.sqrt(5)/2 - 0.5 #this is "small phi", about 0.61

class PenroseTile:
    def __init__(self, a,b,c, right):
        '''a,b,c are 2d vectors, side is left=False, right=True'''
        self.a = a
        self.b = b
        self.c = c
        self.right = right
    
    def __repr__(self):
        return f"{str(self.__class__).split('.')[-1][:-2]}(a=({self.a[0]:.2f},{self.a[1]:.2f}), b=({self.b[0]:.2f},{self.b[1]:.2f}),c=({self.c[0]:.2f},{self.c[1]:.2f}), right={self.right})"
        
    def inflate(self):
        pass

class HalfKite(PenroseTile):
    def __init__(self, a, b, c, right):
        super().__init__(a,b,c,right)
        self.kind = "kite"
    
    def inflate(self):
        self.d = PHI*self.c + (1-PHI)* self.a
        self.e = PHI*self.a + (1-PHI)* self.b
        return (
            HalfKite(self.b,self.c,self.d,self.right),
            HalfKite(self.b,self.e,self.d,not self.right),
            HalfDart(self.a,self.d,self.e,not self.right)
        )
    
class HalfDart(PenroseTile):
    def __init__(self, a, b, c, right):
        super().__init__(a,b,c,right)
        self.kind = "dart"
        
    def inflate(self):
        self.f = PHI*self.b + (1-PHI)*self.a
        return (
            HalfDart(self.b,self.c,self.f,self.right),
            HalfKite(self.a, self.f,self.c,self.right)
        )


def zeta(a):
    return np.array([np.cos(a*np.pi/5),np.sin(a*np.pi/5)])

d=[HalfKite(np.zeros(2),zeta(2*i+1), zeta(2*i), True) for i in range(5)] + [HalfKite(np.zeros(2),zeta(2*i+1), zeta(2*i+2), False) for i in range(5)]

for i in range(ITERATIONS):
    d=[i for t in d for i in t.inflate()]

coords = {tuple(i) for t in d for i in (t.a,t.b,t.c)}
x_min_raw, x_max_raw, y_min_raw, y_max_raw = (
    min(i[0] for i in coords),
    max(i[0] for i in coords),
    min(i[1] for i in coords),
    max(i[1]for i in coords)
)

dart = Image.open(DART_IMAGE)
w_dart_raw, h_dart_raw = dart.size

dart = dart.resize((int(w_dart_raw*SCALING),int(h_dart_raw*SCALING)))

w_dart,h_dart = dart.size

long = np.sqrt(w_dart**2/4 + h_dart**2)
short = PHI*long

tile_block_size = int(long+1)*2

dart_template = Image.new("RGBA",(tile_block_size,tile_block_size))

dart_template.paste(dart,((tile_block_size-w_dart)//2,tile_block_size//2))

kite = Image.open("kite_mask.png")
w_kite_raw, h_kite_raw = kite.size

kite = kite.resize((int(w_kite_raw*SCALING),int(h_kite_raw*SCALING)))
w_kite,h_kite = kite.size
kite_template = Image.new("RGBA",(tile_block_size,tile_block_size))
kite_template.paste(kite,((tile_block_size-w_kite)//2,tile_block_size//2))

long_raw = np.sqrt(((d[0].a-d[0].b)**2).sum())
scaling_factor = long/long_raw

canvas_w = int((x_max_raw-x_min_raw)*scaling_factor+2*long+10)
canvas_h = int((y_max_raw-y_min_raw)*scaling_factor+2*long+10)
top_corner = np.array(x_min_raw, y_min_raw)

canvas = Image.new("RGBA",(canvas_w, canvas_h))

for t in d:
    if t.right:
        angle = np.rad2deg(np.arctan2(*(t.c-t.a)))
        if t.kind == "kite":
            temp_tile = kite_template.copy()
        else:
            temp_tile = dart_template.copy()
        temp_tile = temp_tile.rotate(round(angle))
        position = (t.a - top_corner) * scaling_factor
        canvas.paste(temp_tile, tuple(position.astype(int)), temp_tile)

canvas.save(OUT_FILE)
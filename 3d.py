import math

tmatrix = [[0 for x in range(4)] for x in range(4)]
ematrix = [[] for x in range(4)]
pixels = []
s = []
pixelx = 0
pixely = 0
color = [255,255,255]

def mult(a,b):
    m = [[0 for x in range(len(b[0]))] for y in range(len(a))]
    for x in range(len(a)):
        for y in range(len(b[0])):
            for z in range(len(b)):
                m[x][y] += a[x][z]*b[z][y]
    return m

def drawLine(a,b,c,d):
    global pixels
    if a == c and b == d:
        for i in range(3):
            pixels[a][b][i] = color[i]
        return 1
    if abs(a-c) > abs(b-d):
        x1 = min(a,c)
        x2 = max(a,c)
        if x1 == a:
            y1 = b
            y2 = d
        else:
            y1 = d
            y2 = b
        x_major(x1,y1,x2,y2)
    else:
        y1 = min(b,d)
        y2 = max(b,d)
        if y1 == b:
            x1 = a
            x2 = c
        else:
            x1 = c
            x2 = a
        y_major(x1,y1,x2,y2)
    return 1

def x_major(x1,y1,x2,y2):
    global pixels
    delta_x = x2-x1
    delta_y = y2-y1
    x = x1
    y = y1
    count = 0
    for i in range(3):
        pixels[x][y][i] = color[i]
    while (x < x2):
        x += 1
        count += abs(delta_y)
        if count >= delta_x:
            if delta_y > 0:
                y += 1
            else:
                y -= 1
            count -= delta_x
        for i in range(3):
            pixels[x][y][i] = color[i]

def y_major(x1,y1,x2,y2):
    global pixels
    delta_x = x2-x1
    delta_y = y2-y1
    x = x1
    y = y1
    count = 0
    for i in range(3):
        pixels[x][y][i] = color[i]
    while (y < y2):
        y += 1
        count += abs(delta_x)
        if count >= delta_y:
            if delta_x > 0:
                x += 1
            else:
                x -= 1
            count -= delta_y
        for i in range(3):
            pixels[x][y][i] = color[i]

def lines(x1,y1,z1,x2,y2,z2):
    ematrix[0].append(x1)
    ematrix[0].append(x2)
    ematrix[1].append(y1)   
    ematrix[1].append(y2)
    ematrix[2].append(z1)
    ematrix[2].append(z2)
    ematrix[3].append(1)
    ematrix[3].append(1)

def sphere(r,cx,cy,cz):
    a = math.pi/10
    b = len(ematrix[0])
    for phi in range(21):
        for theta in range(11):
            for i in range(2):
                ematrix[0].append(r*math.cos(theta*a)+cx)
                ematrix[1].append(r*math.sin(theta*a)*math.cos(phi*a)+cy)
                ematrix[2].append(r*math.sin(theta*a)*math.sin(phi*a)+cz)
                ematrix[3].append(1)
    c = len(ematrix[0])-1
    ematrix[0].pop(c)
    ematrix[0].pop(b)
    ematrix[1].pop(c)
    ematrix[1].pop(b)
    ematrix[2].pop(c)
    ematrix[2].pop(b)
    ematrix[3].pop(c)
    ematrix[3].pop(b)

def identity():
    global tmatrix
    tmatrix = [[1 if y==x else 0 for y in range(4)] for x in range(4)]

def move(p,q,r):
    global tmatrix
    a = [[1 if y==x else 0 for y in range(4)] for x in range(4)]
    a[0][3] = p
    a[1][3] = q
    a[2][3] = r
    tmatrix = mult(a,tmatrix)

def scale(p,q,r):
    global tmatrix
    a = [[1 if y==x else 0 for y in range(4)] for x in range(4)]
    a[0][0] = p
    a[1][1] = q
    a[2][2] = r
    tmatrix = mult(a,tmatrix)

def rotateX(d):
    global tmatrix
    theta = math.radians(d)
    a = [[1 if y==x else 0 for y in range(4)] for x in range(4)]
    a[1][1] = math.cos(theta)
    a[1][2] = -1*math.sin(theta)
    a[2][1] = math.sin(theta)
    a[2][2] = math.cos(theta)
    tmatrix = mult(a,tmatrix)
    
def rotateY(d):
    global tmatrix
    theta = math.radians(d)
    a = [[1 if y==x else 0 for y in range(4)] for x in range(4)]
    a[0][0] = math.cos(theta)
    a[0][2] = -1*math.sin(theta)
    a[2][0] = math.sin(theta)
    a[2][2] = math.cos(theta)
    tmatrix = mult(a,tmatrix)

def rotateZ(d):
    global tmatrix
    theta = math.radians(d)
    a = [[1 if y==x else 0 for y in range(4)] for x in range(4)]
    a[0][0] = math.cos(theta)
    a[0][1] = -1*math.sin(theta)
    a[1][0] = math.sin(theta)
    a[1][1] = math.cos(theta)
    tmatrix = mult(a,tmatrix)

def screen(x1,y1,x2,y2):
    global s
    s = [x1,y1,x2,y2]

def pixel(x,y):
    global pixelx,pixely,pixels
    pixelx = x
    pixely = y
    pixels = [[[0,0,0] for i in range(pixelx)] for j in range(pixely)]

def transform():
    global tmatrix, ematrix
    ematrix = mult(tmatrix,ematrix)

def renderParallel():
    for i in range(0,len(ematrix[0]),2):
        x1 = int((pixelx/(s[2]-s[0]))*(ematrix[0][i]-s[0]))
        y1 = int((pixely/(s[3]-s[1]))*(ematrix[1][i]-s[1]))
        x2 = int((pixelx/(s[2]-s[0]))*(ematrix[0][i+1]-s[0]))
        y2 = int((pixely/(s[3]-s[1]))*(ematrix[1][i+1]-s[1]))
        drawLine(x1,y1,x2,y2)

def renderCyclops(x,y,z):
    for i in range(0,len(ematrix[0]),2):
        x1 = (0-z)*(ematrix[0][i]-x)/(ematrix[2][i]-z)+x
        y1 = (0-z)*(ematrix[1][i]-y)/(ematrix[2][i]-z)+y
        x2 = (0-z)*(ematrix[0][i+1]-x)/(ematrix[2][i+1]-z)+x
        y2 = (0-z)*(ematrix[1][i+1]-y)/(ematrix[2][i+1]-z)+y
        x1 = int((pixelx/(s[2]-s[0]))*(x1-s[0]))
        y1 = int((pixely/(s[3]-s[1]))*(y1-s[1]))
        x2 = int((pixelx/(s[2]-s[0]))*(x2-s[0]))
        y2 = int((pixely/(s[3]-s[1]))*(y2-s[1]))
        drawLine(x1,y1,x2,y2)

def renderStereo(xl,yl,zl,xr,yr,zr):
    global color
    color = [255,0,0]
    renderCyclops(xl,yl,zl)
    color = [0,255,255]
    renderCyclops(xr,yr,zr)
    color = [255,255,255]
    
def clearEdges():
    global ematrix
    ematrix = [[] for x in range(4)]

def clearPixels():
    global pixels
    pixels = [[[0,0,0] for x in range(pixelx)] for y in range(pixely)]

def File(fn):
    f = open(fn, 'w')
    f.write('P3\n'+str(pixelx)+" "+str(pixely)+'\n255\n')
    for x in range(pixelx):
        for y in range(pixely):
            for i in range(3):
                f.write(str(pixels[y][x][i])+' ')
            f.write('\n')
    f.close()

def inputs(i):
    try:
        f = open(i,'r')
    except:
        return "File could not be opened"
    for line in f:
        x = line.split()
        if x[0] == '#':
            pass
        elif x[0] == 'end':
            break
        elif x[0] == 'line':
            lines(float(x[1]),float(x[2]),float(x[3]),float(x[4]),float(x[5]),float(x[6]))
        elif x[0] == 'sphere':
            sphere(float(x[1]),float(x[2]),float(x[3]),float(x[4]))
        elif x[0] == 'identity':
            identity()
        elif x[0] == 'move':
            move(float(x[1]),float(x[2]),float(x[3]))
        elif x[0] == 'scale':
            scale(float(x[1]),float(x[2]),float(x[3]))
        elif x[0] == 'rotate-x':
            rotateX(float(x[1]))
        elif x[0] == 'rotate-y':
            rotateY(float(x[1]))
        elif x[0] == 'rotate-z':
            rotateZ(float(x[1]))
        elif x[0] == 'screen':
            screen(float(x[1]),float(x[2]),float(x[3]),float(x[4]))
        elif x[0] == 'pixels':
            pixel(int(x[1]),int(x[2]))
        elif x[0] == 'transform':
            transform()
        elif x[0] == 'render-parallel':
            renderParallel()
        elif x[0] == 'render-perspective-cyclops':
            renderCyclops(float(x[1]),float(x[2]),float(x[3]))
        elif x[0] == 'render-perspective-stereo':
            renderStereo(float(x[1]),float(x[2]),float(x[3]),float(x[4]),float(x[5]),float(x[6]))
        elif x[0] == 'clear-edges':
            clearEdges()
        elif x[0] == 'clear-pixels':
            clearPixels()
        elif x[0] == 'file':
            File(x[1])
        else:
            return "Unknown command"
    f.close()

inputs('test.txt')

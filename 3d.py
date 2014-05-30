import math

#transformation matrix
tmatrix = [[0 for x in range(4)] for x in range(4)]
#edge matrix
ematrix = [[] for x in range(4)]
#pixel values
pixels = []
#screen
s = []
#pixel screen lengths
pixelx = 0
pixely = 0
#color of pixel
color = [255,255,255]
#frame number
f = 1
#start and end frame
frame1 = 0
frame2 = 0
#repeat?
r = True
#dictionary of variables
varies = {}

#multiply matrices
def mult(a,b):
    m = [[0 for x in range(len(b[0]))] for y in range(len(a))]
    for x in range(len(a)):
        for y in range(len(b[0])):
            for z in range(len(b)):
                m[x][y] += a[x][z]*b[z][y]
    return m

#line drawing
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

#helper function depending on which major
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

#add a line into the edge matrix
def lines(x1,y1,z1,x2,y2,z2):
    ematrix[0].append(x1)
    ematrix[0].append(x2)
    ematrix[1].append(y1)   
    ematrix[1].append(y2)
    ematrix[2].append(z1)
    ematrix[2].append(z2)
    ematrix[3].append(1)
    ematrix[3].append(1)

#add a point from matrix b into a
def add(a,b,n):
    a[0].append(b[0][n])
    a[1].append(b[1][n])
    a[2].append(b[2][n])
    a[3].append(b[3][n])
    return a

#checks if the xth triangle in the edge matrix is front facing
def backface(x1,y1,z1,x2,y2,z2,x3,y3,z3):
    view = [0,0,-1]
    a = [0,0,0]
    b = [0,0,0]
    n = [0,0,0]
    d = [0,0,0]
    a[0] = x1-x2
    a[1] = y1-y2
    a[2] = z1-z2
    b[0] = x1-x3
    b[1] = y1-y3
    b[2] = z1-z3
    n[0] = a[1]*b[2]-a[2]*b[1]
    n[1] = a[2]*b[0]-a[0]*b[2]
    n[2] = a[0]*b[1]-a[1]*b[0]
    d[0] = n[0]*view[0]
    d[1] = n[1]*view[1]
    d[2] = n[2]*view[2]
    return d[0]+d[1]+d[2] < 0

#returns value for given frame
def vary(beg,end,f1,f2):
    global f
    if f <= f2 and f >= f1: 
        return (end - beg) / (f2 - f1 + 1) * f + beg
    else:
        return False

#calls vary function with values from stored command if needed
#don't worry about the messiness
#I was trying to make it so that things could change direction
def animation(points, args):
    global f
    for i in range(9):
        try:
            args[i] = float(args[i])
        except:
            j = 0
            v = varies[args[i]]
            while j < len(varies[args[i]]):
                beg = v[j][2]
                end = v[j][3]
                if f <= end and f >= beg:
                    break
                else:
                    j += 1
            if f >= v[j][2] and f <= v[j][3]:
                args[i] = vary(v[j][0],v[j][1], v[j][2],v[j][3])
                if isinstance(args[i],bool):
                    return False
            else:
                return False
    scale(args[0],args[1],args[2])
    rotateX(args[3])
    rotateY(args[4])
    rotateZ(args[5])
    move(args[6],args[7],args[8])
    points = mult(tmatrix,points)
    identity()
    return points

#import
def imp(fn, args):
    points = [[],[],[],[]]
    try:
        F = open(fn,'r')
    except:
        return "import file not found"
    for line in F:
        count = 0
        x = line.split()
        if x[0] is not "#" and len(x) > 1:
            for point in x:
                points[count].append(float(point))
                count += 1
                if count >= 3:
                    count = 0
                    points[3].append(1)
    points = animation(points,args)
    if not isinstance(points, bool):
        for i in range(0,len(points[0]),3):
            drawTri(points,i)

#box with triangular tesselation
def boxT(args):
    box = [[.5,.5,-.5,-.5,.5,.5,-.5,-.5],
           [.5,-.5,-.5,.5,.5,-.5,-.5,.5],
           [.5,.5,.5,.5,-.5,-.5,-.5,-.5],
           [1,1,1,1,1,1,1,1]]
    box = animation(box,args)
    if not isinstance(x,bool):
        tri = [[],[],[],[]]
        #front
        tri = add(tri,box,0)
        tri = add(tri,box,3)
        tri = add(tri,box,1)
        tri = add(tri,box,3)
        tri = add(tri,box,2)
        tri = add(tri,box,1)
        #left
        tri = add(tri,box,3)
        tri = add(tri,box,7)
        tri = add(tri,box,2)
        tri = add(tri,box,7)
        tri = add(tri,box,6)
        tri = add(tri,box,2)
        #top
        tri = add(tri,box,7)
        tri = add(tri,box,3)
        tri = add(tri,box,0)
        tri = add(tri,box,4)
        tri = add(tri,box,7)
        tri = add(tri,box,0)
        #back
        tri = add(tri,box,4)
        tri = add(tri,box,6)
        tri = add(tri,box,7)
        tri = add(tri,box,6)
        tri = add(tri,box,4)
        tri = add(tri,box,5)
        #bottom
        tri = add(tri,box,6)
        tri = add(tri,box,5)
        tri = add(tri,box,2)
        tri = add(tri,box,5)
        tri = add(tri,box,1)
        tri = add(tri,box,2)
        #right
        tri = add(tri,box,5)
        tri = add(tri,box,0)
        tri = add(tri,box,1)
        tri = add(tri,box,0)
        tri = add(tri,box,5)
        tri = add(tri,box,4)
        for i in range(0,len(tri[0]),3):
            drawTri(tri,i)

#sphere with triangular tesselation
def sphereT(args):
    a = math.pi/10
    sphere = [[],[],[],[]]
    tri = [[],[],[],[]]
    for phi in range(21):
        for theta in range(11):
            sphere[0].append(.5*math.cos(theta*a))
            sphere[1].append(.5*math.sin(theta*a)*math.cos(phi*a))
            sphere[2].append(.5*math.sin(theta*a)*math.sin(phi*a))
            sphere[3].append(1)
    sphere = animation(sphere,args)
    if not isinstance(sphere,bool):
        l = len(sphere[0])
        for i in range(l):
            if i%11 != 10:
                tri = add(tri,sphere,i)
                tri = add(tri,sphere,(i+1)%l)
                tri = add(tri,sphere,(i+12)%l)
                tri = add(tri,sphere,i)
                tri = add(tri,sphere,(i+12)%l)
                tri = add(tri,sphere,(i+11)%l)
        for i in range(0,len(tri[0]),3):
            drawTri(tri,i)

#draws a triangle given a matrix and the starting index of the first line
def drawTri(tri,n):
    global ematrix
    ematrix = add(ematrix,tri,n)
    ematrix = add(ematrix,tri,n+1)
    ematrix = add(ematrix,tri,n+1)
    ematrix = add(ematrix,tri,n+2)
    ematrix = add(ematrix,tri,n+2)
    ematrix = add(ematrix,tri,n)

#probably non-working sphere code (without triangular tesselation)
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

#makes the transformtion matrix the identity matrix
def identity():
    global tmatrix
    tmatrix = [[1 if y==x else 0 for y in range(4)] for x in range(4)]

#multiples a move matrix into the transformation matrix
def move(p,q,r):
    global tmatrix
    a = [[1 if y==x else 0 for y in range(4)] for x in range(4)]
    a[0][3] = p
    a[1][3] = q
    a[2][3] = r
    tmatrix = mult(a,tmatrix)

#multiples a scale matrix into the transformation matrix
def scale(p,q,r):
    global tmatrix
    a = [[1 if y==x else 0 for y in range(4)] for x in range(4)]
    a[0][0] = p
    a[1][1] = q
    a[2][2] = r
    tmatrix = mult(a,tmatrix)

#multiplies a rotation matrix into the transformation matrix
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

#changes the screen size
def screen(x1,y1,x2,y2):
    global s
    s = [x1,y1,x2,y2]

#creates pixel array
def pixel(x,y):
    global pixelx,pixely,pixels
    pixelx = x
    pixely = y
    pixels = [[[0,0,0] for i in range(pixelx)] for j in range(pixely)]

#multiplies the transformation matrix into the edge matrix
#does not reset the transformation matrix
def transform():
    global tmatrix, ematrix
    ematrix = mult(tmatrix,ematrix)
    identity()

#renders
def renderParallel():
    for i in range(0,len(ematrix[0]),6):
        x1 = int((pixelx/(s[2]-s[0]))*(ematrix[0][i]-s[0]))
        y1 = int((pixely/(s[3]-s[1]))*(ematrix[1][i]-s[1]))
        x2 = int((pixelx/(s[2]-s[0]))*(ematrix[0][i+1]-s[0]))
        y2 = int((pixely/(s[3]-s[1]))*(ematrix[1][i+1]-s[1]))
        x3 = int((pixelx/(s[2]-s[0]))*(ematrix[0][i+3]-s[0]))
        y3 = int((pixely/(s[3]-s[1]))*(ematrix[1][i+3]-s[1]))
        if backface(x1,y1,ematrix[2][i],x2,y2,ematrix[2][i+1],x3,y3,ematrix[2][i+3]):
            drawLine(x1,y1,x2,y2)
            drawLine(x2,y2,x3,y3)
            x4 = int((pixelx/(s[2]-s[0]))*(ematrix[0][i+5]-s[0]))
            y4 = int((pixely/(s[3]-s[1]))*(ematrix[1][i+5]-s[1]))
            drawLine(x3,y3,x4,y4)
def renderCyclops(x,y,z):
    for i in range(0,len(ematrix[0]),6):
        x1 = (0-z)*(ematrix[0][i]-x)/(ematrix[2][i]-z)+x
        y1 = (0-z)*(ematrix[1][i]-y)/(ematrix[2][i]-z)+y
        x2 = (0-z)*(ematrix[0][i+1]-x)/(ematrix[2][i+1]-z)+x
        y2 = (0-z)*(ematrix[1][i+1]-y)/(ematrix[2][i+1]-z)+y
        x1 = int((pixelx/(s[2]-s[0]))*(x1-s[0]))
        y1 = int((pixely/(s[3]-s[1]))*(y1-s[1]))
        x2 = int((pixelx/(s[2]-s[0]))*(x2-s[0]))
        y2 = int((pixely/(s[3]-s[1]))*(y2-s[1]))
        x3 = (0-z)*(ematrix[0][i+3]-x)/(ematrix[2][i+3]-z)+x
        y3 = (0-z)*(ematrix[1][i+3]-y)/(ematrix[2][i+3]-z)+y
        x3 = int((pixelx/(s[2]-s[0]))*(x3-s[0]))
        y3 = int((pixely/(s[3]-s[1]))*(y3-s[1]))
        if backface(x1,y1,ematrix[2][i],x2,y2,ematrix[2][i+1],x3,y3,ematrix[2][i+3]):
            drawLine(x1,y1,x2,y2)
            drawLine(x2,y2,x3,y3)
            x4 = (0-z)*(ematrix[0][i+5]-x)/(ematrix[2][i+5]-z)+x
            y4 = (0-z)*(ematrix[1][i+5]-y)/(ematrix[2][i+5]-z)+y
            x4 = int((pixelx/(s[2]-s[0]))*(x4-s[0]))
            y4 = int((pixely/(s[3]-s[1]))*(y4-s[1]))
            drawLine(x3,y3,x4,y4)
def renderStereo(xl,yl,zl,xr,yr,zr):
    global color
    color = [255,0,0]
    renderCyclops(xl,yl,zl)
    color = [0,255,255]
    renderCyclops(xr,yr,zr)
    color = [255,255,255]

#clears the edge matrix
def clearEdges():
    global ematrix
    ematrix = [[] for x in range(4)]

#clears the pixel array
def clearPixels():
    global pixels
    pixels = [[[0,0,0] for x in range(pixelx)] for y in range(pixely)]

#writes a ppm file from the pixel array
def File(fn):
    global f, frame1, frame2
    if f <= frame2 and f >= frame1:
        if f < 10:
            fn += "00" + str(f) + ".ppm"
        elif f < 100:
            fn += "0" + str(f) + ".ppm"
        else:
            fn += ".ppm"
        F = open(fn, 'w')
        F.write('P3\n'+str(pixelx)+" "+str(pixely)+'\n255\n')
        for x in range(pixelx):
            for y in range(pixely):
                for i in range(3):
                    F.write(str(pixels[y][x][i])+' ')
                F.write('\n')
        F.close()

#takes in inputs from the command file
def inputs(i):
    global r,f,frame1,frame2
    while r:
        try:
            F = open(i,'r')
        except:
            return "File could not be opened"
        for line in F:
            x = line.split()
            if x[0] == '#':
                pass
            elif x[0] == 'end':
                break
            elif x[0] == 'line':
                lines(float(x[1]),float(x[2]),float(x[3]),float(x[4]),float(x[5]),float(x[6]))
            elif x[0] == 'frames':
                frame1 = int(x[1])
                frame2 = int(x[2])
                if f == 1:
                    f = frame1
            elif x[0] == 'box-t':
                boxT([x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]])
            elif x[0] == 'sphere-t':
                sphereT([x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]])
            #elif x[0] == 'sphere':
            #    sphere(float(x[1]),float(x[2]),float(x[3]),float(x[4]))
            elif x[0] == 'import':
                imp(x[1],[x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10]])
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
            elif x[0] == 'vary':
                try:
                    varies[x[1]].append([float(x[2]),float(x[3]),float(x[4]),float(x[5])])
                except:
                    varies[x[1]] = [[float(x[2]),float(x[3]),int(x[4]),int(x[5])]]
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
        F.close()
        clearEdges()
        clearPixels()
        identity()
        f += 1
        r = f <= frame2

inputs('test.txt')

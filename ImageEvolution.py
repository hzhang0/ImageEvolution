import os, sys
from PIL import Image, ImageDraw
from random import randint, uniform, choice, shuffle

inputPath= 'picture.jpg'
outputPath = 'altered.png'

def evolveImage():
    """Given an image, returns an altered version of the image"""
    img = readImage(inputPath)
    width, height = img.size    
        
def readImage(path):
    """Returns a PIL image object given a path."""
    return Image.open(path)

def saveImage(img):
    """Given a PIL image, saves it to disk."""
    img.save(outputPath)

def initializePopulation(x,y):
    """Input: x,y dimensions
        Output: An initial population.
        Each individual is a list of four lists.
        The first three lists are [x,y] coordinates.
        The fourth list corresponds to a [R,G,B] color."""
    pop = []
    numPop = (int)((x*y)**(0.5))
    for i in range(numPop):
        pop.append(randomTri(x,y))
    curImg = popToImage(x,y,pop)
    size = 0.3
    offset= 0.3
    tri = Image.new('RGBA', (x, y)) 
    draw = ImageDraw.Draw(curImg)
    draw_tri = ImageDraw.Draw(tri)
    for i in range(x):
        for j in range(y):
            pixel = curImg.getpixel((i,j))
            if pixel == (255,255,255,255):
                c1 = [max((int)(-offset*x), (int)(i-size*x)), j]
                c2 = [i,max((int)(-offset*y), (int)(j-size*y))]
                c3 = [min((int)(x*(1+offset)), (int)(i+size*x)), j]
                A = [randint(c1[0],c2[0]), randint(c2[1],c1[1])]
                B = [randint(c2[0],c3[0]), randint(c2[1],c3[1])]
                C = [i, randint(j+1, min((int)(j+size*y), (int)(y*(1+offset))))]
                RGBA = [randint(0,255),randint(0,255),randint(0,255),randint(130,255)]
                pop.append([A,B,C,RGBA])
                draw_tri.polygon([(0, 0), (0, y), (x, y), (x, 0)], fill = (255,255,255,0))
                draw_tri.polygon([tuple(A),tuple(B),tuple(C)], fill=tuple(RGBA))
                curImg = Image.alpha_composite(curImg, tri)                
    return pop

def popToImage(x,y,population):
    """Input: x,y dimensions, the whole population
        Output: a PIL image object created by overlaying
        individuals triangles on top of each other and mixing the
        RGB color values.
        population is a list and has items in the form of [(x1,y1),(x2,y2),(x3,y3),(r,b,g,a)]"""
    num_pop = len(population)
    img = Image.new('RGBA', (x, y)) # Use RGBA
    tri = Image.new('RGBA', (x, y)) # Use RGBA
    #creates draw object for background and triangles
    draw = ImageDraw.Draw(img)
    draw_tri = ImageDraw.Draw(tri)

    draw.polygon([(0, 0), (0, y), (x, y), (x, 0)], fill = (255,255,255,255)) #draws a white background
    
    for i in range(num_pop):
        draw_tri.polygon([(0, 0), (0, y), (x, y), (x, 0)], fill = (255,255,255,0)) #update the triangle to a blank canvas
        draw_tri.polygon([tuple(population[i][0]),tuple(population[i][1]),tuple(population[i][2])], fill=tuple(population[i][3]))
        img = Image.alpha_composite(img, tri)
        
    return img

def evaluation(population, img, imgAltered):
    """Input: the entire population, the original image, an altered image
        Output: a list of length len(population), composed of
        floats between 0 and 100, where 0 is the least fit,
        and 100 is the most fit.
        population is a list and has items in the form of [(x1,y1),(x2,y2),(x3,y3),(r,g,b,a)]
        returns a tuple, tuple[0] is the list of scores for each triangles, tuple[1] is the over score of the picture"""

    scores = [0]*len(population)
    accuracy = 85 #this is in % of how accurate the colours should be
    total = 0
    steps = 4
    
    #creates pixel access objects
    pixel_alter = imgAltered.load()
    pixel_ori = img.load()

    #loops through each pixels to assign score 0 or 1 to that pixel
    for i in range(1,width,steps):
        for j in range(1,height,steps):
            pixo = pixel_ori[i,j]
            pixa = pixel_alter[i,j]
            #this is in percent how accurate this pixel is to the original
            percent = (1 - (abs(pixo[0]-pixa[0])+abs(pixo[1]-pixa[1])+abs(pixo[2]-pixa[2]))/765.0)*100
            
            total += percent
            
            if percent >= accuracy:
                #loops through the population to find triangles that has this pixel
                for k in range(len(population)):
                    if inTriangle([i,j],population[k]):
                        scores[k] += 1
        
    hi = max(scores)
    for i in range(len(scores)):
        scores[i] /= float(hi)
        scores[i] *= 100
        scores[i] = int(scores[i])

    total /= (width/steps)*(height/steps)
    return scores, total

def crossover(population, scores):
    """Input: the entire population
        Output: a population list with length longer than the input"""
    newTri = []
    ch = population[scores.index(min(scores))]
    vertices = ch[0:3]
    shuffle(vertices)
    newPoint = midpoint(vertices[1], vertices[2])
    newTri.append(vertices[0])
    newTri.append(vertices[1])
    newTri.append(newPoint)
    ch[0], ch[1], ch[2] = vertices[0], newPoint, vertices[2]
    newTri.append(ch[3])
    population.append(newTri)
    return population
    
    
def mutation(width, height, population, scores):
    """Input: the entire population
        Output: a population list with some random properties of
        some of the individuals altered."""
    dist = 0.1
    numMutations = randint(len(population)/3, len(population))
    weights = [100-i for i in scores]    
    for i in range(numMutations):
        index = weightedRandom(population,scores)
        ch = choice(population[index])
        if len(ch)==2:
            ch[0] = ch[0] + (int)(uniform(-dist*width, dist*width))
            ch[1] = ch[0] + (int)(uniform(-dist*height, dist*height))
        elif len(ch)==3:
            ch[0], ch[1], ch[2], ch[3] = randint(0,255),randint(0,255),randint(0,255),randint(130,255)
    return population

#utility functions
def randomTri(width,height):
    """
    given height and width of image, generate a triangle with size relative to the dimensions
    """
    offset = 0.3
    size = 0.6
    A = [randint((int)(-width*offset), (int)(width*(1+offset))),randint((int)(-height*offset), (int)(height*(1+offset)))]
    c1 = [max((int)(A[0]-size*width),(int)(-width*offset)), max((int)(A[1]-size*height),(int)(-height*offset))]
    c2 = [min((int)(A[0]+size*width), (int)(width*(1+offset))), min((int)(A[1]+size*height), (int)(height*(1+offset)))]
    B =  [randint(c1[0],c2[0]), randint(c1[1],c2[1])]
    c3 = [min((int)(B[0]+size*width), (int)(width*(1+offset))), min((int)(B[1]+size*height), (int)(height*(1+offset)))]
    C = [randint(c1[0],c3[0]), randint(c1[1],c3[1])]
    
    RGBA = [randint(0,255),randint(0,255),randint(0,255),randint(130,255)]    
    return [A,B,C,RGBA]
    
def inTriangle(pt_coord,tri_coord):
    """
    pt_coord is a list(point) containing 2 coordinates
    tri_coord is a list containing 3 lists or tuples(points)

    returns True if point is in triangle, False otherwise
    """
    x,y = pt_coord[0], pt_coord[1]
    A = [tri_coord[0][0], tri_coord[0][1]]
    B = [tri_coord[1][0], tri_coord[1][1]]
    C = [tri_coord[2][0], tri_coord[2][1]]
    
    x_low = min(A[0], B[0],C[0])
    x_hi = max(A[0], B[0],C[0])
    if x > x_hi or x < x_low:
        return False
    
    y_low = min(A[1], B[1],C[1])
    y_hi = max(A[1], B[1],C[1])
    if y  > y_hi or y < y_low:
        return False
    
    lines = []
    if x >= min(A[0],B[0]) and x <= max(A[0],B[0]):
        lines.append([A,B])
    if x >= min(C[0],B[0]) and x <= max(C[0],B[0]):
        lines.append([B,C])
    if x >= min(A[0],C[0]) and x <= max(A[0],C[0]):
        lines.append([C,A])
        
    if y in range(findY(lines[0][0],lines[0][1],x), findY(lines[1][0],lines[1][1],x)):
        return True
    else:
        return False
    
def findY(A,B,x):
    """
    given a line formed by 2 points A and B
    returns the value of y at x on that line
    """
    if B[0] - A[0] == 0:
        return 0
    m = (B[1]-A[1]) / (B[0]-A[0])
    b = A[1] - m*A[0]
    return m*x + b

def weightedRandom(choices, weights):
    total = sum(weights)
    r = uniform(0, total)
    upto = 0
    for i in range(len(choices)):
        if upto + weights[i] >= r:
            return i
        upto += weights[i]    

def midpoint(c1, c2):
    return [(c1[0]+c2[0])/2, (c1[1]+c2[1])/2]

#saveImage(evolveImage())

import os, sys
from PIL import Image, ImageDraw
from random import randint

inputPath= 'picture.jpg'
outputPath = 'altered.png'

def evolveImage():
    """Given an image, returns an altered version of the image"""
        
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

def popToImage(x,y,population):
    """Input: x,y dimensions, the whole population
        Output: a PIL image object created by overlaying
        individuals triangles on top of each other and mixing the
        RGB color values."""

def evaluation(population, img, imgAltered):
    """Input: the entire population, the original image, an altered image
        Output: a list of length len(population), composed of
        floats between 0 and 100, where 0 is the least fit,
        and 100 is the most fit."""

def selection(population, fitness):
    """Input: the entire population, fitness output from the evaluation function
        Output: a population list with length less than the input"""

def crossover(population):
    """Input: the entire population
        Output: a population list with length longer than the input"""
    
def mutation(population):
    """Input: the entire population
        Output: a population list with some random properties of
        some of the individuals altered."""

saveImage(evolveImage())

"""
JACK
"""
def randomRBG():
    """returns a tuple with 3 random values"""
    return (randint(0,255),randint(0,255),randint(0,255))

def randomTri(height,width):
    """
    given height and width of image, generate a triangle with size relative to the dimensions
    returns a list of tuples
    """
    x_offset = randint(-width/5,width)
    y_offset = randint(-height/5,height)
    #offset of the triangle
    
    factor = 2
    #the maximum size of the triangle relative to dimensions. ie 1/factor
    h = int(height / factor)
    w = int(width / factor)

    A = [randint(0, int(w/2)),randint(0,int(2*h/3))]
    B = [randint(int(w/2), w),randint(0, int(2*h/3))]
    C = [randint(0, w),randint(int(2*h/3), h)]

    A[0] += x_offset
    B[0] += x_offset
    C[0] += x_offset
    A[1] += y_offset
    B[1] += y_offset
    C[1] += y_offset

    return [tuple(A),tuple(B),tuple(C)]
        

def inTriangle(pt_coord,tri_coord):
    """
    pt_coord is a list(point) containing 2 coordinates
    tri_coord is a list containing 3 lists(points)

    returns True if point is in triangle, False otherwise
    """
    x,y = pt_coord[0], pt_coord[1]
    A = [tri_coord[0][0], tri_coord[0][1]]
    B = [tri_coord[1][0], tri_coord[1][1]]
    C = [tri_coord[2][0], tri_coord[2][1]]
    
    x_low = min(A[0], B[0],C[0])
    x_hi = max(A[0], B[0],C[0])
    if x not in range(x_low, x_hi):
        return False
    
    y_low = min(A[1], B[1],C[1])
    y_hi = max(A[1], B[1],C[1])
    if y not in range(y_low, y_hi):
        return False
    
    lines = []
    if x in range(min(A[0],B[0]), max(A[0],B[0])):
        lines.append([A,B])
    if x in range(min(C[0],B[0]), max(C[0],B[0])):
        lines.append([B,C])
    if x in range(min(A[0],C[0]), max(A[0],C[0])):
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
    m = (B[1]-A[1]) / (B[0]-A[0])
    b = A[1] - m*A[0]
    return m*x + b

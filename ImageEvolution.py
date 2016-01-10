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
    WIDTH = x
    HEIGHT = y
    img = Image.new('RGBA', (WIDTH, HEIGHT)) # Use RGBA
    tri = Image.new('RGBA', (WIDTH, HEIGHT)) # Use RGBA
    draw = ImageDraw.Draw(img)
    draw_tri = ImageDraw.Draw(tri)

    draw.polygon([(0, 0), (0, HEIGHT), (WIDTH, HEIGHT), (WIDTH, 0)], fill = (255,255,255,255)) #draws a white background

    transparence = 100 # Define transparency for the triangle.
    
    for i in range(population):
        draw_tri.polygon([(0, 0), (0, HEIGHT), (WIDTH, HEIGHT), (WIDTH, 0)], fill = (255,255,255,0)) #resets triangle to white
        draw_tri.polygon(randomTri(HEIGHT, WIDTH), fill = randomRBG(transparence))
        img = Image.alpha_composite(img, tri)

    return img

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
def randomRBG(trans):
    """returns a tuple with 3 random values"""
    return (randint(0,255),randint(0,255),randint(0,255), trans)

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
    

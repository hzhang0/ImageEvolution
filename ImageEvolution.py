import os, sys
from PIL import Image
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

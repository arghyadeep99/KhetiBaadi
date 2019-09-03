import io
import torch
import numpy as np
import time
from torch import nn, optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models
import torchvision
from collections import OrderedDict
from torch.autograd import Variable
from PIL import Image
from torch.optim import lr_scheduler
import matplotlib.pyplot as plt
import copy
import json
import os
from os.path import exists

def get_model():
    filepath = 'models/pytorch_resnet152.pth'
    checkpoint = torch.load(filepath, map_location=torch.device('cpu'))
    model = models.resnet152()
    classifier = nn.Sequential(OrderedDict([
        ('fc1', nn.Linear(2048, 512)),
        ('relu', nn.ReLU()),
        ('fc2', nn.Linear(512, 39)),
        ('output', nn.LogSoftmax(dim=1))
        ]))
    model.fc = classifier
    model.load_state_dict(checkpoint['state_dict'])
    return model, checkpoint['class_to_idx']

model, class_to_idx = get_model()

idx_to_class = {v:k for k, v in class_to_idx.items()}

def process_image(image):
    size = 256, 256
    image.thumbnail(size, Image.ANTIALIAS)
    image = image.crop((128 - 112, 128 - 112, 128 + 112, 128 + 112))
    npImage = np.array(image)
    npImage = npImage/255.
    imgA = npImage[:,:,0]
    imgB = npImage[:,:,1]
    imgC = npImage[:,:,2]
    imgA = (imgA - 0.485)/(0.229) 
    imgB = (imgB - 0.456)/(0.224)
    imgC = (imgC - 0.406)/(0.225)
    npImage[:,:,0] = imgA
    npImage[:,:,1] = imgB
    npImage[:,:,2] = imgC
    npImage = np.transpose(npImage, (2,0,1))
    return npImage

def imshow(image, ax=None, title=None):
    if ax is None:
        fig, ax = plt.subplots()
    image = image.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    image = std * image + mean
    image = np.clip(image, 0, 1)
    ax.imshow(image)
    return ax

def get_plant_name(image_bytes):
    topk=3
    image = torch.FloatTensor([process_image(Image.open(image_bytes))])
    model.eval()
    output = model.forward(Variable(image))
    probabilities = torch.exp(output).data.numpy()[0]
    top_idx = np.argsort(probabilities)[-topk:][::-1] 
    top_class = [idx_to_class[x] for x in top_idx]
    top_probability = probabilities[top_idx]
    return top_probability, top_class
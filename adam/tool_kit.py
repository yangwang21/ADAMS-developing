"""
Direct-extract-from-SAM-file
    Copyright (C) 2023  Guo Zhengyang

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
import cupy as cp
from cupyx.scipy.spatial import distance_matrix as dm
from scipy.spatial import distance_matrix
from Bio.PDB import *
import cv2
import os
from tqdm import tqdm
import pickle as pkl

def get_coordinate(pdb_path, name):
    p = PDBParser()
    st = p.get_structure(name, pdb_path)
    ca = np.array([atom.coord for atom in st.get_atoms() if atom.name == 'CA'])
    return ca

def extract_features(mat):
    mat = cv2.normalize(mat, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
    sift = cv2.SIFT_create()
    kp, des = sift.detectAndCompute(mat, None)
    return des

def norm(x):
    x = x.T
    x1 = np.linalg.norm(x=x, ord=2, axis=0, keepdims=True)
    x = x / x1
    return x.T

from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np
from os import listdir
import shutil
   
# for filename in listdir('/var/www/html/repo/static/repos44/'):
#   if filename.endswith('.png'):
#     try:
#       img = Image.open('/var/www/html/repo/static/repos44/'+filename) # open the image file
#       o=img.verify() # verify that it is, in fact an image
#       # print(o)
#       fe = FeatureExtractor()
#       files=filename.split('.')
#       img_path='/var/www/html/repo/static/repos44/'+filename
#       print(img_path)  # e.g., ./static/img/xxx.jpg
#       feature = fe.extract(img=Image.open('/var/www/html/repo/static/repos44/'+filename))
#       feature_path = '/var/www/html/repo/static/feature/'+files[0]+'.npy'
#       np.save(feature_path, feature)
#       print(filename)
#     except (IOError, SyntaxError) as e:
#       # shutil.copy('/var/www/html/repo/static/repos44/'+filename, '/var/www/html/repo/static/bad_img/'+filename)
#       print('Bad file:', filename) # print out the names of corrupt files

if __name__ == '__main__':
    fe = FeatureExtractor()

    for img_path in sorted(Path("/var/www/html/amazon/repo/").glob("*.png")):
        print(img_path)  # e.g., ./static/img/xxx.jpg
        feature = fe.extract(img=Image.open(img_path))
        feature_path = Path("/var/www/html/imagefinder/static/feature") / (img_path.stem + ".npy")  # e.g., ./static/feature/xxx.npy
        np.save(feature_path, feature)


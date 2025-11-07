from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np
import shutil
from os import listdir
if __name__ == '__main__':
    fe = FeatureExtractor()
    for filename in listdir('static/repo_126/'):
        try:
            img = Image.open('static/repo_126/'+filename) # open the image file
            o=img.verify() # verify that it is, in fact an image
            #   fe = FeatureExtractor()
            files=filename.split('.')
            img_path='static/repo_126/'+filename
              # e.g., .static/img/xxx.jpg
            feature = fe.extract(img=Image.open('static/repo_126/'+filename))
            feature_path = 'static/feature/'+files[0]+'.npy'
            np.save(feature_path, feature)
            print(filename)
            shutil.move(img_path, 'static/Images/'+filename)
            print('Moved file:', filename) # print out the names of corrupt files
        except MemoryError as mem_error:
            # If there's a memory error, move the image to bad_img and continue the process
            shutil.move(img_path, 'static/bad_img/' + filename)
            print(f"Memory Error with file {filename}. Moved to bad_img.")
        except ValueError as ve:
            # If the decompression data is too large, move the image to bad_img and continue
            if "Decompressed Data Too Large" in str(ve):
                shutil.move('static/repo_126/'+filename, 'static/bad_img/' + filename)
                print(f"Decompression Error with file {filename}. Moved to bad_img.")
            else:
                raise ve  # Re-raise other ValueErrors

        except (IOError, SyntaxError) as e:
            shutil.move('static/repo_126/'+filename, 'static/bad_img/'+filename)
            print('Bad file:', filename) # print out the names of corrupt files
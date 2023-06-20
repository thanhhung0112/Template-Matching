from turbojpeg import TurboJPEG
from time import time

class TurboJpegLoader:
    def __init__(self):
        super(TurboJpegLoader, self).__init__()
        
        # create TurboJPEG object for image reading
        self.jpeg_reader = TurboJPEG() 
 
    def load(self, path):
        start = time()
        # open the input file as bytes
        file = open(path, "rb")  
        full_time = time() - start
 
        start = time()
        # decode raw image
        image = self.jpeg_reader.decode(file.read(), 1)  
        full_time += time() - start
        file.close()
        
        return image, full_time
    
if __name__ == "__main__":
    path = 'Dataset/input_image.jpg'
    loader = TurboJpegLoader()
    
    s = time()
    img, t = loader.load(path)
    e = time()
    print(f'time: {e-s}')
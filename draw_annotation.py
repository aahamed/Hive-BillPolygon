import argparse
import pickle
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

class Annotation( object ):

    def __init__( self, img_file, label, points ):
        self.img_file = img_file
        self.label = label
        self.points = np.array( points )
        self.classname = self.get_classname()
        self.area = self.get_area()

    def get_classname( self ):
        m = re.search( '([A-Z]*)\d\d\d', self.img_file )
        abbrv = m.group(1)
        assert abbrv in ABBRV_TO_CLASS
        classname = ABBRV_TO_CLASS[ abbrv ]
        return classname

    def get_area( self ):
        if self.label == 'inconclusive': return 0
        # import pdb; pdb.set_trace()
        x = self.points[:, 0]
        y = self.points[:, 1]
        pgon = Polygon(zip(x, y))
        return pgon.area

def load_ann( args ):
    annotations = pickle.load( open( args.ann_file, 'rb' ) )
    return annotations

def main( args ):
    annotations = load_ann( args )
    img_path = args.img_file
    img_file = img_path.split( '/' )[ -1 ]
    img = np.asarray( Image.open(img_path) )
    H, W, C = img.shape
    ann = annotations[ img_file ]
    if ann.label == 'inconclusive':
        raise Exception( f'Annotation was inconclusive for {img_file}' )
    fig, ax = plt.subplots(1, 1)
    ax.imshow( img )
    points = np.array( ann.points )
    x = (points[:, 0] * W).astype(int)
    y = (points[:, 1] * H).astype(int)
    ax.plot( x, y, 'r' )
    ax.axis('off')
    ax.set(title=ann.img_file)
    fig.savefig( args.output_file )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate image with polygon')
    parser.add_argument( '--img-file',
                        help='path to image to be annotated' )
    parser.add_argument( '--output-file',
                        help='path where output will be saved' )
    parser.add_argument( '--ann-file',
                        help='Pickle file containing annotation data' )
    args = parser.parse_args()
    main( args )

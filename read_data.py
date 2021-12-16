import argparse
import csv
import json
import pickle
import re
import numpy as np
from shapely.geometry import Polygon

from collections import defaultdict

ABBRV_TO_CLASS = {
    'AMAV' : 'American_Avocet',
    'BHN' : 'Brown-headed_Nuthatch',
    'BF' : 'Bufflehead',
    'PW' : 'Prothonotary_Warbler',
    'SDL' : 'Sanderling',
    'WGR' : 'Western_Grebe',
    'WHMB' : 'Whimbrel',
    'WIB' : 'Whte_Ibis',
}

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

def get_points( points ):
    '''
    Convert list of dicts to list of lists
    '''
    assert isinstance( points, list )
    assert isinstance( points[0], dict )
    points_list = []
    for point in points:
        x, y = point['x'], point['y']
        points_list.append( [ x, y ] )
    return points_list

def read_csv( filename ):
    annotations = {}
    with open(filename, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate( datareader ):
            if i == 0: continue # skip header
            img_file = row[7]
            ann = json.loads( row[9] )
            if not ann: continue
            ann = ann[0]
            if ann == 'inconclusive':
                label = 'inconclusive'
                points = []
            else:
                label = ann['label']
                points = get_points( ann['points'] )
            annotations[ img_file ] = Annotation( img_file, label, points )
            # print( ', '.join(row) )
    return annotations

def save_ann( annotations, save_name ):
    pickle.dump( annotations, open( save_name, "wb" ) )

def load_ann( save_name ):
    annotations = pickle.load( open( save_name, 'rb' ) )
    return annotations

def area_stats( annotations ):
    print( 'Area Stats:' )
    areas = []
    for img_file, ann in annotations.items():
        if ann.label == 'inconclusive': continue
        areas.append( ann.area )
    mean, std = np.mean( areas ), np.std( areas )
    print( f'mean: {mean:.4f} std: {std:.4f}' )

def stats( annotations ):
    label_counter = defaultdict(int)
    for img_file, ann in annotations.items():
        label_counter[ ann.label ] += 1
    N = len( annotations )
    assert sum( label_counter.values() ) == N
    print( 'STATS:' )
    print( 'Label Counts Frac' )

    for label, count in label_counter.items():
        frac = count / N
        print( f'{label:20s}: {count:03d} {frac:.2f}' )

    area_stats( annotations )

def main( args ):
    # import pdb; pdb.set_trace()
    # filename = 'bill-polygon.csv'
    filename = args.csv_file
    annotations = read_csv( filename )
    output_file = args.output_file
    save_ann( annotations, output_file )
    annotations = load_ann( output_file )
    # stats( annotations )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse polygon data from csv file')
    parser.add_argument( '--csv-file',
                        help='path to csv file containing annotations' )
    parser.add_argument( '--output-file',
                        help='path where output will be saved' )
    args = parser.parse_args()
    main( args )

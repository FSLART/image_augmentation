import visualise as vis
import dataWrite as dw40
import argparse

DEFAULT_CONFIG="configs/default.ini"

# Create parser
parser = argparse.ArgumentParser(
                    prog='augmentIMG',
                    description='Create single/multiple augmented images of images in a directory.')

# Parse argument
parser.add_argument('-c',
                    '--config',
                    type=str,
                    action='store',
                    default=DEFAULT_CONFIG,
                    help='The path (relative or absolute) from the current directory to the config file [default: ' + DEFAULT_CONFIG + ']')

args = parser.parse_args()

# call DataWriter
dw40.DataWriter(args.config)
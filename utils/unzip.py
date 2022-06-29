import subprocess
import argparse

parser = argparse.ArgumentParser(description='Unzip file',
                                 add_help=False)

parser.add_argument('src_file',
                    metavar='src_file',
                    type=str,
                    help='Archive file to unzip')

parser.add_argument('target_dir',
                    metavar='target_dir',
                    type=str,
                    help='Folder to save extracted contents to')

args = parser.parse_args()

src_file = args.src_file
target_dir = args.target_dir

if __name__ == '__main__':
    subprocess.call(['7z', 'x', src_file, '-o'+target_dir])

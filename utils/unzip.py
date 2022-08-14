import zipfile
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Unzip file',
                                 add_help=False)

parser.add_argument('--src_file',
                    type=str,
                    help='Archive file to unzip')

parser.add_argument('--target_dir',
                    type=str,
                    help='Folder to save extracted contents to')

parser.add_argument('--folder',
                    type=str,
                    default='all',
                    help='Specific folder in zip file, default=all')


def unzip_file(src_file, target_dir, folder):
    if folder=='all':
        subprocess.call(['7z', 'e', src_file, '-o'+target_dir, '-aoa'])
    else:
        archive = zipfile.ZipFile(src_file)
        for file in archive.namelist():
            if file.startswith(folder+'/'):
                archive.extract(file, f'{target_dir}/{src_file.split("/")[-1].replace(".zip","")}')

if __name__=='__main__':
    args = parser.parse_args()

    src_file = args.src_file
    target_dir = args.target_dir
    folder = args.folder
    unzip_file(src_file, target_dir, folder)
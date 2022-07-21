import shutil
import os
from rename import rename_files
import argparse

parser = argparse.ArgumentParser(description='Merge subdirectories into one')
parser.add_argument('--root_dir', type=str,
                    help='The directory to merge subdirectories')
parser.add_argument('--to_rename',  type=bool, default=False,
                    help='If True renames all the files')
args = parser.parse_args()

root_dir = args.root_dir
to_rename = args.to_rename


if __name__ == '__main__':
    sub_dirs = os.listdir(root_dir)

    sub_dirs = [sd for sd in sub_dirs if os.path.isdir(f'{root_dir}/{sd}')]
    print(f'Merging {len(sub_dirs)} subdirectories')

    for sub_dir in sub_dirs:

        s_dir = sub_dir
        sub_dir = f'{root_dir}/{sub_dir}'
        file_names = os.listdir(sub_dir)
        for file_name in file_names:
            ext = file_name.split('.')[-1].lower()
            file_name = file_name
            file_name_x = file_name[:-4]+f'___{s_dir}.{ext}'
            shutil.move(os.path.join(sub_dir, file_name),
                        os.path.join(root_dir, file_name_x.replace('  ', '')))
        shutil.rmtree(sub_dir)
    if to_rename:
        rename_files(root_dir)

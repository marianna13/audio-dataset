import os


def rename_files(path):
    files = sorted(os.listdir(path))
    jsons = [f for f in files if f.endswith(".json")]
    flacs = [f for f in files if f.endswith(".flac")]

    index = 0
    for j, f in zip(jsons, flacs):
        os.rename(os.path.join(path, j), os.path.join(
            path, f'{index}.json'))
        os.rename(os.path.join(path, f), os.path.join(
            path, f'{index}.flac'))
        index += 1

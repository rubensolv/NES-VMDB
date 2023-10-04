import os
import shutil 
import argparse
import re

def traverse_dir(
        root_dir,
        extension=('mid', 'MID', 'midi'),
        amount=None,
        str_=None,
        is_pure=False,
        verbose=False,
        is_sort=False,
        is_ext=True):

    if verbose:
        print('[*] Scanning...')

    cnt, file_list = 0, []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(extension):
                if (amount is not None) and (cnt == amount):
                    break
                if str_ is not None:
                    if str_ not in file:
                        continue

                mix_path = os.path.join(root, file)
                pure_path = mix_path[len(root_dir)+1:] if is_pure else mix_path

                if not is_ext:
                    ext = pure_path.split('.')[-1]
                    pure_path = pure_path[:-(len(ext)+1)]
                if verbose:
                    print(pure_path)
                file_list.append(pure_path)
                cnt += 1
    if verbose:
        print('Total: %d files' % len(file_list))
        print('Done!!!')

    if is_sort:
        file_list.sort()

    return file_list

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='clean.py')
    parser.add_argument('--path_indir', type=str, required=True)
    parser.add_argument('--path_outdir', type=str, required=True)
    args = parser.parse_args()

    os.makedirs(args.path_outdir, exist_ok=True)

    # list files
    midifiles = traverse_dir(
        args.path_indir,
        is_pure=True,
        is_sort=True)
    n_files = len(midifiles)
    print('num files:', n_files)

    # collect
    data = []
    for fidx in range(n_files):
        path_midi = midifiles[fidx]
        print('{}/{}'.format(fidx, n_files))
        
        # Prefix remove regex
        x = re.search("\d\d\d_", path_midi)
        _,j = x.span()

        # Suffix remove regex
        y = re.search("(_\d\d_\d\d|_\d\d)(.*)$", path_midi[j:])
        i,_ = y.span()

        game_name = path_midi[j:][:i]
        midi_name = os.path.basename(path_midi)
        game_outdir = os.path.join(args.path_outdir, game_name)

        # paths
        path_infile = os.path.join(args.path_indir, path_midi)
        path_outfile = os.path.join(game_outdir, midi_name)

        os.makedirs(game_outdir, exist_ok=True)
        
        print(path_midi)
        print(path_outfile)

        shutil.copyfile(path_infile, path_outfile)

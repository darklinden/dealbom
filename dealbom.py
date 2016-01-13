#!/usr/bin/python
import os
import sys
import shutil
import codecs
import stat

BOM_UTF8 = '\xef\xbb\xbf'

def add_bom(file_path):
    file_old = open(file_path, mode='r')
    if file_old.read(3) == BOM_UTF8:
        print("file " + file_path + " already has bom")
        return

    file_old.seek(0)

    file_new = open(file_path + '-tmp', mode='w')
    file_new.write(BOM_UTF8)
    file_new.write(file_old.read())
    file_old.close()
    file_new.close()

    shutil.copymode(file_path, file_path + '-tmp')
    os.remove(file_path)
    shutil.move(file_path + '-tmp', file_path)
    print('add bom for ' + file_path)

def remove_bom(file_path):
    file_old = open(file_path, mode='r')
    if file_old.read(3) != BOM_UTF8:
        print("file " + file_path + " does not have bom")
        return

    file_old.seek(3)

    file_new = open(file_path + '-tmp', mode='w')
    file_new.write(file_old.read())
    file_old.close()
    file_new.close()

    shutil.copymode(file_path, file_path + '-tmp')
    os.remove(file_path)
    shutil.move(file_path + '-tmp', file_path)
    print('remove bom for ' + file_path)

def __main__():
    # param
    if len(sys.argv) != 3:
        print("using dealbom [a: add bom; r: remove bom] [file or folder path] to add or remove bom")
        return

    param_cmd = sys.argv[1]
    param_path = sys.argv[2]

    if os.path.isfile(param_path):
        if param_cmd == 'a':
            add_bom(param_path)
        elif param_cmd == 'r':
            remove_bom(param_path)
    elif os.path.isdir(param_path):
        path_array = []
        for root, dirs, files in os.walk(param_path):
            sub_files = os.listdir(root)
            for fn in sub_files:
                file_path = root + "/" + fn
                if os.path.isfile(file_path):
                    if param_cmd == 'a':
                        add_bom(file_path)
                    elif param_cmd == 'r':
                        remove_bom(file_path)

    print('done')

__main__();

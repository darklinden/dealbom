#!/usr/bin/python
import os
import sys
import shutil
import codecs
import stat
import chardet
import subprocess

BOM_UTF8 = '\xef\xbb\xbf'

PRAGMA_UTF8_MAC = '#pragma execution_character_set("utf-8")\n'
PRAGMA_UTF8_WIN = '#pragma execution_character_set("utf-8")\r\n'

EN_UTF8 = "utf-8"
EN_UTF8_BOM = "utf-8-sig"

def run_cmd(cmd):
    print("run cmd: " + " ".join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print(err)
    return out

def self_install(file, des):

    file_path = os.path.realpath(file)

    filename = file_path

    pos = filename.rfind("/")
    if pos:
        filename = filename[pos + 1:]

    pos = filename.find(".")
    if pos:
        filename = filename[:pos]

    to_path = os.path.join(des, filename)

    print("installing [" + file_path + "] \n\tto [" + to_path + "]")
    os.remove(to_path)
    shutil.copy(file_path, to_path)
    run_cmd(['chmod', 'a+x', to_path])

def file_is_src(file_path):
    filename, file_extension = os.path.splitext(file_path)
    if file_extension == '.c' or file_extension == '.cc' or file_extension == '.cpp' or file_extension == '.h' or file_extension == '.hpp':
        return True
    else:
        return False

def convert_encoding(file_path, des_encoding):
    convertFile = open(file_path, 'rb')
    data = convertFile.read(1024 * 10)
    convertFile.close()

    src_encoding = chardet.detect(data)['encoding']

    if src_encoding == des_encoding:
        return

    try:
        file_old = codecs.open(file_path, mode='rb', encoding=src_encoding)
        file_new = codecs.open(file_path + '-tmp', mode='wb', encoding=des_encoding)

        file_new.write(file_old.read())
        file_old.close()
        file_new.close()

        shutil.copystat(file_path, file_path + '-tmp')
        os.remove(file_path)
        shutil.move(file_path + '-tmp', file_path)
        print('convert encodeing from ' + src_encoding + ' to ' + des_encoding + ' for ' + file_path)
    except:
        print('convertiong failed from ' + src_encoding + ' to ' + des_encoding + ' for ' + file_path)
        pass

def add_bom(file_path):
    file_old = open(file_path, mode='rb')

    if file_old.read(len(BOM_UTF8)) == BOM_UTF8:
        print("file " + file_path + " already has bom")
        return
    else:
        file_old.seek(0)

    file_new = open(file_path + '-tmp', mode='wb')
    file_new.write(BOM_UTF8)
    file_new.write(file_old.read())
    file_old.close()
    file_new.close()

    shutil.copystat(file_path, file_path + '-tmp')
    os.remove(file_path)
    shutil.move(file_path + '-tmp', file_path)
    print('add bom for ' + file_path)

def remove_bom(file_path):
    file_old = open(file_path, mode='rb')

    if file_old.read(len(BOM_UTF8)) == BOM_UTF8:
        file_old.seek(len(BOM_UTF8))
    else:
        print("file " + file_path + " does not have bom")
        return

    file_new = open(file_path + '-tmp', mode='wb')
    file_new.write(file_old.read())
    file_old.close()
    file_new.close()

    shutil.copystat(file_path, file_path + '-tmp')
    os.remove(file_path)
    shutil.move(file_path + '-tmp', file_path)
    print('remove bom for ' + file_path)

def add_pragma(file_path):
    file_old = open(file_path, mode='rb')

    if file_old.read(len(PRAGMA_UTF8_WIN)) == PRAGMA_UTF8_WIN:
        print("file " + file_path + " already has pragma")
        return
    else:
        file_old.seek(0)
        if  file_old.read(len(PRAGMA_UTF8_MAC)) == PRAGMA_UTF8_MAC:
            print("file " + file_path + " already has pragma")
            return
        else:
            file_old.seek(0)

    file_new = open(file_path + '-tmp', mode='wb')
    file_new.write(PRAGMA_UTF8_MAC)
    file_new.write(file_old.read())
    file_old.close()
    file_new.close()

    shutil.copystat(file_path, file_path + '-tmp')
    os.remove(file_path)
    shutil.move(file_path + '-tmp', file_path)
    print('add pragma for ' + file_path)

def remove_pragma(file_path):
    file_old = open(file_path, mode='rb')
    if file_old.read(len(PRAGMA_UTF8_WIN)) == PRAGMA_UTF8_WIN:
        file_old.seek(len(PRAGMA_UTF8_WIN))
    else:
        file_old.seek(0)
        if file_old.read(len(PRAGMA_UTF8_MAC)) == PRAGMA_UTF8_MAC:
            file_old.seek(len(PRAGMA_UTF8_MAC))
        else:
            print("file " + file_path + " does not have pragma")
            return

    file_new = open(file_path + '-tmp', mode='wb')
    file_new.write(file_old.read())
    file_old.close()
    file_new.close()

    shutil.copystat(file_path, file_path + '-tmp')
    os.remove(file_path)
    shutil.move(file_path + '-tmp', file_path)
    print('remove pragma for ' + file_path)

def __main__():
    # param
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        self_install("dealbom.py", "/usr/local/bin")
        return

    if len(sys.argv) != 3:
        print("using dealbom [a: add prgma; r: remove pragma; u: convert utf-8; b: convert utf-8-sig; fb: force add bom and pragma; fu: force remove bom and pragma] [file or folder path] to add or remove bom")
        return

    param_cmd = sys.argv[1]
    param_path = sys.argv[2]

    if os.path.isfile(param_path):
        if not file_is_src(param_path):
            print('file is not src, skip ' + param_path)
            return

        if param_cmd == 'a':
            convert_encoding(param_path, EN_UTF8)
            add_pragma(param_path)
        elif param_cmd == 'r':
            convert_encoding(param_path, EN_UTF8)
            remove_pragma(param_path)
        elif param_cmd == 'u':
            convert_encoding(param_path, EN_UTF8)
        elif param_cmd == 'b':
            convert_encoding(param_path, EN_UTF8_BOM)
        elif param_cmd == 'fb':
            add_pragma(param_path)
            add_bom(param_path)
        elif param_cmd == 'fu':
            remove_bom(param_path)
            remove_pragma(param_path)

    elif os.path.isdir(param_path):
        path_array = []
        for root, dirs, files in os.walk(param_path):
            sub_files = os.listdir(root)
            for fn in sub_files:
                file_path = root + "/" + fn
                if os.path.isfile(file_path):
                    if not file_is_src(file_path):
                        print('file is not src, skip ' + file_path)
                        continue

                    if param_cmd == 'a':
                        convert_encoding(file_path, EN_UTF8)
                        add_pragma(file_path)
                    elif param_cmd == 'r':
                        convert_encoding(file_path, EN_UTF8)
                        remove_pragma(file_path)
                    elif param_cmd == 'u':
                        convert_encoding(file_path, EN_UTF8)
                    elif param_cmd == 'b':
                        convert_encoding(file_path, EN_UTF8_BOM)
                    elif param_cmd == 'fb':
                        add_pragma(file_path)
                        add_bom(file_path)
                    elif param_cmd == 'fu':
                        remove_bom(file_path)
                        remove_pragma(file_path)

    print('\nDone')

__main__()

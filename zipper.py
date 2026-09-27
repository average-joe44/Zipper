import zipfile
import shutil
import sys
import os

def one_folder(source_folder, output_zip_folder):
    print(f"Making zip archive of '{source_folder}' folder")

    try:
        shutil.make_archive(output_zip_folder, "zip", source_folder)
    except FileNotFoundError:
        exit("Folder not found!")
    except NotADirectoryError:
        exit("Directory is a file!")

    print(f"Successfully made an archive out of '{source_folder}' folder into '{output_zip_folder}'")

def multiple_files(files, output):
    try:
        to_zip = files

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
            for file in to_zip:
                if not output.endswith('.zip'):
                    print("Wrong file extension! (must be .zip)")
                    raise ValueError

                print(f"Zipping {file}")
                if os.path.isdir(file):
                    print("File is a directory!")
                    raise ValueError

                if not os.path.exists(file):
                    print("File not found!")
                    raise FileNotFoundError
                
                if os.path.exists(file):
                    zipped.write(file)
            print("Zipping process completed")
                
    except (FileNotFoundError, ValueError):
        if os.path.exists(output):
            os.remove(output)
                
def unzip_file(source_file, output_folder):
    print(f"Extracting zip file from '{source_file}' file")

    try:
        shutil.unpack_archive(source_file, output_folder)
    except FileNotFoundError:
        exit("The zip file is not found!")
    except IsADirectoryError:
        exit("Zip file is a directory!")

    print(f"Successfully unpacked a zip '{source_file}' file into '{output_folder}' folder")

try:
    option = sys.argv[1]
    if option in ('--multiple', '-mtp'):
        files = sys.argv[2:]
        delimiter = "-o"
        if not delimiter in files:
            exit("You must use '-o' to specify the output name, and ensure the extension is .zip!")
        elif delimiter in files:
            slice = files.index(delimiter)
            flist = files[:slice]
            output_name = files[slice+1]
            multiple_files(flist, output_name)
    elif option in ('--onefolder', '-f'):
        source_folder = sys.argv[2]
        output_folder = sys.argv[3]
        one_folder(source_folder, output_folder)
    elif option in ('--help', '-h'):
        print("Usage: (--onefolder or -f) <source_folder_name> <output_zipped_folder_name>")
        print("Usage: (--multiple or -mtp) <file_names> -o <output_name.zip>")
        print("Usage: (--unpack or -up) <zip_file> <output_name>")
    elif option in ('--unpack', '-up'):
        source_file = sys.argv[2]
        output_folder_name = sys.argv[3]
        unzip_file(source_file, output_folder_name)
    elif not option in ('--multiple', '-mtp') or ('--onefolder', '-f'):
        exit("Use '--multiple' or '-mtp' for files, or '--onefolder' and '-f' to make zip archive of a folder!")
except KeyboardInterrupt:
    exit('Operation canceled by user!')
except IndexError:
    exit("Argument is incomplete. Type '-h' for help!")
import os
import utils.consts as consts
import utils.assets_import as imports
import utils.profiles as profiles

profileList = profiles.get_profiles()

for idx, option in enumerate(profileList):
    
    fileList = os.listdir(consts.DIRECTORY_ASSETS)

    fileToRead = []

    for row in fileList:
        nome, extensao = os.path.splitext(row)

        if (extensao not in option["extensions"]): continue

        # Se existem arquivos específicos para listar
        if (len(option["files"]) > 0):
            if (row not in option["files"]): continue

        file_path = os.path.join(consts.DIRECTORY_ASSETS, row)

        if (not os.path.exists(file_path)):
            print("     n encontrado: " + file_path);
            continue

        fileToRead.append(row)

    print(idx)

    if (len(fileToRead) > 0):
        imports.config_retriever(fileToRead, idx)
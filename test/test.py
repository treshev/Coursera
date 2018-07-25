import os


def rename_item(folder, olde_name_item):
    try:
        old_name_in_byte = olde_name_item.encode('ibm437')
        new_name = old_name_in_byte.decode("ibm866")
        try:
            os.rename(os.path.join(folder, olde_name_item), os.path.join(folder, new_name))
        except Exception as er:
            print("Не удалось переименовать", os.path.join(folder, new_name))
            print(er)
    except UnicodeEncodeError:
        print("Файл уже переименован", olde_name_item)
        pass


def rename_folder_and_files(parent_folder, folder_name):
    if folder_name:
        current_folder = os.path.join(parent_folder, folder_name)
    else:
        current_folder = parent_folder

    current_folder_list = os.listdir(current_folder)
    for item in current_folder_list:
        item_path = os.path.join(current_folder, item)
        if os.path.isdir(item_path):
            rename_folder_and_files(current_folder, item)
        else:
            rename_item(current_folder, item)

    if folder_name:
        rename_item(parent_folder, folder_name)


if __name__ == '__main__':
    rename_folder_and_files('.', None)

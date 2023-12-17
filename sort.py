import os
import shutil
import sys
from datetime import datetime
from datetime import date


# Можливі формати файлів для пошуку
IMAGES = ('JPEG', 'PNG', 'JPG', 'SVG', 'GIF', 'ICO')
VIDEO = ('AVI', 'MP4', 'MOV', 'MKV', 'MPEG4')
TEXTDOC = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'RTF')
MUSIC = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVES = ('ZIP', 'GZ', 'TAR')


# Строки які потрібні функції normalize для перекладу з кирилеці на латину
SUMBOLS = '''!"#$%&'()*+№,-/:;<=>?@[\]^_`{|}~ '''
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
"f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g"
)


def normalize(path:str):
    filename = path.split('\\')[-1]
    '''Функція яка в разі потреби буде перекладати назву файлу з кирилиці на латину'''
    # Розіляємо назву файлу на дві частини.Розділювачем є ".".Частина після крапики записується в змінну format_of_normalized_file щоб в подальшому повернути файлу його формат
    format_of_normalized_file = f".{filename.split('.')[-1]}"
    # Розіляємо назву файлу на дві частини.Розділювачем є ".".Частина перед крапкою записується в змінну old_name_without_format_of_file щоб проводити подальші дії з назвою файлу
    old_name_without_format_of_file = f'{filename[:filename.find(format_of_normalized_file)]}'
    # Нова назва файлу
    new_name = ''
    # За допомогою циклу перебераємо кожен символ назви файлу
    for laters in old_name_without_format_of_file:
        # Перевіряємо чи символ є кирилецею, якщо кирилецею також перевіряєм чи це мала буква 
        if CYRILLIC_SYMBOLS.find(laters.lower()) > -1 and laters == laters.lower():
            # Перекладаємо літеру кирилецею на латинську
            laters = TRANSLATION[CYRILLIC_SYMBOLS.find(laters.lower())]
            # Записуємо літеру в нову назву файлу
            new_name += laters
        # Перевіряємо чи символ є кирилецею, якщо кирилецею також перевіряєм чи це велика буква 
        elif CYRILLIC_SYMBOLS.find(laters.lower()) > -1 and laters == laters.upper():
            # Перекладаємо літеру кирилецею на латинську
            laters = TRANSLATION[CYRILLIC_SYMBOLS.find(laters.lower())].upper()
            # Записуємо літеру в нову назву файлу
            new_name += laters
        # Перевіряємо чи символ знаходиться в рядку SUMBOLS - рядок з  символами
        elif SUMBOLS.find(laters) > -1:
            # Якщо символ є в списку SUMBOLS його буде замінено та записано "_" в нову назву файлу
            new_name += '_'
        # Якщо ж це був символ не керилецею на відсутній в списку SUMBOLS 
        else:
            # Одразу записуємо його до нової назви файлу
            new_name += laters
    # До нової назви файлу додаємо його формат який був записаний завчасно
    new_name += format_of_normalized_file
    # Переіменовуємо файл з старої назви на нову
    if str(new_name) != str(filename):
        os.rename(f'{path}',f'{path[:path.find(filename)]}{new_name}')
    # Повертає нову назву файлу щоб в подальшому працювати з новою назвою файлу
    return f'{path[:path.find(filename)]}{new_name}'


def folder_creator_for_all_file_tipes(path:str):
    '''Створюємо папки в вказаному місці для сортування файлів'''
    # Також перевіривши чи таких ще не існує
    if not os.path.exists(f'{path}\\images'):
        os.makedirs(f'{path}\\images')
    if not os.path.exists(f'{path}\\video'):
        os.makedirs(f'{path}\\video')
    if not os.path.exists(f'{path}\\textdoc'):
        os.makedirs(f'{path}\\textdoc')
    if not os.path.exists(f'{path}\\music'):
        os.makedirs(f'{path}\\music')
    if not os.path.exists(f'{path}\\archives'):
        os.makedirs(f'{path}\\archives')
    if not os.path.exists(f'{path}\\other'):
        os.makedirs(f'{path}\\other')


def list_files(path:str):
    '''Функція для пошуку файлів за переданим шляхом 
        повертає список з адресами файлів що містяться за переданим шляхом'''
    # Список з повними адресами файлів
    files = []
    # запускаємо цикл що буде проходити по всіх файлах та папках за заданою адресою
    for file in os.listdir(path):
        # Створює рядок з повною адресою для кожного файла 
        file_path = os.path.join(path, file)
        # Ігнорує папки з назвою 'images','video','textdoc','music','archives','other'
        if os.path.isdir(file_path) and file_path.split('\\')[-1] in ['images','video','textdoc','music','archives','other']:
            continue
        # Якщо це папка функція рекурсивно викликає себе
        elif os.path.isdir(file_path):
            files += list_files(file_path)
        else:
            # Якщо це файл перевіряє його повну адресу якщо вона довша за 249 симворів його вкорочує для подальшої роботи з ним
            if len(file_path) > 249:
                start_of_string_of_path = ''
                filish_of_string_of_path = ''
                for item in file_path.split('\\')[:8]:
                    start_of_string_of_path += item + '\\'
                for item in file_path.split('\\')[-4:]:
                    filish_of_string_of_path += '\\' + item
                file_path = start_of_string_of_path + '...' + filish_of_string_of_path
                files.append(file_path)
                continue
            # Назву файлу пропускає через функцію normalize щоб в майбутньому коректно працювати з файлом
            file_path = normalize(file_path)
            # Додає коректну адресу файлу в список
            files.append(file_path)
    #
    return files


def rename_file_if_already_exists(path_to_removed:str,format:str,name_of_file:str):
    '''Функція перевіряє чи немає в папці з відсортованими файлами немає файла з таким амим імям
       якщо є то добавляє до файла "___" та індекс починаючи від 1 якщо таких файлів більше то індек росте на 1
       в подальшому адреса до файлу де він знаходився раніше та його нова назва
       буде записано в текстовий файл з результатом  '''
    new_name = name_of_file
    index = 1
    while True:
        # функція приймає два аргументи шлях до папки в яку потрібно помістити файл та повний адрес файлу
        # Цикл завершиться якщо файла з переданим імям немає в папці в яку потрібно помістити файл
        # В даному випадку ми передбачаємо що файлів з таким самим імям буде не більше 1000
        if os.path.isfile(f'{path_to_removed}\\{format}\\{new_name}') == False:
            return new_name
        if os.path.isfile(f'{path_to_removed}\\{format}\\{new_name}') and index > 100:
           new_name = str(new_name.split('.')[0])[:-3] + f'{index}.' + new_name.split('.')[-1]
        elif os.path.isfile(f'{path_to_removed}\\{format}\\{new_name}') and index > 10:
           new_name = str(new_name.split('.')[0])[:-2] + f'{index}.' + new_name.split('.')[-1]
        elif os.path.isfile(f'{path_to_removed}\\{format}\\{new_name}') and index > 1:
            new_name = str(new_name.split('.')[0])[:-1] + f'{index}.' + new_name.split('.')[-1]
        elif os.path.isfile(f'{path_to_removed}\\{format}\\{new_name}') and name_of_file.find('__reename__') == -1:
            new_name = new_name.split('.')[0] + f'__rename__{index}.' + new_name.split('.')[-1]
        index +=1
            

def function_of_sorting(file_list:list,path_to_removed:str):
    '''Функція яка буде переміщати файли в папки відповідно до розширення файлу'''
    # Словники з файлами відповідних форматів та їх старий адрес
    dict_for_files_images_format = {}
    dict_for_files_video_format = {}
    dict_for_files_textdoc_format = {}
    dict_for_files_music_format = {}
    dict_for_files_archives_format = {}
    # Словник з файлами невідомого формату та їх старий адрес
    dict_for_files_with_unknown_format = {}
    # Список невідомих форматів файлів
    list_of_unknown_formats = []
    # Проходимо по списку в якому елементами є шлях до файлу який треба відсортувати
    for item in file_list:
        try:# Розділяємо назву файлу розділяючим символом є '.' щоб мати формат файлу відокремлений від назви
            file_extension = item.split('.')[-1].upper()
            # Перевіряємо формат файлу та відправляємо його у папку з відсортованими файлами відповідного формату
            # Додаємо назву файлу в словник відповідно формату
            # Переміщає файл в папку з назвою відповідною до формату
            name_of_file = item.split('\\')[-1]
            if file_extension in IMAGES:
                name_of_file = rename_file_if_already_exists(path_to_removed,'images',name_of_file)
                dict_for_files_images_format[name_of_file] = item
                os.rename(str(item),f'{path_to_removed}\\images\\{name_of_file}')
            elif file_extension in VIDEO:
                name_of_file = rename_file_if_already_exists(path_to_removed,'video',name_of_file)
                dict_for_files_video_format[name_of_file] = item
                os.rename(str(item),f'{path_to_removed}\\video\\{name_of_file}')     
            elif file_extension in TEXTDOC:
                name_of_file = rename_file_if_already_exists(path_to_removed,'textdoc',name_of_file)
                dict_for_files_textdoc_format[name_of_file] = item               
                os.rename(str(item),f'{path_to_removed}\\textdoc\\{name_of_file}')
            elif file_extension in MUSIC:
                name_of_file = rename_file_if_already_exists(path_to_removed,'music',name_of_file)
                dict_for_files_music_format[name_of_file] = item
                os.rename(str(item),f'{path_to_removed}\\music\\{name_of_file}')
            elif file_extension in ARCHIVES:
                name_of_file = rename_file_if_already_exists(path_to_removed,'archives',name_of_file)
                dict_for_files_archives_format[name_of_file] = item
                os.rename(str(item),f'{path_to_removed}\\archives\\{name_of_file}')
            else:
                # Також додаю невідомий формат файлу в список 'list_of_unknown_formats'                
                if file_extension not in list_of_unknown_formats:
                    list_of_unknown_formats.append(file_extension)
                name_of_file = rename_file_if_already_exists(path_to_removed,'other',name_of_file)
                dict_for_files_with_unknown_format[name_of_file] = item
                os.rename(str(item),f'{path_to_removed}\\other\\{name_of_file}')
            # Може виникнути помилка якщо файлів з подібним імям надто багато ми їх залишимо на своєму місці це понад 1000 файлів з однаковим імям
        except FileNotFoundError:
            continue    
    return [dict_for_files_images_format],[len(dict_for_files_images_format)],[dict_for_files_video_format],[len(dict_for_files_video_format)],[dict_for_files_textdoc_format],[len(dict_for_files_textdoc_format)],\
           [dict_for_files_music_format],[len(dict_for_files_music_format)],[dict_for_files_archives_format],[len(dict_for_files_archives_format)],[dict_for_files_with_unknown_format],[len(dict_for_files_with_unknown_format)],\
           [list_of_unknown_formats],[len(list_of_unknown_formats)]
    # Повертає список з словниками у такому форматі 
    # Число це індекс словника
    # 0=[Список файлів формату image] 1=[Кількість файлів формату image] 2=[Список файлів формату video] 3=[Кількість файлів формату video]4=[Список файлів формату textdoc]
    # 5=[Кількість файлів формату textdoc] 6=[Список файлів формату music] 7=[Кількість файлів формату music] 8=[Список файлів формату archive]
    # 9=[Кількість файлів формату archive] 10=[Список файлів невідомого формату] 11=[Кількість файлів невідомого формату ] 12=[Список невідомих форматів]
    # 13=[Кількість невідомих форматів]

def unpacking_archive(path:str,archive_name_list:str):
    # Список для запису адреси папки з розархівованими файлами
    list_name_of_folders_with_unpaking_files = []
    # Проходить по списку з назвами файлів які потрібно розархівувати
    for file in archive_name_list:
        # Відділяє формат файлу від загальної назви щоб в подпльшому назвати папку такою ж назвою як файл але без формату у кінці назви
        format_of_file = file.split(".")[-1]
        # Розпаковує архів у папці archives створивши для розпакованих файлів папку з ідентичною назвою до файлу 
        shutil.unpack_archive(f'{path}\\archives\\{file}', f'{path}\\archives\\{file[:file.find(format_of_file)]}')
        # Записує шлях до папки з розпакованим архівом в список
        list_name_of_folders_with_unpaking_files.append(f'{path}\\archives\\{file[:file.find(file.split(".")[-1])-1]}')
    return list_name_of_folders_with_unpaking_files


def creator_for_txt_file_with_result(path:str,result_list_of_sorting:list):
    with open(f'{path}\\result_of_sorting.txt','w',encoding='utf-8') as file:
        file.write(f'Після сортування ми маємо такий результат:\n\
Сортування було виконано {date.today()} о {str(datetime.now().time())[:8]}\n\
Було виявлено таку кількість файлів формату images: {str(result_list_of_sorting[1])[1:-1]}\n\
    Ось перелік файлів цього формату та адрес звідки вони були скопійовані:\n')
        for items in result_list_of_sorting[0]:
            for files in items:
                file.write(f'    {files}: {items[files]}\n')
        file.write(f'Було виявлено таку кількість файлів формату video: {str(result_list_of_sorting[3])[1:-1]}\n\
    Ось перелік файлів цього формату та адрес звідки вони були скопійовані:\n')
        for items in result_list_of_sorting[2]:
            for files in items:
                file.write(f'    {files}: {items[files]}\n')
        file.write(f'Було виявлено таку кількість файлів формату textdoc: {str(result_list_of_sorting[5])[1:-1]}\n\
    Ось перелік файлів цього формату та адрес звідки вони були скопійовані:\n')
        for items in result_list_of_sorting[4]:
            for files in items:
                file.write(f'    {files}: {items[files]}\n')
        file.write(f'Було виявлено таку кількість файлів формату music: {str(result_list_of_sorting[7])[1:-1]}\n\
    Ось перелік файлів цього формату та адрес звідки вони були скопійовані:\n')
        for items in result_list_of_sorting[6]:
            for files in items:
                file.write(f'    {files}: {items[files]}\n')
        file.write(f'Було виявлено таку кількість файлів формату archive: {str(result_list_of_sorting[9])[1:-1]}\n\
    Ось перелік файлів цього формату та адрес звідки вони були скопійовані:\n')
        for items in result_list_of_sorting[8]:
            for files in items:
                file.write(f'    {files}: {items[files]}\n')
        file.write(f'Було виявлено таку кількість файлів невідомого формату: {str(result_list_of_sorting[11])[1:-1]}\n\
    Ось перелік файлів невідомого формату:\n')
        for items in result_list_of_sorting[10]:
            for files in items:
                file.write(f'    {files}: {items[files]}\n')
        file.write(f'Було виявлено таку кількість невідомих форматів файлів: {str(result_list_of_sorting[13])[1:-1]}\n\
Ось перелік невідомих форматів файлів: {str(result_list_of_sorting[12])[2:-2]}\n') 
        

def delete_empty_folder(path:str):
    # Функція видаляє усі порожні папки 
    for dirs in os.listdir(path):
        dir = os.path.join(path, dirs)
        if os.path.isdir(dir):
            delete_empty_folder(dir)
            if not os.listdir(dir):
                os.rmdir(dir)


def sorter_of_files(path:str):
    '''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Функція яка буде запускає правильний поряд виконання функці щоб даний код працюва в правильному порядку
    Даний код зроблений для сортування файлів за їхнім розширенням
    Якщо файлів з однаковим імя буде понад 1000 всі наступні файли залишаться за старою адресою
    Якщо недостатньо дозволів для переміщення або переіменування файлу він також залишеться за старою фдресою
    Всі архіви буде розпаковано в папку та названо відповідно до назви файлу, в цих папках також відбудеться сортування
    Буде створено звіт про переміщені файли в текстовому файлі
    'result_of_sorting.txt' який буде записаний в папку за фдресою переданою для сортування 
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''
    # Записує список з адресами файлів які потрібно відсортувати 
    file_list = list_files(path)
    # Створює папки в які потрібно перемістити відсортовані файли
    folder_creator_for_all_file_tipes(path)
    # Сортує всі файли які були за заданою адресою папки та записує їх в форматі словників 
    result_list_of_sorting = function_of_sorting(file_list,path)
    # Створює текстовий файл за записом статистики по виконанню програми 
    creator_for_txt_file_with_result(path,result_list_of_sorting)
    # Видаляє пусті папки 
    delete_empty_folder(path)
    # Цикл що буде проходитися по файлах в папці архів якщо вони є
    if len(result_list_of_sorting[8][0]) > 0:
        for file in result_list_of_sorting[8]:
            #  Розпаковує архіви в папки з такоюж назвою як файли(без формату) та записує шлях до цих папок
            adres_of_unpacking_files = unpacking_archive(path,file)
            # Запитуємо у користувача чи посортувати файл в розархівованих папках
            sorting_archives_q = input(f'Do you want to sorting unpacking files in {path}\\archive y/n: ') 
            if sorting_archives_q == 'y':
                for item in adres_of_unpacking_files:
                    # Рекурсивно запускає програму для сортування файлів в розпакованих папках
                    sorter_of_files(item)


# Обробляємо помилку якщо було передано неправильні значення для запуску програми
# Та запускаємо саму програму
try:
    path_to_sorting = sys.argv
    if len(path_to_sorting) == 2:
        sorter_of_files(path_to_sorting[1])
except IndexError:
    print('After name of file sort.py must be path to folder what you want sorting')


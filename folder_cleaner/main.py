from pathlib import Path
import shutil
import sys


# Translation
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANS = {}
INVALI_CHAR = set('!@#$%^&*()-+=`~:;}{\/?')

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

for i in INVALI_CHAR:
    TRANS[ord(i)] = "_"

#  Folders and category 
FILE_CATEGORY={
    'images': ['jpeg', 'png', 'jpg', 'svg'],
    'video': ['avi', 'mp4', 'mov', 'mkv'],
    'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    'audio':  ['mp3', 'ogg', 'wav', 'amr'],
    'archives': ['zip', 'gz', 'tar']
    }


# Name normalize
def normalize(name: str) -> str:
    name = name.translate(TRANS) 
    return name

def rename_file(item:Path):
    name = str(item.stem + '_copy' + item.suffix)
    return item.rename(item.parent/name)


# Moving file
def move_file(file: Path, root_dir: Path) -> None:
    suffix = str(file.suffix)[1:]
    ctg = 'unknown'

    for k, v in  FILE_CATEGORY.items():
        if suffix in v:
            ctg = k

    try:
        match ctg:
            case 'images':
                shutil.move(file, root_dir / 'images')
            case 'video':
                shutil.move(file, root_dir / 'video')
            case 'documents':
                shutil.move(file, root_dir / 'documents')
            case 'audio':
                shutil.move(file, root_dir / 'audio')
            case 'archives':
                shutil.move(file, root_dir / 'archives')
            case 'unknown':
                shutil.move(file, root_dir / 'unknown')              
    except shutil.Error:
        file = rename_file(file)
        move_file(file, root_dir)


# Result
def print_result(path: Path):
    result = {}
    for item in path.iterdir():
        count = 0
        for j in item.iterdir():
            count +=1
        result.update({item.name:count})

    print('Відсортовано :')
    print(f"      {result['images']} - зображень")
    print(f"      {result['video']} - відео")
    print(f"      {result['audio']} - аудіо")
    print(f"      {result['documents']} - документів")
    print(f"      {result['archives']} - архівів розпаковано")
    print(f"      {result['unknown']} - невідомих файлів.")


def sort(path: Path, root_dir, first_round = True):
    #Провірка на перший прохід
    folders = []
    if first_round:
        folders = [Path(path/x) for x in FILE_CATEGORY.keys()]
        folders.append(Path(path/'unknown'))
        try:
            p = path / 'tmp_dir'
            p.mkdir()
        except FileExistsError:
            pass
            
        for item in path.iterdir():
            if item in folders:
                try:
                    shutil.move(item, path / 'tmp_dir')
                except shutil.Error:
                    item = rename_file(item)

        for ctg in folders:
            try:
                ctg.mkdir()
            except FileExistsError as exc:
                continue

    # Прохід по папках
    for item in path.iterdir():
        if item in folders:
            continue
        elif item.is_dir():
            sort(item, root_dir, first_round=False)
            item.rmdir()
        elif item.is_file():
            
            new_name = normalize(item.stem)+item.suffix
            item = item.rename(item.parent/new_name)

            if item.suffix[1:] in FILE_CATEGORY['archives']:      
                shutil.unpack_archive(item, path/'archives'/item.stem)
                item.unlink()

            move_file(item, root_dir)

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return"Введіть силку на папку"
    

    if  not path.exists():
        return "Вибачте, папка пуста"
    
    sort(path, path)

    return print_result(path)

if __name__=='__main__':
    main()
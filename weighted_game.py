import json
import random
import os
from tkinter import *
from tkinter import ttk

DATA_FILE = "games.json"
game_list = []
imported_games = [] 
heat_del = 0
local_heat = 0
def mass_import_from_file(filename="games_import.txt"):
    global imported_games
    imported_games = []
    print("Добавляет игры из текстового файла в game_list.\nФормат строки: название|вес|путь\nВес может быть целым или дробным")
  
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден!")
        return 0
    
    added = 0
    errors = 0
    
    with open(filename, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            parts = line.split("|")
            if len(parts) < 2:
                print(f"⚠️ Строка {line_num}: неверный формат (нужно имя|вес|путь)")
                errors += 1
                continue
            
            name = parts[0].strip()
            # Парсим минимальный вес
            try:
                min_weight = float(parts[1].strip())
            except ValueError:
                print(f"⚠️ Строка {line_num}: вес не число, пропускаем")
                errors += 1
                continue
            # Путь опционально
            path = parts[2].strip() if len(parts) >= 3 else ""
            
            # Добавляем игру
            game_list.append({
                "name": name,
                "weight": 10,
                "path": path,
                "min_weight": min_weight 
            })
            imported_games.append({
                "name": name,
                "weight": 10,
                "path": path,
                "min_weight": min_weight 
            })
            added += 1
            print(f"✓ {name} (мин.вес: {min_weight})")
    look_game()
    save_to_json()
    print(f"\n✅ Добавлено {added} игр, ошибок {errors}")
    return added

def rng_weight(number):
    pulweight = game_list[number]['weight'] - game_list[number]['min_weight']
    game_list[number]['weight'] = game_list[number]['min_weight']
    try:
        new_weight = pulweight / (len(game_list)-1)
    except:
        print("Мало игр, фу")
    i = 0
    for game in game_list:
        if i != number:
           game['weight'] += new_weight
        i += 1

def save_to_json():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(game_list, f, ensure_ascii=False, indent=2)
        
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

def load_from_json():
    global game_list
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            game_list = json.load(f)
        print("Список Игра-Вес найден!")
        return True
    except FileNotFoundError:
        print("Файл не найден, создан новый список")
        game_list = []
        return False
    except json.JSONDecodeError:
        print("Ошибка чтения файла! Файл повреждён.")
        game_list = []
        return False
    
def start_game(path):
    if not os.path.exists(path):
        print("Данной директории нет")
        return False
    os.startfile(path)
    return True
load_from_json()


def add_game(): 
    name = ename.get()
    path = (epath.get()+"\\" + name)
    weight_input = eweight.get()
    if weight_input == "": 
       inweights = None
    else:
        try:
            inweights = float(weight_input)
        except ValueError:
            nweights = None
    if inweights is None: 
        game_list.append ({"name": name,"weight": 10,"path": path, "min_weight": 0})
    else: game_list.append ({"name": name,"weight": 10,"path": path, "min_weight": inweights})
    look_game()
    save_to_json()

def look_game():
    game_lists.delete(0, END)  # Очищаем список
    if not game_list:
        game_lists.insert(END, "Список игр пуст!")
        return
    for i, game in enumerate(game_list, 1):
        game_lists.insert(END, f"{i}. {game['name']} - Вес: {game['weight']}")

def delete_game(): 
    global local_heat
    local_heat +=1
    if local_heat == 5:
        local_heat = 0
        i = 0
        for game in game_list:
            i += 1
        ac = int(edel.get())
        try:
            if ac != 0: game_list.pop(ac-1)
        except:
            print("Ошибка: не указана цифра")
        look_game()
        save_to_json()

def randomize():
    weights = [game["weight"] for game in game_list]
    chosen = random.choices(game_list, weights=weights, k=1)[0]
    chosen_index = game_list.index(chosen)  
    rng_weight(chosen_index)
    start_game(chosen['path'])
    desidet.config(text=(f"Выбрано: {chosen['name']}"))
    look_game()
    save_to_json()

def update_listbox():
    game_imp.delete(0, END)
    for i, game in enumerate(imported_games, 1):
        game_imp.insert(
            END, 
            f"{i:>3}. {game['name']} | Путь: {game['path']} | Мин: {game.get('min_weight', '—')}"
        )

def pull_up():
    result_text = mass_import_from_file("games_import.txt")
    update_listbox()
    if result_text > 0:
        game_imp.config(text=f"Импортировано {result_text} игр")
    else:
        game_imp.config(text="Ошибка импорта. Проверьте файл games_import.txt")
    

def wipe_out():
    global heat_del
    heat_del += 1
    if heat_del == 5:
        game_list.clear()
        heat_del = 0
    look_game()
    save_to_json()


#Блок TKinter!!!!!!!!!
root = Tk()
root.title("Weighed-game Roulete")
root.geometry("950x450")
fbuttonfield = Frame(borderwidth=1)
ffinout = Frame(fbuttonfield,borderwidth=1)
ffname = Frame(ffinout,borderwidth=1)
ffpath = Frame(ffinout,borderwidth=1)
ffdel = Frame(ffinout,borderwidth=1)
flistimp = Frame(borderwidth=1)
fflist = Frame(flistimp,borderwidth=1)
ffimp = Frame(flistimp,borderwidth=1)
ffweight = Frame(ffinout,borderwidth=1)
ffbutton = Frame(fbuttonfield, borderwidth=1)
ename = Entry(ffname)
epath = Entry(ffpath, width=70)
eweight = Entry(ffweight)
edel = Entry(ffdel)
game_name = Label(ffname,text="Название")
game_path = Label(ffpath,text="Путь")
game_minweight = Label(ffweight,text="Минимальный вес")
dellab = Label(ffdel,text="Удалить номер..")
desidet = Label(fbuttonfield,text="Судьба за тебя решит...", bg="white")
btn1 = ttk.Button(ffbutton,text="Добавить игру", command=add_game)
btn2 = ttk.Button(ffbutton,text="Стереть список(нажать 5 раз)", command=wipe_out)
btn3 = ttk.Button(ffbutton,text="Удалить игру(нажать 5 раз)", command=delete_game)
btn4 = ttk.Button(ffbutton,text="Рулетка", command=randomize)
btn5 = ttk.Button(ffbutton,text="Пул-ап из файла games_import.txt", command=pull_up)
game_listst = Label(fflist,text="Номер, название, текущий вес", width=50)
game_lists = Listbox(fflist, bg="white", width=60, height= 20)
game_lists.insert(0,"Ожидание games.json")
game_impt = Label(ffimp,text="Список импортируемых игр", width=50)
game_imp = Listbox(ffimp, bg="white" , width=100, height= 20)
game_imp.insert(0,"Ожидание games_import.txt")
fbuttonfield.pack(side='top', pady=25, anchor="center")

ffbutton.pack(side='top')
ffinout.pack(side='top', anchor="center")
ffpath.pack(side='left')
ffname.pack(side='left')
ffweight.pack(side='left')
flistimp.pack(side='top', anchor="center")
fflist.pack(side='left')
ffimp.pack(side='left')
ffdel.pack(side="left")
ename.pack(side='top')
epath.pack(side='top')
eweight.pack(side='top')
game_name.pack(side='top')
edel.pack(side='top')
dellab.pack(side='top')
game_path.pack(side='top')
game_minweight.pack(side='top')
game_listst.pack(side='top')
game_lists.pack(side='top')
desidet.pack(side='top')
game_impt.pack(side='top')
game_imp.pack(side='top')
btn1.pack(side='left')
btn2.pack(side='left')
btn3.pack(side='left')
btn4.pack(side='left')
btn5.pack(side='left')
look_game()
root.mainloop()
"""
while True:
    try:
        menu = int(input("\nМеню рандомайзера, выберите пункт:\n1. Добавить игру\n2. Посмотреть игры и веса\n3. Удалить игру\n4. Рандомизация\n5. Массовый пул-ап игр из текстового файла\n6. Выход\nВыбор  :  "))
    except:
        print("Ошибка: введите цифру")
    if menu == 1:
        name = input("Название:")
        path = input("Путь:")
        weight_input = input("Минимальный вес (Enter - 10 по умолчанию): ")

        if weight_input == "": 
            inweights = None
        else:
            try:
                inweights = float(weight_input)
            except ValueError:
                print("Ошибка: нужно ввести число! Вес = 10 по умолчанию")
                inweights = None

        if inweights is None: 
            game_list.append ({"name": name,"weight": 10,"path": path, "min_weight": 0})
        else: game_list.append ({"name": name,"weight": 10,"path": path, "min_weight": inweights})

        print("Добавлено")
        save_to_json()

    elif menu == 2: 
        print("\n")
        for game in game_list:
            print("Название:", game['name'], "// Вес:", game['weight'])
    elif menu == 3: 
        print("Список игр на удаление:\n")
        i = 0
        for game in game_list:
            i += 1
            print(i,". Название:", game['name'])
        print("\n")   
        try:
            ac = int(input("Номер на удаление?(Для отмены - 0): "))
            if ac != 0: game_list.pop(ac-1)
            else: break
        except:
            print("Ошибка: не указана цифра")
        save_to_json()
    elif menu == 4:
        weights = [game["weight"] for game in game_list]
        chosen = random.choices(game_list, weights=weights, k=1)[0]
        chosen_index = game_list.index(chosen)  
        rng_weight(chosen_index)
        start_game(chosen['path'])
        save_to_json()
    elif menu == 5:
        mass_import_from_file("games_import.txt")
    elif menu == 6: break
    """

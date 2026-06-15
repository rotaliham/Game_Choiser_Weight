import json
import random
import os
import tkinter

DATA_FILE = "games.json"
game_list = []

def mass_import_from_file(filename="games_import.txt"):
    print("Добавляет игры из текстового файла в game_list.\nФормат строки: название|вес|путь\nВес может быть целым или дробным")
  
    if not os.path.exists(filename):
        print(f"❌ Файл {filename} не найден!")
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
            added += 1
            print(f"✓ {name} (мин.вес: {min_weight})")
    
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
import pyautogui
import time
import pyperclip
import json

turno = 1

# Función para guardar tareas en el archivo JSON
def guardar_tareas_en_json(tareas):
    with open('tareas.json', 'w') as f:
        json.dump(tareas, f, indent=4)

# Cargar el contenido actual del archivo JSON
def cargar_tareas_del_json():
    try:
        with open('tareas.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"ntareas": "0", "tareas": {}}

def agregar_tarea(nombre, fecha):
    tareas = cargar_tareas_del_json()
    
    # Crear una nueva tarea
    nueva_tarea = {
        "nombre": nombre,
        "descripcion": "no definido",
        "fecha_entrega": fecha
    }
    
    # Incrementar el contador de tareas
    ntareas = int(tareas["ntareas"]) + 1
    tareas["ntareas"] = str(ntareas)
    
    # Añadir la nueva tarea
    tareas["tareas"][str(ntareas)] = nueva_tarea
    
    # Guardar las tareas actualizadas en el archivo JSON
    guardar_tareas_en_json(tareas)

def listar_tareas():
    tareas = cargar_tareas_del_json()
    ntareas = int(tareas["ntareas"])
    
    if ntareas == 0:
        print("No hay tareas.")
        pyautogui.click(1523, 1003)
        pyautogui.write("No hay tareas actualmente.")
        time.sleep(1)
        pyautogui.press('Enter')
    else:
        print("Tareas:")
        for id_tarea, tarea in tareas["tareas"].items():
            print(f"Tarea {id_tarea}:")
            pyautogui.click(1523, 1003)
            pyautogui.write(f"Tarea {id_tarea}:")
            time.sleep(1)
            pyautogui.press('Enter')
            print(f"  Nombre: {tarea['nombre']}")
            pyautogui.write(f"  Materia: {tarea['nombre']}")
            time.sleep(1)
            pyautogui.press('Enter')
            print(f"  Descripcion: {tarea['descripcion']}")
            pyautogui.write(f"  Descripcion: {tarea['descripcion']}")
            time.sleep(1)
            pyautogui.press('Enter')
            print(f"  Fecha de Entrega: {tarea['fecha_entrega']}")
            pyautogui.write(f"  Fecha de Entrega: {tarea['fecha_entrega']}")
            time.sleep(1)
            pyautogui.press('Enter')

def borrar_tarea_por_id(id_tarea):
    tareas = cargar_tareas_del_json()
    
    if id_tarea in tareas["tareas"]:
        del tareas["tareas"][id_tarea]
        print(f"Tarea con ID {id_tarea} ha sido borrada.")
        
        # Renumerar las tareas restantes
        tareas_renumeradas = {}
        for nuevo_id, (id_original, tarea) in enumerate(tareas["tareas"].items(), start=1):
            tareas_renumeradas[str(nuevo_id)] = tarea
        
        tareas["tareas"] = tareas_renumeradas
        tareas["ntareas"] = str(len(tareas_renumeradas))  # Actualizar el contador de tareas
        
        guardar_tareas_en_json(tareas)
        
        pyautogui.click(1523, 1003)
        pyautogui.write(f"Tarea con ID {id_tarea} ha sido borrada.")
        time.sleep(1)
        pyautogui.press('Enter')
    else:
        print(f"No se encontro la tarea con ID {id_tarea}.")
        pyautogui.click(1523, 1003)
        pyautogui.write(f"No se encontro la tarea con ID {id_tarea}.")
        time.sleep(1)
        pyautogui.press('Enter')

def borrar_todas_las_tareas():
    tareas = {"ntareas": "0", "tareas": {}}
    guardar_tareas_en_json(tareas)
    print("Todas las tareas han sido borradas.")

def actualizar_descripcion_tarea(id_tarea, nueva_descripcion):
    tareas = cargar_tareas_del_json()
    
    if id_tarea in tareas["tareas"]:
        tareas["tareas"][id_tarea]["descripcion"] = nueva_descripcion
        guardar_tareas_en_json(tareas)
        print(f"Descripcion actualizada para la tarea {id_tarea}.")
        pyautogui.click(1523, 1003)
        pyautogui.write(f"Descripcion actualizada para la tarea {id_tarea}.")
        time.sleep(1)
        pyautogui.press('Enter')
    else:
        print(f"No se encontro la tarea con ID {id_tarea}.")
        pyautogui.click(1523, 1003)
        pyautogui.write(f"No se encontro la tarea con ID {id_tarea}.")
        time.sleep(1)
        pyautogui.press('Enter')

while True:
    time.sleep(2.5)

    # Obtener el contenido actual del portapapeles
    for i in range(3):
        if turno == 1:
            pyautogui.click(716, 935)
        else:
            pyautogui.click(1598, 936)
    turno = turno * -1
    pyautogui.hotkey('ctrl', 'c')
    comando = pyperclip.paste()

    if str(comando).startswith('?'):
        # Procesar el comando sin el símbolo '?'
        comando_sin_pregunta = comando[1:].strip()

        if comando_sin_pregunta.startswith('add'):
            # Extraer los parámetros de la tarea
            partes = comando_sin_pregunta[4:].strip().split(' ', 1)
            if len(partes) == 2:
                nombre, fecha = partes
                agregar_tarea(nombre, fecha)
                print("Tarea añadida.")
                pyautogui.click(1523, 1003)
                pyautogui.write("Tarea anadida con exito! Usa ?list para verla.")
                time.sleep(1)
                pyautogui.press('Enter')
            else:
                print("Formato de comando incorrecto. Usa: ?add nombre fecha")
                pyautogui.click(1523, 1003)
                pyautogui.write("Formato de comando incorrecto. Usa: '?add (nombre) (fecha)'")
                time.sleep(1)
                pyautogui.press('Enter')
        elif comando_sin_pregunta.startswith('borrar'):
            partes = comando_sin_pregunta.split(' ', 1)
            if len(partes) == 2:
                id_tarea = partes[1]
                borrar_tarea_por_id(id_tarea)
            else:
                borrar_todas_las_tareas()
                pyautogui.click(1523, 1003)
                pyautogui.write("Todas las tareas han sido borradas.")
                time.sleep(1)
                pyautogui.press('Enter')
        elif comando_sin_pregunta.startswith('list'):
            listar_tareas()
        elif comando_sin_pregunta.startswith('descripcion'):
            partes = comando_sin_pregunta.split(' ', 2)
            if len(partes) == 3:
                id_tarea, nueva_descripcion = partes[1], partes[2]
                actualizar_descripcion_tarea(id_tarea, nueva_descripcion)
            else:
                print("Formato de comando incorrecto. Usa: ?descripcion id_tarea nueva_descripcion")
                pyautogui.click(1523, 1003)
                pyautogui.write("Formato de comando incorrecto. Usa: '?descripcion id_tarea nueva_descripcion'")
                time.sleep(1)
                pyautogui.press('Enter')
        elif comando_sin_pregunta.startswith('help'):
            pyautogui.click(1523, 1003)
            pyautogui.write("Lista de comandos:")
            time.sleep(1)
            pyautogui.press('Enter')
            pyautogui.click(1523, 1003)
            pyautogui.write("'?add (nombre_sin_espacios) (Fecha_sin_espacios)' - Anadir Tarea")
            time.sleep(1)
            pyautogui.press('Enter')
            pyautogui.click(1523, 1003)
            pyautogui.write("'?list' - Lista de tareas")
            time.sleep(1)
            pyautogui.press('Enter')
            pyautogui.click(1523, 1003)
            pyautogui.write("'?descripcion (id_tarea) (nueva_descripcion)' - Actualizar descripcion de la tarea")
            time.sleep(1)
            pyautogui.press('Enter')
            pyautogui.click(1523, 1003)
            pyautogui.write("'?help' - Lista de comandos")
            time.sleep(1)
            pyautogui.press('Enter')
        else:
            print("Comando desconocido.")
            pyautogui.click(1523, 1003)
            pyautogui.write("Comando desconocido.")
            time.sleep(1)
            pyautogui.press('Enter')

    pyautogui.click(1892, 958)
    pyautogui.click(1090, 696)


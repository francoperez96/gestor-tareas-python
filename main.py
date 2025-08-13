import sqlite3

# --- Función para crear la tabla ---
def crear_tabla():
    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN DEFAULT 0,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# --- Función para agregar tarea ---
def agregar_tarea(titulo, descripcion):
    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tareas (titulo, descripcion)
        VALUES (?, ?)
    ''', (titulo, descripcion))
    conn.commit()
    conn.close()
    print(f"✅ Tarea agregada: {titulo}")

# --- Función para listar tareas ---
def listar_tareas():
    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, titulo, descripcion, completada FROM tareas')
    tareas = cursor.fetchall()
    conn.close()

    print("\n📋 Lista de tareas:")
    if not tareas:
        print("No hay tareas guardadas.")
    else:
        for tarea in tareas:
            id, titulo, descripcion, completada = tarea
            estado = "✅" if completada else "🔴"
            print(f"  {estado} [{id}] {titulo}")
            if descripcion:
                print(f"      📝 {descripcion}")

def marcar_completada(id_tarea):
    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    
    # Verificamos si existe la tarea
    cursor.execute('SELECT titulo FROM tareas WHERE id = ?', (id_tarea,))
    tarea = cursor.fetchone()
    
    if tarea is None:
        print(f"❌ No existe una tarea con ID {id_tarea}")
    else:
        cursor.execute('UPDATE tareas SET completada = 1 WHERE id = ?', (id_tarea,))
        conn.commit()
        print(f"✅ Tarea '{tarea[0]}' marcada como completada")
    
    conn.close()

# --- Programa principal ---
if __name__ == '__main__':
    crear_tabla()

    while True:
        print("\n📝 Gestor de Tareas")
        print("1. Agregar una tarea")
        print("2. Listar todas las tareas")
        print("3. Marcar una tarea como completada")
        print("4. Salir")

        opcion = input("Elige una opción (1-4): ").strip()

        if opcion == "1":
            titulo = input("Título de la tarea: ").strip()
            descripcion = input("Descripción (opcional): ").strip()
            if titulo:
                agregar_tarea(titulo, descripcion)
            else:
                print("❌ El título no puede estar vacío")

        elif opcion == "2":
            listar_tareas()

        elif opcion == "3":
            listar_tareas()
            try:
                id_input = input("Ingresá el ID de la tarea a marcar como completada: ").strip()
                id_tarea = int(id_input)
                marcar_completada(id_tarea)
            except ValueError:
                print("❌ Por favor, ingresá un número válido")

        elif opcion == "4":
            print("👋 ¡Hasta luego! Guardaste tus tareas en la base de datos.")
            break  # Sale del bucle

        else:
            print("❌ Opción no válida. Elegí entre 1 y 4.")
        
        # Pausa antes de volver al menú
        input("\nPresioná Enter para continuar...")
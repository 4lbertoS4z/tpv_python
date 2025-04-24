import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from cargar_productos import cargar_productos
import os

productos_por_categoria = cargar_productos()
pedido_actual = {}
imagenes_cache = {}

def mostrar_categoria(categoria):
    for widget in frame_productos.winfo_children():
        widget.destroy()

    for nombre, datos in productos_por_categoria[categoria].items():
        precio = datos["precio"]
        imagen_path = datos.get("imagen", "")

        # Cargar imagen o usar imagen vacía
        if os.path.exists(imagen_path):
            img = Image.open(imagen_path).resize((100, 100))
        else:
            img = Image.new("RGB", (100, 100), "gray")

        photo = ImageTk.PhotoImage(img)
        imagenes_cache[nombre] = photo

        btn = tk.Button(frame_productos, image=photo,
                        text=f"{nombre}\n€{precio:.2f}",
                        compound="top", width=130, height=130,
                        command=lambda n=nombre, p=precio: agregar_producto(n, p))
        btn.pack(side="left", padx=5, pady=5)

def agregar_producto(nombre, precio):
    if nombre in pedido_actual:
        pedido_actual[nombre]["cantidad"] += 1
    else:
        pedido_actual[nombre] = {"precio": precio, "cantidad": 1}
    actualizar_pedido()

def cambiar_cantidad(nombre, delta):
    if nombre in pedido_actual:
        pedido_actual[nombre]["cantidad"] += delta
        if pedido_actual[nombre]["cantidad"] <= 0:
            del pedido_actual[nombre]
    actualizar_pedido()

def actualizar_pedido():
    for widget in frame_lista_pedido.winfo_children():
        widget.destroy()

    total = 0
    for nombre, info in pedido_actual.items():
        cantidad = info["cantidad"]
        precio = info["precio"]
        subtotal = cantidad * precio
        total += subtotal

        fila = tk.Frame(frame_lista_pedido, bg="white")
        fila.pack(anchor="w", fill="x", padx=5)

        tk.Label(fila, text=f"{nombre}", bg="white", width=14, anchor="w").pack(side="left")
        tk.Label(fila, text=f"x{cantidad}", bg="white", width=4).pack(side="left")
        tk.Label(fila, text=f"€{subtotal:.2f}", bg="white", width=8).pack(side="left")

        tk.Button(fila, text="+", width=2, command=lambda n=nombre: cambiar_cantidad(n, 1)).pack(side="left")
        tk.Button(fila, text="–", width=2, command=lambda n=nombre: cambiar_cantidad(n, -1)).pack(side="left")

    label_total.config(text=f"Total: €{total:.2f}")

def cobrar():
    if not pedido_actual:
        messagebox.showwarning("Atención", "No hay productos en el pedido.")
        return
    total = sum(info["precio"] * info["cantidad"] for info in pedido_actual.values())

    def confirmar_pago():
        try:
            recibido = float(entry_pago.get())
            if recibido < total:
                messagebox.showerror("Error", "Dinero insuficiente.")
            else:
                cambio = recibido - total
                messagebox.showinfo("Pago realizado", f"Cambio: €{cambio:.2f}")
                pedido_actual.clear()
                actualizar_pedido()
                ventana_pago.destroy()
        except:
            messagebox.showerror("Error", "Introduce un número válido.")

    ventana_pago = tk.Toplevel(root)
    ventana_pago.title("Cobrar")
    tk.Label(ventana_pago, text=f"Total: €{total:.2f}").pack(pady=10)
    entry_pago = tk.Entry(ventana_pago)
    entry_pago.pack(pady=5)
    tk.Button(ventana_pago, text="Confirmar", command=confirmar_pago).pack(pady=10)

# Interfaz
root = tk.Tk()
root.title("TPV Bar/Cafetería")
root.attributes('-fullscreen', True)

frame_categorias = tk.Frame(root, bg="#ccc")
frame_categorias.pack(fill="x")

for categoria in productos_por_categoria:
    btn_cat = tk.Button(frame_categorias, text=categoria, font=("Arial", 12, "bold"),
                        command=lambda c=categoria: mostrar_categoria(c))
    btn_cat.pack(side="left", padx=10, pady=5)

frame_productos = tk.Frame(root)
frame_productos.pack(side="left", fill="both", expand=True)

frame_pedido = tk.Frame(root, width=300, bg="white")
frame_pedido.pack(side="right", fill="y")

frame_lista_pedido = tk.Frame(frame_pedido, bg="white")
frame_lista_pedido.pack(padx=10, pady=10, fill="both", expand=True)

label_total = tk.Label(frame_pedido, text="Total: €0.00", font=("Arial", 14, "bold"), bg="white")
label_total.pack(pady=10)

tk.Button(frame_pedido, text="Cobrar", font=("Arial", 16, "bold"), bg="green", fg="red", command=cobrar).pack(pady=10)
tk.Button(frame_pedido, text="Salir", font=("Arial", 16, "bold"), bg="red", fg="red", command=root.destroy).pack(pady=10)

# Mostrar primera categoría
primera_categoria = list(productos_por_categoria.keys())[0]
mostrar_categoria(primera_categoria)

root.mainloop()
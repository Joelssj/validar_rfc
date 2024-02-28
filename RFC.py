import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import re
from graphviz import Digraph

def valida_rfc(rfc, exp):
    if exp == "Expresión 1":
        return bool(re.match(r'^L(?:O(?:R(?:J)?)?)?$', rfc, re.IGNORECASE))
    elif exp == "Expresión 2":
        
        return bool(re.match(r'^L[ORJ]{3}$', rfc, re.IGNORECASE))
    return False

def handle_validate():
    rfc = entry.get().upper() 
    selected_exp = exp_combobox.get()
    is_valid = valida_rfc(rfc, selected_exp)
    
    if is_valid:
        result_label.config(text="RFC válido", fg="green")
        diagram = Digraph(comment='Autómata RFC', graph_attr={'rankdir':'LR'})
        diagram.node('start', shape='point')
        diagram.node('q0', shape='circle')
        diagram.edge('start', 'q0')
        current_node = 'q0'
        for i, char in enumerate(rfc):
            next_node = f'q{i+1}'
            diagram.node(next_node, shape='circle')
            diagram.edge(current_node, next_node, label=char)
            current_node = next_node
        diagram.node(next_node, shape='doublecircle')
        diagram.render(f'rfc_diagram_{rfc}', format='png', cleanup=True)
        image = Image.open(f'rfc_diagram_{rfc}.png')
        photo = ImageTk.PhotoImage(image)
        diagram_label.config(image=photo)
        diagram_label.image = photo
    else:
        result_label.config(text="Expresión inválida", fg="red")
        diagram_label.config(image='')

def clear_result(_):
    result_label.config(text="")

root = tk.Tk()
root.title("Validador de RFC")

frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

label = tk.Label(frame, text="RFC: LORJ", font=("Arial", 20), fg="black", bg="white")
label.pack()

entry = tk.Entry(frame, font=("Arial", 16))
entry.pack(pady=10)

exp_combobox_label = tk.Label(frame, text="Seleccione la expresión:", font=("Arial", 16), bg="white")
exp_combobox_label.pack(pady=10)
exp_combobox = ttk.Combobox(frame, values=["Expresión 1", "Expresión 2"], state="readonly", font=("Arial", 16))
exp_combobox.pack(pady=10)
exp_combobox.current(0) 

validate_button = tk.Button(frame, text="Validar RFC", font=("Arial", 16), bg="green", fg="white", command=handle_validate)
validate_button.pack(pady=10)

result_label = tk.Label(frame, text="", font=("Arial", 16), bg="white")
result_label.pack(pady=10)

diagram_label = tk.Label(frame, bg="white")
diagram_label.pack(pady=10)

entry.bind("<KeyRelease>", clear_result)

root.mainloop()


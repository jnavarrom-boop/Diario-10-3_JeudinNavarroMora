import flet as ft
    
def main(page: ft.Page):
    page.title = "Mi primera app con flet"
    mensaje = ft.Text("Aqui va un mensaje")
    nombre = ft.TextField(label="Escriba su nombre" , autofocus=True)
    
    def mostrar_mensaje(txt_mensaje):
        dialogo = ft.AlertDialog(
            title=ft.Text("mensaje"),
            content=ft.Text(txt_mensaje)
        )
        page.show_dialog(dialogo)
        
    def saludar(e):
        if nombre.value.strip() == "":
            mensaje.value = "Hola, Desconocido"
        else:
            mensaje.value = "Hola," + nombre.value
        mostrar_mensaje(mensaje.value)
    
    page.add(
        ft.Text("Jeudin Navarro Mora!"),
        ft.Button("Click aqui!" , on_click = saludar),
        mensaje,
        nombre
    )
    
ft.run(main)
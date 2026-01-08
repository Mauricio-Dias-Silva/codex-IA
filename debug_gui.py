import flet as ft

def main(page: ft.Page):
    page.title = "Teste de Sanidade"
    page.add(ft.Text("Se você está lendo isso, o Flet funciona!", size=30, color="green"))
    page.update()

if __name__ == "__main__":
    ft.app(target=main)

import flet as ft 

import flet as ft
from dataclasses import field

def main(page: ft.page):
    page.title = "Calc App"
    result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)
    
    @ft.control
    class CalcButton(ft.Button):
        expand: int = field(default_factory=lambda: 1)
    @ft.control
    class DigitButton(CalcButton):
        bgcolor: ft.Colors = ft.Colors.WHITE_24
        color: ft.Colors = ft.Colors.WHITE
    @ft.control
    class ActonButton(CalcButton):
        bgcolor: ft.Colors = ft.Colors.ORANGE
        color: ft.Colors = ft.Colors.WHITE
    @ft.control
    class ExtraActionButton(CalcButton):
        bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
        color: ft.Colors = ft.Colors.BLACK
    
    screen_row = ft.Row(controls=[result]),
    row_1 = ft.Row(controls=[ft.Button("AC"), ft.Button("+/-"), ft.Button("%"), ft.Button("/")])
    row_2 = ft.Row(controls=[ft.Button("7"), ft.Button("8"), ft.Button("9"), ft.Button("*")])
    row_3 = ft.Row(controls=[ft.Button("4"), ft.Button("5"), ft.Button("6"), ft.Button("-")])
    row_4 = ft.Row(controls=[ft.Button("1"), ft.Button("2"), ft.Button("3"),ft.Button("+")])
    row_5 = ft.Row(controls=[ft.Button("0"), ft.Button("."), ft.Button("=")])
    
    
    calculator_content = ft.Column(
        controls=[screen_row, row_1, row_2, row_3, row_4, row_5]
    )
    
    calculator = ft.Container(
        width=350,
        bgcolor=ft.Colors.BLACK,
        border_radius=ft.BorderRadius.all(20),
        padding=20,
        content=calculator_content,
    )
    
    page.add(calculator)

if __name__ == "__main__":
    ft.run(main)
    
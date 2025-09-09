import flet as ft

def main(page: ft.Page):
    page.title = "Conversor de Temperatura"
    page.padding = 24
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Campo de entrada
    input_field = ft.TextField(
        label="Valor",
        hint_text="Digite a temperatura",
        prefix_text="",
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=False,
        width=260,
    )

    # Seleção de direção (aperfeiçoamento)
    direction = ft.Dropdown(
        label="Conversão",
        width=260,
        options=[
            ft.dropdown.Option("Celsius → Fahrenheit"),
            ft.dropdown.Option("Fahrenheit → Celsius"),
        ],
        value="Celsius → Fahrenheit",  # Default = versão inicial
    )

    # Saída
    result_text = ft.Text("", size=20, weight=ft.FontWeight.W_600)

    # Mensagem de erro/aviso (usando cor HEX em vez de ft.colors)
    error_text = ft.Text("", color="#FF5252")

    def format_number(x: float) -> str:
        # Formata com no máx. 4 casas e remove zeros desnecessários
        s = f"{x:.4f}"
        s = s.rstrip("0").rstrip(".") if "." in s else s
        return s

    def convert(_=None):
        error_text.value = ""
        result_text.value = ""

        raw = input_field.value.strip().replace(",", ".")
        if raw == "":
            error_text.value = "Digite um valor para converter."
            page.update()
            return
        try:
            val = float(raw)
        except ValueError:
            error_text.value = "Valor inválido. Use apenas números (ex.: 37.5)."
            page.update()
            return

        if direction.value == "Celsius → Fahrenheit":
            # Versão inicial (C → F)
            converted = val * 9 / 5 + 32
            result_text.value = f"{format_number(val)} °C = {format_number(converted)} °F"
        else:
            # Aperfeiçoamento (F → C)
            converted = (val - 32) * 5 / 9
            result_text.value = f"{format_number(val)} °F = {format_number(converted)} °C"

        page.update()

    def clear_fields(_):
        input_field.value = ""
        result_text.value = ""
        error_text.value = ""
        page.update()

    convert_btn = ft.ElevatedButton("Converter", on_click=convert)
    clear_btn = ft.OutlinedButton("Limpar", on_click=clear_fields)

    # Converte ao pressionar Enter
    input_field.on_submit = convert

    # Atualiza placeholder/prefixo conforme direção
    def on_direction_change(e):
        if direction.value == "Celsius → Fahrenheit":
            input_field.label = "Valor em °C"
            input_field.prefix_text = "°C "
        else:
            input_field.label = "Valor em °F"
            input_field.prefix_text = "°F "
        page.update()

    direction.on_change = on_direction_change
    on_direction_change(None)

    card = ft.Card(
        elevation=6,
        content=ft.Container(
            padding=20,
            content=ft.Column(
                width=360,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Text("Conversor de Temperatura", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Versão inicial: °C → °F. Aperfeiçoado para também converter °F → °C.",
                        size=12,
                        color="#666666",
                    ),
                    ft.Divider(),
                    direction,
                    input_field,
                    ft.Row([convert_btn, clear_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=8),
                    error_text,
                    result_text,
                ],
            ),
        ),
    )

    page.add(card)


if __name__ == "__main__":
    ft.app(target=main)

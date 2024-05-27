import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # button for the "hello" reply
        self._title = ft.Text("TdP Flights Manager 2024", color="blue", size=24)
        self._page.controls.append(self._title)

        # row1
        self._txtInNumC = ft.TextField(label = "Num compagnie", width=250)
        self._btnAnalizza = ft.ElevatedButton(text="Analizza aeroporti", width=250, on_click=self._controller.handleAnalizza)
        self._btnConnessi = ft.ElevatedButton(text="Aeroporti connessi", on_click=self._controller.handleConnessi, disabled=True)
        self._btnTestConnessione = ft.ElevatedButton(text="Test connessione", on_click=self._controller.handleTestConnessione,
                                              disabled=True)
        row1 = ft.Row([self._txtInNumC, self._btnAnalizza, self._btnConnessi, self._btnTestConnessione], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        self._DD_aeroprtiPartenza = ft.Dropdown(label="Aeroporti partenza", disabled=True)
        self._DD_aeroprtiArrivo = ft.Dropdown(label="Aeroporti arrivo", disabled=True)
        row2 = ft.Row([self._DD_aeroprtiPartenza, self._DD_aeroprtiArrivo], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self._txtInNumTratte = ft.TextField(label="Numero tratte max", width=250, disabled=True)
        self._btnCercaItinerario = ft.ElevatedButton(text="Cerca itinerario", on_click=self._controller.handleCercaItinerario, disabled=True)
        row3 = ft.Row([self._txtInNumTratte, self._btnCercaItinerario], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()

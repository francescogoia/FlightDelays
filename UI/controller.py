import time

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choice_aeroport_arrivo = None
        self._choice_aeroport_partenza = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()


    def handleAnalizza(self, e):
        nMin_str = self._view._txtInNumC.value
        try:
            nMin_int = int(nMin_str)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero intero"))
            self._view.update_page()
            return
        self._model.build_graph(nMin_int)
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Num nodi: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Num archi: {self._model.getNumArchi()}"))

        self._view._DD_aeroprtiPartenza.disabled = False
        self._view._DD_aeroprtiArrivo.disabled = False
        self._view._btnConnessi.disabled = False
        self._view._btnTestConnessione.disabled = False
        self.fillDD()
        self._view.update_page()

    def handleConnessi(self, e):
        v0 = self._choice_aeroport_partenza
        if v0 is None:
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un aeroporto di partenza"))
            return
        vicini = self._model.getSortedVicini(v0)
        self._view.txt_result.controls.append(ft.Text(f"Ecco i vicini di {v0}"))
        for v in vicini:
            self._view.txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))

        self._view.update_page()
        print("handleConnessi called")

    def handleCercaItinerario(self, e):
        v0 = self._choice_aeroport_partenza
        v1 = self._choice_aeroport_arrivo
        tint = 0
        try:
            tint = int(self._view._txtInNumTratte.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero intero"))
        t0 = time.time()
        path, nTot = self._model.getCamminoOttimo(v0, v1, tint)
        t1 = time.time()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il percorso ottimo fra {v0} e {v1} è:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero totale di voli: {nTot}"))
        self._view.txt_result.controls.append(ft.Text(f"Trovate in {t1 - t0} secondi"))
        self._view.update_page()

    def handleTestConnessione(self, e):
        v0 = self._choice_aeroport_partenza
        v1 = self._choice_aeroport_arrivo
        # verificare che ci sia un percorso
        if not self._model.esistePercorso(v0, v1):
            self._view.txt_result.controls.append(ft.Text(f"Non esiste un percorso fra {v0} e {v1}"))
            return
        else:
            self._view.txt_result.controls.append(ft.Text(f"Esiste un percorso fra {v0} e {v1}"))
            # trovare un possibile percorso
            pathBFS = self._model.trovaCamminoBFS(v0, v1)
            self._view.txt_result.controls.append(ft.Text(f"Il cammino con il minor numero di archi"
                                                          f"tra {v0} e {v1} è: "))
            for p in pathBFS:
                self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view._txtInNumTratte.disabled = False
        self._view._btnCercaItinerario.disabled = False
        self._view.update_page()

    
    def fillDD(self):
        allNodes = self._model.getAllNodes()
        for n in allNodes:
            self._view._DD_aeroprtiPartenza.options.append(
                ft.dropdown.Option(data = n,
                                   on_click=self.readDDAeroportoP,
                                   text=n.AIRPORT))
            self._view._DD_aeroprtiArrivo.options.append(
                ft.dropdown.Option(data=n,
                                   on_click=self.readDDAeroportoA,
                                   text=n.AIRPORT))

    def readDDAeroportoP(self, e):
        if e.control.data is None:
            self._choice_aeroport_partenza = None
        else:
            self._choice_aeroport_partenza = e.control.data
        print(f"readDDAeroortoP called -- {self._choice_aeroport_partenza}")


    def readDDAeroportoA(self, e):
        if e.control.data is None:
            self._choice_aeroport_arrivo = None
        else:
            self._choice_aeroport_arrivo = e.control.data
        print(f"readDDAeroortoA called -- {self._choice_aeroport_arrivo}")

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime, timedelta

class GestioneDipendentiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Dipendenti e Ore Lavorate")
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password='WJ28@krhps',
            database="employee_management"
        )
        self.cursor = self.connection.cursor()

        self.create_widgets()

    def create_widgets(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        gestione_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Gestione", menu=gestione_menu)
        gestione_menu.add_command(label="Gestione Dipendenti", command=self.mostra_gestione_dipendenti)
        gestione_menu.add_command(label="Gestione Orari", command=self.mostra_gestione_orari)

        self.frame_gestione_dipendenti = tk.Frame(self.root)
        self.frame_gestione_orari = tk.Frame(self.root)

        self.mostra_gestione_dipendenti()

    def mostra_gestione_dipendenti(self):
        self.frame_gestione_orari.pack_forget()
        self.frame_gestione_dipendenti.pack(fill="both", expand=True)
        self.crea_form_dipendenti()

    def mostra_gestione_orari(self):
        self.frame_gestione_dipendenti.pack_forget()
        self.frame_gestione_orari.pack(fill="both", expand=True)
        self.crea_form_orari()

    def crea_form_dipendenti(self):
        for widget in self.frame_gestione_dipendenti.winfo_children():
            widget.destroy()

        tk.Label(self.frame_gestione_dipendenti, text="Gestione Dipendenti").pack()

        form_frame = tk.Frame(self.frame_gestione_dipendenti)
        form_frame.pack()

        tk.Label(form_frame, text="Nome").grid(row=0, column=0)
        tk.Label(form_frame, text="Cognome").grid(row=1, column=0)
        tk.Label(form_frame, text="Data di nascita").grid(row=2, column=0)
        tk.Label(form_frame, text="Indirizzo").grid(row=3, column=0)
        tk.Label(form_frame, text="Telefono").grid(row=4, column=0)
        tk.Label(form_frame, text="Email").grid(row=5, column=0)
        tk.Label(form_frame, text="Data di assunzione").grid(row=6, column=0)

        self.nome_entry = tk.Entry(form_frame)
        self.cognome_entry = tk.Entry(form_frame)
        self.data_nascita_entry = tk.Entry(form_frame)
        self.indirizzo_entry = tk.Entry(form_frame)
        self.telefono_entry = tk.Entry(form_frame)
        self.email_entry = tk.Entry(form_frame)
        self.data_assunzione_entry = tk.Entry(form_frame)

        self.nome_entry.grid(row=0, column=1)
        self.cognome_entry.grid(row=1, column=1)
        self.data_nascita_entry.grid(row=2, column=1)
        self.indirizzo_entry.grid(row=3, column=1)
        self.telefono_entry.grid(row=4, column=1)
        self.email_entry.grid(row=5, column=1)
        self.data_assunzione_entry.grid(row=6, column=1)

        tk.Button(form_frame, text="Aggiungi Dipendente", command=self.aggiungi_dipendente).grid(row=7, column=0, columnspan=2)

        search_frame = tk.Frame(self.frame_gestione_dipendenti)
        search_frame.pack()

        tk.Label(search_frame, text="Cerca Dipendente").grid(row=0, column=0, columnspan=2)

        tk.Label(search_frame, text="Nome e Cognome").grid(row=1, column=0)
        self.cerca_dipendente_combobox = ttk.Combobox(search_frame)
        self.cerca_dipendente_combobox.grid(row=1, column=1)
        self.cerca_dipendente_combobox.bind("<KeyRelease>", self.update_cerca_dipendente_combobox)
        self.cerca_dipendente_combobox.bind("<<ComboboxSelected>>", self.visualizza_dipendente)

        tk.Button(search_frame, text="Cerca", command=self.visualizza_dipendente).grid(row=2, column=0, columnspan=2)
        tk.Button(search_frame, text="Pulizia", command=self.reset_dipendente_fields).grid(row=3, column=0, columnspan=2)

    def aggiungi_dipendente(self):
        nome = self.nome_entry.get()
        cognome = self.cognome_entry.get()
        data_nascita = self.data_nascita_entry.get()
        indirizzo = self.indirizzo_entry.get()
        telefono = self.telefono_entry.get()
        email = self.email_entry.get()
        data_assunzione = self.data_assunzione_entry.get()

        try:
            self.cursor.execute(
                "INSERT INTO dipendenti (nome, cognome, data_nascita, indirizzo, telefono, email, data_assunzione) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (nome, cognome, data_nascita, indirizzo, telefono, email, data_assunzione)
            )
            self.connection.commit()
            messagebox.showinfo("Successo", "Dipendente aggiunto con successo!")
            self.reset_dipendente_fields()
        except mysql.connector.Error as err:
            messagebox.showerror("Errore", f"Errore: {err}")

    def update_cerca_dipendente_combobox(self, event):
        search_text = self.cerca_dipendente_combobox.get()
        if search_text:
            try:
                self.cursor.execute(
                    "SELECT CONCAT(nome, ' ', cognome) AS full_name FROM dipendenti WHERE CONCAT(nome, ' ', cognome) LIKE %s",
                    ('%' + search_text + '%',)
                )
                results = self.cursor.fetchall()
                names = [result[0] for result in results]

                self.cerca_dipendente_combobox['values'] = names
                if not self.cerca_dipendente_combobox.get():
                    self.root.after(100, lambda: self.cerca_dipendente_combobox.event_generate('<Down>'))
            except mysql.connector.Error as err:
                messagebox.showerror("Errore", f"Errore: {err}")

    def visualizza_dipendente(self, event=None):
        selected_item = self.cerca_dipendente_combobox.get()
        if not selected_item:
            return

        try:
            self.cursor.execute(
                "SELECT * FROM dipendenti WHERE CONCAT(nome, ' ', cognome) = %s",
                (selected_item,)
            )
            dipendente = self.cursor.fetchone()

            if dipendente:
                self.nome_entry.delete(0, tk.END)
                self.cognome_entry.delete(0, tk.END)
                self.data_nascita_entry.delete(0, tk.END)
                self.indirizzo_entry.delete(0, tk.END)
                self.telefono_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                self.data_assunzione_entry.delete(0, tk.END)

                self.nome_entry.insert(0, dipendente[1])
                self.cognome_entry.insert(0, dipendente[2])
                self.data_nascita_entry.insert(0, dipendente[3])
                self.indirizzo_entry.insert(0, dipendente[4])
                self.telefono_entry.insert(0, dipendente[5])
                self.email_entry.insert(0, dipendente[6])
                self.data_assunzione_entry.insert(0, dipendente[7])
            else:
                messagebox.showinfo("Errore", "Dipendente non trovato.")
        except mysql.connector.Error as err:
            messagebox.showerror("Errore", f"Errore: {err}")

    def reset_dipendente_fields(self):
        self.nome_entry.delete(0, tk.END)
        self.cognome_entry.delete(0, tk.END)
        self.data_nascita_entry.delete(0, tk.END)
        self.indirizzo_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.data_assunzione_entry.delete(0, tk.END)
        self.cerca_dipendente_combobox.set('')
        self.cerca_dipendente_combobox['values'] = []

    def crea_form_orari(self):
        for widget in self.frame_gestione_orari.winfo_children():
            widget.destroy()

        control_frame = tk.Frame(self.frame_gestione_orari)
        control_frame.pack()

        tk.Label(control_frame, text="Seleziona Dipendente").grid(row=0, column=0)

        # Create a Combobox for selecting employees
        self.dipendente_combobox = ttk.Combobox(control_frame)
        self.dipendente_combobox.grid(row=0, column=1)
        self.dipendente_combobox.bind("<KeyRelease>", self.update_combobox)
        self.dipendente_combobox.bind("<<ComboboxSelected>>", self.load_employee_hours)

        # Add buttons for previous and next month
        tk.Button(control_frame, text="Mese Precedente", command=self.mese_precedente).grid(row=1, column=0)
        tk.Button(control_frame, text="Mese Successivo", command=self.mese_successivo).grid(row=1, column=1)

        # Add button for loading hours
        #tk.Button(control_frame, text="Carica", command=self.load_employee_hours).grid(row=1, column=2)

        self.mese_label = tk.Label(control_frame, text=f"{self.current_year}-{self.current_month:02d}")
        self.mese_label.grid(row=1, column=3)

        self.orari_treeview = ttk.Treeview(self.frame_gestione_orari, columns=(
            "Giorno", "Inizio 1", "Fine 1", "Inizio 2", "Fine 2", "Inizio 3", "Fine 3", "Inizio 4", "Fine 4", "Ore Lavorate"), show="headings")
        self.orari_treeview.heading("Giorno", text="Giorno")
        self.orari_treeview.heading("Inizio 1", text="Inizio 1")
        self.orari_treeview.heading("Fine 1", text="Fine 1")
        self.orari_treeview.heading("Inizio 2", text="Inizio 2")
        self.orari_treeview.heading("Fine 2", text="Fine 2")
        self.orari_treeview.heading("Inizio 3", text="Inizio 3")
        self.orari_treeview.heading("Fine 3", text="Fine 3")
        self.orari_treeview.heading("Inizio 4", text="Inizio 4")
        self.orari_treeview.heading("Fine 4", text="Fine 4")
        self.orari_treeview.heading("Ore Lavorate", text="Ore Lavorate")

        self.orari_treeview.column("Giorno", width=80)
        self.orari_treeview.column("Inizio 1", width=100)
        self.orari_treeview.column("Fine 1", width=100)
        self.orari_treeview.column("Inizio 2", width=100)
        self.orari_treeview.column("Fine 2", width=100)
        self.orari_treeview.column("Inizio 3", width=100)
        self.orari_treeview.column("Fine 3", width=100)
        self.orari_treeview.column("Inizio 4", width=100)
        self.orari_treeview.column("Fine 4", width=100)
        self.orari_treeview.column("Ore Lavorate", width=120)

        self.orari_treeview.pack(fill="both", expand=True)
        scroll_x = ttk.Scrollbar(self.frame_gestione_orari, orient="horizontal", command=self.orari_treeview.xview)
        scroll_x.pack(side="bottom", fill="x")
        self.orari_treeview.configure(xscrollcommand=scroll_x.set)

        self.orari_treeview.bind("<Double-1>", self.modifica_orario)

        self.sommario_label = tk.Label(self.frame_gestione_orari, text="Totale Ore Lavorate: 0")
        self.sommario_label.pack()

        self.carica_giorni_mese_corrente()

    def update_combobox(self, event):
        search_text = self.dipendente_combobox.get()
        if search_text:
            try:
                self.cursor.execute(
                    "SELECT CONCAT(nome, ' ', cognome) AS full_name FROM dipendenti WHERE CONCAT(nome, ' ', cognome) LIKE %s",
                    ('%' + search_text + '%',)
                )
                results = self.cursor.fetchall()
                names = [result[0] for result in results]

                self.dipendente_combobox['values'] = names
                if not self.dipendente_combobox.get():
                    self.root.after(100, lambda: self.dipendente_combobox.event_generate('<Down>'))
            except mysql.connector.Error as err:
                messagebox.showerror("Errore", f"Errore: {err}")

    def load_employee_hours(self, event=None):
        selected_item = self.dipendente_combobox.get()
        if not selected_item:
            return

        try:
            self.cursor.execute(
                "SELECT id FROM dipendenti WHERE CONCAT(nome, ' ', cognome) = %s",
                (selected_item,)
            )
            dipendente = self.cursor.fetchone()

            if dipendente:
                self.dipendente_id = dipendente[0]
                totale_ore = 0
                for item in self.orari_treeview.get_children():
                    day = self.orari_treeview.item(item)["values"][0]
                    data = datetime(self.current_year, self.current_month, day).date()
                    self.cursor.execute(
                        "SELECT orario_inizio_1, orario_fine_1, orario_inizio_2, orario_fine_2, orario_inizio_3, orario_fine_3, orario_inizio_4, orario_fine_4 "
                        "FROM ore_lavorate WHERE dipendente_id = %s AND DATE(data) = %s",
                        (self.dipendente_id, data)
                    )
                    result = self.cursor.fetchone()
                    if result:
                        # Assicurati che tutti i valori siano stringhe nel formato "%H:%M:%S"
                        orario_inizio_1 = self.format_time(result[0])
                        orario_fine_1 = self.format_time(result[1])
                        orario_inizio_2 = self.format_time(result[2])
                        orario_fine_2 = self.format_time(result[3])
                        orario_inizio_3 = self.format_time(result[4])
                        orario_fine_3 = self.format_time(result[5])
                        orario_inizio_4 = self.format_time(result[6])
                        orario_fine_4 = self.format_time(result[7])

                        ore_lavorate = (
                            self.calcola_ore_lavorate(orario_inizio_1, orario_fine_1) +
                            self.calcola_ore_lavorate(orario_inizio_2, orario_fine_2) +
                            self.calcola_ore_lavorate(orario_inizio_3, orario_fine_3) +
                            self.calcola_ore_lavorate(orario_inizio_4, orario_fine_4)
                        )
                        self.orari_treeview.item(item, values=(day, orario_inizio_1, orario_fine_1, orario_inizio_2, orario_fine_2, orario_inizio_3, orario_fine_3, orario_inizio_4, orario_fine_4, ore_lavorate))
                        totale_ore += ore_lavorate
                    else:
                        self.orari_treeview.item(item, values=(day, "", "", "", "", "", "", "", "", ""))
                self.sommario_label.config(text=f"Totale Ore Lavorate: {totale_ore:.2f}")
                self.evidenzia_sovrapposizioni()
            else:
                messagebox.showinfo("Errore", "Dipendente non trovato.")
        except mysql.connector.Error as err:
            messagebox.showerror("Errore", f"Errore: {err}")

    def format_time(self, time_value):
        # Converte un valore di orario in stringa nel formato "%H:%M:%S"
        if time_value is None:
            return ""  # Orario predefinito per valori None

        if isinstance(time_value, str):
            return time_value if time_value != "00:00:00" else ""  # Se è già una stringa nel formato corretto, restituiscila

        # Gestisci altri tipi di valori, ad esempio, timedelta o datetime
        if isinstance(time_value, timedelta):
            # Converti timedelta in una stringa nel formato "%H:%M"
            total_seconds = int(time_value.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_time= f"{hours:02}:{minutes:02}"
            return formatted_time if formatted_time != "00:00" else ""

        if isinstance(time_value, datetime):
            formatted_time= time_value.strftime("%H:%M")
            return formatted_time if formatted_time != "00:00" else ""

        return ""  # Valore di fallback


    def mese_precedente(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.mese_label.config(text=f"{self.current_year}-{self.current_month:02d}")
        self.carica_giorni_mese_corrente()

    def mese_successivo(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.mese_label.config(text=f"{self.current_year}-{self.current_month:02d}")
        self.carica_giorni_mese_corrente()

    def carica_giorni_mese_corrente(self):
        for item in self.orari_treeview.get_children():
            self.orari_treeview.delete(item)

        days_in_month = (datetime(self.current_year, self.current_month % 12 + 1, 1) - timedelta(days=1)).day
        for day in range(1, days_in_month + 1):
            self.orari_treeview.insert("", "end", values=(day, "", "", ""))

        # If a dipendente is selected, reload their hours for the current month
        if self.dipendente_combobox.get():
            self.load_employee_hours()
        else:
            self.calcola_ore_lavorate()

    def calcola_ore_lavorate(self, orario_inizio, orario_fine):
        formato_orario = "%H:%M"

        if not orario_inizio or not orario_fine:
            return 0.0

        try:
            # Assicurati che orario_inizio e orario_fine siano stringhe nel formato previsto
            if isinstance(orario_inizio, timedelta):
                orario_inizio = str(orario_inizio)
            if isinstance(orario_fine, timedelta):
                orario_fine = str(orario_fine)

            # Converti le stringhe in oggetti datetime
            inizio = datetime.strptime(orario_inizio, formato_orario)
            fine = datetime.strptime(orario_fine, formato_orario)

            # Calcola la durata e le ore lavorate
            durata = fine - inizio
            ore = durata.total_seconds() / 3600
            return ore
        except ValueError as e:
            print(f"Errore nel formato dell'orario: {e}")
            return 0.0
        except TypeError as e:
            print(f"Errore di tipo: {e}")
            return 0.0
        
    def check_overlap(self, start1, end1, start2, end2):
        """ Verifica se due fasce orarie si sovrappongono. """
        return max(start1, start2) < min(end1, end2)

    def convert_to_datetime(self, orario):
        """ Converte una tupla di orari (inizio, fine) in oggetti datetime. """
        from datetime import datetime

        format_str = "%H:%M"  # Formato dell'orario

        # Controlla se i valori sono vuoti e assegna un valore predefinito se necessario
        if not orario[0] or not orario[1]:
            return datetime.strptime("00:00", format_str), datetime.strptime("00:00", format_str)

        start = datetime.strptime(orario[0], format_str)
        end = datetime.strptime(orario[1], format_str)
        return start, end

    def evidenzia_sovrapposizioni(self):
        for item in self.orari_treeview.get_children():
            values = self.orari_treeview.item(item)["values"]
            if len(values) < 10:
                continue
            
            giorno, inizio1, fine1, inizio2, fine2, inizio3, fine3, inizio4, fine4, _ = values
            
            orari = [
                (inizio1, fine1),
                (inizio2, fine2),
                (inizio3, fine3),
                (inizio4, fine4)
            ]

            # Converte orari in datetime per il confronto
            datetime_orari = [self.convert_to_datetime(orario) for orario in orari]

            overlap_found = False
            for i in range(len(datetime_orari)):
                for j in range(i + 1, len(datetime_orari)):
                    start1, end1 = datetime_orari[i]
                    start2, end2 = datetime_orari[j]
                    
                    if self.check_overlap(start1, end1, start2, end2):
                        overlap_found = True
                        break
                if overlap_found:
                    break

            if overlap_found:
                self.orari_treeview.item(item, tags=('overlap',))

        # Applica colori ai tag dopo aver aggiornato tutte le voci
        self.orari_treeview.tag_configure('overlap', background='red', foreground='white')
    def modifica_orario(self, event):
        selected_item = self.orari_treeview.selection()[0]
        giorno = self.orari_treeview.item(selected_item)["values"][0]
        orario_inizio_1_esistente = self.orari_treeview.item(selected_item)["values"][1]
        orario_fine_1_esistente = self.orari_treeview.item(selected_item)["values"][2]
        orario_inizio_2_esistente = self.orari_treeview.item(selected_item)["values"][3]
        orario_fine_2_esistente = self.orari_treeview.item(selected_item)["values"][4]
        orario_inizio_3_esistente = self.orari_treeview.item(selected_item)["values"][5]
        orario_fine_3_esistente = self.orari_treeview.item(selected_item)["values"][6]
        orario_inizio_4_esistente = self.orari_treeview.item(selected_item)["values"][7]
        orario_fine_4_esistente = self.orari_treeview.item(selected_item)["values"][8]

        modifica_orario_window = tk.Toplevel(self.root)
        modifica_orario_window.title(f"Modifica Orario - Giorno {giorno}")

        tk.Label(modifica_orario_window, text="Orario Inizio 1").grid(row=0, column=0)
        orario_inizio_1_entry = tk.Entry(modifica_orario_window)
        orario_inizio_1_entry.grid(row=0, column=1)
        orario_inizio_1_entry.insert(0, orario_inizio_1_esistente)

        tk.Label(modifica_orario_window, text="Orario Fine 1").grid(row=1, column=0)
        orario_fine_1_entry = tk.Entry(modifica_orario_window)
        orario_fine_1_entry.grid(row=1, column=1)
        orario_fine_1_entry.insert(0, orario_fine_1_esistente)

        tk.Label(modifica_orario_window, text="Orario Inizio 2").grid(row=2, column=0)
        orario_inizio_2_entry = tk.Entry(modifica_orario_window)
        orario_inizio_2_entry.grid(row=2, column=1)
        orario_inizio_2_entry.insert(0, orario_inizio_2_esistente)

        tk.Label(modifica_orario_window, text="Orario Fine 2").grid(row=3, column=0)
        orario_fine_2_entry = tk.Entry(modifica_orario_window)
        orario_fine_2_entry.grid(row=3, column=1)
        orario_fine_2_entry.insert(0, orario_fine_2_esistente)

        tk.Label(modifica_orario_window, text="Orario Inizio 3").grid(row=4, column=0)
        orario_inizio_3_entry = tk.Entry(modifica_orario_window)
        orario_inizio_3_entry.grid(row=4, column=1)
        orario_inizio_3_entry.insert(0, orario_inizio_3_esistente)

        tk.Label(modifica_orario_window, text="Orario Fine 3").grid(row=5, column=0)
        orario_fine_3_entry = tk.Entry(modifica_orario_window)
        orario_fine_3_entry.grid(row=5, column=1)
        orario_fine_3_entry.insert(0, orario_fine_3_esistente)

        tk.Label(modifica_orario_window, text="Orario Inizio 4").grid(row=6, column=0)
        orario_inizio_4_entry = tk.Entry(modifica_orario_window)
        orario_inizio_4_entry.grid(row=6, column=1)
        orario_inizio_4_entry.insert(0, orario_inizio_4_esistente)

        tk.Label(modifica_orario_window, text="Orario Fine 4").grid(row=7, column=0)
        orario_fine_4_entry = tk.Entry(modifica_orario_window)
        orario_fine_4_entry.grid(row=7, column=1)
        orario_fine_4_entry.insert(0, orario_fine_4_esistente)

        tk.Button(modifica_orario_window, text="Salva", command=lambda: self.salva_modifiche(modifica_orario_window, giorno, selected_item,
                                                                                        orario_inizio_1_entry.get(),
                                                                                        orario_fine_1_entry.get(),
                                                                                        orario_inizio_2_entry.get(),
                                                                                        orario_fine_2_entry.get(),
                                                                                        orario_inizio_3_entry.get(),
                                                                                        orario_fine_3_entry.get(),
                                                                                        orario_inizio_4_entry.get(),
                                                                                        orario_fine_4_entry.get())).grid(row=8, column=0, columnspan=2)

    def salva_modifiche(self, window, giorno, item, inizio_1, fine_1, inizio_2, fine_2, inizio_3, fine_3, inizio_4, fine_4):
        giorno_date = datetime(self.current_year, self.current_month, giorno).date()

        try:
            self.cursor.execute(
                "INSERT INTO ore_lavorate (dipendente_id, data, orario_inizio_1, orario_fine_1, orario_inizio_2, orario_fine_2, orario_inizio_3, orario_fine_3, orario_inizio_4, orario_fine_4) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                "ON DUPLICATE KEY UPDATE orario_inizio_1 = VALUES(orario_inizio_1), orario_fine_1 = VALUES(orario_fine_1), orario_inizio_2 = VALUES(orario_inizio_2), orario_fine_2 = VALUES(orario_fine_2), orario_inizio_3 = VALUES(orario_inizio_3), orario_fine_3 = VALUES(orario_fine_3), orario_inizio_4 = VALUES(orario_inizio_4), orario_fine_4 = VALUES(orario_fine_4)",
                (self.dipendente_id, giorno_date, inizio_1, fine_1, inizio_2, fine_2, inizio_3, fine_3, inizio_4, fine_4)
            )
            self.connection.commit()
            self.carica_giorni_mese_corrente()
            window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Errore", f"Errore: {err}")


    def calcola_ore_lavorate(self, orario_inizio, orario_fine):

        if not orario_inizio or not orario_fine:
            return 0
        inizio = datetime.strptime(orario_inizio, "%H:%M")
        fine = datetime.strptime(orario_fine, "%H:%M")
        differenza = fine - inizio
        return differenza.total_seconds() / 3600

if __name__ == "__main__":
    root = tk.Tk()
    app = GestioneDipendentiApp(root)
    root.mainloop()

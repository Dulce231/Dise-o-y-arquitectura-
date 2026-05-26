import tkinter as tk  
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk

try:
    from tkcalendar import DateEntry
except Exception:
    DateEntry = None

from database.db_config import DatabaseConnection
from models.ano import Ano
from models.cliente import Cliente
from models.fallo import Fallo
from models.marca import Marca
from models.modelo import Modelo
from models.refaccion import Refaccion
from models.servicio import Servicio
from models.servicio_fallo import ServicioFallo
from models.servicio_refaccion import ServicioRefaccion
from models.usuario import Usuario
from models.vehiculo import Vehiculo
from utils.reporte import construir_texto_comprobante, generar_comprobante
from utils.session import Session

BG = "#0f172a"
SURFACE = "#111827"
SURFACE_ALT = "#1e293b"
CARD = "#ffffff"
TEXT = "#e5e7eb"
TEXT_DARK = "#0f172a"
ACCENT = "#2563eb"
SUCCESS = "#16a34a"
WARNING = "#f59e0b"
DANGER = "#dc2626"
MUTED = "#64748b"


class AutoTallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoTaller Pro")
        self.geometry("1320x820")
        self.minsize(980, 640)
        self.configure(bg=BG)
        self.protocol("WM_DELETE_WINDOW", self.safe_exit)

        self.db = DatabaseConnection()
        self.session = Session()
        self.usuario_model = Usuario()
        self.cliente_model = Cliente()
        self.vehiculo_model = Vehiculo()
        self.servicio_model = Servicio()
        self.servicio_refaccion_model = ServicioRefaccion()
        self.servicio_fallo_model = ServicioFallo()
        self.marca_model = Marca()
        self.modelo_model = Modelo()
        self.ano_model = Ano()
        self.refaccion_model = Refaccion()
        self.fallo_model = Fallo()

        self.current_user = None
        self.editing_folio = None
        self.catalog_current_id = None
        self.marcas = []
        self.modelos = []
        self.anos = []
        self.refacciones = []
        self.fallos = []
        self.form_vars = {}
        self.stats_vars = {}
        self.service_total_var = tk.StringVar(value="$0.00")
        self.service_total_breakdown_var = tk.StringVar(value="Refacciones: $0.00 | Fallos: $0.00")

        self._configure_styles()
        self.show_login()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=SURFACE_ALT, foreground=TEXT, padding=(18, 10), font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", ACCENT)], foreground=[("selected", "white")])
        style.configure("Treeview", background="white", foreground=TEXT_DARK, rowheight=28, fieldbackground="white", borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#dbeafe", foreground=TEXT_DARK, font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#bfdbfe")], foreground=[("selected", TEXT_DARK)])
        style.configure("Accent.TButton", background=ACCENT, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=10)
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("Success.TButton", background=SUCCESS, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=10)
        style.map("Success.TButton", background=[("active", "#15803d")])

    def _clear_root(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self._clear_root()
        self.editing_folio = None

        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=24, pady=24)
        container.grid_columnconfigure(0, weight=3)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)

        hero = tk.Frame(container, bg=SURFACE, bd=0, highlightthickness=0)
        hero.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        tk.Label(hero, text="AutoTaller Pro", bg=SURFACE, fg="white", font=("Segoe UI", 28, "bold")).pack(anchor="w", padx=32, pady=(40, 8))
        tk.Label(hero, text="Gestión integral para agencia y taller con acceso privado para administradores.", bg=SURFACE, fg="#cbd5e1", font=("Segoe UI", 13), wraplength=520, justify="left").pack(anchor="w", padx=32)

        for item in [
            "• Login privado para administradores",
            "• CRUD visual de marcas, modelos, años y refacciones",
            "• Registro, consulta y modificación por folio o cliente",
            "• Dashboard con estatus y próximos servicios",
        ]:
            tk.Label(hero, text=item, bg=SURFACE, fg="#93c5fd", font=("Segoe UI", 12), anchor="w").pack(fill="x", padx=34, pady=6)

        login = tk.Frame(container, bg=CARD)
        login.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        tk.Label(login, text="Iniciar sesión", bg=CARD, fg=TEXT_DARK, font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=28, pady=(40, 6))
        tk.Label(login, text="Solo el personal administrador puede registrar o modificar servicios.", bg=CARD, fg=MUTED, font=("Segoe UI", 10), wraplength=340, justify="left").pack(anchor="w", padx=28, pady=(0, 20))

        self.username_var = tk.StringVar(value="admin")
        self.password_var = tk.StringVar(value="admin123")
        self._login_field(login, "Usuario", self.username_var)
        self._login_field(login, "Contraseña", self.password_var, show="•")
        ttk.Button(login, text="Entrar al sistema", style="Accent.TButton", command=self._attempt_login).pack(fill="x", padx=28, pady=(18, 10))

        help_box = tk.Frame(login, bg="#eff6ff")
        help_box.pack(fill="x", padx=28, pady=(10, 30))
        tk.Label(help_box, text="Acceso demo", bg="#eff6ff", fg="#1d4ed8", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=14, pady=(12, 2))
        tk.Label(help_box, text="Usuario: admin\nContraseña: admin123", bg="#eff6ff", fg=TEXT_DARK, justify="left", font=("Segoe UI", 10)).pack(anchor="w", padx=14, pady=(0, 12))
        self.bind("<Return>", lambda event: self._attempt_login())

    def _login_field(self, parent, label, variable, show=None):
        tk.Label(parent, text=label, bg=CARD, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=28, pady=(6, 4))
        entry = tk.Entry(parent, textvariable=variable, show=show, relief="flat", bg="#f8fafc", fg=TEXT_DARK, font=("Segoe UI", 11), insertbackground=TEXT_DARK)
        entry.pack(fill="x", padx=28, ipady=9)

    def _attempt_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        user = self.usuario_model.authenticate(username, password)
        if not user:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
            return
        self.session.login(user)
        self.current_user = user
        self.show_main_screen()

    def show_main_screen(self):
        self.unbind("<Return>")
        self._clear_root()

        header = tk.Frame(self, bg=SURFACE)
        header.pack(fill="x")
        tk.Label(header, text="Sistema de servicios automotrices", bg=SURFACE, fg="white", font=("Segoe UI", 20, "bold")).pack(side="left", padx=24, pady=16)

        actions = tk.Frame(header, bg=SURFACE)
        actions.pack(side="right", padx=16)
        tk.Label(actions, text=f"Sesión: {self.current_user.get('nombre', 'Administrador')}", bg=SURFACE, fg="#cbd5e1", font=("Segoe UI", 10)).pack(side="left", padx=12)
        tk.Button(actions, text="Cerrar sesión", command=self.logout, bg="#f59e0b", fg="white", relief="flat", padx=14, pady=7).pack(side="left", padx=4)
        tk.Button(actions, text="Salir del sistema", command=self.safe_exit, bg=DANGER, fg="white", relief="flat", padx=14, pady=7).pack(side="left", padx=4)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=18)
        self.notebook = ttk.Notebook(body)
        self.notebook.pack(fill="both", expand=True)

        self.dashboard_tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.register_tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.services_tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.receipt_tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.catalog_tab = tk.Frame(self.notebook, bg="#f8fafc")

        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.register_tab, text="Registro")
        self.notebook.add(self.services_tab, text="Consulta y control")
        self.notebook.add(self.receipt_tab, text="Comprobante")
        self.notebook.add(self.catalog_tab, text="Catálogos")

        self._build_dashboard_tab()
        self._build_register_tab()
        self._build_services_tab()
        self._build_receipt_tab()
        self._build_catalog_tab()
        self._load_catalogs()
        self.refresh_all()
        self.bind("<Configure>", self._on_window_resize)
        self.after(100, self._update_all_layouts)

    def _build_dashboard_tab(self):
        dashboard_canvas = tk.Canvas(self.dashboard_tab, bg="#f8fafc", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.dashboard_tab, orient="vertical", command=dashboard_canvas.yview)
        dashboard_canvas.configure(yscrollcommand=scrollbar.set)
        
        scroll_frame = tk.Frame(dashboard_canvas, bg="#f8fafc")
        scroll_frame.bind(
            "<Configure>",
            lambda e: dashboard_canvas.configure(scrollregion=dashboard_canvas.bbox("all"))
        )
        dashboard_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        
        def on_mousewheel(event):
            dashboard_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        dashboard_canvas.bind("<MouseWheel>", on_mousewheel)
        scroll_frame.bind("<MouseWheel>", on_mousewheel)
        
        dashboard_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.dashboard_top = tk.Frame(scroll_frame, bg="#f8fafc")
        self.dashboard_top.pack(fill="x", padx=16, pady=16)
        self.stats_vars = {key: tk.StringVar(value="0") for key in ["total", "espera", "proceso", "finalizado"]}

        self.card_frames = []
        cards = [
            ("Servicios totales", self.stats_vars["total"], "#dbeafe"),
            ("En espera", self.stats_vars["espera"], "#fef3c7"),
            ("En proceso", self.stats_vars["proceso"], "#fde68a"),
            ("Finalizados", self.stats_vars["finalizado"], "#dcfce7"),
        ]
        for title, variable, color in cards:
            card = tk.Frame(self.dashboard_top, bg=color, width=220, height=90)
            card.pack(side="left", fill="both", expand=True, padx=8)
            card.pack_propagate(False)
            tk.Label(card, text=title, bg=color, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=16, pady=(14, 4))
            tk.Label(card, textvariable=variable, bg=color, fg=TEXT_DARK, font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=16)
            self.card_frames.append(card)

        self.chart_box = tk.Frame(scroll_frame, bg="white")
        self.chart_box.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(self.chart_box, text="Estatus de solicitudes", bg="white", fg=TEXT_DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(12, 4))

        filter_row = tk.Frame(self.chart_box, bg="white")
        filter_row.pack(fill="x", padx=14)
        self.chart_filter = tk.StringVar(value="total")
        tk.Radiobutton(filter_row, text="Total de registros", variable=self.chart_filter, value="total", command=self.refresh_all, bg="white", fg=TEXT_DARK).pack(side="left")
        tk.Radiobutton(filter_row, text="Solo hoy", variable=self.chart_filter, value="hoy", command=self.refresh_all, bg="white", fg=TEXT_DARK).pack(side="left", padx=8)

        self.chart_canvas = tk.Canvas(self.chart_box, height=240, bg="white", highlightthickness=0)
        self.chart_canvas.pack(fill="x", padx=12, pady=10)

        self.dashboard_lower = tk.Frame(scroll_frame, bg="#f8fafc")
        self.dashboard_lower.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.dashboard_lower.grid_columnconfigure(0, weight=3)
        self.dashboard_lower.grid_columnconfigure(1, weight=2)
        self.dashboard_lower.grid_rowconfigure(0, weight=1)

        self.recent_box = tk.Frame(self.dashboard_lower, bg="white")
        self.recent_box.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(self.recent_box, text="Servicios recientes", bg="white", fg=TEXT_DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=12)
        self.recent_tree = ttk.Treeview(self.recent_box, columns=("folio", "cliente", "placas", "estatus"), show="headings", height=8)
        for col, title, width in [("folio", "Folio", 150), ("cliente", "Cliente", 220), ("placas", "Placas", 120), ("estatus", "Estatus", 120)]:
            self.recent_tree.heading(col, text=title)
            self.recent_tree.column(col, width=width, anchor="center")
        self.recent_tree.pack(fill="both", expand=True, padx=12, pady=(0, 14))

        self.upcoming_box = tk.Frame(self.dashboard_lower, bg="white")
        self.upcoming_box.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(self.upcoming_box, text="Próximos servicios", bg="white", fg=TEXT_DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=12)
        self.upcoming_tree = ttk.Treeview(self.upcoming_box, columns=("folio", "cliente", "fecha"), show="headings", height=8)
        for col, title, width in [("folio", "Folio", 130), ("cliente", "Cliente", 170), ("fecha", "Fecha", 110)]:
            self.upcoming_tree.heading(col, text=title)
            self.upcoming_tree.column(col, width=width, anchor="center")
        self.upcoming_tree.pack(fill="both", expand=True, padx=12, pady=(0, 14))


    def _build_register_tab(self):
        register_canvas = tk.Canvas(self.register_tab, bg="#f8fafc", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.register_tab, orient="vertical", command=register_canvas.yview)
        register_canvas.configure(yscrollcommand=scrollbar.set)
        
        scroll_frame = tk.Frame(register_canvas, bg="#f8fafc")
        scroll_frame.bind(
            "<Configure>",
            lambda e: register_canvas.configure(scrollregion=register_canvas.bbox("all"))
        )
        register_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        
        def on_mousewheel_reg(event):
            register_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        register_canvas.bind_all("<MouseWheel>", on_mousewheel_reg)
        
        register_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        wrapper = tk.Frame(scroll_frame, bg="#f8fafc")
        wrapper.pack(fill="both", expand=True, padx=16, pady=16)
        wrapper.grid_columnconfigure(0, weight=2)
        wrapper.grid_columnconfigure(1, weight=1)
        wrapper.grid_rowconfigure(0, weight=1)
        wrapper.grid_rowconfigure(1, weight=0)
        wrapper.grid_rowconfigure(2, weight=0)

        self.register_wrapper = wrapper
        left = tk.Frame(wrapper, bg="#f8fafc")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left.grid_columnconfigure(0, weight=1)
        left.grid_columnconfigure(1, weight=1)
        self.register_left = left

        self.mode_label = tk.Label(left, text="Modo actual: Nuevo registro", bg="#f8fafc", fg=ACCENT, font=("Segoe UI", 12, "bold"))
        self.mode_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

        defaults = {
            "cliente": "",
            "telefono": "",
            "direccion": "",
            "placas": "",
            "color": "",
            "marca": "",
            "modelo": "",
            "ano": "",
            "quien_llevo": "",
            "fecha_proximo": (date.today() + timedelta(days=180)).isoformat(),
        }
        self.form_vars = {key: tk.StringVar(value=value) for key, value in defaults.items()}

        fields = [
            ("Nombre del dueño", "cliente", 1, 0),
            ("Teléfono", "telefono", 1, 1),
            ("Dirección", "direccion", 2, 0),
            ("Placas", "placas", 2, 1),
            ("Color", "color", 3, 0),
            ("Marca", "marca", 3, 1),
            ("Modelo", "modelo", 4, 0),
            ("Año", "ano", 4, 1),
            ("Quién llevó el vehículo", "quien_llevo", 5, 0),
            ("Próximo servicio", "fecha_proximo", 5, 1),
        ]

        self.inputs = {}
        for label, key, row, col in fields:
            box = tk.Frame(left, bg="#f8fafc")
            box.grid(row=row, column=col, sticky="ew", padx=10, pady=8)
            tk.Label(box, text=label, bg="#f8fafc", fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
            if key in {"marca", "modelo", "ano"}:
                widget = ttk.Combobox(box, textvariable=self.form_vars[key], state="readonly")
                if key == "marca":
                    widget.bind("<<ComboboxSelected>>", self._on_brand_change)
            elif key == "fecha_proximo" and DateEntry is not None:
                widget = DateEntry(
                    box,
                    textvariable=self.form_vars[key],
                    date_pattern="yyyy-mm-dd",
                    background=ACCENT,
                    foreground="white",
                    borderwidth=1,
                    font=("Segoe UI", 10),
                )
            else:
                widget = tk.Entry(box, textvariable=self.form_vars[key], relief="flat", bg="white", fg=TEXT_DARK, font=("Segoe UI", 10), insertbackground=TEXT_DARK)
            widget.pack(fill="x", ipady=7)
            self.inputs[key] = widget

        obs_box = tk.Frame(left, bg="#f8fafc")
        obs_box.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=8)
        tk.Label(obs_box, text="Observaciones", bg="#f8fafc", fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        self.obs_text = tk.Text(
            obs_box,
            height=7,
            relief="solid",
            bd=1,
            bg="white",
            fg=TEXT_DARK,
            insertbackground=TEXT_DARK,
            font=("Segoe UI", 11),
            highlightthickness=1,
            highlightbackground="#cbd5e1",
            highlightcolor=ACCENT,
        )
        self.obs_text.pack(fill="x")

        right = tk.Frame(wrapper, bg="white")
        right.grid(row=0, column=1, sticky="nsew")
        self.register_right = right
        tk.Label(right, text="Tipo de fallo", bg="white", fg=TEXT_DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(14, 6))
        tk.Label(right, text="Selecciona uno o varios fallos comunes del vehículo.", bg="white", fg=MUTED, font=("Segoe UI", 9), wraplength=280, justify="left").pack(anchor="w", padx=14, pady=(0, 8))
        self.fallos_listbox = tk.Listbox(right, selectmode="multiple", exportselection=0, relief="flat", bg="#f8fafc", fg=TEXT_DARK, font=("Segoe UI", 10), height=7)
        self.fallos_listbox.pack(fill="both", expand=False, padx=14, pady=(0, 8))
        self.fallos_listbox.bind("<<ListboxSelect>>", lambda event: self.update_service_total_preview())
        self.fallos_hint = tk.Label(right, text="", bg="white", fg="#475569", font=("Segoe UI", 9), justify="left", wraplength=280)
        self.fallos_hint.pack(anchor="w", padx=14, pady=(0, 10))

        tk.Label(right, text="Refacciones del servicio", bg="white", fg=TEXT_DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(4, 6))
        tk.Label(right, text="Selecciona una o varias refacciones para vincularlas al servicio.", bg="white", fg=MUTED, font=("Segoe UI", 9), wraplength=280, justify="left").pack(anchor="w", padx=14, pady=(0, 8))
        self.refacciones_listbox = tk.Listbox(right, selectmode="multiple", exportselection=0, relief="flat", bg="#f8fafc", fg=TEXT_DARK, font=("Segoe UI", 10), height=7)
        self.refacciones_listbox.pack(fill="both", expand=False, padx=14, pady=(0, 8))
        self.refacciones_listbox.bind("<<ListboxSelect>>", lambda event: self.update_service_total_preview())
        self.refacciones_hint = tk.Label(right, text="", bg="white", fg="#475569", font=("Segoe UI", 9), justify="left", wraplength=280)
        self.refacciones_hint.pack(anchor="w", padx=14, pady=(0, 10))

        summary_box = tk.Frame(right, bg="#eff6ff")
        summary_box.pack(fill="x", padx=14, pady=(0, 14))
        tk.Label(summary_box, text="Total estimado", bg="#eff6ff", fg="#1d4ed8", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=(12, 2))
        tk.Label(summary_box, textvariable=self.service_total_var, bg="#eff6ff", fg=TEXT_DARK, font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=12)
        tk.Label(summary_box, textvariable=self.service_total_breakdown_var, bg="#eff6ff", fg="#475569", font=("Segoe UI", 9), wraplength=260, justify="left").pack(anchor="w", padx=12, pady=(0, 12))

        actions = tk.Frame(wrapper, bg="#f8fafc")
        actions.grid(row=1, column=0, columnspan=2, sticky="e", padx=10, pady=(10, 0))
        ttk.Button(actions, text="Cancelar edición", command=self.clear_form).pack(side="right", padx=6)
        ttk.Button(actions, text="Guardar registro", style="Success.TButton", command=self.save_service).pack(side="right", padx=6)
        self.register_actions = actions

    def _on_window_resize(self, event=None):
        if event is not None and event.widget is not self:
            return
        self._update_all_layouts()

    def _update_all_layouts(self):
        compact = self.winfo_width() < 1220
        extremely_compact = self.winfo_width() < 900
        
        self._update_register_layout(compact)
        self._update_dashboard_layout(compact, extremely_compact)
        self._update_catalog_layout(compact)
        self._update_services_layout(extremely_compact)

    def _update_register_layout(self, compact):
        if not hasattr(self, "register_wrapper"):
            return

        if compact:
            self.register_wrapper.grid_columnconfigure(0, weight=1)
            self.register_wrapper.grid_columnconfigure(1, weight=0)
            self.register_wrapper.grid_rowconfigure(0, weight=1)
            self.register_wrapper.grid_rowconfigure(1, weight=1)
            self.register_wrapper.grid_rowconfigure(2, weight=0)

            self.register_left.grid_configure(row=0, column=0, columnspan=2, padx=(0, 0), pady=(0, 10), sticky="nsew")
            self.register_right.grid_configure(row=1, column=0, columnspan=2, padx=(0, 0), pady=(0, 10), sticky="nsew")
            self.register_actions.grid_configure(row=2, column=0, columnspan=2, sticky="e", padx=10, pady=(10, 0))
        else:
            self.register_wrapper.grid_columnconfigure(0, weight=2)
            self.register_wrapper.grid_columnconfigure(1, weight=1)
            self.register_wrapper.grid_rowconfigure(0, weight=1)
            self.register_wrapper.grid_rowconfigure(1, weight=0)
            self.register_wrapper.grid_rowconfigure(2, weight=0)

            self.register_left.grid_configure(row=0, column=0, columnspan=1, padx=(0, 10), pady=(0, 0), sticky="nsew")
            self.register_right.grid_configure(row=0, column=1, columnspan=1, padx=(0, 0), pady=(0, 0), sticky="nsew")
            self.register_actions.grid_configure(row=1, column=0, columnspan=2, sticky="e", padx=10, pady=(10, 0))

    def _update_dashboard_layout(self, compact, extremely_compact):
        if not hasattr(self, "dashboard_top"):
            return

        for card in self.card_frames:
            if compact:
                card.pack(side="top", fill="x", expand=True, padx=8, pady=4)
                card.pack_propagate(False)
                card.configure(height=80)
            else:
                card.pack(side="left", fill="both", expand=True, padx=8, pady=0)
                card.pack_propagate(False)
                card.configure(height=90)

        if extremely_compact:
            self.dashboard_lower.grid_columnconfigure(0, weight=1)
            self.dashboard_lower.grid_columnconfigure(1, weight=0)
            self.dashboard_lower.grid_rowconfigure(0, weight=1)
            self.dashboard_lower.grid_rowconfigure(1, weight=1)
            
            self.recent_box.grid_configure(row=0, column=0, columnspan=1, sticky="nsew", padx=(0, 0), pady=(0, 8))
            self.upcoming_box.grid_configure(row=1, column=0, columnspan=1, sticky="nsew", padx=(0, 0), pady=(0, 0))
        else:
            self.dashboard_lower.grid_columnconfigure(0, weight=3)
            self.dashboard_lower.grid_columnconfigure(1, weight=2)
            self.dashboard_lower.grid_rowconfigure(0, weight=1)
            
            self.recent_box.grid_configure(row=0, column=0, columnspan=1, sticky="nsew", padx=(0, 8), pady=(0, 0))
            self.upcoming_box.grid_configure(row=0, column=1, columnspan=1, sticky="nsew", padx=(8, 0), pady=(0, 0))

    def _update_catalog_layout(self, compact):
        if not hasattr(self, "catalog_body"):
            return

        if compact:
            self.catalog_body.grid_columnconfigure(0, weight=1)
            self.catalog_body.grid_columnconfigure(1, weight=0)
            self.catalog_body.grid_rowconfigure(0, weight=1)
            self.catalog_body.grid_rowconfigure(1, weight=1)
            
            self.catalog_left.grid_configure(row=0, column=0, columnspan=2, sticky="nsew", padx=(0, 0), pady=(0, 10))
            self.catalog_right.grid_configure(row=1, column=0, columnspan=2, sticky="nsew", padx=(0, 0), pady=(0, 0))
        else:
            self.catalog_body.grid_columnconfigure(0, weight=2)
            self.catalog_body.grid_columnconfigure(1, weight=1)
            self.catalog_body.grid_rowconfigure(0, weight=1)
            
            self.catalog_left.grid_configure(row=0, column=0, columnspan=1, sticky="nsew", padx=(0, 10), pady=(0, 0))
            self.catalog_right.grid_configure(row=0, column=1, columnspan=1, sticky="nsew", padx=(0, 0), pady=(0, 0))

    def _update_services_layout(self, extremely_compact):
        if not hasattr(self, "services_bottom"):
            return

        if extremely_compact:
            for widget in self.services_bottom.winfo_children():
                widget.pack(side="top", fill="x", expand=True, padx=2, pady=2)
        else:
            for i, widget in enumerate(self.services_bottom.winfo_children()):
                if widget.cget("text") == "Eliminar":
                    widget.pack(side="right", padx=4)
                else:
                    widget.pack(side="left", padx=4)

    def _build_services_tab(self):
        services_canvas = tk.Canvas(self.services_tab, bg="#f8fafc", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.services_tab, orient="vertical", command=services_canvas.yview)
        services_canvas.configure(yscrollcommand=scrollbar.set)
        
        scroll_frame = tk.Frame(services_canvas, bg="#f8fafc")
        scroll_frame.bind(
            "<Configure>",
            lambda e: services_canvas.configure(scrollregion=services_canvas.bbox("all"))
        )
        services_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        
        def on_mousewheel_srv(event):
            services_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        services_canvas.bind_all("<MouseWheel>", on_mousewheel_srv)
        
        services_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.services_top = tk.Frame(scroll_frame, bg="#f8fafc")
        self.services_top.pack(fill="x", padx=16, pady=16)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.services_top, textvariable=self.search_var, relief="flat", bg="white", fg=TEXT_DARK, font=("Segoe UI", 10), insertbackground=TEXT_DARK)
        search_entry.pack(side="left", fill="x", expand=True, ipady=8)
        ttk.Button(self.services_top, text="Buscar por folio o dueño", command=self.refresh_services_table).pack(side="left", padx=8)
        ttk.Button(self.services_top, text="Ver todo", command=self._reset_search).pack(side="left")

        self.services_table_box = tk.Frame(scroll_frame, bg="white")
        self.services_table_box.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        columns = ("folio", "cliente", "placas", "estatus", "proximo", "llevo")
        self.service_tree = ttk.Treeview(self.services_table_box, columns=columns, show="headings")
        config = [
            ("folio", "Folio", 160),
            ("cliente", "Dueño", 180),
            ("placas", "Placas", 120),
            ("estatus", "Estatus", 110),
            ("proximo", "Próximo servicio", 140),
            ("llevo", "Quién llevó", 160),
        ]
        for col, title, width in config:
            self.service_tree.heading(col, text=title)
            self.service_tree.column(col, width=width, anchor="center")
        self.service_tree.pack(fill="both", expand=True, padx=12, pady=12)
        self.service_tree.bind("<Double-1>", lambda event: self.load_selected_service_for_edit())

        self.services_bottom = tk.Frame(scroll_frame, bg="#f8fafc")
        self.services_bottom.pack(fill="x", padx=16, pady=(0, 16))
        ttk.Button(self.services_bottom, text="Cargar para editar", command=self.load_selected_service_for_edit).pack(side="left", padx=4)
        ttk.Button(self.services_bottom, text="Comprobante", command=self.generate_selected_receipt).pack(side="left", padx=4)
        ttk.Button(self.services_bottom, text="En espera", command=lambda: self.update_status("En espera")).pack(side="left", padx=4)
        ttk.Button(self.services_bottom, text="En proceso", command=lambda: self.update_status("En proceso")).pack(side="left", padx=4)
        ttk.Button(self.services_bottom, text="Finalizado", style="Success.TButton", command=lambda: self.update_status("Finalizado")).pack(side="left", padx=4)
        ttk.Button(self.services_bottom, text="Eliminar", command=self.delete_selected_service).pack(side="right", padx=4)

    def _build_receipt_tab(self):
        wrapper = tk.Frame(self.receipt_tab, bg="#f8fafc")
        wrapper.pack(fill="both", expand=True, padx=16, pady=16)

        header = tk.Frame(wrapper, bg="white")
        header.pack(fill="x")
        tk.Label(header, text="Vista previa del comprobante", bg="white", fg=TEXT_DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(12, 2))
        tk.Label(header, text="Se actualiza al guardar un servicio o al generar un comprobante desde consulta.", bg="white", fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=14, pady=(0, 10))

        viewer = tk.Frame(wrapper, bg="white")
        viewer.pack(fill="both", expand=True, pady=(10, 0))
        scrollbar = tk.Scrollbar(viewer)
        scrollbar.pack(side="right", fill="y")
        self.receipt_text = tk.Text(
            viewer,
            wrap="word",
            relief="flat",
            bg="white",
            fg=TEXT_DARK,
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            padx=16,
            pady=12,
        )
        self.receipt_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.receipt_text.yview)
        self.receipt_text.insert(
            "1.0",
            "Aun no hay comprobante para mostrar.\n\n"
            "1) Registra o actualiza un servicio para generar uno automaticamente.\n"
            "2) O selecciona un servicio en 'Consulta y control' y presiona 'Comprobante'.",
        )
        self.receipt_text.config(state="disabled")

    def _show_receipt_in_tab(self, folio, datos_servicio):
        contenido = construir_texto_comprobante(folio, datos_servicio)
        self.receipt_text.config(state="normal")
        self.receipt_text.delete("1.0", "end")
        self.receipt_text.insert("1.0", contenido)
        self.receipt_text.config(state="disabled")
        self.notebook.select(self.receipt_tab)

    def _build_catalog_tab(self):
        catalog_canvas = tk.Canvas(self.catalog_tab, bg="#f8fafc", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.catalog_tab, orient="vertical", command=catalog_canvas.yview)
        catalog_canvas.configure(yscrollcommand=scrollbar.set)
        
        scroll_frame = tk.Frame(catalog_canvas, bg="#f8fafc")
        scroll_frame.bind(
            "<Configure>",
            lambda e: catalog_canvas.configure(scrollregion=catalog_canvas.bbox("all"))
        )
        catalog_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        
        def on_mousewheel_cat(event):
            catalog_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        catalog_canvas.bind_all("<MouseWheel>", on_mousewheel_cat)
        
        catalog_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.catalog_wrapper = tk.Frame(scroll_frame, bg="#f8fafc")
        self.catalog_wrapper.pack(fill="both", expand=True, padx=16, pady=16)

        self.catalog_top = tk.Frame(self.catalog_wrapper, bg="#f8fafc")
        self.catalog_top.pack(fill="x", pady=(0, 12))
        tk.Label(self.catalog_top, text="Catálogo a administrar:", bg="#f8fafc", fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.catalog_var = tk.StringVar(value="Marcas")
        catalog_combo = ttk.Combobox(self.catalog_top, textvariable=self.catalog_var, state="readonly", values=["Marcas", "Modelos", "Años", "Refacciones", "Fallos"], width=20)
        catalog_combo.pack(side="left", padx=10)
        catalog_combo.bind("<<ComboboxSelected>>", self.on_catalog_change)

        self.catalog_body = tk.Frame(self.catalog_wrapper, bg="#f8fafc")
        self.catalog_body.pack(fill="both", expand=True)
        self.catalog_body.grid_columnconfigure(0, weight=2)
        self.catalog_body.grid_columnconfigure(1, weight=1)
        self.catalog_body.grid_rowconfigure(0, weight=1)

        self.catalog_left = tk.Frame(self.catalog_body, bg="white")
        self.catalog_left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.catalog_tree = ttk.Treeview(self.catalog_left, show="headings")
        self.catalog_tree.pack(fill="both", expand=True, padx=12, pady=12)
        self.catalog_tree.bind("<<TreeviewSelect>>", lambda event: self.load_catalog_item())

        self.catalog_right = tk.Frame(self.catalog_body, bg="white")
        self.catalog_right.grid(row=0, column=1, sticky="nsew")
        tk.Label(self.catalog_right, text="Formulario de catálogo", bg="white", fg=TEXT_DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(14, 8))
        self.catalog_form_frame = tk.Frame(self.catalog_right, bg="white")
        self.catalog_form_frame.pack(fill="both", expand=True, padx=14)
        self.catalog_button_row = tk.Frame(self.catalog_right, bg="white")
        self.catalog_button_row.pack(fill="x", padx=14, pady=14)
        ttk.Button(self.catalog_button_row, text="Nuevo", command=self.clear_catalog_form).pack(side="left", padx=4)
        ttk.Button(self.catalog_button_row, text="Guardar", style="Success.TButton", command=self.save_catalog_item).pack(side="left", padx=4)
        ttk.Button(self.catalog_button_row, text="Eliminar", command=self.delete_catalog_item).pack(side="left", padx=4)
        self.on_catalog_change()

    def _load_catalogs(self):
        self.marcas = self.marca_model.get_all()
        self.modelos = self.modelo_model.get_all()
        self.anos = self.ano_model.get_all()
        self.refacciones = self.refaccion_model.get_all()
        self.fallos = self.fallo_model.get_all()

        if hasattr(self, "inputs"):
            self.inputs["marca"]["values"] = [m["nombre"] for m in self.marcas]
            self.inputs["ano"]["values"] = [str(a["año"]) for a in self.anos]
            self.inputs["modelo"]["values"] = []
            if self.marcas:
                if not self.form_vars.get("marca", tk.StringVar()).get():
                    self.form_vars["marca"].set(self.marcas[0]["nombre"])
                self._on_brand_change()
            if self.anos and not self.form_vars.get("ano", tk.StringVar()).get():
                self.form_vars["ano"].set(str(self.anos[0]["año"]))

        if hasattr(self, "refacciones_listbox"):
            self.refacciones_listbox.delete(0, "end")
            for item in self.refacciones:
                self.refacciones_listbox.insert("end", f"{item['nombre']} | ${float(item['precio']):,.2f} | stock {item['stock']}")
            self.refacciones_hint.config(text=f"Disponibles: {len(self.refacciones)}")

        if hasattr(self, "fallos_listbox"):
            self.fallos_listbox.delete(0, "end")
            for item in self.fallos:
                self.fallos_listbox.insert("end", f"{item['nombre']} | ${float(item['costo']):,.2f}")
            self.fallos_hint.config(text=f"Disponibles: {len(self.fallos)}")

        if hasattr(self, "catalog_var"):
            self.on_catalog_change()
        self.update_service_total_preview()

    def _on_brand_change(self, event=None):
        brand = self.form_vars["marca"].get()
        marca = next((m for m in self.marcas if m["nombre"] == brand), None)
        filtered = [m["nombre"] for m in self.modelos if marca and m["marca_id"] == marca["id"]]
        if not filtered:
            filtered = [m["nombre"] for m in self.modelos]
        self.inputs["modelo"]["values"] = filtered
        if filtered and self.form_vars["modelo"].get() not in filtered:
            self.form_vars["modelo"].set(filtered[0])

    def _get_filtered_services(self):
        services = self.servicio_model.get_all()
        if self.chart_filter.get() == "hoy":
            today = date.today().isoformat()
            return [s for s in services if str(s.get("fecha_registro", ""))[:10] == today]
        return services

    def _draw_chart(self, services):
        self.chart_canvas.delete("all")
        self.chart_canvas.update_idletasks()
        width = max(self.chart_canvas.winfo_width(), 700)
        height = 230
        self.chart_canvas.config(width=width, height=height)

        counts = {
            "En espera": sum(1 for s in services if s["estatus"] == "En espera"),
            "En proceso": sum(1 for s in services if s["estatus"] == "En proceso"),
            "Finalizado": sum(1 for s in services if s["estatus"] == "Finalizado"),
        }
        colors = {"En espera": "#f59e0b", "En proceso": "#fb923c", "Finalizado": "#16a34a"}
        max_count = max(counts.values()) if counts else 1
        x_positions = [140, 360, 580]

        self.chart_canvas.create_line(60, 190, width - 40, 190, fill="#cbd5e1", width=2)
        for i, (label, value) in enumerate(counts.items()):
            bar_height = 0 if max_count == 0 else int((value / max_count) * 120)
            x = x_positions[i]
            self.chart_canvas.create_rectangle(x, 190 - bar_height, x + 90, 190, fill=colors[label], width=0)
            self.chart_canvas.create_text(x + 45, 175 - bar_height, text=str(value), fill=TEXT_DARK, font=("Segoe UI", 11, "bold"))
            self.chart_canvas.create_text(x + 45, 208, text=label, fill=TEXT_DARK, font=("Segoe UI", 10))

    def refresh_all(self):
        services = self.servicio_model.get_all()
        self.stats_vars["total"].set(str(len(services)))
        self.stats_vars["espera"].set(str(sum(1 for s in services if s["estatus"] == "En espera")))
        self.stats_vars["proceso"].set(str(sum(1 for s in services if s["estatus"] == "En proceso")))
        self.stats_vars["finalizado"].set(str(sum(1 for s in services if s["estatus"] == "Finalizado")))

        for tree in [self.recent_tree, self.upcoming_tree]:
            for item in tree.get_children():
                tree.delete(item)

        for service in services[:12]:
            self.recent_tree.insert("", "end", values=(service["folio"], service["cliente_nombre"], service["placas"], service["estatus"]))

        upcoming = [s for s in services if s.get("fecha_proximo_servicio")]
        upcoming.sort(key=lambda s: str(s.get("fecha_proximo_servicio", "")))
        for service in upcoming[:12]:
            self.upcoming_tree.insert("", "end", values=(service["folio"], service["cliente_nombre"], service["fecha_proximo_servicio"]))

        self._draw_chart(self._get_filtered_services())
        self.refresh_services_table()
        if hasattr(self, "catalog_tree"):
            self.refresh_catalog_table()

    def refresh_services_table(self):
        text = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
        services = self.servicio_model.get_all()
        for item in self.service_tree.get_children():
            self.service_tree.delete(item)

        for service in services:
            haystack = f"{service['folio']} {service['cliente_nombre']} {service['placas']} {service.get('quien_llevo', '')}".lower()
            if text and text not in haystack:
                continue
            self.service_tree.insert("", "end", values=(service["folio"], service["cliente_nombre"], service["placas"], service["estatus"], service.get("fecha_proximo_servicio", ""), service.get("quien_llevo", "")))

    def _reset_search(self):
        self.search_var.set("")
        self.refresh_services_table()

    def clear_form(self):
        self.editing_folio = None
        self.mode_label.config(text="Modo actual: Nuevo registro")
        for key, variable in self.form_vars.items():
            if key == "fecha_proximo":
                variable.set((date.today() + timedelta(days=180)).isoformat())
            else:
                variable.set("")
        self.obs_text.delete("1.0", "end")
        if DateEntry is not None and "fecha_proximo" in self.inputs:
            try:
                self.inputs["fecha_proximo"].set_date(self.form_vars["fecha_proximo"].get())
            except Exception:
                pass
        if hasattr(self, "refacciones_listbox"):
            self.refacciones_listbox.selection_clear(0, "end")
        if hasattr(self, "fallos_listbox"):
            self.fallos_listbox.selection_clear(0, "end")
        self._load_catalogs()
        self.update_service_total_preview()

    def _get_selected_refaccion_ids(self):
        return [self.refacciones[index]["id"] for index in self.refacciones_listbox.curselection()] if self.refacciones else []

    def _get_selected_fallo_ids(self):
        return [self.fallos[index]["id"] for index in self.fallos_listbox.curselection()] if self.fallos else []

    def _format_currency(self, value):
        return f"${float(value or 0):,.2f}"

    def _sum_refacciones(self, refacciones):
        return sum(float(item.get("precio", 0) or 0) * int(item.get("cantidad", 1) or 1) for item in refacciones)

    def _sum_fallos(self, fallos):
        return sum(float(item.get("costo", 0) or 0) * int(item.get("cantidad", 1) or 1) for item in fallos)

    def update_service_total_preview(self):
        if not hasattr(self, "refacciones_listbox") or not hasattr(self, "fallos_listbox"):
            return 0.0, 0.0, 0.0

        selected_refacciones = set(self._get_selected_refaccion_ids())
        selected_fallos = set(self._get_selected_fallo_ids())
        total_refacciones = sum(float(item.get("precio", 0) or 0) * int(item.get("cantidad", 1) or 1) for item in self.refacciones if item["id"] in selected_refacciones)
        total_fallos = sum(float(item.get("costo", 0) or 0) * int(item.get("cantidad", 1) or 1) for item in self.fallos if item["id"] in selected_fallos)
        total_general = total_refacciones + total_fallos
        self.service_total_var.set(self._format_currency(total_general))
        self.service_total_breakdown_var.set(f"Refacciones: {self._format_currency(total_refacciones)} | Fallos: {self._format_currency(total_fallos)}")
        return total_refacciones, total_fallos, total_general

    def _get_service_details(self, folio):
        datos = self.servicio_model.get_by_folio(folio) or {}
        datos["refacciones"] = self.servicio_refaccion_model.get_by_service(folio)
        datos["fallos"] = self.servicio_fallo_model.get_by_service(folio)
        datos["total_refacciones"] = self.servicio_refaccion_model.get_total_by_service(folio)
        datos["total_fallos"] = self.servicio_fallo_model.get_total_by_service(folio)
        datos["total_general"] = float(datos["total_refacciones"]) + float(datos["total_fallos"])
        return datos

    def save_service(self):
        try:
            nombre = self.form_vars["cliente"].get().strip()
            telefono = self.form_vars["telefono"].get().strip()
            direccion = self.form_vars["direccion"].get().strip()
            placas = self.form_vars["placas"].get().strip().upper()
            color = self.form_vars["color"].get().strip()
            marca_nombre = self.form_vars["marca"].get().strip()
            modelo_nombre = self.form_vars["modelo"].get().strip()
            ano_valor = self.form_vars["ano"].get().strip()
            quien_llevo = self.form_vars["quien_llevo"].get().strip()
            fecha_proximo = self.form_vars["fecha_proximo"].get().strip()
            observaciones = self.obs_text.get("1.0", "end").strip()
            refaccion_ids = self._get_selected_refaccion_ids()
            fallo_ids = self._get_selected_fallo_ids()

            refacciones_validas = {item["id"] for item in self.refacciones}
            fallos_validos = {item["id"] for item in self.fallos}
            if any(refaccion_id not in refacciones_validas for refaccion_id in refaccion_ids):
                messagebox.showerror("Datos inválidos", "Hay una refacción seleccionada que ya no existe.")
                return
            if any(fallo_id not in fallos_validos for fallo_id in fallo_ids):
                messagebox.showerror("Datos inválidos", "Hay un fallo seleccionado que ya no existe.")
                return

            required = [nombre, placas, marca_nombre, modelo_nombre, ano_valor, quien_llevo]
            if not all(required):
                messagebox.showwarning("Datos incompletos", "Completa los campos obligatorios antes de guardar.")
                return

            marca = next((m for m in self.marcas if m["nombre"] == marca_nombre), None)
            modelo = next((m for m in self.modelos if m["nombre"] == modelo_nombre and marca and m["marca_id"] == marca["id"]), None)
            if not modelo:
                modelo = next((m for m in self.modelos if m["nombre"] == modelo_nombre), None)
            ano = next((a for a in self.anos if str(a["año"]) == ano_valor), None)
            if not (marca and modelo and ano):
                messagebox.showerror("Catálogo incompleto", "Selecciona marca, modelo y año válidos.")
                return

            if self.editing_folio:
                actual = self.servicio_model.get_by_folio(self.editing_folio)
                cliente_id = actual["cliente_id"]
                vehiculo_id = actual["vehiculo_id"]
                self.cliente_model.update(cliente_id, nombre, telefono, direccion)
                self.vehiculo_model.update(vehiculo_id, cliente_id, marca["id"], modelo["id"], ano["id"], placas, color)
                self.servicio_model.update(self.editing_folio, vehiculo_id, cliente_id, fecha_proximo, quien_llevo, observaciones)
                folio = self.editing_folio
                mensaje = "Servicio actualizado"
            else:
                clientes = self.cliente_model.get_by_name(nombre)
                cliente = next((c for c in clientes if c["nombre"].strip().lower() == nombre.lower()), None)
                cliente_id = cliente["id"] if cliente else self.cliente_model.create(nombre, telefono, direccion)

                vehiculos = self.vehiculo_model.get_by_placas(placas)
                vehiculo_id = vehiculos[0]["id"] if vehiculos else self.vehiculo_model.create(cliente_id, marca["id"], modelo["id"], ano["id"], placas, color)
                folio = self.servicio_model.create(vehiculo_id, cliente_id, quien_llevo, fecha_proximo, observaciones)
                mensaje = "Servicio registrado"

            if not folio:
                messagebox.showerror("Error", "No fue posible guardar el servicio.")
                return

            self.servicio_refaccion_model.replace_for_service(folio, refaccion_ids)
            self.servicio_fallo_model.replace_for_service(folio, fallo_ids)
            datos = self._get_service_details(folio)
            comprobante = generar_comprobante(folio, datos)
            self._show_receipt_in_tab(folio, datos)

            messagebox.showinfo(mensaje, f"Operación completada correctamente.\nFolio: {folio}\nComprobante: {comprobante}")
            self.clear_form()
            self.refresh_all()
        except Exception as exc:
            messagebox.showerror("Error inesperado", str(exc))

    def _get_selected_folio(self):
        selected = self.service_tree.selection()
        if not selected:
            messagebox.showwarning("Selecciona un servicio", "Elige un registro en la tabla primero.")
            return None
        return self.service_tree.item(selected[0], "values")[0]

    def load_selected_service_for_edit(self):
        folio = self._get_selected_folio()
        if not folio:
            return
        servicio = self.servicio_model.get_by_folio(folio)
        if not servicio:
            messagebox.showerror("No encontrado", "No fue posible cargar el servicio seleccionado.")
            return

        self.editing_folio = folio
        self.mode_label.config(text=f"Modo actual: Editando {folio}")
        self.form_vars["cliente"].set(servicio.get("cliente_nombre", ""))
        self.form_vars["telefono"].set(servicio.get("telefono", ""))
        self.form_vars["direccion"].set(servicio.get("direccion", ""))
        self.form_vars["placas"].set(servicio.get("placas", ""))
        self.form_vars["color"].set(servicio.get("color", ""))
        self.form_vars["marca"].set(servicio.get("marca_nombre", ""))
        self._on_brand_change()
        self.form_vars["modelo"].set(servicio.get("modelo_nombre", ""))
        self.form_vars["ano"].set(str(servicio.get("año", "")))
        self.form_vars["quien_llevo"].set(servicio.get("quien_llevo", ""))
        fecha_valor = str(servicio.get("fecha_proximo_servicio", "")) or (date.today() + timedelta(days=180)).isoformat()
        self.form_vars["fecha_proximo"].set(fecha_valor)
        if DateEntry is not None and "fecha_proximo" in self.inputs:
            try:
                self.inputs["fecha_proximo"].set_date(fecha_valor)
            except Exception:
                pass
        self.obs_text.delete("1.0", "end")
        self.obs_text.insert("1.0", servicio.get("observaciones", "") or "")

        refacciones = self.servicio_refaccion_model.get_by_service(folio)
        ids = {r["refaccion_id"] for r in refacciones}
        self.refacciones_listbox.selection_clear(0, "end")
        for index, item in enumerate(self.refacciones):
            if item["id"] in ids:
                self.refacciones_listbox.selection_set(index)

        fallos = self.servicio_fallo_model.get_by_service(folio)
        ids_fallos = {r["fallo_id"] for r in fallos}
        self.fallos_listbox.selection_clear(0, "end")
        for index, item in enumerate(self.fallos):
            if item["id"] in ids_fallos:
                self.fallos_listbox.selection_set(index)

        self.update_service_total_preview()

        self.notebook.select(self.register_tab)

    def update_status(self, status):
        folio = self._get_selected_folio()
        if not folio:
            return
        self.servicio_model.update_status(folio, status)
        self.refresh_all()

    def delete_selected_service(self):
        folio = self._get_selected_folio()
        if not folio:
            return
        if messagebox.askyesno("Confirmar", f"¿Deseas eliminar el servicio {folio}?"):
            self.servicio_refaccion_model.clear_for_service(folio, restore_stock=True)
            self.servicio_fallo_model.clear_for_service(folio)
            self.servicio_model.delete(folio)
            if self.editing_folio == folio:
                self.clear_form()
            self.refresh_all()

    def generate_selected_receipt(self):
        folio = self._get_selected_folio()
        if not folio:
            return
        datos = self.servicio_model.get_by_folio(folio)
        if not datos:
            messagebox.showerror("Error", "No se encontró el servicio seleccionado.")
            return
        datos = self._get_service_details(folio)
        self._show_receipt_in_tab(folio, datos)
        ruta = generar_comprobante(folio, datos)
        messagebox.showinfo("Comprobante generado", f"Archivo creado en:\n{ruta}")

    def on_catalog_change(self, event=None):
        if not hasattr(self, "catalog_tree"):
            return

        for widget in self.catalog_form_frame.winfo_children():
            widget.destroy()

        catalog = self.catalog_var.get()
        self.catalog_fields = {}
        self.catalog_current_id = None

        if catalog == "Marcas":
            columns = ("id", "nombre")
            self._set_catalog_tree(columns, ["ID", "Nombre"])
            self._catalog_field("Nombre", "nombre")
        elif catalog == "Modelos":
            columns = ("id", "nombre", "marca")
            self._set_catalog_tree(columns, ["ID", "Modelo", "Marca"])
            self._catalog_field("Modelo", "nombre")
            self._catalog_field("Marca", "marca", combo=True, values=[m["nombre"] for m in self.marcas])
        elif catalog == "Años":
            columns = ("id", "año")
            self._set_catalog_tree(columns, ["ID", "Año"])
            self._catalog_field("Año", "año")
        elif catalog == "Fallos":
            columns = ("id", "nombre", "costo")
            self._set_catalog_tree(columns, ["ID", "Fallo", "Costo"])
            self._catalog_field("Fallo", "nombre")
            self._catalog_field("Costo", "costo")
        else:
            columns = ("id", "nombre", "precio", "stock")
            self._set_catalog_tree(columns, ["ID", "Nombre", "Precio", "Stock"])
            self._catalog_field("Nombre", "nombre")
            self._catalog_field("Precio", "precio")
            self._catalog_field("Stock", "stock")

        self.refresh_catalog_table()

    def _set_catalog_tree(self, columns, titles):
        self.catalog_tree.configure(columns=columns)
        for col, title in zip(columns, titles):
            self.catalog_tree.heading(col, text=title)
            self.catalog_tree.column(col, width=110 if col == "id" else 170, anchor="center")

    def _catalog_field(self, label, key, combo=False, values=None):
        box = tk.Frame(self.catalog_form_frame, bg="white")
        box.pack(fill="x", pady=6)
        tk.Label(box, text=label, bg="white", fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        variable = tk.StringVar()
        widget = ttk.Combobox(box, textvariable=variable, state="readonly", values=values or []) if combo else tk.Entry(box, textvariable=variable, relief="flat", bg="#f8fafc", fg=TEXT_DARK, font=("Segoe UI", 10), insertbackground=TEXT_DARK)
        widget.pack(fill="x", ipady=7)
        self.catalog_fields[key] = variable

    def refresh_catalog_table(self):
        if not hasattr(self, "catalog_tree"):
            return
        for item in self.catalog_tree.get_children():
            self.catalog_tree.delete(item)

        catalog = self.catalog_var.get()
        if catalog == "Marcas":
            for item in self.marca_model.get_all():
                self.catalog_tree.insert("", "end", values=(item["id"], item["nombre"]))
        elif catalog == "Modelos":
            for item in self.modelo_model.get_all():
                self.catalog_tree.insert("", "end", values=(item["id"], item["nombre"], item.get("marca_nombre", "")))
        elif catalog == "Años":
            for item in self.ano_model.get_all():
                self.catalog_tree.insert("", "end", values=(item["id"], item["año"]))
        elif catalog == "Fallos":
            for item in self.fallo_model.get_all():
                self.catalog_tree.insert("", "end", values=(item["id"], item["nombre"], item["costo"]))
        else:
            for item in self.refaccion_model.get_all():
                self.catalog_tree.insert("", "end", values=(item["id"], item["nombre"], item["precio"], item["stock"]))

    def clear_catalog_form(self):
        self.catalog_current_id = None
        for variable in self.catalog_fields.values():
            variable.set("")

    def load_catalog_item(self):
        selected = self.catalog_tree.selection()
        if not selected:
            return
        values = self.catalog_tree.item(selected[0], "values")
        self.catalog_current_id = values[0]
        catalog = self.catalog_var.get()
        if catalog == "Marcas":
            self.catalog_fields["nombre"].set(values[1])
        elif catalog == "Modelos":
            self.catalog_fields["nombre"].set(values[1])
            self.catalog_fields["marca"].set(values[2])
        elif catalog == "Años":
            self.catalog_fields["año"].set(values[1])
        elif catalog == "Fallos":
            self.catalog_fields["nombre"].set(values[1])
            self.catalog_fields["costo"].set(values[2])
        else:
            self.catalog_fields["nombre"].set(values[1])
            self.catalog_fields["precio"].set(values[2])
            self.catalog_fields["stock"].set(values[3])

    def save_catalog_item(self):
        catalog = self.catalog_var.get()
        try:
            if catalog == "Marcas":
                nombre = self.catalog_fields["nombre"].get().strip()
                if self.catalog_current_id:
                    self.marca_model.update(self.catalog_current_id, nombre)
                else:
                    self.marca_model.create(nombre)
            elif catalog == "Modelos":
                nombre = self.catalog_fields["nombre"].get().strip()
                marca_nombre = self.catalog_fields["marca"].get().strip()
                marca = next((m for m in self.marcas if m["nombre"] == marca_nombre), None)
                if not marca:
                    raise ValueError("Selecciona una marca válida.")
                if self.catalog_current_id:
                    self.modelo_model.update(self.catalog_current_id, nombre, marca["id"])
                else:
                    self.modelo_model.create(nombre, marca["id"])
            elif catalog == "Años":
                año = self.catalog_fields["año"].get().strip()
                if self.catalog_current_id:
                    self.ano_model.update(self.catalog_current_id, año)
                else:
                    self.ano_model.create(año)
            elif catalog == "Fallos":
                nombre = self.catalog_fields["nombre"].get().strip()
                costo = float(self.catalog_fields["costo"].get().strip())
                if self.catalog_current_id:
                    self.fallo_model.update(self.catalog_current_id, nombre, costo)
                else:
                    self.fallo_model.create(nombre, costo)
            else:
                nombre = self.catalog_fields["nombre"].get().strip()
                precio = float(self.catalog_fields["precio"].get().strip())
                stock = int(self.catalog_fields["stock"].get().strip())
                if self.catalog_current_id:
                    self.refaccion_model.update(self.catalog_current_id, nombre, precio, stock)
                else:
                    self.refaccion_model.create(nombre, precio, stock)

            self._load_catalogs()
            self.refresh_catalog_table()
            self.clear_catalog_form()
            messagebox.showinfo("Catálogo", "Operación realizada correctamente.")
        except Exception as exc:
            messagebox.showerror("Error de catálogo", str(exc))

    def delete_catalog_item(self):
        selected = self.catalog_tree.selection()
        if not selected:
            messagebox.showwarning("Selecciona un registro", "Elige un elemento del catálogo primero.")
            return
        item_id = self.catalog_tree.item(selected[0], "values")[0]
        if not messagebox.askyesno("Confirmar", "¿Deseas eliminar el registro seleccionado?"):
            return

        catalog = self.catalog_var.get()
        try:
            result = None
            if catalog == "Marcas":
                result = self.marca_model.delete(item_id)
            elif catalog == "Modelos":
                result = self.modelo_model.delete(item_id)
            elif catalog == "Años":
                result = self.ano_model.delete(item_id)
            elif catalog == "Fallos":
                result = self.fallo_model.delete(item_id)
            else:
                result = self.refaccion_model.delete(item_id)

            if not result:
                nombre_catalogo = {
                    "Marcas": "marca",
                    "Modelos": "modelo",
                    "Años": "año",
                    "Refacciones": "refacción",
                    "Fallos": "fallo",
                }.get(catalog, "registro")
                messagebox.showwarning(
                    "No se puede eliminar",
                    f"No se pudo eliminar este {nombre_catalogo} porque está relacionado con uno o más vehículos/servicios.",
                )
                return

            self._load_catalogs()
            self.refresh_catalog_table()
            self.clear_catalog_form()
            messagebox.showinfo("Catálogo", "Registro eliminado correctamente.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def logout(self):
        self.session.logout()
        self.current_user = None
        self.clear_form()
        self.show_login()

    def safe_exit(self):
        try:
            self.session.logout()
            self.current_user = None
            self.db.close()
        finally:
            self.destroy()


def launch_app():
    app = AutoTallerApp()
    app.mainloop()
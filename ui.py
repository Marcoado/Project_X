import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from simulator import Simulator, SimulationConfig


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timerzone")
        self.resizable(False, False)

        self.simulator = Simulator(SimulationConfig())
        self._running = False

        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        ttk.Label(main, text="Cliques por minuto (CPM)").grid(row=0, column=0, sticky="w")
        self.cpm_var = tk.IntVar(value=120)
        self.cpm_spin = ttk.Spinbox(main, from_=0, to=1000, textvariable=self.cpm_var, width=8)
        self.cpm_spin.grid(row=0, column=1, sticky="w", padx=8)

        ttk.Label(main, text="Tecla").grid(row=1, column=0, sticky="w")
        self.key_var = tk.StringVar(value="space")
        self.key_entry = ttk.Entry(main, textvariable=self.key_var, width=12)
        self.key_entry.grid(row=1, column=1, sticky="w", padx=8)

        self.mouse_enable_var = tk.BooleanVar(value=True)
        self.mouse_check = ttk.Checkbutton(main, text="Simular mouse", variable=self.mouse_enable_var)
        self.mouse_check.grid(row=2, column=0, columnspan=2, sticky="w")

        ttk.Label(main, text="Intervalo mouse (s)").grid(row=3, column=0, sticky="w")
        self.mouse_interval_var = tk.DoubleVar(value=5.0)
        self.mouse_interval_spin = ttk.Spinbox(main, from_=0.0, to=60.0, increment=0.5, textvariable=self.mouse_interval_var, width=8)
        self.mouse_interval_spin.grid(row=3, column=1, sticky="w", padx=8)

        self.randomize_var = tk.BooleanVar(value=False)
        self.randomize_check = ttk.Checkbutton(main, text="Aleatorizar intervalos", variable=self.randomize_var)
        self.randomize_check.grid(row=4, column=0, columnspan=2, sticky="w")

        btns = ttk.Frame(main)
        btns.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        self.start_btn = ttk.Button(btns, text="Iniciar", command=self.on_start)
        self.start_btn.grid(row=0, column=0, padx=6)
        self.stop_btn = ttk.Button(btns, text="Parar", command=self.on_stop)
        self.stop_btn.grid(row=0, column=1, padx=6)

        save_btn = ttk.Button(main, text="Salvar config.json", command=self.on_save)
        save_btn.grid(row=6, column=0, columnspan=2, pady=(10, 0))

    def _build_config(self) -> SimulationConfig:
        return SimulationConfig(
            clicks_per_minute=int(self.cpm_var.get()),
            key=str(self.key_var.get() or "space"),
            mouse_enable=bool(self.mouse_enable_var.get()),
            mouse_interval_seconds=float(self.mouse_interval_var.get()),
            randomize_interval=bool(self.randomize_var.get()),
        )

    def on_start(self):
        if self._running:
            return
        try:
            self.simulator.stop()
        except Exception:
            pass
        self.simulator = Simulator(self._build_config())
        self.simulator.start()
        self._running = True

    def on_stop(self):
        if not self._running:
            return
        try:
            self.simulator.stop()
        finally:
            self._running = False

    def on_save(self):
        data = {
            "cpm": int(self.cpm_var.get()),
            "key": str(self.key_var.get() or "space"),
            "mouse_enable": bool(self.mouse_enable_var.get()),
            "mouse_interval": float(self.mouse_interval_var.get()),
            "randomize_interval": bool(self.randomize_var.get()),
        }
        try:
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Configuração", "Arquivo config.json salvo com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar config.json: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()



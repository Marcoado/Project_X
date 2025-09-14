import os
import json
import sys
import servicemanager
import win32event
import win32service
import win32serviceutil

from simulator import Simulator, SimulationConfig


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def load_config() -> SimulationConfig:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    except Exception as e:  # fallback to defaults if config invalid
        servicemanager.LogErrorMsg(f"Erro ao ler config.json: {e}")
        data = {}
    return SimulationConfig(
        clicks_per_minute=int(data.get("cpm", 120)),
        key=str(data.get("key", "space")),
        mouse_enable=bool(data.get("mouse_enable", True)),
        mouse_interval_seconds=float(data.get("mouse_interval", 5.0)),
        randomize_interval=bool(data.get("randomize_interval", False)),
    )


class SimulatorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SimulatorService"
    _svc_display_name_ = "Simulador Mouse/Teclado"
    _svc_description_ = "Simula uso do computador (mouse e teclado) com configurações via config.json"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.simulator = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.simulator:
            try:
                self.simulator.stop()
            except Exception:
                pass
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("SimulatorService iniciando...")
        config = load_config()
        self.simulator = Simulator(config)
        try:
            self.simulator.start()
            # Espera até sinal de parada
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        except Exception as e:
            servicemanager.LogErrorMsg(f"Erro no serviço: {e}")
        finally:
            try:
                self.simulator.stop()
            except Exception:
                pass
            servicemanager.LogInfoMsg("SimulatorService finalizado.")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        try:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(SimulatorService)
            servicemanager.StartServiceCtrlDispatcher()
        except Exception as e:
            servicemanager.LogErrorMsg(str(e))
    else:
        win32serviceutil.HandleCommandLine(SimulatorService)



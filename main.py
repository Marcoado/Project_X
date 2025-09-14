import argparse
import sys
from simulator import Simulator, SimulationConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simula uso do computador com mouse e teclado.")
    parser.add_argument("--cpm", type=int, default=120, help="Cliques de teclado por minuto (CPM). Padrão: 120")
    parser.add_argument("--key", type=str, default="space", help="Tecla a pressionar. Padrão: space")
    parser.add_argument("--mouse-interval", type=float, default=5.0, help="Segundos entre movimentos do mouse. Padrão: 5")
    parser.add_argument("--mouse-enable", dest="mouse_enable", action="store_true", help="Ativa a simulação do mouse")
    parser.add_argument("--no-mouse", dest="mouse_enable", action="store_false", help="Desativa a simulação do mouse")
    parser.set_defaults(mouse_enable=True)
    parser.add_argument("--duration", type=float, default=0.0, help="Duração total em segundos (0 = infinito)")
    parser.add_argument("--randomize-interval", action="store_true", help="Adiciona aleatoriedade leve nos intervalos")
    parser.add_argument("--list-keys", action="store_true", help="Lista teclas suportadas e sai")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list_keys:
        import pyautogui
        try:
            keys = sorted(getattr(pyautogui, "KEYBOARD_KEYS", []))
        except Exception:
            keys = []
        if not keys:
            print("Não foi possível obter a lista de teclas. Verifique a instalação do pyautogui.")
            return 1
        print("Teclas suportadas:")
        print(", ".join(keys))
        return 0
    config = SimulationConfig(
        clicks_per_minute=args.cpm,
        key=args.key,
        mouse_enable=args.mouse_enable,
        mouse_interval_seconds=args.mouse_interval,
        randomize_interval=args.randomize_interval,
    )
    simulator = Simulator(config)
    simulator.run_for(duration_seconds=args.duration)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())




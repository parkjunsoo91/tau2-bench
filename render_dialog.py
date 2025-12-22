from typing import List, Dict, Optional, Union
import json
import os
import sys

def render_dialog(messages: List[Dict]):
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text
        from rich.table import Table
        from rich import box

        console = Console()
        console.rule("[bold cyan]Conversation")

        role_colors = {
            "system": "magenta",
            "user": "green",
            "assistant": "yellow",
            "tool": "blue",
        }

        for idx, m in enumerate(messages, 1):
            role = m.get("role", "unknown")
            content = m.get("content", "")
            tool_calls = m.get("tool_calls")
            ts = m.get("timestamp")
            turn_idx = m.get("turn_idx")

            header = Text(f"{idx}. {role.upper()}", style=role_colors.get(role, "white"))
            body = Text(content if content is not None else "", style="white")

            table = Table.grid(expand=True)
            table.add_row(Text("ROLE", style="bold dim"), Text(role, style=role_colors.get(role, "white")))
            if turn_idx is not None:
                table.add_row(Text("TURN", style="bold dim"), Text(str(turn_idx), style="bold"))
            if ts:
                table.add_row(Text("TIME", style="bold dim"), Text(ts, style="dim"))
            table.add_row(Text("CONTENT", style="bold dim"), body)

            if tool_calls:
                table.add_row(Text("TOOL CALLS", style="bold dim"), Text(json.dumps(tool_calls, ensure_ascii=False, indent=2), style="blue"))

            console.print(Panel(table, title=header, border_style=role_colors.get(role, "white"), box=box.ROUNDED))

        console.rule("[bold cyan]End")
    except Exception:
        # Fallback: simple print without rich
        sep = "\n" + "=" * 80 + "\n"
        for idx, m in enumerate(messages, 1):
            role = m.get("role", "unknown").upper()
            content = m.get("content", "")
            tool_calls = m.get("tool_calls")
            print(f"{sep}{idx}. ROLE: {role}")
            turn_idx = m.get("turn_idx")
            if turn_idx is not None:
                print(f"TURN: {turn_idx}")
            ts = m.get("timestamp")
            if ts:
                print(f"TIME: {ts}")
            print("\nCONTENT:\n" + (content if content is not None else ""))
            if tool_calls:
                print(f"\nTOOL CALLS:\n{tool_calls}")

def load_dialogs_from_file(
    path: str,
    simulation_selector: Optional[Union[int, str]] = None
) -> List[Dict]:
    """
    Load dialogs (messages) from a TauBench2 simulation JSON file.

    - path: full path to the JSON file.
    - simulation_selector:
        * int -> pick simulation by index (0-based).
        * str -> pick simulation by task_id (e.g., "0", "1").
        * None -> if only one simulation, pick that; else pick the first.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sims = data.get("simulations", [])
    if not sims:
        raise ValueError("No simulations found in the file.")

    selected = None
    if isinstance(simulation_selector, int):
        if simulation_selector < 0 or simulation_selector >= len(sims):
            raise IndexError(f"simulation index out of range: {simulation_selector}")
        selected = sims[simulation_selector]
    elif isinstance(simulation_selector, str):
        for sim in sims:
            if sim.get("task_id") == simulation_selector:
                selected = sim
                break
        if selected is None:
            raise ValueError(f"No simulation with task_id={simulation_selector}")
    else:
        # default: if exactly one, use it; else first
        selected = sims[0]

    messages = selected.get("messages", [])
    if not messages:
        raise ValueError("Selected simulation has no messages.")
    return messages

def main():
    """
    Usage:
      python tools/render_dialog.py /path/to/simulation.json [selector]

    selector:
      - integer simulation index (0-based), e.g., 0 or 1
      - string task_id, e.g., "0" or "1"
      - omit to select the first simulation
    """
    if len(sys.argv) < 2:
        print("Usage: python tools/render_dialog.py /path/to/simulation.json [selector]")
        sys.exit(1)

    path = sys.argv[1]
    selector: Optional[Union[int, str]] = None
    if len(sys.argv) >= 3:
        arg = sys.argv[2]
        # try int, else keep as str
        try:
            selector = int(arg)
        except ValueError:
            selector = arg

    messages = load_dialogs_from_file(path, selector)
    render_dialog(messages)

if __name__ == "__main__":
    main()
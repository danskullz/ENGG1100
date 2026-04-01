import asyncio
import websockets
from pynput import keyboard

PICO_IP   = "172.20.10.7"
PICO_PORT = 788
URI       = f"ws://{PICO_IP}:{PICO_PORT}"

_prev_cmd = None
_ws       = None

def resolve_command(keys_held: set) -> str:
    w = keyboard.KeyCode.from_char('w') in keys_held
    s = keyboard.KeyCode.from_char('s') in keys_held
    if w and not s:
        return "forward"
    if s and not w:
        return "backward"
    return "stop"

async def sender(keys_held: set):
    global _prev_cmd, _ws
    async for ws in websockets.connect(URI, ping_interval=None, close_timeout=2):
        _ws = ws
        try:
            print(f"connected to the pi: {URI}")
            print("forward is w, backward is s, control-c to quit\n")
            _prev_cmd = None
            while True:
                cmd = resolve_command(keys_held)
                if cmd != _prev_cmd:
                    await ws.send(cmd)
                    _prev_cmd = cmd
                    label = {"forward": "goin' forward", "backward": "rewind that bitch", "stop": "lower the masts!"}[cmd]
                    print(f"\r{label}          ", end="", flush=True)
                await asyncio.sleep(0.01)
        except (websockets.ConnectionClosed, OSError) as e:
            print(f"\ndisconnected ({e}), reconnecting...")
            _ws = None
            await asyncio.sleep(1)

def main():
    loop      = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    keys_held = set()

    def on_press(key):
        if isinstance(key, keyboard.KeyCode) and key.char in ('w', 's'):
            keys_held.add(keyboard.KeyCode.from_char(key.char))

    def on_release(key):
        try:
            keys_held.discard(keyboard.KeyCode.from_char(key.char))
        except AttributeError:
            pass
        if key == keyboard.Key.esc:
            return False

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    try:
        loop.run_until_complete(sender(keys_held))
    except KeyboardInterrupt:
        print("\nquitting...")
    finally:
        if _ws:
            try:
                loop.run_until_complete(_ws.send("stop"))
            except Exception:
                pass
        loop.close()
        listener.stop()

if __name__ == "__main__":
    main()
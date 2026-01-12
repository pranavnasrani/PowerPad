import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import KeysScanner
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.display import Display, TextEntry, ImageEntry
from kmk.extensions.display.ssd1306 import SSD1306

# Initialize Keyboard
keyboard = KMKKeyboard()

# -------------------------------------------------------------------------
# 1. OLED Display Setup (PowerPad)
# -------------------------------------------------------------------------
i2c_bus = busio.I2C(board.D5, board.D4) 

driver = SSD1306(
    i2c=i2c_bus,
    device_address=0x3C,
)

display = Display(
    display_buffer=driver,
    entries=[
        # CHANGED: Title updated to PowerPad
        TextEntry(text='PowerPad', x=0, y=0, y_anchor='M'),
        TextEntry(text='Layer: Base', x=0, y=10, y_anchor='M'),
    ],
    width=128,
    height=32,
    dim_time=20,
    dim_target=0.1,
    off_time=1200,
    brightness=1,
)
keyboard.extensions.append(display)

# -------------------------------------------------------------------------
# 2. Switch Matrix (Same as before)
# -------------------------------------------------------------------------
keyboard.matrix = KeysScanner(
    pins=[
        board.D0, # SW1
        board.D1, # SW2
        board.D2, # SW3
        board.D3, # SW4
        board.D7, # SW5
        board.D9, # SW6
        board.D6, # Encoder Button
    ],
    value_when_pressed=False,
    pull=True,
    interval=0.02,
)

# -------------------------------------------------------------------------
# 3. Rotary Encoder Setup
# -------------------------------------------------------------------------
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
encoder_handler.pins = ((board.D8, board.D10, None, False),)

# -------------------------------------------------------------------------
# 4. Keymap Configuration (Productivity)
# -------------------------------------------------------------------------
keyboard.extensions.append(MediaKeys())

# Macros / Combo definitions
# LCTRL(...) holds Control while pressing the key
CUT = KC.LCTRL(KC.X)
COPY = KC.LCTRL(KC.C)
PASTE = KC.LCTRL(KC.V)
UNDO = KC.LCTRL(KC.Z)
ALT_TAB = KC.LALT(KC.TAB)
# Windows Screenshot (Win + Shift + S)
SCREENSHOT = KC.LGUI(KC.LSFT(KC.S))

keyboard.keymap = [
    [
        # SW1: Cut      SW2: Copy     SW3: Paste
        CUT,            COPY,         PASTE,
        
        # SW4: Alt-Tab  SW5: Undo     SW6: Screenshot
        ALT_TAB,        UNDO,         SCREENSHOT,
        
        # Encoder Button: Mute
        KC.MUTE,
    ]
]

# Rotary Encoder: Volume Up / Down
encoder_handler.map = [
    ((KC.VOLU, KC.VOLD),), 
]

if __name__ == '__main__':
    keyboard.go()
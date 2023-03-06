# 8085 microprocessor emulator

## Running

-   make sure python and tkinter are setup. Running `python -m tkinter` from the command line should open a window demonstrating a simple Tk interface, letting you know that tkinter is properly installed on your system
-   `pip install pygubu`
-   `python index.py` to launch the application

## Using

1. make sure you fill all the entry with valid values
2. writing directly in machine code
    - fill the address you want to go and PRESS "next" Button
    - Now you can start filling the data of your program
    - u should PRESS next, prev, fill so that the values u filled are written to memory
    - before pressing run button check the memory layout if value are filled (by doing prev & next)
3. for writing code in editor
    - where ever u are running this program create yourcodes and youropcodes folders
    - if u want to save file as new file after loading enter different filename
4. Various kinds of opcodes and their syntax
    ```
    # hlt, ret
    # add b
    # adi 0a
    # mvi a ff
    # mov a,b
    # inx d
    # dcx b
    # inr a
    # dcr a
    # push b
    # pop psw
    # dad sp or dad b
    # rst 5
    # jmp 2050, lhdl 2050,
    # jnz 2050 (jc, jm, jnc ...)
    # cnz 2050
    # lxi d 40ff
    # stax b
    ```

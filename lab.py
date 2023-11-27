import time
import sys

def imprimir_cargando():
    while True:
        sys.stdout.write("\rCargando   ")
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write("\rCargando.  ")
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write("\rCargando.. ")
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write("\rCargando...")
        sys.stdout.flush()
        time.sleep(0.5)

imprimir_cargando()
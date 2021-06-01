# Luis Bodart A01635000

from random import choice, randrange
from tkinter import *

"""
Algoritmo RSA

Tomar 2 primos distintos y grandes 𝑝, 𝑞 con longitud de bits similar
𝑛 = 𝑝 * 𝑞
El totiente de 𝑛 es 𝜑(𝑛) = (𝑝 - 1) * (𝑞 - 1)
Tomar un 𝑒 coprimo 1 < 𝑒 < 𝑛
𝑑 = 𝑑 * 𝑒 ≡ 1 mod 𝜑(𝑛)
La llave publica es (𝑒, 𝑛)
La llave privada es (𝑑, 𝑛)
"""

# tamaño y pos de la ventana
def window(frame, width=600, height=300):
    frame.title("Criptosistema RSA")
    frame.minsize(width, height)
    frame.maxsize(width, height)
    frame.resizable(False, False)
    screenW = frame.winfo_screenwidth()
    screenH = frame.winfo_screenheight()
    x = (screenW / 2) - (width / 2)
    y = (screenH / 2.15) - (height / 2)
    frame.geometry("%dx%d+%d+%d" % (width, height, x, y))

# app
class App(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.widgets()

    # widgets principales
    def widgets(self):
        for i in range(7):
            label = Label(self, width=10).grid(row=0, column=i, sticky=W+E)

        self.generateKeys = Button(self, text="Generar llaves", command=self.generate_key_pair)
        self.generateKeys.grid(row=1, column=2, columnspan=3, sticky=N+S+W+E)

        self.generateStatus = StringVar()
        generateKeysLabel = Label(self, textvariable=self.generateStatus)
        generateKeysLabel.grid(row=2, column=2, columnspan=3, sticky=W+E)

    # Prueba de primordialidad para saber si un numero es primo (optimizacion 6k+-1)
    def is_prime(self, n):
        if(n <= 3):
            return n > 1
        if(n % 2 == 0 or n % 3 == 0):
            return False
        i = 5
        while i**2 <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    # algoritmo de Euclides para determinar el maximo comun divisor
    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    # algoritmo de Euclides extendido para sacar el inverso multiplicativo modular
    def mod_inverse(self, a, mod):
        d = 0
        x1, x2, y1 = 0, 1, 1
        tmp_mod = mod
        while a > 0 and tmp_mod != 1:
            tmp1 = tmp_mod // a
            tmp2 = tmp_mod - tmp1 * a
            tmp_mod = a
            a = tmp2

            x = x2 - tmp1 * x1
            y = d - tmp1 * y1

            x2 = x1
            x1 = x
            d = y1
            y1 = y
        return d + mod
    
    # exponenciacion rapida
    def fast_pow(self, a, n):
        if (n == 0):
            return 1
        x = self.fast_pow(a, n // 2)
        x = x * x
        if (n % 2 == 1):
            x = x * a
        return x

    # generar las llaves publicas y privadas
    def generate_key_pair(self):
        self.generateStatus.set("Generando llaves...")

        # longitud en bits 3-5
        bits = self.fast_pow(2, randrange(3, 6))
        
        # min y max numero con longitud en bits similar
        min = self.fast_pow(2, bits - 1)
        max = self.fast_pow(2, bits) - 1
        
        # los primeros 10 num primos
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        
        # inicio y fin de los numeros primos
        start = 2 ** (bits // 2 - 1)
        stop = 2 ** (bits // 2 + 1)    
        
        # generar los numeros primos
        for i in range(31, stop + 1, 2):
            if self.is_prime(i):
                primes.append(i)
        
        # asegurar que todos los primos >= start
        while (primes and primes[0] < start):
            primes.pop(0)
        
        # elegir p y q de los primos generados
        while primes:
            p = choice(primes)
            primes.remove(p)
            q_values = [q for q in primes if min <= p*q <= max]
            if q_values:
                q = choice(q_values)
                break

        n = p * q
        
        # totiente de n
        phi = (p - 1) * (q - 1)

        # generar llave publica 1 < e < phi(n)
        e = randrange(2, phi)
        g = self.gcd(e, phi)

        # verificar que e y phi(n) sean coprimos
        while g != 1:
            e = randrange(2, phi)
            g = self.gcd(e, phi)

        # generar la llave privada
        d = self.mod_inverse(e, phi)
        
        # llave publica y privada en hexadecimal
        self.publicKey = (hex(e), hex(n))
        self.privateKey = (hex(d), hex(n))

        self.createKeysMsgWidgets()

    # widgets para ver las llaves generadas y escribir el mensaje a cifrar
    def createKeysMsgWidgets(self):
        self.generateStatus.set("Llaves generadas")

        self.publicKeyLabel = Label(self, text="Llave Publica")
        self.publicKeyLabel.grid(row=3, column=0, columnspan=3, sticky=W+E)

        self.publicKeyData = StringVar()
        self.publicKeyEntry = Entry(self, textvariable=self.publicKeyData, justify="center", state='readonly')
        self.publicKeyEntry.grid(row=4, column=0, columnspan=3, sticky=W+E)

        self.privateKeyLabel = Label(self, text="Llave Privada")
        self.privateKeyLabel.grid(row=3, column=4, columnspan=3, sticky=W+E)

        self.privateKeyData = StringVar()
        self.privateKeyEntry = Entry(self, textvariable=self.privateKeyData, justify="center", state='readonly')
        self.privateKeyEntry.grid(row=4, column=4, columnspan=3, sticky=W+E)

        self.publicKeyData.set("%s-%s" % self.publicKey)
        self.privateKeyData.set("%s-%s" % self.privateKey)

        self.messageLabel = Label(self, text="Mensaje")
        self.messageLabel.grid(row=5, column=0, columnspan=5, sticky=W+E)

        self.message = Entry(self)
        self.message.grid(row=6, column=0, columnspan=5, sticky=W+E)

        self.encryptMsg = Button(self, text="Encriptar Mensaje", command=self.encrypt)
        self.encryptMsg.grid(row=6, column=5, columnspan=2, sticky=N+S+W+E)

    # encriptar el mensaje en hexadecimal
    def encrypt(self):
        msg = self.message.get()
        if len(msg) > 0:
            key, n = int(self.publicKey[0], 16), int(self.publicKey[1], 16)
            # convertir cada caracter del mensaje a numeros hexadecimales usando la llave publica (a^b mod n)
            self.cipher = [hex(pow(ord(char), key, n)) for char in msg]

            self.encryptedMsgLabel = Label(self, text="Mensaje Encriptado")
            self.encryptedMsgLabel.grid(row=7, column=0, columnspan=5, sticky=W+E)

            self.scrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.xScrollHandler)
            self.scrollbar.grid(row=9, column=0, columnspan=5, sticky=W+E)
            
            self.encryptedMsgData = StringVar()
            self.encryptedMsg = Entry(self, textvariable=self.encryptedMsgData, justify="center", state='readonly', xscrollcommand=self.scrollbar.set)
            self.encryptedMsg.grid(row=8, column=0, columnspan=5, sticky=W+E)
            
            self.decryptMsg = Button(self, text="Descifrar Mensaje", command=self.decrypt)
            self.decryptMsg.grid(row=8, column=5, columnspan=2, sticky=N+S+W+E)

            self.encryptedMsgData.set(''.join(map(lambda x: str(x), self.cipher)))

    # desencriptar el mensaje cifrado a texto
    def decrypt(self):
        key, n = int(self.privateKey[0], 16), int(self.privateKey[1], 16)
        # convertir a texto los valores hexadecimales del cipher usando la llave privada (a^b mod n)
        decipher = [chr(pow(int(char, 16), key, n)) for char in self.cipher]
        
        self.decryptedMsgLabel = Label(self, text="Mensaje Descifrado")
        self.decryptedMsgLabel.grid(row=10, column=0, columnspan=6, sticky=W+E)
        
        self.decryptedMsgData = StringVar()
        self.decryptedMsg = Entry(self, textvariable=self.decryptedMsgData, state='readonly')
        self.decryptedMsg.grid(row=11, column=0, columnspan=7, sticky=W+E)

        self.decryptedMsgData.set(''.join(decipher))

    # barra para scroll horizontal
    def xScrollHandler(self, *A):
        move = A[1]
        if A[0] == "scroll":
            self.encryptedMsg.xview_scroll(move, 'units')
        elif A[0] == "moveto":
            self.encryptedMsg.xview_moveto(move)

tk = Tk()
window(tk)
app = App(tk)
app.mainloop()

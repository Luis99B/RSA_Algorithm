# Luis Bodart A01635000

from random import randrange
from tkinter import *

# Numeros primos hasta el 2000
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
          73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
          179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
          283, 297, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
          419, 421, 431, 433, 439, 443, 439, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
          547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 531, 641, 643, 647, 656, 659,
          661, 679, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
          811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
          947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
          1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223,
          1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373,
          1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511,
          1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657,
          1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811,
          1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987,
          1993, 1997, 1999]

maxN = 2000

"""
Algoritmo RSA

Tomar 2 primos distintos y grandes 𝑝, 𝑞
Longitud de bytes similar
𝑛 = 𝑝 * 𝑞
El totiente de n es 𝜑(𝑛) = (𝑝 - 1) * (𝑞 - 1)
Tomar un 𝑒 coprimo 1 < 𝑒 < n
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

    # generar las llaves publicas y privadas
    def generate_key_pair(self):
        self.generateStatus.set("Generando llaves...")

        # sacar la posicion del arreglo de numeros primos
        pPos = randrange(0, len(primes))
        qPos = randrange(0, len(primes))

        # verificar que no sean la misma posicion
        while pPos == qPos:
            pPos = randrange(0, len(primes))
            qPos = randrange(0, len(primes))

        p = primes[pPos]
        q = primes[qPos]
        
        # verificar que p y q sean numeros primos
        while not (self.is_prime(p) and self.is_prime(q)):
            p = randrange(2, maxN)
            q = randrange(2, maxN)

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

        # llave publica y privada
        self.publicKey = (e, n)
        self.privateKey = (d, n)

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

        self.publicKeyData.set(str(self.publicKey))
        self.privateKeyData.set(str(self.privateKey))

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
            key, n = self.publicKey
            # convertir cada caracter del mensaje a numeros hexadecimales usando la llave publica (a^b mod n)
            self.cipher = [hex(pow(ord(char), key, n)) for char in msg]

            self.encryptedMsgLabel = Label(self, text="Mensaje Encriptado")
            self.encryptedMsgLabel.grid(row=7, column=0, columnspan=5, sticky=W+E)

            self.scrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.xScrollHandler)
            self.scrollbar.grid(row=9, column=0, columnspan=5, sticky=W+E)
            
            self.encryptedMsgData = StringVar()
            self.encryptedMsg = Entry(self, textvariable=self.encryptedMsgData, justify="center", state='readonly', xscrollcommand=self.scrollbar.set)
            self.encryptedMsg.grid(row=8, column=0, columnspan=5, sticky=W+E)
            
            self.decryptMsg = Button(self, text="Desencriptar Mensaje", command=self.decrypt)
            self.decryptMsg.grid(row=8, column=5, columnspan=2, sticky=N+S+W+E)

            self.encryptedMsgData.set(''.join(map(lambda x: str(x), self.cipher)))

    # desencriptar el mensaje cifrado a texto
    def decrypt(self):
        key, n = self.privateKey
        # convertir a texto los valores hexadecimales del cipher usando la llave privada (a^b mod n)
        decipher = [chr(pow(int(char, 16), key, n)) for char in self.cipher]
        
        self.decryptedMsgLabel = Label(self, text="Mensaje Desencriptado")
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

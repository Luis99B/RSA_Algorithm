# RSA_Algorithm
Algoritmo RSA para criptosistemas hecho en Python

Algoritmo RSA
Tomar 2 primos distintos y grandes 𝑝, 𝑞
Longitud de bytes similar
𝑛 = 𝑝 * 𝑞
El totiente de n es 𝜑(𝑛) = (𝑝 - 1) * (𝑞 - 1)
Tomar un 𝑒 coprimo 1 < 𝑒 < n
𝑑 = 𝑑 * 𝑒 ≡ 1 mod 𝜑(𝑛)
La llave publica es (𝑒, 𝑛)
La llave privada es (𝑑, 𝑛)

# RSA_Algorithm
Algoritmo RSA para criptosistemas hecho en Python


### Algoritmo RSA
- Tomar 2 primos distintos y grandes 𝑝, 𝑞 con longitud de bits similar
- 𝑛 = 𝑝 * 𝑞
- El totiente de 𝑛 es 𝜑(𝑛) = (𝑝 - 1) * (𝑞 - 1)
- Tomar un 𝑒 coprimo 1 < 𝑒 < 𝑛
- 𝑑 = 𝑑 * 𝑒 ≡ 1 mod 𝜑(𝑛)
- La llave publica es (𝑒, 𝑛)
- La llave privada es (𝑑, 𝑛)

![ejemplo](https://user-images.githubusercontent.com/30879359/120264720-fb623400-c263-11eb-84de-34526e52c495.png)

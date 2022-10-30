# FileCompressor-Perez
 Compresor de archivo desarrollado por Jose María Perez como evaluación práctica de la materia Teoría de la Información 2022 - FCEFyN - UNSJ

main program: program.py
-----------------------------------------------------------------------------------------
Compress spects:
> Huffman Estatico
> Markov Orden 1
> Burrows Wheeler
-----------------------------------------------------------------------------------------
File spects:
> Header:
    - [4 Bytes]     FileSize: Full file size (Byte)
    - [4 Bytes]     HeaderSize: Full header size (Byte)
    - [4 Bytes]     FileExtension: Source file extension.
    > CharsCode:
        - [65636 Codes] CodeMatrix: Codes associated with each Markov-1stOrd transition.
        										~ around 240 kBytes
        Code = 
        {
            + [1 Byte]      CharA: Initial State.
            + [1 Byte]      CharB: Final State.
            + [5 Bits]      Length: Code length.
            + [1:32 Bits]   Code: CharA-CharB transition code.
        }
> Data:
    - [4 Bytes]     PayLoad: Number of bytes of information.
    - [0:4 GBytes]  Data: compress data.
-----------------------------------------------------------------------------------------
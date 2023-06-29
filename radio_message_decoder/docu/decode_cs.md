### Ceasar Shift Decoder - C#

```cs
using System;

namespace CeasarDecoder
{
    class Decoder {     
    
        static void Main ()
        {
            Console.WriteLine(Decode("ifmmp xpsme", 1));
        }

        // Ceasar shift decoder
        static public string Decode (string encrypted, int shift)
        {
          string decoded = "";
          const string ALPHABET = "abcdefghijklmnopqrstuvwxyz";
          const string NUMBERS = "0123456789";
          foreach (char character in encrypted)
          {
            string characterString = Char.ToString(character); // <--
            if (ALPHABET.Contains(characterString))
            {
              int position = ALPHABET.IndexOf(characterString);
              decoded = decoded + ALPHABET[position - shift];
            }
            else if (NUMBERS.Contains(characterString))
            {
              int position = NUMBERS.IndexOf(characterString);
              decoded = decoded + NUMBERS[position - shift];
            }
            else
            {
              decoded = decoded + characterString; // no shift needed
            }
          }
          return decoded;
        }

    }
}
```
```
hello world
```

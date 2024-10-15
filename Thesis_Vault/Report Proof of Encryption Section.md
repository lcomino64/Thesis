Show that the device is actually encryption/decryption capable. Make sure server is running.
1. Create test text file.
i.e.
```shell
yes "This is repeating text." | head -n 200 > test-text.txt
```
This creates 200 lines of the same repeating text.

1. Take sha256sum of test file.
```shell
sha256sum test-text.txt > test-text1.sha256
```
We get:
```shell
cc53431630af0ef13af7e76baf742d5fc062fdffb2ed00ab95f4e1b55048cc23  test-text.txt
```
3. Encrypt the test file via the board.
Run:
```
python3 client.py demo_enc_proof/test-text.txt encrypt
```
5. Check that test file is encrypted.
First few lines:
```c
3ß<93>ÆA}¬üÚ0<8c>fHÛ<8f>£:ugõwr¶t^DM_^A^R^@^R)<8f>{4AJ^\ª^Eh^G¦^H
^[§4^L^@iÖ<91>2ê<_/^X3§x1!2h^Y<8b>È-SÅ^]<99>^SÍ^G Û¸½Ó<8a>^N½ä%ÇÜª<8d>gR°®<94>rÿ£¾<85>^Z)<9f>á<9d>R0^P2ãûÒ¶ÄÁ<93>ê^Z`\Þ<85>t0Jâº.Öþ®«à<8e>[)æ^S#^F4Ó¸+<89>|ä¯ÊE»O<95>Çs¾Æ<8e>ÜA«gÍ®<^U<9d>;¸QÄ^@e<91>í®^Z]u^RU)¶Í^NÇ<84>æù<81>æíV¢|!^]n^Ch5óHW^?<8f>Ã<95>Ïf^^sÃGÜ<H^H^@;<84>^Uú"¶aX<8e>Ù<8f>«gÇ/ê³<8a><89>£hI§^NÞ<8e><81> ¦<92>Î^F¨xcMÊª<8d>ª<86>a«Ìï<9d>öäÚe^cB%<91>^U_Ü±31Ba¼B<90>g^?§<9f>#<8f>3^M^D;A®°ýÉ&æ^YTÆ¥Ug!^Y<94>O#PKA<9a>ý<8f>Ñ<9c>ÂÁ<92>Ï§yLª^Z^Y<90>QVï^F<97>h^@^ZFÍ(<87>¥,Õ.ç^[a¯¾*ÛY<82>^EÅãcíxM<8a>^Y^Lë0û±ì,DE^K?¢Þì©^Dæi<87>^Y<9a>ûæ
S<8f>Éõ,U       {^R^F<92><9c>Î<9d>ùÌ^C"^<9d>.ùbý^[@R<96>Q<92> g^N^M^_Dçä^_BÊ<90>[<çÕ^Q®%Yþ<8f>^W`Ü!¬{<8d>Z:I<ß>M Jw¤õø?í^VKsz^]<84><9c>º<91><82>^C^Z¬pÌû½<82>Ìã^R(,é<9c>ð<8d>}úªð@jkÚðW<81>9
```
7. Delete original file as the client.py saves the decrypted file as the same file name.
8. Decrypt the file via the board.
By Running:
```shell
python3 client.py demo_enc_proof/test-text.txt.enc decrypt
```
9. Take sha256sum of decrypted file
10. Check if sha256sum is the same. 
Using diff or cat:
```shell
cat test-text2.sha256 test-text1.sha256
cc53431630af0ef13af7e76baf742d5fc062fdffb2ed00ab95f4e1b55048cc23  test-text.txt
cc53431630af0ef13af7e76baf742d5fc062fdffb2ed00ab95f4e1b55048cc23  test-text.txt
```
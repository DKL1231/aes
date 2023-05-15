import encryption as e
import decryption as d

plain_text = input("영어 문장을 입력하세요\n>> ").replace(" ", "")
plain_text_len = len(plain_text.replace(" ", ""))

if plain_text_len%16 == 0:
    repeat = plain_text_len // 16
else:
    repeat = plain_text_len // 16 + 1

encrypted = ""
temp = 0
for i in range(repeat):
    encrypted += e.encrypt(plain_text[temp: temp+16])
    temp += 16

print("\n암호화된 문장\n>> " + encrypted)


temp = 0
decrypted = ""
for i in range(repeat):
    decrypted += d.decrypt(encrypted[temp: temp+16])
    temp += 16

print("\n복호화된 문장\n>> " + decrypted[:plain_text_len])

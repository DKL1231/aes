import math
import keyexpansion as k


def invsubbytes(s):
    state = []
    for i in range(4):
        temp = []
        for j in range(4):
            # 입력 상태에 맞는 InverseSbox값을 16진수로 저장
            temp.append(hex(k.Inv_S_box[int(s[i][j], 16)]))
        state.append(temp)
    return state


def invshiftrows(s):
    state = []
    for i in range(4):
        temp = []
        for j in range(4):
            # shift연산 수행
            temp.append(s[i][(j-i) % 4])
        state.append(temp)
    return state


def invmixcolumns(s):
    state = []
    for i in range(4):
        state.append(invmixcolumn([s[0][i], s[1][i], s[2][i], s[3][i]]))
    return transpose(state)


# 행렬을 전치시키는 함수
def transpose(s):
    state = []
    for i in range(4):
        state.append([s[0][i], s[1][i], s[2][i], s[3][i]])
    return state


def invmixcolumn(s):
    temp = copy(s)
    # e b d 9
    s[0] = hex(multi(int(temp[0], 16), 0xe) ^ multi(int(temp[1], 16), 0xb)
               ^ multi(int(temp[2], 16), 0xd) ^ multi(int(temp[3], 16), 0x9))
    # 9 e b d
    s[1] = hex(multi(int(temp[0], 16), 0x9) ^ multi(int(temp[1], 16), 0xe)
               ^ multi(int(temp[2], 16), 0xb) ^ multi(int(temp[3], 16), 0xd))
    # d 9 e b
    s[2] = hex(multi(int(temp[0], 16), 0xd) ^ multi(int(temp[1], 16), 0x9)
               ^ multi(int(temp[2], 16), 0xe) ^ multi(int(temp[3], 16), 0xb))
    # b d 9 e
    s[3] = hex(multi(int(temp[0], 16), 0xb) ^ multi(int(temp[1], 16), 0xd)
               ^ multi(int(temp[2], 16), 0x9) ^ multi(int(temp[3], 16), 0xe))
    return s


# 깊은 복사를 수행하는 함수
def copy(arr):
    temp = []
    for i in range(4):
        temp.append(arr[i])
    return temp


# 비트 곱 함수
def multi(num, mlt):
    temp = num
    lst = [temp]
    for i in range(3):
        # 100 0000 이상이면 1비트 shift하고 XOR연산
        if temp >= 0x80:
            temp = (temp << 1) & 0xff
            temp ^= 0x1b
        # 아니면 1비트 shift만 수행
        else:
            temp = (temp << 1) & 0xff
        lst.append(temp)
    tmp = mlt
    cnt = 3
    result = 0
    while tmp != 0:
        if tmp >= math.pow(2, cnt):
            result ^= lst[cnt]
            tmp -= math.pow(2, cnt)
        cnt -= 1
    return result


def AddRoundKey(s, rnd, word):
    state = []
    for i in range(4):
        state.append(add_round_key([s[0][i], s[1][i], s[2][i], s[3][i]], rnd, i, word))
    return transpose(state)


def add_round_key(s, rnd, col, word):
    temp = []
    for i in range(4):
        temp.append(hex(int(s[i], 16) ^ word[40-(4*rnd)+col][i]))
    return temp


def aes_round(s, num, word):
    # round 출력
    if __name__ == '__main__':
        print("round :", num, "\n")

    # input 출력
    if __name__ == '__main__':
        print("input : ")
        print_state(s)

    # 암호화 진행
    s = invshiftrows(s)
    s = invsubbytes(s)
    s = AddRoundKey(s, num, word)
    # 마지막 라운드인 경우는 invmixcolumns 제외
    if num != 10:
        s = invmixcolumns(s)

    # output 출력
    if __name__ == '__main__':
        print("output : ")
        print_state(s)
        print("\n")
    return s


def aes_decryption(s, word):
    if __name__ == '__main__':
        print("round :", 0, "\n")

        print("input : ")
        print_state(s)

    # pre-round 의 경우 Addroundkey만 수행
    s = AddRoundKey(s, 0, word)

    if __name__ == '__main__':
        print("output : ")
        print_state(s)
        print("\n")

    # round 1~10 수행
    for i in range(1, 11):
        s = aes_round(s, i, word)
    return s


def print_state(s):
    for i in range(4):
        for j in range(4):
            print(format(int(s[i][j], 16), '02x'), end="\t")
        print()
    print()


def decrypt(plain_txt):
    word = k.key_expansion()
    temp = plain_txt

    # 4*4행렬화
    txt_lst = [[], [], [], []]
    j = 0
    for i in temp:
        txt_lst[j].append(hex(ord(i)))
        j += 1
        j %= 4

    txt_lst = aes_decryption(txt_lst, word)

    result = ''
    for i in range(4):
        for j in range(4):
            result += chr(int(txt_lst[j][i], 16)+97)
    return result


if __name__ == '__main__':
    result = decrypt("Ymý7÷ kp¿;Y/")
    print("암호문:\tYmý7÷ kp¿;Y/")
    print("복호화:", end="\t")
    print(result)

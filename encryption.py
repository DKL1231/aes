import math
import keyexpansion as k


def subbytes(s):
    state = []
    for i in range(4):
        temp = []
        for j in range(4):
            # 입력 상태에 맞는 Sbox값을 16진수로 저장
            temp.append(hex(k.S_box[int(s[i][j], 16)]))
        state.append(temp)
    return state


def shiftrows(s):
    state = []
    for i in range(4):
        temp = []
        for j in range(4):
            # shift연산 수행
            temp.append(s[i][(j+i) % 4])
        state.append(temp)
    return state


def mixcolumns(s):
    state = []
    for i in range(4):
        state.append(mixcolumn([s[0][i], s[1][i], s[2][i], s[3][i]]))
    return transpose(state) # 열을 기준으로 행렬을 만들었으므로 전치하여 return


# 행렬을 전치시키는 함수
def transpose(s):
    state = []
    for i in range(4):
        state.append([s[0][i], s[1][i], s[2][i], s[3][i]])
    return state


def mixcolumn(s):
    temp = copy(s)
    # 2 3 1 1
    s[0] = hex(multi(int(temp[0], 16), 2) ^ multi(int(temp[1], 16), 3)
               ^ int(temp[2], 16) ^ int(temp[3], 16))
    # 1 2 3 1
    s[1] = hex(int(temp[0], 16) ^ multi(int(temp[1], 16), 2)
               ^ multi(int(temp[2], 16), 3) ^ int(temp[3], 16))
    # 1 1 2 3
    s[2] = hex(int(temp[0], 16) ^ int(temp[1], 16)
               ^ multi(int(temp[2], 16), 2) ^ multi(int(temp[3], 16), 3))
    # 3 1 1 2
    s[3] = hex(multi(int(temp[0], 16), 3) ^ int(temp[1], 16)
               ^ int(temp[2], 16) ^ multi(int(temp[3], 16), 2))
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
        # 0100 0000 이상이면 1비트 shift하고 XOR연산
        if temp >= 0x80:
            temp = (temp << 1) & 0xff
            temp ^= 0x1b
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
        state.append(add_round_key([s[0][i], s[1][i], s[2][i], s[3][i]],
                                   rnd, i, word))
    return transpose(state)


def add_round_key(s, rnd, col, word):
    temp = []
    for i in range(4):
        temp.append(hex(int(s[i], 16) ^ word[4*rnd+col][i]))
    return temp


def aes_round(s, num, word):
    if __name__ == '__main__':
        print(f"Round {num}\n\ninput:")
        print_state(s)
    s = subbytes(s)
    s = shiftrows(s)
    # 마지막 라운드인 경우는 mixcolumns 제외
    if num != 10:
        s = mixcolumns(s)
    s = AddRoundKey(s, num, word)

    if __name__ == '__main__':
        print("output:")
        print_state(s)
    return s


def aes_encryption(s, word):
    # pre-round 의 경우 Addroundkey만 수행
    s = AddRoundKey(s, 0, word)

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


def txt_to_array(plain_txt):
    temp = plain_txt
    temp = temp.lower().replace(' ', '')
    # 16개 단위로 만듦
    while True:
        if len(temp) % 16 != 0:
            temp += 'z'
        else:
            break

    # 4*4행렬화
    txt_lst = [[], [], [], []]
    j = 0
    for i in temp:
        txt_lst[j].append(hex(ord(i) - 97))
        j += 1
        j %= 4
    if __name__ == '__main__':
        txt_lst[1][3] = '0x23'  # 교재 오류?
    return txt_lst


def array_to_txt(txt_lst):
    result = ''
    for i in range(4):
        for j in range(4):
            result += chr(int(txt_lst[j][i], 16))
    return result


def encrypt(plain_txt):
    word = k.key_expansion()
    txt_lst = txt_to_array(plain_txt)
    txt_lst = aes_encryption(txt_lst, word)
    result = array_to_txt(txt_lst)
    return result


if __name__ == '__main__':
    # 본문 시작
    plain_text = 'AES uses a matrix'
    result = encrypt(plain_text)
    print("평문:", end='\t')
    print(plain_text.lower().replace(' ', ''))
    print("암호문:", end='\t')
    print(result)

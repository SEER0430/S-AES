# S盒
S_BOX = [
    [9, 4, 10, 11],
    [13, 1, 8, 5],
    [6, 2, 0, 3],
    [12, 14, 15, 7]
]

# 逆S盒
INV_S_BOX = [
    [10, 5, 9, 11],
    [1, 7, 8, 15],
    [6, 0, 2, 3],
    [12, 4, 13, 14]
]

# 替换表
REPLACE_TABLE = [
    [0, 0, 0, 0], [0, 0, 0, 1],
    [0, 0, 1, 0], [0, 0, 1, 1],
    [0, 1, 0, 0], [0, 1, 0, 1],
    [0, 1, 1, 0], [0, 1, 1, 1],
    [1, 0, 0, 0], [1, 0, 0, 1],
    [1, 0, 1, 0], [1, 0, 1, 1],
    [1, 1, 0, 0], [1, 1, 0, 1],
    [1, 1, 1, 0], [1, 1, 1, 1]
]

# 逆替换表
INV_REPLACE_TABLE = [
    [0, 0, 0, 0], [0, 0, 0, 1],
    [0, 0, 1, 0], [0, 0, 1, 1],
    [0, 1, 0, 0], [0, 1, 0, 1],
    [0, 1, 1, 0], [0, 1, 1, 1],
    [1, 0, 0, 0], [1, 0, 0, 1],
    [1, 0, 1, 0], [1, 0, 1, 1],
    [1, 1, 0, 0], [1, 1, 0, 1],
    [1, 1, 1, 0], [1, 1, 1, 1]
]

# 轮常数
RCON1 = [1, 0, 0, 0, 0, 0, 0, 0]
RCON2 = [0, 0, 1, 1, 0, 0, 0, 0]


def xor_8(a, b):
    """对两个长度为8的数组进行异或操作，返回一个长度也为8的数组"""
    return [a[i] ^ b[i] for i in range(8)]


def sub_bytes(temp):
    """对输入的8位数组进行字节替换"""
    t1 = 2 * temp[0] + temp[1]
    t2 = 2 * temp[2] + temp[3]
    t3 = 2 * temp[4] + temp[5]
    t4 = 2 * temp[6] + temp[7]
    num1 = S_BOX[t1][t2]
    num2 = S_BOX[t3][t4]
    for i in range(4):
        temp[i] = REPLACE_TABLE[num1][i]
    for i in range(4):
        temp[i + 4] = REPLACE_TABLE[num2][i]


def inv_sub_bytes(temp):
    """对输入的8位数组进行逆字节替换"""
    t1 = 2 * temp[0] + temp[1]
    t2 = 2 * temp[2] + temp[3]
    t3 = 2 * temp[4] + temp[5]
    t4 = 2 * temp[6] + temp[7]
    num1 = INV_S_BOX[t1][t2]
    num2 = INV_S_BOX[t3][t4]
    for i in range(4):
        temp[i] = INV_REPLACE_TABLE[num1][i]
    for i in range(4):
        temp[i + 4] = INV_REPLACE_TABLE[num2][i]


def g_function(temp, rcon):
    """g函数，对输入的8位数组进行循环左移、S盒替换和轮常数异或"""
    t = temp.copy()
    t = t[4:] + t[:4]  # 循环左移
    sub_bytes(t)
    return xor_8(t, rcon)


def add_round_key(mingwen, key):
    """轮密钥加，对明文和密钥进行异或操作"""
    for i in range(2):
        for j in range(8):
            mingwen[i][j] ^= key[i][j]


def shift_rows(temp):
    """行变换，对输入的二维数组进行行变换"""
    for i in range(4, 8):
        temp[0][i], temp[1][i] = temp[1][i], temp[0][i]


def xor_4(a, b):
    """对两个长度为4的数组进行异或操作，返回一个长度也为4的数组"""
    return [a[i] ^ b[i] for i in range(4)]


def x_fx(f, a):
    """进行有限域上的多项式除法运算，用于求解一个元素的逆元"""
    if a[0] == 0:
        for i in range(3):
            f[i] = a[i + 1]
    else:
        f[1] = a[2]
        f[2] = 0 if a[3] == 1 else 1
        f[3] = 1


def multiply(a, b):
    """在有限域 GF(2^4) 上的多项式乘法运算"""
    f = [0] * 4
    x_fx(f, a)
    f2 = [0] * 4
    x_fx(f2, f)
    f3 = [0] * 4
    x_fx(f3, f2)

    result = [0] * 4
    if b[0] == 1:
        result = xor_4(result, f3)
    if b[1] == 1:
        result = xor_4(result, f2)
    if b[2] == 1:
        result = xor_4(result, f)
    if b[3] == 1:
        result = xor_4(result, a)

    return result


def mix_columns(mingwen):
    """列混淆，对输入的二维数组进行列混淆操作"""
    erjinzhi_1 = [0, 0, 0, 1]  # 1的二进制
    erjinzhi_4 = [0, 1, 0, 0]  # 4的二进制
    m00 = mingwen[0][:4]
    m10 = mingwen[0][4:]
    m01 = mingwen[1][:4]
    m11 = mingwen[1][4:]

    n00 = xor_4(multiply(erjinzhi_1, m00), multiply(erjinzhi_4, m10))
    n10 = xor_4(multiply(erjinzhi_4, m00), multiply(erjinzhi_1, m10))
    n01 = xor_4(multiply(erjinzhi_1, m01), multiply(erjinzhi_4, m11))
    n11 = xor_4(multiply(erjinzhi_4, m01), multiply(erjinzhi_1, m11))

    mingwen[0][:4] = n00
    mingwen[0][4:] = n10
    mingwen[1][:4] = n01
    mingwen[1][4:] = n11


def inv_mix_columns(mingwen):
    """逆向列混淆，对输入的二维数组进行逆向列混淆操作"""
    erjinzhi_9 = [1, 0, 0, 1]  # 9的二进制
    erjinzhi_2 = [0, 0, 1, 0]  # 2的二进制
    m00 = mingwen[0][:4]
    m10 = mingwen[0][4:]
    m01 = mingwen[1][:4]
    m11 = mingwen[1][4:]

    n00 = xor_4(multiply(erjinzhi_9, m00), multiply(erjinzhi_2, m10))
    n10 = xor_4(multiply(erjinzhi_2, m00), multiply(erjinzhi_9, m10))
    n01 = xor_4(multiply(erjinzhi_9, m01), multiply(erjinzhi_2, m11))
    n11 = xor_4(multiply(erjinzhi_2, m01), multiply(erjinzhi_9, m11))

    mingwen[0][:4] = n00
    mingwen[0][4:] = n10
    mingwen[1][:4] = n01
    mingwen[1][4:] = n11


def ades_encrypt(mingwen_str, key_str):
    mingwen = [[int(mingwen_str[i * 8 + j]) for j in range(8)] for i in range(2)]
    key = [[int(key_str[i * 8 + j]) for j in range(8)] for i in range(2)]
    # 密钥扩展
    key1 = [[0] * 8 for _ in range(2)]
    key2 = [[0] * 8 for _ in range(2)]
    key1[0] = xor_8(key[0], g_function(key[1], RCON1))
    key1[1] = xor_8(key1[0], key[1])
    key2[0] = xor_8(key1[0], g_function(key1[1], RCON2))
    key2[1] = xor_8(key2[0], key1[1])

    # 第零轮
    # 轮密钥加
    add_round_key(mingwen, key)

    # 第一轮
    # 明文半字节代替
    sub_bytes(mingwen[0])
    sub_bytes(mingwen[1])
    # 明文的行移位
    shift_rows(mingwen)
    # 明文的列混淆
    mix_columns(mingwen)
    # 明文的轮密钥加
    add_round_key(mingwen, key1)

    # 第二轮
    # 明文半字节代替
    sub_bytes(mingwen[0])
    sub_bytes(mingwen[1])
    # 明文的行移位
    shift_rows(mingwen)
    # 明文的轮密钥加
    add_round_key(mingwen, key2)

    # 将列表中的每个子列表转换为字符串，并拼接在一起
    mingwen_str = ''.join([''.join(map(str, sublist)) for sublist in mingwen])
    return mingwen_str


def ades_decrypt(miwen_str, key_str):
    """解密函数，对密文进行解密"""
    miwen = [[int(miwen_str[i * 8 + j]) for j in range(8)] for i in range(2)]
    key = [[int(key_str[i * 8 + j]) for j in range(8)] for i in range(2)]

    # 密钥扩展
    key1 = [[0] * 8 for _ in range(2)]
    key2 = [[0] * 8 for _ in range(2)]
    key1[0] = xor_8(key[0], g_function(key[1], RCON1))
    key1[1] = xor_8(key1[0], key[1])
    key2[0] = xor_8(key1[0], g_function(key1[1], RCON2))
    key2[1] = xor_8(key2[0], key1[1])

    # 初始轮密钥加
    add_round_key(miwen, key2)

    # 第一轮解密
    # 密文的行移位
    shift_rows(miwen)
    # 密文的半字节代替
    inv_sub_bytes(miwen[0])
    inv_sub_bytes(miwen[1])
    # 轮密钥加
    add_round_key(miwen, key1)
    # 列混淆
    inv_mix_columns(miwen)

    # 第二轮解密
    # 密文的行移位
    shift_rows(miwen)
    # 密文的半字节代替
    inv_sub_bytes(miwen[0])
    inv_sub_bytes(miwen[1])
    # 轮密钥加
    add_round_key(miwen, key)

    # 将列表中的每个子列表转换为字符串，并拼接在一起
    miwen_str = ''.join([''.join(map(str, sublist)) for sublist in miwen])
    return miwen_str


def meet_in_the_middle_attack(mingwen, miwen):
    # 存储中间状态和对应的密钥
    M1_table = {}
    M2_table = {}

    # 从明文加密到中间状态
    for K1 in range(65536):
        k1 = format(K1, '016b')
        M1 = ades_encrypt(mingwen, k1)
        M1_table[M1] = K1

    # 从密文解密到中间状态
    for K2 in range(65536):
        k2 = format(K2, '016b')
        M2 = ades_decrypt(miwen, k2)
        M2_table[M2] = K2

    # 匹配所有可能的中间状态
    matched_pairs = []

    for M2 in M2_table:
        if M2 in M1_table:
            K1 = M1_table[M2]
            K2 = M2_table[M2]
            k1 = format(K1, '016b')
            k2 = format(K2, '016b')
            key_pair_str = k1 + k2
            matched_pairs.append(key_pair_str)

    return matched_pairs


# 示例使用
key = '10011001100110011001100110011001'

mingwen1 = '0000000000000100'
miwen1 = '0100010110101010'

mingwen2 = '0000000000000001'
miwen2 = '1001010110101000'

mingwen3 = '0000000000000010'
miwen3 = '1011010110100100'

mingwen4 = '0000000000000111'
miwen4 = '1111010110100010'

matched_pairs1 = meet_in_the_middle_attack(mingwen1, miwen1)
matched_pairs2 = meet_in_the_middle_attack(mingwen2, miwen2)
matched_pairs3 = meet_in_the_middle_attack(mingwen3, miwen3)
matched_pairs4 = meet_in_the_middle_attack(mingwen4, miwen4)

# 将列表转换为集合
set1 = set(matched_pairs1)
set2 = set(matched_pairs2)
set3 = set(matched_pairs3)
set4 = set(matched_pairs4)

# 查找交集
common_elements = set1.intersection(set2, set3, set4)

# 打印相同的元素
if common_elements:
    print("在密钥集中相同的元素有:")
    for element in common_elements:
        print(element)
else:
    print("没有相同的元素。")

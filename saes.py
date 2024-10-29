import tkinter as tk
import re

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
    """加密函数"""
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


def double_ades_encrypt(mingwen_str, key_str):
    # 将32位的密钥分成两个16位的密钥
    key1 = key_str[:16]
    key2 = key_str[16:]

    # 第一轮加密
    intermediate_cipher = ades_encrypt(mingwen_str, key1)

    # 第二轮加密
    final_cipher = ades_encrypt(intermediate_cipher, key2)

    return final_cipher


def double_ades_decrypt(miwen_str, key_str):
    # 将32位的密钥分成两个16位的密钥
    key1 = key_str[:16]
    key2 = key_str[16:]

    # 第一轮解密
    intermediate_plain = ades_decrypt(miwen_str, key2)

    # 第二轮解密
    final_plain = ades_decrypt(intermediate_plain, key1)

    return final_plain


def treble_ades_encrypt(mingwen_str, key_str):
    # 将32位的密钥分成两个16位的密钥
    key1 = key_str[:16]
    key2 = key_str[16:]

    # 第一轮加密
    intermediate_cipher = ades_encrypt(mingwen_str, key1)

    # 第二轮加密
    middle_cipher = ades_encrypt(intermediate_cipher, key2)

    # 第三轮加密
    final_cipher = ades_encrypt(middle_cipher, key1)

    return final_cipher


def treble_ades_decrypt(miwen_str, key_str):
    # 将32位的密钥分成两个16位的密钥
    key1 = key_str[:16]
    key2 = key_str[16:]

    # 第一轮解密
    intermediate_plain = ades_decrypt(miwen_str, key1)

    # 第二轮解密
    middle_plain = ades_decrypt(intermediate_plain, key2)

    # 第三轮解密
    final_plain = ades_decrypt(middle_plain, key1)

    return final_plain


def str_to_bin_list(text, length):
    return [int(bit) for bit in text.zfill(length)]


def bin_list_to_str(bin_list):
    return ''.join(str(bit) for bit in bin_list)


# 新增ASCII字符串与二进制的相互转换函数
def ascii_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)


def bin_to_ascii(bin_str):
    chars = [chr(int(bin_str[i:i + 8], 2)) for i in range(0, len(bin_str), 8)]
    return ''.join(chars)


# ASCII加密
def encrypt_ascii(plaintext, key):
    binary_plaintext = ascii_to_bin(plaintext)

    if len(binary_plaintext) % 16 != 0:
        binary_plaintext = binary_plaintext.zfill((len(binary_plaintext) // 16 + 1) * 16)

    result = []
    for i in range(0, len(binary_plaintext), 16):
        plaintext_bits = str_to_bin_list(binary_plaintext[i:i + 16], 16)
        result.extend(ades_encrypt(plaintext_bits, key))
    # 将结果的二进制列表转换为ASCII字符串
    binary_result = bin_list_to_str(result)
    return bin_to_ascii(binary_result)


# ASCII解密
def decrypt_ascii(ciphertext, key):
    binary_ciphertext = ascii_to_bin(ciphertext)
    result = []
    for i in range(0, len(binary_ciphertext), 16):
        ciphertext_bits = str_to_bin_list(binary_ciphertext[i:i + 16], 16)
        result.extend(ades_decrypt(ciphertext_bits, key))

    # 将结果的二进制列表转换为ASCII字符串
    binary_result = bin_list_to_str(result)
    return bin_to_ascii(binary_result)


def xor_16bit(a, b):
    """对两个16位二进制字符串进行异或操作"""
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))


def cbc_encrypt(mingwen_str, key_str, iv):
    """使用CBC模式对明文进行加密"""
    # 初始化密文
    miwen_str = ''

    # 初始化前一个块的密文为IV
    previous_block = iv

    # 逐块加密
    for i in range(0, len(mingwen_str), 16):
        # 获取当前块
        current_block = mingwen_str[i:i + 16]

        # 当前块与前一个块的密文进行异或
        xored_block = xor_16bit(current_block, previous_block)

        # 加密当前块
        encrypted_block = ades_encrypt(xored_block, key_str)

        # 将加密后的块添加到密文中
        miwen_str += encrypted_block

        # 更新前一个块的密文
        previous_block = encrypted_block

    return miwen_str


def cbc_decrypt(miwen_str, key_str, iv):
    """使用CBC模式对密文进行解密"""
    # 初始化明文
    mingwen_str = ''

    # 初始化前一个块的密文为IV
    previous_block = iv

    # 逐块解密
    for i in range(0, len(miwen_str), 16):
        # 获取当前块
        current_block = miwen_str[i:i + 16]

        # 解密当前块
        decrypted_block = ades_decrypt(current_block, key_str)

        # 解密后的块与前一个块的密文进行异或
        xored_block = xor_16bit(decrypted_block, previous_block)

        # 将解密后的块添加到明文中
        mingwen_str += xored_block

        # 更新前一个块的密文
        previous_block = current_block

    return mingwen_str


# ----------------------------------------GUI界面--------------------------------------------------------#


root = tk.Tk()
root.title("欢迎使用S-AES加解密系统！")
root.configure(bg='lightblue')
root.geometry("600x500")

title_font = ("Times", 16, "bold")
label_font = ("Times", 12)
button_font = ("Times", 12, "bold")
result_font = ("Times", 12, "italic")

main_frame = tk.Frame(root, bg='lightblue')
main_frame.pack(expand=True)


def show_home():
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="选择操作：", font=title_font, bg='lightblue').grid(row=0, column=0, columnspan=4, pady=20)

    ascii_button = tk.Button(main_frame, text="ASCII", width=20, font=button_font, command=show_ascii_mode)
    ascii_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    binary_button = tk.Button(main_frame, text="二进制", width=20, font=button_font, command=show_binary_mode)
    binary_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    ascii_button = tk.Button(main_frame, text="双重加密", width=20, font=button_font, command=show_double_binary_mode)
    ascii_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    ascii_button = tk.Button(main_frame, text="三重加密", width=20, font=button_font, command=show_treble_binary_mode)
    ascii_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    ascii_button = tk.Button(main_frame, text="密码分组链(CBC)加密", width=20, font=button_font, command=show_CBC_mode)
    ascii_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")


def show_ascii_mode():
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="输入ASCII字符串/密文：", font=label_font, bg='lightblue').grid(row=0, column=0, pady=10)
    data_entry = tk.Entry(main_frame, font=label_font, width=20)
    data_entry.grid(row=0, column=1, pady=10)

    tk.Label(main_frame, text="输入16位二进制密钥：", font=label_font, bg='lightblue').grid(row=1, column=0, pady=10)
    key_entry = tk.Entry(main_frame, font=label_font, width=20)
    key_entry.grid(row=1, column=1, pady=10)

    tk.Label(main_frame, text="选择操作：", font=label_font, bg='lightblue').grid(row=2, column=0, pady=10)

    # 纵向布局按钮
    encrypt_button = tk.Button(main_frame, text="加密", font=button_font,
                               command=lambda: process_ascii_data(data_entry.get(), key_entry.get(), "encrypt"))
    encrypt_button.grid(row=2, column=1, pady=10)

    decrypt_button = tk.Button(main_frame, text="解密", font=button_font,
                               command=lambda: process_ascii_data(data_entry.get(), key_entry.get(), "decrypt"))
    decrypt_button.grid(row=3, column=1, pady=10)

    # 添加返回按钮
    back_button = tk.Button(main_frame, text="返回", font=button_font, command=show_home)
    back_button.grid(row=4, column=1, pady=10)

    result_label = tk.Label(main_frame, text="结果：", font=result_font, bg='lightblue')
    result_label.grid(row=5, column=0, pady=10)
    result_text = tk.Entry(main_frame, font=result_font, bg='lightblue', width=30)  # 增加宽度
    result_text.grid(row=5, column=1, pady=10)

    def process_ascii_data(data, key, operation):
        if len(key) != 16:
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, "密钥必须为16位二进制")
            return
        if operation == "encrypt":
            result = encrypt_ascii(data, key)
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, f"加密结果: {result}")  # 插入加密结果
        else:
            result = decrypt_ascii(data, key)
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, f"解密结果: {result}")  # 插入解密结果


def show_binary_mode():
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="输入16位二进制数据/密文：", font=label_font, bg='lightblue').grid(row=0, column=0,
                                                                                                pady=10)
    data_entry = tk.Entry(main_frame, font=label_font, width=20)
    data_entry.grid(row=0, column=1, pady=10)

    tk.Label(main_frame, text="输入16位二进制密钥：", font=label_font, bg='lightblue').grid(row=1, column=0, pady=10)
    key_entry = tk.Entry(main_frame, font=label_font, width=20)
    key_entry.grid(row=1, column=1, pady=10)

    tk.Label(main_frame, text="选择操作：", font=label_font, bg='lightblue').grid(row=2, column=0, pady=10)

    # 纵向布局按钮
    encrypt_button = tk.Button(main_frame, text="加密", font=button_font,
                               command=lambda: process_data(data_entry.get(), key_entry.get(), "encrypt"))
    encrypt_button.grid(row=2, column=1, pady=10)

    decrypt_button = tk.Button(main_frame, text="解密", font=button_font,
                               command=lambda: process_data(data_entry.get(), key_entry.get(), "decrypt"))
    decrypt_button.grid(row=3, column=1, pady=10)

    # 添加返回按钮
    back_button = tk.Button(main_frame, text="返回", font=button_font, command=show_home)
    back_button.grid(row=4, column=1, pady=10)

    result_label = tk.Label(main_frame, text="结果：", font=result_font, bg='lightblue')
    result_label.grid(row=5, column=0, pady=10)
    result_text = tk.Entry(main_frame, font=result_font, bg='lightblue', width=30)  # 增加宽度
    result_text.grid(row=5, column=1, pady=10)

    def is_binary(s):
        """检查字符串是否为二进制字符串（只包含0和1）"""
        return re.match(r'^[01]+$', s) is not None

    def process_data(data, key, operation):
        # 检查输入长度是否为16位
        if len(data) != 16 or len(key) != 16:
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, "输入必须为16位二进制")
            return
        # 检查输入是否为二进制
        if not is_binary(data) or not is_binary(key):
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, "输入必须为二进制字符串")
            return
        if operation == "encrypt":
            result = ades_encrypt(data, key)
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, f"加密结果: {result}")  # 插入加密结果
        else:
            result = ades_decrypt(data, key)
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, f"解密结果: {result}")  # 插入解密结果


def show_double_binary_mode():
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="输入16位二进制数据/密文：", font=label_font, bg='lightblue').grid(row=0, column=0,
                                                                                                pady=10)
    data_entry = tk.Entry(main_frame, font=label_font, width=20)
    data_entry.grid(row=0, column=1, pady=10)

    tk.Label(main_frame, text="输入32位二进制密钥：", font=label_font, bg='lightblue').grid(row=1, column=0, pady=10)
    key_entry = tk.Entry(main_frame, font=label_font, width=40)
    key_entry.grid(row=1, column=1, pady=10)

    tk.Label(main_frame, text="选择操作：", font=label_font, bg='lightblue').grid(row=2, column=0, pady=10)

    # 纵向布局按钮
    encrypt_button = tk.Button(main_frame, text="加密", font=button_font,
                               command=lambda: process_data(data_entry.get(), key_entry.get(), "encrypt"))
    encrypt_button.grid(row=2, column=1, pady=10)

    decrypt_button = tk.Button(main_frame, text="解密", font=button_font,
                               command=lambda: process_data(data_entry.get(), key_entry.get(), "decrypt"))
    decrypt_button.grid(row=3, column=1, pady=10)

    # 添加返回按钮
    back_button = tk.Button(main_frame, text="返回", font=button_font, command=show_home)
    back_button.grid(row=4, column=1, pady=10)

    result_label = tk.Label(main_frame, text="结果：", font=result_font, bg='lightblue')
    result_label.grid(row=5, column=0, pady=10)
    result_text = tk.Entry(main_frame, font=result_font, bg='lightblue', width=30)  # 增加宽度
    result_text.grid(row=5, column=1, pady=10)

    def is_binary(s):
        """检查字符串是否为二进制字符串（只包含0和1）"""
        return re.match(r'^[01]+$', s) is not None

    def process_data(data, key, operation):
        # 检查输入长度是否为16位
        if len(data) != 16 or len(key) != 32:
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, "数据/密钥必须为16位/32位二进制")
            return
        # 检查输入是否为二进制
        if not is_binary(data) or not is_binary(key):
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, "输入必须为二进制字符串")
            return
        if operation == "encrypt":
            result = double_ades_encrypt(data, key)
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, f"加密结果: {result}")  # 插入加密结果
        else:
            result = double_ades_decrypt(data, key)
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, f"解密结果: {result}")  # 插入解密结果


def show_treble_binary_mode():
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="输入16位二进制数据/密文：", font=label_font, bg='lightblue').grid(row=0, column=0,
                                                                                                pady=10)
    data_entry = tk.Entry(main_frame, font=label_font, width=20)
    data_entry.grid(row=0, column=1, pady=10)

    tk.Label(main_frame, text="输入32位二进制密钥：", font=label_font, bg='lightblue').grid(row=1, column=0, pady=10)
    key_entry = tk.Entry(main_frame, font=label_font, width=40)
    key_entry.grid(row=1, column=1, pady=10)

    tk.Label(main_frame, text="选择操作：", font=label_font, bg='lightblue').grid(row=2, column=0, pady=10)

    # 纵向布局按钮
    encrypt_button = tk.Button(main_frame, text="加密", font=button_font,
                               command=lambda: process_data(data_entry.get(), key_entry.get(), "encrypt"))
    encrypt_button.grid(row=2, column=1, pady=10)

    decrypt_button = tk.Button(main_frame, text="解密", font=button_font,
                               command=lambda: process_data(data_entry.get(), key_entry.get(), "decrypt"))
    decrypt_button.grid(row=3, column=1, pady=10)

    # 添加返回按钮
    back_button = tk.Button(main_frame, text="返回", font=button_font, command=show_home)
    back_button.grid(row=4, column=1, pady=10)

    result_label = tk.Label(main_frame, text="结果：", font=result_font, bg='lightblue')
    result_label.grid(row=5, column=0, pady=10)
    result_text = tk.Entry(main_frame, font=result_font, bg='lightblue', width=30)  # 增加宽度
    result_text.grid(row=5, column=1, pady=10)

    def is_binary(s):
        """检查字符串是否为二进制字符串（只包含0和1）"""
        return re.match(r'^[01]+$', s) is not None

    def process_data(data, key, operation):
        # 检查输入长度是否为16位
        if len(data) != 16 or len(key) != 32:
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, "数据/密钥必须为16位/32位二进制")
            return
        # 检查输入是否为二进制
        if not is_binary(data) or not is_binary(key):
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, "输入必须为二进制字符串")
            return
        if operation == "encrypt":
            result = treble_ades_encrypt(data, key)
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, f"加密结果: {result}")  # 插入加密结果
        else:
            result = treble_ades_decrypt(data, key)
            result_text.delete(0, tk.END)  # 清空结果框
            result_text.insert(0, f"解密结果: {result}")  # 插入解密结果


def show_CBC_mode():
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="输入长文本（二进制，长度为16的倍数）", font=label_font, bg='lightblue').grid(row=0, column=0,
                                                                                                pady=10)
    data_entry = tk.Text(main_frame, font=label_font, width=20, height=5)  # 使用Text控件，设置高度为5行
    data_entry.grid(row=0, column=1, pady=10)

    tk.Label(main_frame, text="输入16位二进制密钥：", font=label_font, bg='lightblue').grid(row=1, column=0, pady=10)
    key_entry = tk.Entry(main_frame, font=label_font, width=20)
    key_entry.grid(row=1, column=1, pady=10)

    tk.Label(main_frame, text="输入16位二进制IV：", font=label_font, bg='lightblue').grid(row=2, column=0, pady=10)
    iv_entry = tk.Entry(main_frame, font=label_font, width=20)
    iv_entry.grid(row=2, column=1, pady=10)

    tk.Label(main_frame, text="选择操作：", font=label_font, bg='lightblue').grid(row=3, column=0, pady=10)

    # 纵向布局按钮
    encrypt_button = tk.Button(main_frame, text="加密", font=button_font,
                               command=lambda: process_data(data_entry.get("1.0", tk.END).strip(), key_entry.get(),
                                                            iv_entry.get(), "encrypt"))
    encrypt_button.grid(row=3, column=1, pady=10)

    decrypt_button = tk.Button(main_frame, text="解密", font=button_font,
                               command=lambda: process_data(data_entry.get("1.0", tk.END).strip(), key_entry.get(),
                                                            iv_entry.get(), "decrypt"))
    decrypt_button.grid(row=4, column=1, pady=10)

    # 添加返回按钮
    back_button = tk.Button(main_frame, text="返回", font=button_font, command=show_home)
    back_button.grid(row=5, column=1, pady=10)

    result_label = tk.Label(main_frame, text="结果：", font=result_font, bg='lightblue')
    result_label.grid(row=6, column=0, pady=10)
    result_text = tk.Text(main_frame, font=result_font, bg='lightblue', width=20, height=5)  # 使用Text控件，设置高度为5行
    result_text.grid(row=6, column=1, pady=10)

    def is_binary(s):
        """检查字符串是否为二进制字符串（只包含0和1）"""
        return re.match(r'^[01]+$', s) is not None

    def process_data(data, key, iv, operation):
        # 检查密钥和初始向量是否为16位二进制
        if len(key) != 16 or len(iv) != 16:
            result_text.delete("1.0", tk.END)  # 清空结果框
            result_text.insert("1.0", "密钥和初始向量必须为16位二进制")
            return
        # 检查明文长度是否为16位的倍数
        if len(data) % 16 != 0:
            result_text.delete("1.0", tk.END)  # 清空结果框
            result_text.insert("1.0", "数据长度必须是16位的倍数")
            return
        # 检查密钥和初始向量是否为二进制
        if not is_binary(key) or not is_binary(iv) or not is_binary(data):
            result_text.delete("1.0", tk.END)  # 清空结果框
            result_text.insert("1.0", "输入必须为二进制字符串")
            return

        if operation == "encrypt":
            result = cbc_encrypt(data, key, iv)
            result_text.delete("1.0", tk.END)  # 清空结果框
            result_text.insert("1.0", f"加密结果: {result}")  # 插入加密结果
        else:
            result = cbc_decrypt(data, key, iv)
            result_text.delete("1.0", tk.END)  # 清空结果框
            result_text.insert("1.0", f"解密结果: {result}")  # 插入解密结果


show_home()
root.mainloop()

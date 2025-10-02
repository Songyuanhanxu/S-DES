"""
S-DES (Simplified DES) 核心算法模块
==================================
本模块实现了S-DES算法的核心功能，包括基本的加密/解密算法和工具函数。

"""
from typing import List, Tuple

# ---------- S-DES 标准参数定义 ----------
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]  # P10: 10位密钥的置换表
P8 = [6, 3, 7, 4, 8, 5, 10, 9]  # P8: 8位子密钥生成置换表
IP = [2, 6, 3, 1, 4, 8, 5, 7]  # IP: 初始置换表
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]  # IP^-1: 最终置换表（初始置换的逆）
EP = [4, 1, 2, 3, 2, 3, 4, 1]  # EP: 扩展置换表
SP = [2, 4, 3, 1]  # P4: 4位置换表
S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 0, 2],
]  # 第一个替代盒S0

S1 = [
    [0, 1, 2, 3],
    [2, 3, 1, 0],
    [3, 0, 1, 2],
    [2, 1, 0, 3],
]  # 第二个替代盒S1


# ---------- 工具函数 ----------
def permutation(bits: List[int], perm_table: List[int]) -> List[int]:
    """
    根据置换表对比特序列进行置换
    
    参数:
        bits: 输入比特序列
        perm_table: 置换表，索引从1开始
        
    返回:
        置换后的比特序列
    """
    return [bits[i-1] for i in perm_table]


def left_shift(bits: List[int], shift_count: int) -> List[int]:
    """
    对比特序列进行循环左移
    
    参数:
        bits: 输入比特序列
        shift_count: 左移位数
        
    返回:
        循环左移后的比特序列
    """
    shift_count = shift_count % len(bits)
    return bits[shift_count:] + bits[:shift_count]


def bits_from_int(value: int, width: int) -> List[int]:
    """
    将整数转换为指定宽度的比特列表
    """
    return [(value >> (width-1-i)) & 1 for i in range(width)]


def int_from_bits(bits: List[int]) -> int:
    """
    将比特列表转换为整数
    """
    val = 0
    for b in bits:
        val = (val << 1) | (b & 1)
    return val


def bits_from_bitstring(s: str) -> List[int]:
    """
    将二进制字符串转换为比特列表
    """
    s = s.strip()
    if any(ch not in '01' for ch in s):
        raise ValueError("二进制字符串必须只包含 '0' 或 '1'")
    return [int(ch) for ch in s]


def bitstring_from_bits(bits: List[int]) -> str:
    """
    将比特列表转换为二进制字符串
    """
    return ''.join('1' if b else '0' for b in bits)


# ---------- 密钥生成 ----------
def generate_subkeys(key10: List[int]) -> Tuple[List[int], List[int]]:
    """
    从10位主密钥生成两个8位子密钥
    
    参数:
        key10: 10位主密钥
        
    返回:
        元组 (k1, k2)，其中k1和k2是8位子密钥
        
    异常:
        ValueError: 如果输入密钥不是10位
    """
    if len(key10) != 10:
        raise ValueError("主密钥必须为10位")

    permuted = permutation(key10, P10)  # 应用P10置换
    left, right = permuted[:5], permuted[5:]  # 分成左右两部分
    left1, right1 = left_shift(left, 1), left_shift(right, 1)  # 对L,R分别循环左移1位
    k1 = permutation(left1 + right1, P8)  # 合并,经过P8置换得到k1
    left2, right2 = left_shift(left1, 2), left_shift(right1, 2)  # 对L,R再循环左移2位
    k2 = permutation(left2 + right2, P8)  # 合并，经过P8置换得到k2

    return k1, k2


# ---------- S-DES 轮函数 ----------
def sbox_substitution(bits4: List[int], sbox: List[List[int]]) -> List[int]:
    """
    使用S-Box进行4位到2位的替代
    
    参数:
        bits4: 4位输入比特
        sbox: S-Box查找表
        
    返回:
        2位输出比特
    """

    row = (bits4[0] << 1) | bits4[3]  # 行索引由第1位和第4位组成
    col = (bits4[1] << 1) | bits4[2]  # 列索引由第2位和第3位组成
    val = sbox[row][col]  # 查表获取值
    return [(val >> 1) & 1, val & 1]  # 转换为2位比特


def round_func(bits8: List[int], subkey8: List[int]) -> List[int]:
    """
    S-DES的轮函数 fk，对8位数据使用8位子密钥进行一轮加密操作
    """
    if len(bits8) != 8 or len(subkey8) != 8:
        raise ValueError("轮函数需要8位数据和8位子密钥")

    l, r = bits8[:4], bits8[4:]  # 分成L,R两部分，各4bit
    expanded = permutation(r, EP)  # EP-box,扩展R从4bit到8bit
    xored = [a ^ b for a, b in zip(expanded, subkey8)]  # 与子密钥进行异或
    left_x, right_x = xored[:4], xored[4:]  # 分成L,R两部分，各4bit
    s0_out = sbox_substitution(left_x, S0)  # 通过S-Box进行替换
    s1_out = sbox_substitution(right_x, S1)
    s_out = s0_out + s1_out
    p4_out = permutation(s_out, SP)  # 用SP 4bit直接置换
    new_l = [a ^ b for a, b in zip(l, p4_out)]  # 与L进行异或得到新L

    # 8. 返回新的左半部分和原来的右半部分
    return new_l + r

# ---------- 加密/解密单字节块 ----------
def encode(plaintext8: List[int], key10: List[int]) -> List[int]:
    """
    使用S-DES算法加密8位明文块
    """
    if len(plaintext8) != 8:
        raise ValueError("明文必须为8位")

    k1, k2 = generate_subkeys(key10)        # 生成子密钥
    temp = permutation(plaintext8, IP)      # 初始置换IP
    temp = round_func(temp, k1)             # 第一轮加密 fk1
    temp = temp[4:] + temp[:4]              # 交换左右两部分
    temp = round_func(temp, k2)             # 第二轮加密 fk2
    ciphertext = permutation(temp, IP_INV)  # 最终置换IP-1

    return ciphertext

def decode(ciphertext8: List[int], key10: List[int]) -> List[int]:
    """
    使用S-DES算法解密8位密文块
    """

    k1, k2 = generate_subkeys(key10)        # 生成子密钥
    temp = permutation(ciphertext8, IP)     # 初始置换IP
    temp = round_func(temp, k2)             # 第一轮加密 fk1
    temp = temp[4:] + temp[:4]              # 交换左右两部分
    temp = round_func(temp, k1)             # 第二轮加密 fk2
    plaintext = permutation(temp, IP_INV)   # 最终置换IP-1

    return plaintext

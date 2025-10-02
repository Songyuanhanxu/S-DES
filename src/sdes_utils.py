"""
S-DES (Simplified DES) 工具模块
==============================
本模块提供了S-DES算法的扩展功能，包括字符串加密解密和暴力破解。

"""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Optional

# 导入核心功能
from src.sdes_core import (
    bits_from_int, int_from_bits, encode, decode,
    bits_from_bitstring, bitstring_from_bits
)

# ---------- 字符串加密/解密 ----------
def encode_str(plain_bytes: str, key10: List[int]) -> str:
    """
    加密字符串并返回加密后的字符串
    """
    # 将文本转换为UTF-8字节
    text_bytes = plain_bytes.encode('utf-8')
    
    # 逐字节加密
    cipher_bytes = bytearray()
    for b in text_bytes:
        bits = bits_from_int(b, 8)  # 将字节转换为8位比特列表
        cipher_bits = encode(bits, key10)  # 使用S-DES加密
        cipher_bytes.append(int_from_bits(cipher_bits))  # 将加密后的比特列表转换回字节
    
    # 将加密后的字节转换为字符串（使用latin1编码确保所有字节都能被解码）
    return bytes(cipher_bytes).decode('latin1')

def decode_str(cipher_bytes: str, key10: List[int]) -> str:
    """
    解密字符串密文为原始字符串
    """
    cipher_bytes = cipher_bytes.encode('latin1')  # 将密文文本转换为字节序列
    
    # 逐字节解密
    plain_bytes = bytearray()
    for b in cipher_bytes:
        bits = bits_from_int(b, 8)  # 将字节转换为8位比特列表
        plain_bits = decode(bits, key10)  # 使用S-DES解密
        plain_bytes.append(int_from_bits(plain_bits))  # 将解密后的比特列表转换回字节

    return bytes(plain_bytes).decode('latin1', errors='replace')

# ---------- 暴力破解（多线程）----------
def check_key_for_pairs(key_int: int, pairs: List[Tuple[int, int]]) -> Optional[int]:
    """
    检查一个密钥是否符合所有给定的明密文对
    
    参数:
        key_int: 整数形式的密钥(0-1023)
        pairs: 明密文对列表，每对为(明文整数, 密文整数)
        
    返回:
        如果密钥符合所有明密文对，返回密钥整数；否则返回None
    """
    key_bits = bits_from_int(key_int, 10)
    for p, c in pairs:
        encrypted = int_from_bits(encode(bits_from_int(p, 8), key_bits))
        if encrypted != c:
            return None
    return key_int

def brute_force_known_pairs(pairs: List[Tuple[int, int]], workers: int=8) -> Tuple[List[int], float]:
    """
    暴力破解已知明密文对的密钥
    
    参数:
        pairs: 明密文对列表，每对为(明文整数, 密文整数)
        workers: 线程数
        
    返回:
        元组 (候选密钥列表, 耗时秒数)
    """
    start = time.time()
    candidates = []
    
    # 使用多线程加速破解
    with ThreadPoolExecutor(max_workers=workers) as ex:
        # 提交所有可能的密钥(0-1023)进行检查
        futures = {ex.submit(check_key_for_pairs, k, pairs): k for k in range(1024)}
        
        # 收集结果
        for fut in as_completed(futures):
            res = fut.result()
            if res is not None:
                candidates.append(res)
                
    elapsed = time.time() - start
    return sorted(candidates), elapsed

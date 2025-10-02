"""
S-DES (Simplified DES) 主程序
===========================
本文件是S-DES实验的主入口点，整合了所有模块功能。

"""
import sys
import argparse

# 导入所有模块
from src.sdes_core import (
    bits_from_bitstring, bitstring_from_bits, encode, decode
)
from src.sdes_utils import (
    encode_str, decode_str,
    brute_force_known_pairs
)
from src.sdes_web import start_web_app

def print_banner():
    """打印程序横幅"""
    banner = """
    ╔═══════════════════════════════════════════════╗
                       S-DES实验                    
    ║        Simplified Data Encryption Standard    ║
    ╚═══════════════════════════════════════════════╝

    """
    print(banner)

def parse_args():
    """解析命令行参数"""
    p = argparse.ArgumentParser(description="S-DES 实验工具 — 五关测试")
    
    # 基本选项
    p.add_argument('--web', action='store_true', help='启动 Web 界面（第1关）')
    p.add_argument('--port', type=int, default=5000, help='Web 界面端口号（默认：5000）')
    p.add_argument('--interactive', '-i', action='store_true', help='启动交互式模式')
    p.add_argument('--version', action='store_true', help='显示版本信息')
    
    return p.parse_args()

def interactive_mode():
    """交互式模式"""
    print_banner()
    print("\n欢迎使用S-DES实验工具交互式模式!\n")
    
    while True:
        print("\n请选择操作模式:")
        print("1. 启动Web界面")
        print("2. 单字节加密")
        print("3. 单字节解密")
        print("4. 字符串加密")
        print("5. 字符串解密")
        print("6. 暴力破解")
        print("0. 退出程序")
        
        choice = input("\n请输入选项编号: ")
        
        if choice == '0':
            print("感谢使用S-DES实验工具，再见!")
            break
            
        elif choice == '1':
            print("\n启动Web界面，请在浏览器中访问 http://127.0.0.1:5000/")
            start_web_app()
            break
            
        elif choice == '2':
            plaintext = input("请输入8位二进制明文(如10101010): ")
            key = input("请输入10位二进制密钥(如1010000010): ")
            try:
                pbits = bits_from_bitstring(plaintext)
                kbits = bits_from_bitstring(key)
                cbits = encode(pbits, kbits)
                print(f"\n加密结果: {bitstring_from_bits(cbits)}")
            except Exception as e:
                print(f"\n错误: {str(e)}")
                
        elif choice == '3':
            ciphertext = input("请输入8位二进制密文(如10001101): ")
            key = input("请输入10位二进制密钥(如1010000010): ")
            try:
                cbits = bits_from_bitstring(ciphertext)
                kbits = bits_from_bitstring(key)
                pbits = decode(cbits, kbits)
                print(f"\n解密结果: {bitstring_from_bits(pbits)}")
            except Exception as e:
                print(f"\n错误: {str(e)}")
                
        elif choice == '4':
            text = input("请输入要加密的字符串: ")
            key = input("请输入10位二进制密钥(如1010000010): ")
            try:
                kbits = bits_from_bitstring(key)
                result = encode_str(text, kbits)
                print(f"\n加密结果: {result}")
                print("注意: 加密结果可能包含不可打印字符")
            except Exception as e:
                print(f"\n错误: {str(e)}")
                
        elif choice == '5':
            ciphertext = input("请输入加密后的字符串: ")
            key = input("请输入10位二进制密钥(如1010000010): ")
            try:
                kbits = bits_from_bitstring(key)
                text = decode_str(ciphertext, kbits)
                print(f"\n解密结果: {text}")
            except Exception as e:
                print(f"\n错误: {str(e)}")
                
        elif choice == '6':
            plaintext = input("请输入8位二进制明文(如10101010): ")
            ciphertext = input("请输入8位二进制密文(如10001101): ")
            workers_str = input("请输入线程数(默认4): ")
            workers = int(workers_str) if workers_str.isdigit() else 4
            
            try:
                print("\n使用多线程暴力破解中...")
                p = int(plaintext, 2)
                c = int(ciphertext, 2)
                pairs = [(p, c)]
                keys, elapsed = brute_force_known_pairs(pairs, workers=workers)
                    
                print(f"\n找到 {len(keys)} 个匹配密钥:")
                print(f"十进制: {keys}")
                print(f"二进制: {[format(k, '010b') for k in keys]}")
                print(f"耗时: {elapsed:.4f} 秒")
            except Exception as e:
                print(f"\n错误: {str(e)}")

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 显示版本信息
    if args.version:
        print("S-DES 实验工具 v1.0.0")
        return
    
    # 如果没有参数，进入交互式模式
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    # 交互式模式
    if args.interactive:
        interactive_mode()
        return
        
    # 第1关：Web界面
    if args.web:
        start_web_app(port=args.port)
        return
    
    # 第2关：基本加密解密
    if args.encrypt_block:
        plain, key = args.encrypt_block
        pbits = bits_from_bitstring(plain)
        kbits = bits_from_bitstring(key)
        cbits = encode(pbits, kbits)
        print("密文:", bitstring_from_bits(cbits))
        return
        
    if args.decrypt_block:
        cipher, key = args.decrypt_block
        cbits = bits_from_bitstring(cipher)
        kbits = bits_from_bitstring(key)
        pbits = decode(cbits, kbits)
        print("明文:", bitstring_from_bits(pbits))
        return
    
    # 第3关：文本加密
    if args.encrypt_text:
        text, key = args.encrypt_text
        kbits = bits_from_bitstring(key)
        print(encode_str(text, kbits))
        return
        
    if args.decrypt_hex:
        hx, key = args.decrypt_hex
        kbits = bits_from_bitstring(key)
        print(decode_str(hx, kbits))
        return
    
    # 第4关：暴力破解
    if args.bruteforce:
        pstr, cstr, workers = args.bruteforce
        workers = int(workers)
        p = int(pstr, 2)
        c = int(cstr, 2)
        pairs = [(p, c)]
        print(f"使用多线程暴力破解 (线程数: {workers})...")
        keys, elapsed = brute_force_known_pairs(pairs, workers=workers)
        print(f"找到的密钥(十进制): {keys}")
        print(f"找到的密钥(二进制): {[format(k, '010b') for k in keys]}")
        print(f"耗时: {elapsed:.4f}秒")
        return

    print("请使用 --help 查看可用选项。")

if __name__ == "__main__":
    main()

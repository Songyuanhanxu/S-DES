"""
S-DES (Simplified DES) Web界面模块
================================
本模块提供了S-DES算法的Web界面，使用Flask框架实现。

"""
from flask import Flask, render_template, request, jsonify
import os
import json

# 导入核心功能和工具
from src.sdes_core import (
    bits_from_bitstring, bitstring_from_bits, encode, decode
)
from src.sdes_utils import encode_str, decode_str, brute_force_known_pairs

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 创建Flask应用，指定模板和静态文件目录
app = Flask(__name__, 
           template_folder=os.path.join(ROOT_DIR, 'templates'),
           static_folder=os.path.join(ROOT_DIR, 'static'))

# 确保templates目录存在
templates_dir = os.path.join(ROOT_DIR, 'templates')
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

# 确保static目录存在
static_dir = os.path.join(ROOT_DIR, 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/api/encrypt_block', methods=['POST'])
def api_encrypt_block():
    """API: 加密单个8位块"""
    try:
        data = request.get_json()
        plaintext = data.get('plaintext', '')
        key = data.get('key', '')
        
        # 验证输入
        if len(plaintext) != 8 or not all(bit in '01' for bit in plaintext):
            return jsonify({'error': '明文必须是8位二进制字符串'}), 400
        if len(key) != 10 or not all(bit in '01' for bit in key):
            return jsonify({'error': '密钥必须是10位二进制字符串'}), 400
            
        # 执行加密
        pbits = bits_from_bitstring(plaintext)
        kbits = bits_from_bitstring(key)
        cbits = encode(pbits, kbits)
        ciphertext = bitstring_from_bits(cbits)
        
        return jsonify({'ciphertext': ciphertext})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt_block', methods=['POST'])
def api_decrypt_block():
    """API: 解密单个8位块"""
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext', '')
        key = data.get('key', '')
        
        # 验证输入
        if len(ciphertext) != 8 or not all(bit in '01' for bit in ciphertext):
            return jsonify({'error': '密文必须是8位二进制字符串'}), 400
        if len(key) != 10 or not all(bit in '01' for bit in key):
            return jsonify({'error': '密钥必须是10位二进制字符串'}), 400
            
        # 执行解密
        cbits = bits_from_bitstring(ciphertext)
        kbits = bits_from_bitstring(key)
        pbits = decode(cbits, kbits)
        plaintext = bitstring_from_bits(pbits)
        
        return jsonify({'plaintext': plaintext})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/encrypt_text_direct', methods=['POST'])
def api_encrypt_text_direct():
    """API: 加密文本"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        key = data.get('key', '')
        
        # 验证输入
        if not text:
            return jsonify({'error': '文本不能为空'}), 400
        if len(key) != 10 or not all(bit in '01' for bit in key):
            return jsonify({'error': '密钥必须是10位二进制字符串'}), 400
            
        # 执行加密
        kbits = bits_from_bitstring(key)
        result = encode_str(text, kbits)
        
        return jsonify({'text': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt_text_direct', methods=['POST'])
def api_decrypt_text_direct():
    """API: 解密文本"""
    try:
        data = request.get_json()
        ciphertext = data.get('text', '')
        key = data.get('key', '')
        
        # 验证输入
        if not ciphertext:
            return jsonify({'error': '密文不能为空'}), 400
        if len(key) != 10 or not all(bit in '01' for bit in key):
            return jsonify({'error': '密钥必须是10位二进制字符串'}), 400
            
        # 执行解密
        kbits = bits_from_bitstring(key)
        result = decode_str(ciphertext, kbits)
        
        return jsonify({'text': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bruteforce', methods=['POST'])
def api_bruteforce():
    """API: 暴力破解"""
    try:
        data = request.get_json()
        plaintext = data.get('plaintext', '')
        ciphertext = data.get('ciphertext', '')
        workers = data.get('workers', 4)   # 线程数
        
        # 验证输入
        if len(plaintext) != 8 or not all(bit in '01' for bit in plaintext):
            return jsonify({'error': '明文必须是8位二进制字符串'}), 400
        if len(ciphertext) != 8 or not all(bit in '01' for bit in ciphertext):
            return jsonify({'error': '密文必须是8位二进制字符串'}), 400
        
        # 执行暴力破解
        p = int(plaintext, 2)
        c = int(ciphertext, 2)
        pairs = [(p, c)]
        
        keys, elapsed = brute_force_known_pairs(pairs, workers=workers)
        
        # 格式化结果
        binary_keys = [format(k, '010b') for k in keys]
        
        return jsonify({
            'keys': keys,
            'binary_keys': binary_keys,
            'count': len(keys),
            'elapsed': elapsed
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def start_web_app(host='127.0.0.1', port=5000, debug=False):
    """启动Web应用"""
    print(f"S-DES Web界面启动在 http://{host}:{port}/")
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    # 当作为独立程序运行时，启动Web应用
    start_web_app(debug=True)

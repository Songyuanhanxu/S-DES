# S-DES 开发手册

## 项目架构

### 目录结构
```
PythonProject/
├── src/                     # 源代码目录
│   ├── __init__.py          # Python包标识
│   ├── sdes_core.py         # S-DES核心算法实现
│   ├── sdes_utils.py        # 扩展功能（字符串加密、暴力破解）
│   └── sdes_web.py          # Flask Web服务器
├── static/                  # 静态文件目录
│   ├── css/                 # 样式表
│   │   ├── main.css         # 主样式表
│   │   └── dark-mode.css    # 暗黑模式样式
│   └── js/                  # JavaScript文件
│       ├── app.js           # 主脚本
│       └── animations.js    # 动画效果   
├── templates/               # 模板目录
│   └── index.html           # Web界面模板
├── docs/                    # 文档目录
│   ├── DEVELOPER_GUIDE.md   # 开发者指南
│   └── FIVE_TESTS.md        # 五关测试报告
├── screenshots/             # 项目截图
├── sdes_main.py             # 主程序入口
└── README.md                # 项目说明文档
```

### 模块结构
```
src/sdes_core.py      # 核心算法模块
├── 标准参数定义
├── 工具函数
├── 密钥生成
├── 轮函数
└── 加密/解密

src/sdes_utils.py     # 扩展功能模块
├── 字符串加密/解密
└── 暴力破解

src/sdes_web.py       # Web服务器模块
├── Flask应用
├── API路由
└── 模板渲染

sdes_main.py          # 主程序入口
├── 命令行参数解析
├── 交互式模式
└── 功能分发
```

## 核心组件接口文档

### sdes_core.py 接口

#### 基础工具函数
```python
def permutation(bits: List[int], perm_table: List[int]) -> List[int]
    """根据置换表对比特序列进行置换"""
    
def left_shift(bits: List[int], shift_count: int) -> List[int]
    """对比特序列进行循环左移"""
    
def bits_from_int(value: int, width: int) -> List[int]
    """将整数转换为指定宽度的比特列表"""
    
def int_from_bits(bits: List[int]) -> int
    """将比特列表转换为整数"""
    
def bits_from_bitstring(s: str) -> List[int]
    """将二进制字符串转换为比特列表"""
    
def bitstring_from_bits(bits: List[int]) -> str
    """将比特列表转换为二进制字符串"""
```

#### 密钥生成
```python
def generate_subkeys(key10: List[int]) -> Tuple[List[int], List[int]]
    """
    从10位主密钥生成两个8位子密钥
    
    参数:
        key10: 10位主密钥
        
    返回:
        元组 (k1, k2)，其中k1和k2是8位子密钥
        
    异常:
        ValueError: 如果输入密钥不是10位
    """
```

#### 核心算法
```python
def encode(plaintext8: List[int], key10: List[int]) -> List[int]
    """
    使用S-DES算法加密8位明文块
    
    参数:
        plaintext8: 8位明文比特列表
        key10: 10位密钥比特列表
        
    返回:
        8位密文比特列表
        
    异常:
        ValueError: 如果明文不是8位
    """

def decode(ciphertext8: List[int], key10: List[int]) -> List[int]
    """
    使用S-DES算法解密8位密文块
    
    参数:
        ciphertext8: 8位密文比特列表
        key10: 10位密钥比特列表
        
    返回:
        8位明文比特列表
    """
```

### sdes_utils.py 接口

#### 字符串加密/解密
```python
def encode_str(plain_text: str, key10: List[int]) -> str
    """
    加密字符串并返回加密后的字符串
    
    参数:
        plain_text: 要加密的原始字符串
        key10: 10位密钥比特列表
        
    返回:
        加密后的字符串（可能包含不可打印字符）
    """

def decode_str(cipher_text: str, key10: List[int]) -> str
    """
    解密字符串密文为原始字符串
    
    参数:
        cipher_text: 加密后的字符串
        key10: 10位密钥比特列表
        
    返回:
        解密后的原始字符串
    """
```

#### 暴力破解
```python
def brute_force_known_pairs(pairs: List[Tuple[int, int]], workers: int=8) -> Tuple[List[int], float]
    """
    暴力破解已知明密文对的密钥
    
    参数:
        pairs: 明密文对列表，每对为(明文整数, 密文整数)
        workers: 线程数
        
    返回:
        元组 (候选密钥列表, 耗时秒数)
    """
```

### sdes_web.py 接口

#### Flask应用
```python
def start_web_app(port: int = 5000) -> None
    """启动Flask Web服务器"""
```

#### API端点
```python
@app.route('/api/encrypt_block', methods=['POST'])
def api_encrypt_block():
    """API: 单字节加密"""

@app.route('/api/decrypt_block', methods=['POST'])
def api_decrypt_block():
    """API: 单字节解密"""

@app.route('/api/encrypt_text_direct', methods=['POST'])
def api_encrypt_text_direct():
    """API: 直接文本加密"""

@app.route('/api/decrypt_text_direct', methods=['POST'])
def api_decrypt_text_direct():
    """API: 直接文本解密"""

@app.route('/api/bruteforce', methods=['POST'])
def api_bruteforce():
    """API: 暴力破解"""
```

## 开发规范

### 代码风格
- 使用类型注解
- 遵循PEP 8规范
- 函数和变量使用描述性命名
- 添加详细的文档字符串

### 错误处理
- 使用具体的异常类型
- 提供有意义的错误消息
- 在适当的地方进行输入验证

### 测试
- 为每个核心函数编写单元测试
- 测试边界条件和异常情况
- 保持测试代码的可读性

## 扩展指南

### 添加新的加密模式
1. 在`sdes_core.py`中实现新的算法
2. 在`sdes_utils.py`中添加相应的工具函数
3. 在`sdes_web.py`中添加API端点
4. 在`sdes_main.py`中添加命令行参数

### 添加新的界面
1. 创建新的模块文件
2. 实现界面逻辑
3. 在`sdes_main.py`中集成
4. 更新文档

## 性能优化

### 多线程优化
- 使用`ThreadPoolExecutor`进行并行计算
- 合理设置线程数量
- 避免线程间的数据竞争

### 内存优化
- 及时释放不需要的对象
- 使用生成器处理大数据集
- 避免不必要的数据复制

## 调试技巧

### 日志记录
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### 调试工具
- 使用`pdb`进行交互式调试
- 使用`print`语句输出中间结果
- 使用IDE的调试器

## 部署指南

### 生产环境
1. 使用WSGI服务器（如Gunicorn）
2. 配置反向代理（如Nginx）
3. 设置环境变量
4. 配置日志记录

### Docker部署
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "sdes_main.py", "--web"]
```

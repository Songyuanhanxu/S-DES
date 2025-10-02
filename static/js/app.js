/**
 * S-DES Web界面主脚本
 */

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化暗黑模式
    initDarkMode();
    
    // 初始化工具提示
    initTooltips();
    
    // 绑定事件处理器
    bindEventHandlers();
});

/**
 * 初始化暗黑模式
 */
function initDarkMode() {
    // 创建暗黑模式切换按钮
    const darkModeToggle = document.createElement('div');
    darkModeToggle.className = 'dark-mode-toggle';
    darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    document.body.appendChild(darkModeToggle);
    
    // 检查本地存储中的暗黑模式设置
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    // 绑定暗黑模式切换事件
    darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark);
        darkModeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    });
}

/**
 * 初始化工具提示
 */
function initTooltips() {
    // 添加工具提示到需要解释的元素
    addTooltip('binary-input', '输入8位二进制数据，仅包含0和1');
    addTooltip('binary-key', '输入10位二进制密钥，仅包含0和1');
    addTooltip('bf-workers', '设置并行计算的线程数，更高的数值可能加速破解但会增加CPU负载');
}

/**
 * 添加工具提示到指定元素
 */
function addTooltip(elementId, text) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const label = element.previousElementSibling;
    if (label && label.tagName === 'LABEL') {
        const tooltip = document.createElement('span');
        tooltip.className = 'tooltip';
        tooltip.innerHTML = '<i class="fas fa-question-circle"></i><span class="tooltip-text">' + text + '</span>';
        label.appendChild(tooltip);
    }
}

/**
 * 绑定所有事件处理器
 */
function bindEventHandlers() {
    // 单字节加密
    document.getElementById('encrypt-btn').addEventListener('click', async function() {
        await handleOperation('encrypt');
    });
    
    // 单字节解密
    document.getElementById('decrypt-btn').addEventListener('click', async function() {
        await handleOperation('decrypt');
    });
    
    // 字符串加密
    document.getElementById('encrypt-direct-text-btn').addEventListener('click', async function() {
        await handleTextOperation('encrypt');
    });
    
    // 字符串解密
    document.getElementById('decrypt-direct-text-btn').addEventListener('click', async function() {
        await handleTextOperation('decrypt');
    });
    
    // 暴力破解
    document.getElementById('bruteforce-btn').addEventListener('click', async function() {
        await handleBruteforce();
    });
    
    // 添加输入验证
    addInputValidation('binary-input', validateBinary, 8);
    addInputValidation('binary-key', validateBinary, 10);
    addInputValidation('direct-text-key', validateBinary, 10);
    addInputValidation('bf-plaintext', validateBinary, 8);
    addInputValidation('bf-ciphertext', validateBinary, 8);
}

/**
 * 添加输入验证
 */
function addInputValidation(elementId, validationFunc, length) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.addEventListener('input', function() {
        const error = validationFunc(this.value, length);
        const errorElement = document.getElementById(elementId + '-error');
        if (errorElement) {
            errorElement.textContent = error || '';
            errorElement.style.display = error ? 'block' : 'none';
        }
    });
}

/**
 * 验证二进制输入
 */
function validateBinary(input, length) {
    const value = input.trim();
    if (!value) return '';
    if (value.length !== length) return `必须是${length}位二进制`;
    if (!/^[01]+$/.test(value)) return '只能包含0和1';
    return null;
}

/**
 * 处理单字节操作
 */
async function handleOperation(type) {
    const input = document.getElementById('binary-input').value;
    const key = document.getElementById('binary-key').value;
    
    // 验证输入
    const inputError = validateBinary(input, 8);
    const keyError = validateBinary(key, 10);
    
    showError('binary-input-error', inputError);
    showError('binary-key-error', keyError);
    
    if (!inputError && !keyError) {
        try {
            const url = type === 'encrypt' ? '/api/encrypt_block' : '/api/decrypt_block';
            const data = type === 'encrypt' ? 
                { plaintext: input, key: key } : 
                { ciphertext: input, key: key };
            
            const btn = document.getElementById(type === 'encrypt' ? 'encrypt-btn' : 'decrypt-btn');
            const originalText = btn.textContent;
            
            // 显示加载状态
            btn.innerHTML = '<span class="loading"></span>处理中...';
            btn.disabled = true;
            
            const result = await sendRequest(url, data);
            
            // 恢复按钮状态
            btn.innerHTML = originalText;
            btn.disabled = false;
            
            // 显示结果
            const resultText = type === 'encrypt' ? `密文: ${result.ciphertext}` : `明文: ${result.plaintext}`;
            showResult('binary-result', resultText, true);
        } catch (error) {
            showResult('binary-result', `错误: ${error.message}`, true);
        }
    }
}

/**
 * 处理文本操作
 */
async function handleTextOperation(type) {
    const text = document.getElementById('direct-text-input').value;
    const key = document.getElementById('direct-text-key').value;
    
    // 验证输入
    const keyError = validateBinary(key, 10);
    showError('direct-text-key-error', keyError);
    
    if (!text) {
        showResult('direct-text-result', `错误: ${type === 'encrypt' ? '文本' : '密文'}不能为空`, true);
        return;
    }
    
    if (!keyError) {
        try {
            const url = type === 'encrypt' ? '/api/encrypt_text_direct' : '/api/decrypt_text_direct';
            const data = { text: text, key: key };
            
            const btn = document.getElementById(type === 'encrypt' ? 'encrypt-direct-text-btn' : 'decrypt-direct-text-btn');
            const originalText = btn.textContent;
            
            // 显示加载状态
            btn.innerHTML = '<span class="loading"></span>处理中...';
            btn.disabled = true;
            
            const result = await sendRequest(url, data);
            
            // 恢复按钮状态
            btn.innerHTML = originalText;
            btn.disabled = false;
            
            // 显示结果
            const resultText = `${type === 'encrypt' ? '加密' : '解密'}结果: <pre>${escapeHTML(result.text)}</pre>`;
            showResult('direct-text-result', resultText, true);
        } catch (error) {
            showResult('direct-text-result', `错误: ${error.message}`, true);
        }
    }
}

/**
 * 处理暴力破解
 */
async function handleBruteforce() {
    const plaintext = document.getElementById('bf-plaintext').value;
    const ciphertext = document.getElementById('bf-ciphertext').value;
    const workers = document.getElementById('bf-workers').value;
    
    // 验证输入
    const plaintextError = validateBinary(plaintext, 8);
    const ciphertextError = validateBinary(ciphertext, 8);
    
    showError('bf-plaintext-error', plaintextError);
    showError('bf-ciphertext-error', ciphertextError);
    
    if (!plaintextError && !ciphertextError) {
        try {
            const btn = document.getElementById('bruteforce-btn');
            const originalText = btn.textContent;
            
            // 显示加载状态
            btn.innerHTML = '<span class="loading"></span>破解中...';
            btn.disabled = true;
            
            // 显示正在破解的信息
            showResult('bruteforce-result', '正在进行暴力破解，请稍候...', true);
            
            const result = await sendRequest('/api/bruteforce', {
                plaintext: plaintext,
                ciphertext: ciphertext,
                workers: parseInt(workers)
            });
            
            // 恢复按钮状态
            btn.innerHTML = originalText;
            btn.disabled = false;
            
            // 格式化结果
            let resultText = `找到 ${result.count} 个匹配密钥:\n`;
            resultText += `十进制: ${result.keys.join(', ')}\n`;
            resultText += `二进制: ${result.binary_keys.join(', ')}\n`;
            resultText += `耗时: ${result.elapsed.toFixed(4)} 秒`;
            
            showResult('bruteforce-result', resultText, true);
        } catch (error) {
            showResult('bruteforce-result', `错误: ${error.message}`, true);
        }
    }
}

/**
 * 发送API请求
 */
async function sendRequest(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || '请求失败');
        }
        return result;
    } catch (error) {
        throw error;
    }
}

/**
 * 显示错误信息
 */
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message || '';
        element.style.display = message ? 'block' : 'none';
    }
}

/**
 * 显示结果
 */
function showResult(elementId, message, animate = false) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = message;
        element.style.display = 'block';
        
        if (animate) {
            element.classList.remove('show');
            // 触发重绘
            void element.offsetWidth;
            element.classList.add('show');
        }
    }
}

/**
 * 将字符串转换为安全的HTML显示格式
 */
function escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

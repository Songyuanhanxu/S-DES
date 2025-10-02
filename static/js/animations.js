/**
 * S-DES Web界面动画效果脚本
 */

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化页面动画
    initPageAnimations();
    
    // 初始化加密动画
    initEncryptionAnimations();
});

/**
 * 初始化页面动画
 */
function initPageAnimations() {
    // 添加卡片入场动画
    animateCards();
    
    // 添加标题动画
    animateHeader();
}

/**
 * 卡片入场动画
 */
function animateCards() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach((card, index) => {
        // 初始状态
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        // 延迟显示
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + index * 150);
    });
}

/**
 * 标题动画
 */
function animateHeader() {
    const header = document.querySelector('.header');
    const title = document.querySelector('.header h1');
    const subtitle = document.querySelector('.header p');
    
    if (header && title && subtitle) {
        // 初始状态
        title.style.opacity = '0';
        title.style.transform = 'translateY(-20px)';
        subtitle.style.opacity = '0';
        
        // 标题动画
        setTimeout(() => {
            title.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            title.style.opacity = '1';
            title.style.transform = 'translateY(0)';
            
            // 副标题动画
            setTimeout(() => {
                subtitle.style.transition = 'opacity 0.8s ease';
                subtitle.style.opacity = '1';
            }, 400);
        }, 300);
    }
}

/**
 * 初始化加密动画
 */
function initEncryptionAnimations() {
    // 为加密/解密按钮添加点击波纹效果
    addRippleEffect('encrypt-btn');
    addRippleEffect('decrypt-btn');
    addRippleEffect('encrypt-direct-text-btn');
    addRippleEffect('decrypt-direct-text-btn');
    addRippleEffect('bruteforce-btn');
}

/**
 * 添加按钮点击波纹效果
 */
function addRippleEffect(elementId) {
    const button = document.getElementById(elementId);
    if (!button) return;
    
    button.classList.add('ripple-btn');
    
    button.addEventListener('click', function(e) {
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
    
    // 添加必要的CSS
    if (!document.getElementById('ripple-style')) {
        const style = document.createElement('style');
        style.id = 'ripple-style';
        style.textContent = `
            .ripple-btn {
                position: relative;
                overflow: hidden;
            }
            .ripple {
                position: absolute;
                border-radius: 50%;
                background-color: rgba(255, 255, 255, 0.7);
                transform: scale(0);
                animation: ripple-animation 0.6s linear;
                pointer-events: none;
            }
            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

/**
 * 创建加密过程可视化动画
 * 这个函数可以在将来实现，用于展示S-DES加密过程的可视化
 */
function createEncryptionVisualization(plaintext, key) {
    // 这里可以添加一个更复杂的可视化动画，展示S-DES的加密过程
    // 例如：显示初始置换、轮函数、子密钥生成等步骤
    console.log('可以在这里实现加密过程的可视化动画');
}

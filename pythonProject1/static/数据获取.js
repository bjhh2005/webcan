// 获取表单元素
const form = document.querySelector('form');

// 监听表单提交事件
form.addEventListener('submit', function(event) {
    // 阻止表单默认的提交行为
    event.preventDefault();

    // 获取表单输入的数据
    const email = document.getElementById('email').value;
    const verificationCode = document.getElementById('verification-code').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    // FormData对象来存储表单数据
    const formData = new FormData();
    formData.append('email', email);
    formData.append('verification-code', verificationCode);
    formData.append('password', password);
    formData.append('confirm_password', confirmPassword);

    // 新的XMLHttpRequest对象(ajax对象)
    const xhr = new XMLHttpRequest();

    // 初始化请求
    xhr.open('POST', '/user/captcha/email', true);

    // 监听请求状态改变事件
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // 请求成功，处理响应数据
            const response = xhr.responseText;
            console.log('Response:', response);
        } else if (xhr.readyState === 4) {
            // 请求完成，但状态不是200，处理错误
            console.error('Error:', xhr.status, xhr.statusText);
        }
    };

    // 发送请求
    xhr.send(formData);
});

// 处理发送验证码按钮的点击事件
document.querySelector('input[type="button"]').addEventListener('click', function() {
    // 这里可以添加发送验证码的逻辑，比如调用一个API发送验证码到用户邮箱
    console.log('Send verification code button clicked');
});
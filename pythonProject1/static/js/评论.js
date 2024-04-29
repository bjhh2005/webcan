document.addEventListener('DOMContentLoaded', function() {
    // 假设的后端数据
    const comments = [
        { username: '张三', rating: 4, comment: '商品很不错，物流也很快，下次还会购买！' },
        { username: '李四', rating: 5, comment: '非常满意，质量很好，推荐购买！' },
        // 更多评论...
    ];

    function renderComments(comments) {
        const container = document.getElementById('comments-container');
        container.innerHTML = ''; // 清空容器
        comments.forEach(comment => {
            const div = document.createElement('div');
            div.className = 'user-comment';

            // 创建用户名
            const h3 = document.createElement('h3');
            h3.textContent = comment.username;
            div.appendChild(h3);

            // 创建星级
            const stars = document.createElement('div');
            stars.className = 'stars';
            for (let i = 0; i < 5; i++) {
                const star = document.createElement('i');
                star.className = `fas ${i < comment.rating ? 'fa-star' : 'fa-star-o'}`;
                stars.appendChild(star);
            }
            div.appendChild(stars);

            // 创建评论内容
            const p = document.createElement('p');
            p.textContent = comment.comment;
            div.appendChild(p);

            container.appendChild(div);
        });
    }

    // 渲染评论
    renderComments(comments);
});

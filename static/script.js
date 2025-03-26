document.querySelectorAll('.faq-item').forEach(item => {
    const toggle = item.querySelector('.toggle');
    const answer = item.querySelector('.answer');

    toggle.addEventListener('click', () => {
        const isActive = answer.classList.contains('show');

        // Скрыть все ответы
        document.querySelectorAll('.faq-item .answer').forEach(a => {
            a.classList.remove('show');
        });

        // Убрать активное состояние у всех кнопок
        document.querySelectorAll('.faq-item .toggle').forEach(t => {
            t.classList.remove('active');
        });

        if (!isActive) {
            // Показать ответ и добавить активное состояние
            answer.classList.add('show');
            toggle.classList.add('active');
        }
    });
});

// Управление количеством товаров
document.addEventListener('DOMContentLoaded', function() {
    // Обработчики для кнопок +/-
    document.querySelectorAll('.plus-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.quantity-input');
            input.value = Math.max(1, (parseInt(input.value) || 0) + 1);
        });
    });

    document.querySelectorAll('.minus-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.quantity-input');
            input.value = Math.max(1, (parseInt(input.value) || 1) - 1);
        });
    });

    // Валидация ручного ввода
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function() {
            this.value = Math.max(1, parseInt(this.value) || 1);
        });
    });
});
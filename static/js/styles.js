// Обработчик события клика на элемент a_nav
document.querySelectorAll('.a_nav').forEach(item => {
  item.addEventListener('click', event => {
    // Удаляем класс active у всех элементов с классом a_nav
    document.querySelectorAll('.a_nav').forEach(item => {
      item.classList.remove('active');
    });
    // Добавляем класс active к нажатому элементу
    event.target.classList.add('active');
  });
});
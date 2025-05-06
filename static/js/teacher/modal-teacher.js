const buttons = document.querySelectorAll('.teacher-button');

buttons.forEach(button => {
    const teacherId = button.dataset.teacherId;
    const modal = document.getElementById(`modal_container_${teacherId}`);
    const closeButton = modal.querySelector('.modal-close-button');

    button.addEventListener('click', () => {
        modal.classList.add('show');
    });

    closeButton.addEventListener('click', () => {
        modal.classList.remove('show');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
        }
    });
});

modal_container.addEventListener('click', (e) => {
    if (e.target === modal_container) {
        modal_container.classList.remove('show');
    }
});


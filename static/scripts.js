document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // handles the checkbox toggles 
    const checkboxes = document.querySelectorAll('.task-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', async (e) => {
            const taskId = e.target.dataset.id;

            const taskText = document.getElementById(`task-text-${taskId}`);

            const response = await fetch(`/toggle/${taskId}`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json', 
                    'X-CSRFToken': csrfToken
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.completed) {
                    taskText.classList.add('completed-task');
                } else {
                    taskText.classList.remove('completed-task');
                }
            }
        });
    });

    // handles ajax delete 
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const actionUrl = form.action;
            const taskRow = form.closest('.task_management');

            const response = await fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });

            if (response.ok) {
                taskRow.remove();
            }
        });
    });

});
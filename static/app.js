const form = document.getElementById('lead-form');
const status = document.getElementById('form-status');
const success = document.getElementById('form-success');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    status.textContent = '';

    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();

    try {
        const response = await fetch('/api/lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, phone }),
        });

        if (response.ok) {
            form.classList.add('hidden');
            success.classList.remove('hidden');
        } else {
            const data = await response.json().catch(() => ({}));
            status.textContent = data.detail || 'Что-то пошло не так, попробуйте ещё раз.';
        }
    } catch {
        status.textContent = 'Нет соединения. Попробуйте ещё раз.';
    }
});

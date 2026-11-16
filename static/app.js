const form = document.getElementById('lead-form');
const status = document.getElementById('form-status');
const success = document.getElementById('form-success');
const submitBtn = form.querySelector('button[type="submit"]');
const fields = { name: document.getElementById('name'), phone: document.getElementById('phone') };

function clearFieldError(fieldName) {
    const field = fields[fieldName];
    field.removeAttribute('aria-invalid');
    const error = document.getElementById(`${fieldName}-error`);
    error.textContent = '';
    error.hidden = true;
}

function setFieldError(fieldName, message) {
    const field = fields[fieldName];
    field.setAttribute('aria-invalid', 'true');
    const error = document.getElementById(`${fieldName}-error`);
    error.textContent = message;
    error.hidden = false;
}

Object.entries(fields).forEach(([name, field]) => {
    field.addEventListener('input', () => clearFieldError(name));
});

function showValidationErrors(detail) {
    if (!Array.isArray(detail)) return false;
    let firstInvalid = null;
    detail.forEach((issue) => {
        const fieldName = Array.isArray(issue?.loc) ? issue.loc.at(-1) : null;
        if (!Object.hasOwn(fields, fieldName)) return;
        // FastAPI's internal messages and submitted values are never shown verbatim.
        const message = fieldName === 'name'
            ? 'Укажите имя (не более 100 символов).'
            : 'Укажите корректный номер телефона.';
        setFieldError(fieldName, message);
        firstInvalid ??= fields[fieldName];
    });
    if (firstInvalid) firstInvalid.focus();
    return Boolean(firstInvalid);
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (submitBtn.disabled) return;
    status.textContent = '';
    Object.keys(fields).forEach(clearFieldError);
    submitBtn.disabled = true;

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
            success.focus();
        } else {
            const data = await response.json().catch(() => ({}));
            if (response.status !== 422 || !showValidationErrors(data.detail)) {
                status.textContent = 'Не удалось отправить заявку. Попробуйте ещё раз.';
            }
        }
    } catch {
        status.textContent = 'Нет соединения. Попробуйте ещё раз.';
    } finally {
        submitBtn.disabled = false;
    }
});

// Enable personal-data entry only after the submit handler is registered.
form.querySelectorAll('input, button[type="submit"]').forEach((control) => {
    control.disabled = false;
});
document.getElementById('form-unavailable').hidden = true;

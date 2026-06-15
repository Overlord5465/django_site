document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.getElementById('message-form');
    const messagesContainer = document.querySelector('.chat-messages');

    if (messageForm) {
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const content = (formData.get('content') || '').toString().trim();
            const file = formData.get('attachment');
            if (!content && (!file || !file.size)) {
                alert('Введите текст или прикрепите файл');
                return;
            }

            fetch('/chat/send/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const esc = (s) => {
                        if (s == null || s === '') return '';
                        const d = document.createElement('div');
                        d.textContent = s;
                        return d.innerHTML;
                    };
                    let bodyHtml = esc(data.message.content || '');
                    if (data.message.has_file && data.message.attachment_url) {
                        const name = data.message.attachment_name || 'файл';
                        const safeHref = String(data.message.attachment_url).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
                        const link = '<a href="' + safeHref + '">' + esc(name) + '</a>';
                        bodyHtml = bodyHtml ? bodyHtml + ' ' + link : link;
                    }
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'mb-3 text-end';
                    messageDiv.innerHTML = `
                        <div class="d-flex justify-content-end">
                            <div class="p-3 rounded chat-bubble-self" style="max-width: 70%;">
                                <div>${bodyHtml || '&nbsp;'}</div>
                                <small>${data.message.timestamp}</small>
                            </div>
                        </div>
                    `;
                    messagesContainer.appendChild(messageDiv);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    this.querySelector('input[name="content"]').value = '';
                    const att = this.querySelector('input[name="attachment"]');
                    if (att) att.value = '';
                } else {
                    alert(data.message || 'Ошибка при отправке сообщения');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});

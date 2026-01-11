document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const chatErrors = document.getElementById('chat-errors');
    const messageCount = document.getElementById('message-count');

    // Carrega els missatges només obrir la pàgina
    loadMessages();

    // Actualitza el xat automàticament cada 3 segons
    setInterval(loadMessages, 3000);

    // Enviar missatge quan es prem el botó
    if (chatForm) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault(); // No recarrega la pàgina
            sendMessage();
        });
    }

    // Detectar clic al botó d'eliminar (paperera)
    chatMessages.addEventListener('click', function(e) {
        const deleteBtn = e.target.closest('.delete-message');
        if (deleteBtn) {
            const messageId = deleteBtn.dataset.messageId;
            if (confirm('Vols esborrar aquest missatge?')) {
                deleteMessage(messageId);
            }
        }
    });

    // Demana els missatges nous al servidor
    function loadMessages() {
        if (typeof eventId === 'undefined') return;
        
        fetch(`/chat/${eventId}/messages/`)
            .then(response => response.json())
            .then(data => {
                if (data.messages) {
                    renderMessages(data.messages);
                    updateMessageCount(data.messages.length);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Dibuixa els missatges a la pantalla
    function renderMessages(messages) {
        chatMessages.innerHTML = ''; // Neteja el xat
        
        if (messages.length === 0) {
            chatMessages.innerHTML = '<p class="text-center mt-3 text-muted">Encara no hi ha missatges.</p>';
            return;
        }

        messages.forEach(msg => {
            const el = createMessageElement(msg);
            chatMessages.appendChild(el);
        });

        scrollToBottom(); 
    }

    // Crea l'HTML d'un missatge individual
    function createMessageElement(msg) {
        const div = document.createElement('div');
        div.className = `chat-message ${msg.is_highlighted ? 'highlighted' : ''}`;
        div.dataset.messageId = msg.id;

        // Afegir botó paperera si tens permís
        let deleteBtn = '';
        if (msg.can_delete) {
            deleteBtn = `
                <div class="message-actions text-end">
                    <button class="btn btn-sm btn-link text-danger delete-message p-0 text-decoration-none" data-message-id="${msg.id}" title="Eliminar" style="font-size: 1.2rem;">
                        🗑️
                    </button>
                </div>
            `;
        }
        
        // Convertim text a segur amb escapeHtml per evitar errors
        div.innerHTML = `
            <div class="message-header d-flex justify-content-between">
                <strong>${escapeHtml(msg.display_name)}</strong>
                <small class="text-muted">${msg.created_at}</small>
            </div>
            <div class="message-content text-break mt-1">
                ${escapeHtml(msg.message)}
            </div>
            ${deleteBtn}
        `;
        return div;
    }

    // Enviar el missatge al servidor
    function sendMessage() {
        const formData = new FormData(chatForm);
        
        fetch(`/chat/${eventId}/send/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                chatForm.reset(); // Neteja el quadre de text
                if(chatErrors) chatErrors.innerHTML = '';
                loadMessages(); // Mostra el nou missatge
            } else {
                // Si hi ha error (ex: insult o buit), mostram-ho
                let errorMsg = '';
                if (data.errors) {
                    if (typeof data.errors === 'string') {
                         errorMsg = data.errors;
                    } else {
                        for (const key in data.errors) {
                             errorMsg += `${data.errors[key]}<br>`;
                        }
                    }
                }
                if(chatErrors) chatErrors.innerHTML = errorMsg || 'Error enviant.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if(chatErrors) chatErrors.innerHTML = 'Error de connexió';
        });
    }

    // Eliminar missatge del servidor
    function deleteMessage(messageId) {
        let csrftoken = null;
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input) {
            csrftoken = input.value;
        } else {
            csrftoken = getCookie('csrftoken');
        }

        if (!csrftoken) {
            alert('Error de seguretat (CSRF).');
            return;
        }

        fetch(`/chat/message/${messageId}/delete/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadMessages(); // Actualitza la llista
            } else {
                alert('No s\'ha pogut eliminar.');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function updateMessageCount(count) {
        if (messageCount) {
             messageCount.textContent = count;
        }
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Neteja el text per evitar codi maliciós
    function escapeHtml(text) {
        if (!text) return text;
        return text
            .toString()
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Funció estàndard de Django per llegir cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

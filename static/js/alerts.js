document.addEventListener('DOMContentLoaded', function() {
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        const messages = messageContainer.getElementsByClassName('message');
        
        for (let message of messages) {
            const type = message.dataset.type;
            const content = message.dataset.content;
            
            let icon, title;
            switch(type) {
                case 'success':
                    icon = 'success';
                    title = '¡Éxito!';
                    break;
                case 'error':
                    icon = 'error';
                    title = 'Error';
                    break;
                case 'warning':
                    icon = 'warning';
                    title = 'Advertencia';
                    break;
                default:
                    icon = 'info';
                    title = 'Información';
            }

            Swal.fire({
                icon: icon,
                title: title,
                text: content,
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
            });
        }
    }
});
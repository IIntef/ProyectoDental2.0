document.addEventListener('DOMContentLoaded', function() {
    const numeroInput = document.getElementById('id_numero');
    if (numeroInput) {
        numeroInput.addEventListener('change', function() {
            var numero = this.value;
            fetch(`/fetch-user-details/?numero=${numero}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.username) {
                    document.getElementById('id_username').value = data.username;
                    document.getElementById('id_email').value = data.email;
                    document.getElementById('id_direccion').value = data.direccion;
                    document.getElementById('id_edad').value = data.edad;
                    document.getElementById('id_ocupacion').value = data.ocupacion;
                    document.getElementById('id_celular').value = data.celular;
                    document.getElementById('id_acudiente').value = data.acudiente;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
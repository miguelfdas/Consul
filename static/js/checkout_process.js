const radios = document.querySelectorAll('input[name="payment_method"]');
const taxaAviso = document.getElementById('taxa-cobranca');

radios.forEach(radio => {
    radio.addEventListener('change', function() {
        if (this.value === 'entrega') {
            taxaAviso.style.display = 'block';
        } else {
            taxaAviso.style.display = 'none';
        }
    });
});
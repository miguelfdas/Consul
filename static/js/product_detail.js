function updatePrice(select) {
    const option = select.options[select.selectedIndex];
    document.getElementById('dynamic-price').innerText = option.getAttribute('data-price') + ' €';
}
window.onload = function() { updatePrice(document.getElementById('variant-select')); };
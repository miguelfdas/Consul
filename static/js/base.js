setTimeout(() => {
    const toast = document.getElementById('dynamic-toast');
    if (toast) {
        toast.style.transition = 'opacity 0.5s';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 500);
    }
}, 5000);
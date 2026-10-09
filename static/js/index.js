 document.addEventListener("DOMContentLoaded", () => {
    const track = document.getElementById('product-track');
    const cards = document.querySelectorAll('.carousel-card');
    
    if (cards.length > 0) {
        const updateActiveCard = () => {
            const trackCenter = track.getBoundingClientRect().left + (track.getBoundingClientRect().width / 2);
            let closestCard = null;
            let minDistance = Infinity;

            cards.forEach(card => {
                const cardCenter = card.getBoundingClientRect().left + (card.getBoundingClientRect().width / 2);
                const distance = Math.abs(trackCenter - cardCenter);
                
                if (distance < minDistance) {
                    minDistance = distance;
                    closestCard = card;
                }
            });

            cards.forEach(card => card.classList.remove('active'));
            if (closestCard) closestCard.classList.add('active');
        };

        track.addEventListener('scroll', updateActiveCard);
        window.addEventListener('resize', updateActiveCard);
        
        setTimeout(updateActiveCard, 100); 
    }
});
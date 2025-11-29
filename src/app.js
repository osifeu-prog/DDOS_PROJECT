document.addEventListener('DOMContentLoaded', () => {
    // ... (משתנים גלובליים נשארים זהים) ...
    const signupForm = document.getElementById('signup-form');
    const contactForm = document.getElementById('contact-form'); // טופס חדש

    // ... (לוגיקת מודאל ו-logUserEntry נשארות זהות) ...

    acceptBtn.addEventListener('click', () => {
        if (consentCheck.checked) {
            modal.style.display = 'none';
            mainContent.style.display = 'block';
            logUserEntry();
            updateStatsDisplay(); 
        }
    });

    // 1. לוגיקה לרישום משתמשים (מספר טלפון)
    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const phoneInput = document.getElementById('phone').value;
        
        fetch('/api/register', {
            method: 'POST',
            // ... (שליחה ל-Backend) ...
        })
        .then(response => {
            if (response.status === 201) {
                alert('תודה שנרשמתם! ניצור קשר בהקדם.');
                signupForm.reset();
                updateStatsDisplay();
            } else {
                alert('שגיאה ברישום או שהמספר כבר רשום. אנא נסו שוב.');
            }
        })
        .catch(error => {
            console.error('Registration error:', error);
            alert('שגיאת רשת. אנא ודאו את החיבור.');
        });
    });

    // 2. לוגיקה לשליחת הודעה לאדמין
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('contact-name').value;
        const email = document.getElementById('contact-email').value;
        const message = document.getElementById('contact-message').value;

        fetch('/api/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, message }),
        })
        .then(response => {
            if (response.status === 201) {
                alert('הפנייה נשלחה בהצלחה! האדמין קיבל התראה.');
                contactForm.reset();
            } else {
                alert('שגיאה בשליחת הפנייה. אנא נסו שוב.');
            }
        })
        .catch(error => {
            console.error('Message submission error:', error);
            alert('שגיאת רשת בשליחת הפנייה.');
        });
    });

    // ... (שאר הלוגיקות נשארות זהות) ...

    modal.style.display = 'flex';
});

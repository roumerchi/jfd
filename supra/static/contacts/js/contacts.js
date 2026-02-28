$(document).ready(function () {
    $(document).on('click', '.tb_row', function () {

        const city = $(this).data('city');
        const phone = $(this).data('phone');
        const email = $(this).data('email');

        if (!city || city === '—') {
            return;
        }

        $('#weather-box').replaceWith(`
            <div class="container_1 container_small weather_active" id="weather-box">
                <div>Loading weather...</div>
            </div>
        `);

        $.get('/api/weather/', { city: city })
            .done(function (data) {
                $('#weather-box').html(`
                    <div>${data.city}</div>
                    <div>Phone: ${phone}</div>
                    <div>Email: ${email || '—'}</div>
                    <div class="flex_3">
                        <div>${data.temperature}°C</div>
                        <div>
                            <div>Wind: ${data.wind_speed} km/h</div>
                        </div>
                    </div>
                    <div>Updated: ${new Date(data.updated_at).toLocaleTimeString()}</div>
                `);
            })
            .fail(function () {
                $('#weather-box').html('<div>Failed to load weather</div>');
            });
    });
});

// "additional" validation for client side
document.querySelector('.area_form').addEventListener('submit', function (e) {
    const phoneInput = this.querySelector('input[name="phone"]');
    const emailInput = this.querySelector('input[name="email"]');

    const phoneRegex = /^(\+48)?\s?\d{3}\s?\d{3}\s?\d{3}$/;

    if (!phoneRegex.test(phoneInput.value)) {
        e.preventDefault();
        alert('Invalid Polish phone number format');
        phoneInput.focus();
        return;
    }

    if (!emailInput.checkValidity()) {
        e.preventDefault();
        alert('Invalid email address');
        emailInput.focus();
    }
});
/* 
  HBnB - Part 4: Main Client Logic (Riyadh Luxury Edition)
*/

const API_BASE_URL = 'http://127.0.0.1:5001/api/v1';

const PLACE_IMAGES = [
    'Images/listing-najdi-suite.jpg',
    'Images/listing-desert-retreat.jpg',
    'Images/listing-rooftop-pool.jpg',
    'Images/p1.jpg',
    'Images/p2.jpg',
    'Images/p3.jpg'
];

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            await loginUser(email, password, 'auth/login');
        });
    }

    const ownerLoginForm = document.getElementById('owner-login-form');
    if (ownerLoginForm) {
        ownerLoginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            await loginUser(email, password, 'auth/owner-login');
        });
    }

    if (document.getElementById('places-list')) {
        initIndexPage();
    }

    if (document.getElementById('place-details')) {
        initPlacePage();
    }

    if (document.getElementById('review-form') && window.location.pathname.includes('add_review')) {
        initAddReviewPage();
    }

    if (document.getElementById('create-user-form')) {
        initCreateUserPage();
    }
});

// ---------- Shared Helpers ----------
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return token;

    if (!token) {
        loginLink.style.display = 'inline-block';
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
    } else {
        loginLink.style.display = 'inline-block';
        loginLink.textContent = 'Account';
        loginLink.href = 'index.html';
    }
    return token;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id') || params.get('place_id');
}

// ---------- Task 1: Login ----------
async function loginUser(email, password, endpoint) {
    const errorEl = document.getElementById('login-error') || document.getElementById('error-message');
    try {
        const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/; max-age=86400`;
            window.location.href = 'index.html';
        } else {
            const errData = await response.json().catch(() => ({}));
            if (errorEl) {
                errorEl.textContent = errData.message || 'Login failed: Invalid email or password.';
                errorEl.style.display = 'block';
            }
        }
    } catch (err) {
        if (errorEl) {
            errorEl.textContent = 'Network error: ' + err.message;
            errorEl.style.display = 'block';
        }
    }
}

// ---------- Task 2: Index Page & Price Filtering ----------
function initIndexPage() {
    const token = checkAuthentication();
    fetchPlaces(token);

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.innerHTML = '';

        const sarOptions = [
            { value: 'All', label: 'All Prices' },
            { value: '1000', label: '1,000 SAR' },
            { value: '3000', label: '3,000 SAR' },
            { value: '5000', label: '5,000 SAR' }
        ];

        sarOptions.forEach((optData) => {
            const opt = document.createElement('option');
            opt.value = optData.value;
            opt.textContent = optData.label;
            priceFilter.appendChild(opt);
        });

        priceFilter.addEventListener('change', (event) => {
            const selected = event.target.value;
            document.querySelectorAll('.place-card').forEach((card) => {
                const price = parseFloat(card.dataset.price);
                if (selected === 'All' || price <= parseFloat(selected)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}/places/`, { headers });
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        }
    } catch (err) {
        console.error('Failed to fetch places:', err);
    }
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    list.innerHTML = '';

    if (!places || places.length === 0) {
        list.innerHTML = '<p>No luxury places available at the moment.</p>';
        return;
    }

    places.forEach((place, index) => {
        const imageSrc = PLACE_IMAGES[index % PLACE_IMAGES.length];
        const card = document.createElement('article');
        card.className = 'place-card';
        const priceNum = place.price_by_night || place.price;
        card.dataset.price = priceNum;

        const title = place.title || place.name;
        const specs = place.amenities && place.amenities.length > 0
            ? place.amenities.slice(0, 3).map(a => a.name || a).join(' · ')
            : 'Riyadh · Entire residence';

        card.innerHTML = `
            <img src="${imageSrc}" alt="${title}" class="place-card-img">
            <div class="place-card-body">
                <span class="district-label">Riyadh</span>
                <h3>${title}</h3>
                <p class="place-specs">${specs}</p>
                <div class="place-card-footer">
                    <span class="place-price"><strong>SAR ${Number(priceNum).toLocaleString()}</strong> / night</span>
                </div>
                <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
            </div>
        `;
        list.appendChild(card);
    });
}

// ---------- Task 3: Place Details Page ----------
function initPlacePage() {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    fetchPlaceDetails(token, placeId);

    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        if (token) {
            addReviewSection.style.display = 'block';
            addReviewSection.innerHTML = `
                <a href="add_review.html?id=${placeId}" class="details-button">Add a Review</a>
            `;
        } else {
            addReviewSection.style.display = 'none';
        }
    }

}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, { headers });
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            document.getElementById('place-details').innerHTML = '<p>Place not found.</p>';
        }

        const reviewsResponse = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, { headers });
        if (reviewsResponse.ok) {
            const reviews = await reviewsResponse.json();
            displayReviews(reviews);
        }
    } catch (err) {
        console.error('Failed to fetch place details:', err);
    }
}

function displayPlaceDetails(place) {
    const priceNum = place.price_by_night || place.price;
    const hostName = place.host ? `${place.host.first_name} ${place.host.last_name}` : 'Riyadh Host';

    // Gallery
    const gallery = document.getElementById('place-gallery');
    if (gallery) {
        gallery.innerHTML = `
            <img src="${PLACE_IMAGES[0]}" alt="${place.title || place.name}" class="gallery-main">
            <div class="gallery-side">
                <img src="${PLACE_IMAGES[1]}" alt="">
                <img src="${PLACE_IMAGES[2]}" alt="">
            </div>
        `;
    }

    // Details
    const amenitiesList = place.amenities && place.amenities.length > 0
        ? place.amenities.map(a => `<li>${a.name || a}</li>`).join('')
        : '<li>Private Butler</li><li>Spa Access</li>';

    const container = document.getElementById('place-details');
    container.innerHTML = `
        <p class="hero-eyebrow">Al Olaya · Riyadh · Entire Residence</p>
        <h1>${place.title || place.name}</h1>
        <p>${place.description || 'Exclusive luxury accommodation with panoramic views.'}</p>
        <ul class="amenities-list">
            ${amenitiesList}
        </ul>
        <p style="margin-top: 1rem; color: var(--color-muted);">Hosted by ${hostName}</p>
    `;

    // Booking panel
    const panel = document.getElementById('booking-panel');
    if (panel) {
        panel.innerHTML = `
            <div class="booking-price">SAR ${Number(priceNum).toLocaleString()} <span>/ night</span></div>
            <div class="booking-row"><span>Check in</span><span>24 Aug</span></div>
            <div class="booking-row"><span>Check out</span><span>28 Aug</span></div>
            <div class="booking-row"><span>Guests</span><span>4</span></div>
            <button type="button">Reserve</button>
            <p class="booking-note">You won't be charged yet</p>
        `;
    }

    if (place.reviews && place.reviews.length > 0) {
        displayReviews(place.reviews);
    }
}

function displayReviews(reviews) {
    const container = document.getElementById('reviews-list') || document.getElementById('reviews');
    if (!container) return;

    container.innerHTML = '';
    if (!reviews || reviews.length === 0) {
        container.innerHTML = '<p>No reviews yet for this place.</p>';
        return;
    }

    reviews.forEach((review) => {
        const card = document.createElement('div');
        card.className = 'review-card';
        const author = review.user ? review.user.first_name : 'Guest';

        card.innerHTML = `
            <h3>${author} - ⭐ ${review.rating || 5}/5</h3>
            <p>"${review.text || review.comment}"</p>
        `;
        container.appendChild(card);
    });
}

// ---------- Task 4: Add Review Page ----------
function initAddReviewPage() {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (!token || !placeId) {
        window.location.href = 'index.html';
        return;
    }

    fetchPlaceNameForReview(token, placeId);
    initStarRating();

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const text = document.getElementById('review-text').value;
            const ratingInput = document.getElementById('rating');
            const rating = ratingInput ? parseInt(ratingInput.value, 10) : 5;
            await submitReview(token, placeId, text, rating);
        });
    }
}

async function fetchPlaceNameForReview(token, placeId) {
    const nameEl = document.getElementById('stay-place-name');
    if (!nameEl) return;

    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, { headers });
        if (response.ok) {
            const place = await response.json();
            nameEl.textContent = place.title || place.name || 'Your stay';
        } else {
            nameEl.textContent = 'Your stay';
        }
    } catch (err) {
        nameEl.textContent = 'Your stay';
    }
}

function initStarRating() {
    const starRating = document.getElementById('star-rating');
    const ratingInput = document.getElementById('rating');
    if (!starRating || !ratingInput) return;

    const stars = Array.from(starRating.querySelectorAll('.star'));

    function highlight(value) {
        stars.forEach((star) => {
            const starValue = parseInt(star.dataset.value, 10);
            star.classList.toggle('selected', starValue <= value);
        });
    }

    highlight(parseInt(ratingInput.value, 10));

    stars.forEach((star) => {
        star.addEventListener('click', () => {
            const value = parseInt(star.dataset.value, 10);
            ratingInput.value = value;
            highlight(value);
        });
    });
}

// ---------- Task 5: Create Account Page (Admin only) ----------
function initCreateUserPage() {
    const token = checkAuthentication();
    let accountType = 'user';

    const toggle = document.getElementById('account-type-toggle');
    if (toggle) {
        const chips = Array.from(toggle.querySelectorAll('.chip'));
        chips.forEach((chip) => {
            chip.addEventListener('click', () => {
                chips.forEach((c) => c.classList.remove('active'));
                chip.classList.add('active');
                accountType = chip.dataset.type;
            });
        });
    }

    const form = document.getElementById('create-user-form');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        await createAccount(token, accountType, {
            first_name: document.getElementById('first-name').value.trim(),
            last_name: document.getElementById('last-name').value.trim(),
            email: document.getElementById('email').value.trim(),
            password: document.getElementById('password').value
        }, form);
    });
}

async function createAccount(token, accountType, payload, form) {
    const errorEl = document.getElementById('create-user-error');
    const successEl = document.getElementById('create-user-success');
    errorEl.style.display = 'none';
    successEl.style.display = 'none';

    if (!token) {
        errorEl.textContent = 'Sign in with an admin account to create new accounts.';
        errorEl.style.display = 'block';
        return;
    }

    const endpoint = accountType === 'owner' ? 'owner' : 'users';
    const roleLabel = accountType === 'owner' ? 'Host' : 'Guest';

    try {
        const response = await fetch(`${API_BASE_URL}/${endpoint}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            successEl.textContent = `${roleLabel} account created for ${payload.first_name} ${payload.last_name}.`;
            successEl.style.display = 'block';
            form.reset();
        } else if (response.status === 403) {
            errorEl.textContent = 'Only an admin can create new accounts.';
            errorEl.style.display = 'block';
        } else if (response.status === 401) {
            errorEl.textContent = 'Your session has expired. Please sign in again.';
            errorEl.style.display = 'block';
        } else {
            const errData = await response.json().catch(() => ({}));
            errorEl.textContent = errData.message || errData.msg || 'Failed to create account.';
            errorEl.style.display = 'block';
        }
    } catch (err) {
        errorEl.textContent = 'Network error: ' + err.message;
        errorEl.style.display = 'block';
    }
}

async function submitReview(token, placeId, text, rating = 5) {
    const errorEl = document.getElementById('review-error');
    try {
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ comment: text, rating: rating, place_id: placeId })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const errData = await response.json().catch(() => ({}));
            const msg = errData.message || 'Failed to submit review.';
            if (errorEl) {
                errorEl.textContent = msg;
            } else {
                alert(msg);
            }
        }
    } catch (err) {
        if (errorEl) {
            errorEl.textContent = 'Error submitting review: ' + err.message;
        } else {
            alert('Error submitting review: ' + err.message);
        }
    }
}
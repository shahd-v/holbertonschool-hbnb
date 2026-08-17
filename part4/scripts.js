/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

// document.addEventListener('DOMContentLoaded', () => {
//     /* DO SOMETHING */
//   });
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
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
});

// ---------- Shared helpers ----------
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
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
    }
    return token;
}

// ---------- Login ----------
async function loginUser(email, password) {
    const errorEl = document.getElementById('login-error');
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            if (errorEl) {
                errorEl.textContent = 'Login failed: invalid email or password';
                errorEl.style.display = 'block';
            }
        }
    } catch (err) {
        if (errorEl) {
            errorEl.textContent = 'Login failed: ' + err.message;
            errorEl.style.display = 'block';
        }
    }
}

// ---------- Index page ----------
function initIndexPage() {
    const token = checkAuthentication();
    fetchPlaces(token);

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        ['10', '50', '100', 'All'].forEach((val) => {
            const opt = document.createElement('option');
            opt.value = val;
            opt.textContent = val;
            priceFilter.appendChild(opt);
        });

        priceFilter.addEventListener('change', (event) => {
            const selected = event.target.value;
            document.querySelectorAll('.place-card').forEach((card) => {
                const price = parseFloat(card.dataset.price);
                card.style.display = (selected === 'All' || price <= parseFloat(selected)) ? 'block' : 'none';
            });
        });
    }
}

async function fetchPlaces(token) {
    try {
        const headers = {};
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

    places.forEach((place) => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = place.price;
        card.innerHTML = `
            <h3>${place.title}</h3>
            <p>Price per night: $${place.price}</p>
            <button class="details-button" onclick="window.location.href='place.html?place_id=${place.id}'">View Details</button>
        `;
        list.appendChild(card);
    });
}

// ---------- Place details page ----------
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id');
}

function initPlacePage() {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    fetchPlaceDetails(token, placeId);

    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const text = document.getElementById('review-text').value;
            await submitReview(token, placeId, text);
        });
    }
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, { headers });
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
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
    const container = document.getElementById('place-details');
    container.innerHTML = `
        <div class="place-info">
            <h2>${place.title}</h2>
            <p>${place.description || ''}</p>
            <p>Price per night: $${place.price}</p>
        </div>
    `;
}

function displayReviews(reviews) {
    const container = document.getElementById('reviews');
    container.innerHTML = '';
    reviews.forEach((review) => {
        const card = document.createElement('div');
        card.className = 'review-card';
        card.innerHTML = `
            <p>${review.comment}</p>
            <p>Rating: ${review.rating}/5</p>
        `;
        container.appendChild(card);
    });
}

// ---------- Add review page ----------
function initAddReviewPage() {
    const token = checkAuthentication();
    if (!token) {
        window.location.href = 'index.html';
        return;
    }
}

async function submitReview(token, placeId, text) {
    try {
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ place_id: placeId, comment: text, rating: 5 })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            document.getElementById('review-form').reset();
        } else {
            alert('Failed to submit review');
        }
    } catch (err) {
        alert('Failed to submit review: ' + err.message);
    }
}
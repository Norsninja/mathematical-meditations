// Gallery JavaScript - Interactive functionality

// State management
let currentFilter = 'all';
let currentView = 'gallery';

// DOM Elements
const loadingScreen = document.getElementById('loading');
const galleryGrid = document.getElementById('gallery-grid');
const timelineItems = document.getElementById('timeline-items');
const artworkModal = document.getElementById('artwork-modal');
const codeModal = document.getElementById('code-modal');

// Initialize gallery on page load
document.addEventListener('DOMContentLoaded', () => {
    // Hide loading screen
    setTimeout(() => {
        loadingScreen.style.opacity = '0';
        setTimeout(() => {
            loadingScreen.style.display = 'none';
        }, 500);
    }, 1000);
    
    // Initialize gallery
    renderGallery();
    renderTimeline();
    setupEventListeners();
    updateArtworkCounts();
});

// Update artwork and series counts dynamically
function updateArtworkCounts() {
    const artworkCount = artworkData.length;
    const seriesCount = new Set(artworkData.map(a => a.series)).size;
    
    const artworkCountEl = document.getElementById('artwork-count');
    const seriesCountEl = document.getElementById('series-count');
    
    if (artworkCountEl) {
        artworkCountEl.textContent = artworkCount;
    }
    if (seriesCountEl) {
        seriesCountEl.textContent = seriesCount;
    }
}

// Render gallery grid
function renderGallery() {
    galleryGrid.innerHTML = '';
    
    artworkData.forEach(artwork => {
        const item = createGalleryItem(artwork);
        galleryGrid.appendChild(item);
    });
}

// Create gallery item element
function createGalleryItem(artwork) {
    const item = document.createElement('div');
    item.className = 'gallery-item';
    item.dataset.category = artwork.category;
    
    item.innerHTML = `
        <img src="${artwork.image}" alt="${artwork.title}">
        <div class="gallery-item-info">
            <h3 class="gallery-item-title">${artwork.title}</h3>
            <p class="gallery-item-subtitle">${artwork.series}</p>
            <p class="gallery-item-date">${formatDate(artwork.date)}</p>
        </div>
    `;
    
    item.addEventListener('click', () => openArtworkModal(artwork));
    
    return item;
}

// Render timeline
function renderTimeline() {
    timelineItems.innerHTML = '';
    
    // Group artworks by series for timeline
    const series = {};
    const seriesOrder = []; // Track order of first appearance
    
    artworkData.forEach(artwork => {
        if (!series[artwork.series]) {
            series[artwork.series] = {
                name: artwork.series,
                date: artwork.date,
                artworks: [],
                firstIndex: seriesOrder.length
            };
            seriesOrder.push(artwork.series);
        }
        series[artwork.series].artworks.push(artwork);
    });
    
    // Sort series by first appearance to maintain chronological order
    const sortedSeries = seriesOrder.map(name => series[name]);
    
    // Create timeline items
    sortedSeries.forEach((seriesData, index) => {
        const item = createTimelineItem(seriesData, index);
        timelineItems.appendChild(item);
    });
}

// Create timeline item
function createTimelineItem(seriesData, index) {
    const item = document.createElement('div');
    item.className = 'timeline-item';
    
    const content = document.createElement('div');
    content.className = 'timeline-item-content';
    
    content.innerHTML = `
        <h3>${seriesData.name}</h3>
        <p class="timeline-date">${formatDate(seriesData.date)}</p>
        <p>${seriesData.artworks.length} artwork${seriesData.artworks.length > 1 ? 's' : ''}</p>
        <div class="timeline-thumbnails">
            ${seriesData.artworks.slice(0, 3).map(a => 
                `<img src="${a.image}" alt="${a.title}" width="60" height="60" style="object-fit: cover; margin-right: 0.5rem; border-radius: 4px;">`
            ).join('')}
        </div>
    `;
    
    content.addEventListener('click', () => {
        // Switch to gallery view and filter by series
        switchView('gallery');
        filterByCategory(seriesData.artworks[0].category);
    });
    
    const dot = document.createElement('div');
    dot.className = 'timeline-item-dot';
    
    item.appendChild(content);
    item.appendChild(dot);
    
    return item;
}

// Setup event listeners
function setupEventListeners() {
    // Navigation buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const view = e.target.dataset.view;
            switchView(view);
        });
    });
    
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const filter = e.target.dataset.filter;
            filterGallery(filter);
        });
    });
    
    // Modal close buttons
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', () => {
            closeModals();
        });
    });
    
    // Modal background click
    [artworkModal, codeModal].forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModals();
            }
        });
    });
    
    // View code button
    document.getElementById('view-code-btn').addEventListener('click', () => {
        const artwork = artworkModal.dataset.currentArtwork;
        if (artwork) {
            openCodeModal(JSON.parse(artwork));
        }
    });
    
    // Copy code button
    document.getElementById('copy-code-btn').addEventListener('click', copyCode);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeModals();
        }
    });
}

// Switch views
function switchView(view) {
    currentView = view;
    
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === view);
    });
    
    // Update views
    document.querySelectorAll('.view').forEach(v => {
        v.classList.toggle('active', v.id === `${view}-view`);
    });
}

// Filter gallery
function filterGallery(filter) {
    currentFilter = filter;
    
    // Update filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === filter);
    });
    
    // Filter gallery items
    document.querySelectorAll('.gallery-item').forEach(item => {
        const category = item.dataset.category;
        const shouldShow = filter === 'all' || category === filter;
        item.classList.toggle('hidden', !shouldShow);
    });
}

// Filter by category (used from timeline)
function filterByCategory(category) {
    const filterMap = {
        'emergence': 'emergence',
        'physics': 'physics',
        'consciousness': 'consciousness',
        'emotion': 'emotion'
    };
    
    const filter = filterMap[category] || 'all';
    filterGallery(filter);
}

// Open artwork modal
function openArtworkModal(artwork) {
    // Store current artwork data
    artworkModal.dataset.currentArtwork = JSON.stringify(artwork);
    
    // Update modal content
    document.getElementById('modal-image').src = artwork.image;
    document.getElementById('modal-image').alt = artwork.title;
    document.getElementById('modal-title').textContent = artwork.title;
    document.getElementById('modal-date').textContent = formatDate(artwork.date);
    document.getElementById('modal-description').textContent = artwork.description;
    document.getElementById('download-btn').href = artwork.image;
    document.getElementById('download-btn').download = `${artwork.id}.png`;
    
    // Show modal
    artworkModal.classList.add('active');
}

// Open code modal
async function openCodeModal(artwork) {
    try {
        // Fetch code content
        const response = await fetch(artwork.code);
        const code = await response.text();
        
        // Update modal content
        document.getElementById('code-title').textContent = `${artwork.title} - Source Code`;
        document.getElementById('code-content').textContent = code;
        
        // Show modal
        codeModal.classList.add('active');
    } catch (error) {
        console.error('Error loading code:', error);
        alert('Unable to load source code.');
    }
}

// Copy code to clipboard
async function copyCode() {
    const codeContent = document.getElementById('code-content').textContent;
    
    try {
        await navigator.clipboard.writeText(codeContent);
        
        // Update button text temporarily
        const btn = document.getElementById('copy-code-btn');
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    } catch (error) {
        console.error('Error copying code:', error);
        alert('Unable to copy code to clipboard.');
    }
}

// Close all modals
function closeModals() {
    [artworkModal, codeModal].forEach(modal => {
        modal.classList.remove('active');
    });
}

// Format date
function formatDate(dateString) {
    // Parse as local date, not UTC
    const [year, month, day] = dateString.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}


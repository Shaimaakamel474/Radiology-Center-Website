// Add event listeners to each role link
document.getElementById('doctor-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'admin?role=doctor'; // Redirect to admin.html with role parameter
});

document.getElementById('radiologist-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'admin?role=radiologist';
});

document.getElementById('receptionist-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'admin?role=receptionist';
});

document.getElementById('engineer-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'admin?role=engineer';
});

document.getElementById('hr-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'admin?role=hr';
});

document.getElementById('branch-manager-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'admin?role=branch_manager';
});

// Add event listeners for dropdown options
document.getElementById('front_option').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'front_desk';
});

document.getElementById('radiologist_option').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'radiologist';
});

document.getElementById('pacs_option').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'pacs';
});
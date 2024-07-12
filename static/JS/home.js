document.getElementById('doctor-link').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default action (e.g., navigating to href="#")
    window.location.href = 'radiology_charts'; // Redirect to admin.html
});

document.getElementById('radiologist-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'radiology_charts';
});

document.getElementById('receptionist-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = '';
});

document.getElementById('engineer-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'clinical_charts';
});

document.getElementById('device-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = '/device_charts';
});

document.getElementById('patient-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = '';
});

document.getElementById('branch-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = '';
});

document.getElementById('hr-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'hr_charts';
});

document.getElementById('branch-manager-link').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = 'manager_charts';
});

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
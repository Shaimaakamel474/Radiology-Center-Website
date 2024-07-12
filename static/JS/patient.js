document.addEventListener('DOMContentLoaded', function() {
    const techSelect = document.getElementById('techSelect');
    const modalitySelect = document.getElementById('modalitySelect');
    const locationSelect = document.getElementById('locationSelect');

    // Function to fetch data from the Flask endpoint
    function fetchData() {
        fetch('/devices') // Adjust this URL to your actual endpoint
            .then(response => response.json())
            .then(data => {
                const options = parseData(data);
                initializeTechniques(options);
                initializeListeners(options);
                setDefaultValues(options); // Set default values first
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Function to parse data from the server into a structured format
    function parseData(data) {
        const options = {};
        data.forEach(item => {
            const { device_tech, device_name, bname } = item;
            if (!options[device_tech]) {
                options[device_tech] = { devices: {} };
            }
            if (!options[device_tech].devices[device_name]) {
                options[device_tech].devices[device_name] = [];
            }
            options[device_tech].devices[device_name].push(bname);
        });
        return options;
    }

    // Function to initialize the technique options in the dropdown
    function initializeTechniques(options) {
        const techniques = Object.keys(options);
        updateOptions(techSelect, techniques);
    }

    // Function to initialize event listeners for dropdown changes
    function initializeListeners(options) {
        techSelect.addEventListener('change', function() {
            const selectedTechnique = this.value;
            const selectedDevices = options[selectedTechnique]?.devices || {};
            updateOptions(modalitySelect, Object.keys(selectedDevices));
            modalitySelect.dispatchEvent(new Event('change')); // Trigger change to update locations
        });

        modalitySelect.addEventListener('change', function() {
            const selectedTechnique = techSelect.value;
            const selectedDevice = this.value;
            const locations = options[selectedTechnique]?.devices[selectedDevice] || [];
            updateOptions(locationSelect, locations);
        });
    }

    // Function to update dropdown options and set the first option as selected
    function updateOptions(selectElement, options) {
        selectElement.innerHTML = '';
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            selectElement.appendChild(optionElement);
        });

        // Set the first option as selected
        if (options.length > 0) {
            selectElement.value = options[0];
        }
    }

    // Function to set default values for dropdowns
    function setDefaultValues(options) {
        if (techSelect.options.length > 0) {
            const selectedTechnique = techSelect.value;
            const selectedDevices = options[selectedTechnique]?.devices || {};
            updateOptions(modalitySelect, Object.keys(selectedDevices));

            if (modalitySelect.options.length > 0) {
                modalitySelect.value = modalitySelect.options[0].value;
                const selectedDevice = modalitySelect.value;
                const locations = selectedDevices[selectedDevice] || [];
                updateOptions(locationSelect, locations);

                if (locationSelect.options.length > 0) {
                    locationSelect.value = locationSelect.options[0].value;
                }
            }
        }
    }

    // Fetch and initialize data on page load
    fetchData();

});
    // /////////////////////////////////////////////////

    // Function to fetch patient data from the server and populate the table
    function fetchPatientData() {
        fetch("/send_patient_table")
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Fetched patient data:', data); // Debug: log the fetched data
                if (data.length === 0) {
                    console.log('No patient data found');
                    return;  // Exit if no patient data found
                }
                patientData = data.map(patient => ({ // Assign data to global patientData
                    organ: patient.organ,
                    modality: patient.modality,
                    branch_name: patient.branch_name,
                    datetime: patient.datetime,
                    status: patient.verified,
                    scan: patient.scan_folder || "",  // Default to empty string if undefined
                    report: patient.report || "" 
                }));
                console.log('Processed patient data:', patientData); // Debug: log the processed patient data
                populateTable(patientData);
            })
            .catch(error => {
                console.error('Error fetching patient data:', error);
            });
    }

    // Function to populate the patient table with data
    function populateTable(data) {
        patientTableBody.innerHTML = '';
        data.forEach(patient => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${patient.organ}</td>
                <td>${patient.modality}</td>
                <td>${patient.branch_name}</td>
                <td>${patient.datetime}</td>
                <td>${patient.status}</td>
                <td>${patient.scan ? `<button class="scan-button" data-scan="${patient.scan}">View Scan</button>` : ''}</td>
                <td>${patient.report}</td>
            `;
            patientTableBody.appendChild(row);
        });

        // Add event listeners to dynamically created buttons
        addEventListenersToButtons();
    }

    // Function to add event listeners to dynamically created buttons
    function addEventListenersToButtons() {
        const scanButtons = document.querySelectorAll('.scan-button');
        scanButtons.forEach(button => {
            button.addEventListener('click', function(event) {
                event.preventDefault(); // Prevent the default behavior (page reload)
                const scanValue = this.getAttribute('data-scan');
                showImagesFunction(scanValue, patientData); // Pass patientData to the function
            });
        });
    }

    // Function to open the image folder in a new tab/window
    function showImagesFunction(scan, patientData) {
        const formData = new FormData();
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
        formData.append('scan', scan);
        formData.append('csrf_token', csrfToken);
    
        fetch('/view_images', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.image_urls);
            const imageUrls = data.image_urls;
            showHidden2(patientData); // Pass patientData to the next function
            updateImageSlider(imageUrls);
        })
        .catch(error => {
            console.error('Error:', error.message);
            // Handle error: Display a message or retry logic if appropriate
        });
    }

    // Function to show or hide hidden2 based on patient data availability
    function showHidden2(patientData) {
        const hidden2 = document.getElementById('hidden2');
        // Assuming patientData is accessible here
        if (patientData.length > 0) {
            hidden2.style.display = 'block'; // Show hidden2
        } else {
            hidden2.style.display = 'none'; // Hide hidden2 if no patient data
        }
    }

    // Initial fetch and setup on page load
    
    fetchPatientData();


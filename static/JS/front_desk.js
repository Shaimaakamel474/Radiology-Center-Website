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




//////////////////////////////////////////////////////////////////////////////////////////////////////













// Define a variable to hold patient data
// Define variables to hold patient data and form dictionary

let formDictionary = [];

// let formData=[]


// Function to fetch data for different appointment types
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('button1').addEventListener('click', function() {
        fetchData_table('today_app');
    });

    document.getElementById('button2').addEventListener('click', function() {
        fetchData_table('next_app');
    });

    document.getElementById('button3').addEventListener('click', function() {
        fetchData_table('previous_app');
    });
    document.getElementById('button4').addEventListener('click', function() {
        fetchData_table('all_app');
    });

    // Fetch data from endpoint1 by default when the page loads
    fetchData_table('all_app');
});

// Define a variable to hold patient data
let patientData = [];

// Function to fetch data from the server for patient table
function fetchData_table(endpoint) {
    return fetch(`/${endpoint}`)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Data:", data); // Optional logging for fetched data
            patientData = data.map(patient => ({
                name: patient.name,
                patient_ssn: patient.patient_ssn.toString(),
                gender: patient.gender,
                age: patient.age,
                phone_number: patient.phone_number,
                organ: patient.organ,
                modality: patient.modality,
                branch_name: patient.bname || patient.branch_name,
                datetime: patient.datetime,
                payment: (patient.payment !== undefined && patient.payment !== null) ? patient.payment : null
            }));
            console.log(patientData);
            populateTable(patientData); // Populate the table with fetched data
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// Function to populate the table with patient data
function populateTable(data) {
    const tableBody = document.getElementById('patientTableBody');
    tableBody.innerHTML = '';
    data.forEach((patient, index) => {
        const row = createTableRow(patient, index);
        tableBody.appendChild(row);
    });
}

// Function to create a table row for a patient
function createTableRow(patient, index) {
    const row = document.createElement('tr');
    row.setAttribute('id', `row-${index}`);
    row.innerHTML = `
        <td>${patient.name}</td>
        <td>${patient.patient_ssn}</td>
        <td>${patient.gender}</td>
        <td>${patient.age}</td>
        <td>${patient.phone_number}</td>
        <td>${patient.organ}</td>
        <td>${patient.modality}</td>
        <td>${patient.branch_name}</td>
        <td>${patient.datetime}</td>
        <td>
            ${patient.payment !== null ?
                `<span class="payment-text">${patient.payment}</span>` :
                `<input type="text" name="payment" placeholder="Enter Payment" class="payment-input" data-index="${index}">`
            }
        </td>
        <td>
            ${patient.payment !== null ?
                `<button class="edit-btn" data-index="${index}">Edit</button>` :
                `<button class="payment-btn" data-index="${index}">Add</button>`
            }
        </td>
        <td><button class="cancel-btn" data-index="${index}">Cancel</button></td>
    `;

    // Attach event listeners after ensuring elements exist
    const editButton = row.querySelector('.edit-btn');
    const paymentButton = row.querySelector('.payment-btn');
    const cancelButton = row.querySelector('.cancel-btn');

    if (editButton) {
        editButton.addEventListener('click', () => editPayment(index));
    }
    if (paymentButton) {
        paymentButton.addEventListener('click', () => addPayment(index));
    }
    if (cancelButton) {
        cancelButton.addEventListener('click', () => cancelRow(index));
    }

    return row;
}

// Function to handle adding payment
function addPayment(index) {
    const paymentInput = document.querySelector(`.payment-input[data-index="${index}"]`);
    const payment = paymentInput.value.trim();
    if (payment) {
        const patient = patientData[index];
        const formData = new FormData();
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        formData.append('csrf_token', csrfToken);
        for (const key in patient) {
            formData.append(key, patient[key]);
        }
        formData.set('payment', payment);

        fetch('/get_payment', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                patient.payment = payment;
                console.log(`Added payment ${payment} for ${patient.name}`);
                formDictionary.push(patient);  // Save to form dictionary
                populateTable(patientData); // Refresh the table with updated data
            } else {
                console.error('Error adding payment:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error adding payment:', error);
        });
    }
}

// Function to handle editing payment
function editPayment(index) {
    const paymentElement = document.getElementById(`row-${index}`).querySelector('.payment-text');
    if (!paymentElement) {
        console.error(`Payment element not found for index ${index}`);
        return;
    }

    // Assuming you want to allow editing by replacing the span with an input
    const currentPayment = patientData[index].payment;
    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.value = currentPayment || '';
    inputField.classList.add('payment-input');

    inputField.addEventListener('blur', () => {
        const updatedPayment = inputField.value.trim();
        if (updatedPayment !== currentPayment) {
            patientData[index].payment = updatedPayment;
            updatePayment(index, updatedPayment);
        } else {
            // If no change, revert back to span
            renderPayment(index);
        }
    });

    paymentElement.innerHTML = '';
    paymentElement.appendChild(inputField);
    inputField.focus(); // Auto-focus on the input field
}

function renderPayment(index) {
    const paymentElement = document.getElementById(`payment-${index}`);
    if (!paymentElement) {
        console.error(`Payment element not found for index ${index}`);
        return;
    }

    const currentPayment = patientData[index].payment;
    paymentElement.innerHTML = `<span class="payment-text">${currentPayment}</span>`;
}



// Function to handle canceling an appointment
function cancelRow(index) {
    const patient = patientData[index];
    // const formData = createFormData(patient);

    fetch('/cancel_app', {
        method: 'POST',
        // body: formData
    })
    .then(response => {
        if (response.ok) {
            // console.log(`Canceled appointment for ${patient.name}`);
            // Remove the canceled patient from the data array
            patientData.splice(index, 1);
            populateTable(patientData); // Refresh the table
        } else {
            console.error('Error canceling appointment:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error canceling appointment:', error);
    });
}

// Function to update payment in the backend
function updatePayment(index, updatedPayment) {
    const patient = patientData[index];
    const formData = new FormData();

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    formData.append('csrf_token', csrfToken);
    for (const key in patient) {
        formData.append(key, patient[key]);
    }
    formData.set('payment', updatedPayment);


    fetch('/front_desk_updated', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            patient.payment = updatedPayment;
            console.log(`Updated payment for ${patient.name} to ${updatedPayment}`);
            populateTable(patientData); // Refresh the table with updated data
        } else {
            console.error('Error updating payment:', response.statusText);
            renderPayment(index); // If update fails, revert to original view
        }
    })
    .catch(error => {
        console.error('Error updating payment:', error);
        renderPayment(index); // If update fails, revert to original view
    });
}












// ////////////////////////////////////////
// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInputs = document.querySelectorAll('.bars input');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchValue = input.value.toLowerCase();
            const filteredData = patientData.filter(patient => {
                const patientSSN = patient.patient_ssn.toLowerCase();
                const patientBranch = patient.branch_name.toLowerCase();
                const patientModality = patient.modality.toLowerCase();
                const patientDate = patient.datetime.toLowerCase();
                return patientSSN.includes(searchValue) ||
                       patientBranch.includes(searchValue) ||
                       patientModality.includes(searchValue) ||
                       patientDate.includes(searchValue);
            });
            console.log('Filtered Data:', filteredData);
            populateTable(filteredData); // Update table with filtered data
        });
    });
});
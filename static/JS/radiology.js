document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('button1').addEventListener('click', function () {
        fetchData_table('today_rad');
    });

    document.getElementById('button2').addEventListener('click', function () {
        fetchData_table('next_rad');
    });

    document.getElementById('button3').addEventListener('click', function () {
        fetchData_table('previous_rad');
    });

    document.getElementById('button4').addEventListener('click', function () {
        fetchData_table('all_rad');
    });

        // Fetch data from endpoint1 by default when the page loads
        fetchData_table('all_rad');
});

let patientData = []; // Array to store patient data from server
let formDictionary = []; // Array to store form data for submission

// Function to fetch data from the server
async function fetchData_table(endpoint) {
    try {
        const response = await fetch(`/${endpoint}`);
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        if (!data || !Array.isArray(data)) {
            throw new Error('Invalid data format received');
        }
        // Transform each patient object received from server
        patientData = data.map(patient => ({
            name: patient.name,
            patient_ssn: patient.patient_ssn.toString(),
            organ: patient.organ,
            modality: patient.modality,
            branch_name: patient.bname || patient.branch_name,
            datetime: patient.datetime,
            rad_id: patient.radiologist_id !== undefined && patient.radiologist_id !== null ? patient.radiologist_id : null,
            scan: patient.scan_folder !== undefined && patient.scan_folder !== null ? patient.scan_folder : null
        }));
        populateTable(patientData); // Populate table with fetched data
    } catch (error) {
        console.error('Error fetching data:', error);
        // Handle error gracefully, e.g., show a message to the user
    }
}

// Function to populate the table with patient data
function populateTable(data) {
    const tableBody = document.getElementById('patientTableBody');
    tableBody.innerHTML = ''; // Clear existing table rows

    // Create table rows for each patient data
    data.forEach((patient, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${patient.name}</td>
            <td>${patient.patient_ssn}</td>
            <td>${patient.organ}</td>
            <td>${patient.modality}</td>
            <td>${patient.branch_name}</td>
            <td>${patient.datetime}</td>
            <td>
                ${patient.rad_id !== null ?
                    `<span class="payment-text">${patient.rad_id}</span> ` :
                    `<input type="text" name="rad_id" placeholder="Enter your ID" class="payment-input" data-index="${index}">`
                }
            </td>
            <td>
                ${patient.scan !== null ?
                    `${patient.scan}` :
                    `<input type="file" name="scan" class="upload-input payment-input" data-index="${index}" multiple accept="image/*" webkitdirectory>`
                }
            </td>
            <td>
                ${patient.rad_id !== null ?
                    `verified` :
                    `<button class="payment-btn" data-index="${index}">Add</button>`
                }
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Event delegation for button clicks within the table body
document.getElementById('patientTableBody').addEventListener('click', async (event) => {
    if (event.target.classList.contains('payment-btn')) {
        const index = event.target.getAttribute('data-index');
        const rad_id_input = document.querySelector(`.payment-input[name="rad_id"][data-index="${index}"]`);
        const rad_id = rad_id_input.value.trim();

        const patient = patientData[index];
        const formData = new FormData();
        formData.append('csrf_token', document.querySelector('meta[name="csrf-token"]').getAttribute('content'));

        // Append all patient data to formData
        Object.keys(patient).forEach(key => {
            formData.append(key, patient[key]);
        });

        formData.set('rad_id', rad_id);

        // Handle file upload
        const uploadFileInput = document.querySelector(`.upload-input[data-index="${index}"]`);
        if (uploadFileInput.files.length > 0) {
            for (let i = 0; i < uploadFileInput.files.length; i++) {
                const file = uploadFileInput.files[i];
                formData.append('files', file);
            }
        }

        try {
            const response = await fetch('/get_scan', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                // Update patient object if needed
                patient.rad_id = rad_id;
                formDictionary.push(patient); // Save to form dictionary
                populateTable(patientData); // Refresh table
            } else {
                console.error('Error in get_scan:', response.statusText);
            }
        } catch (error) {
            console.error('Fetch error:', error);
        }
    }
});

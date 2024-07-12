document.addEventListener('DOMContentLoaded', function () {
    let patientData = []; // Array to store patient data from server
    let formDictionary = []; // Array to store form data for submission

    // Function to fetch data from the server
    async function fetchData() {
        try {
            const response = await fetch("/radiology_table");
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const data = await response.json();
            if (!data || !Array.isArray(data)) {
                throw new Error('Invalid data format received');
            }
            // Transform each patient object received from server
            return data.map(patient => ({
                name: patient.name,
                patient_ssn: patient.patient_ssn.toString(),
                organ: patient.organ,
                modality: patient.modality,
                branch_name: patient.branch_name,
                datetime: patient.datetime,
                rad_id: (patient.rad_id !== undefined && patient.rad_id !== null) ? patient.rad_id : null,
                scan: (patient.scan !== undefined && patient.scan !== null) ? patient.scan : null
            }));
        } catch (error) {
            console.error('Error fetching data:', error);
            throw error; // Propagate the error to handle it outside
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
                `<span class="payment-text">${patient.rad_id}</span> `:
               ` <input type="text" name="rad_id" placeholder="Enter your ID" class="payment-input" data-index="${index}"`>
            }
        </td>
                <td>
            ${patient.scan !== null ?
               ` ${patient.scan} `:
                `<input type="file" name="scan" class="upload-input payment-input" data-index="${index}" multiple accept="image/*" webkitdirectory>`
            }
              </td>

       
        <td>
            ${patient.rad_id !== null ?
               ` <button class="edit-btn" data-index="${index}">Edit</button>` :
               ` <button class="payment-btn" data-index="${index}">Add</button>`
            }
        </td>

            `;
            tableBody.appendChild(row);
        });

        // Add event listener for button clicks within the table body
        tableBody.addEventListener('click', async (event) => {
            if (event.target.classList.contains('payment-btn')) {
                const index = event.target.getAttribute('data-index');
                const rad_id_input = document.querySelector(`.payment-input[name="rad_id"][data-index="${index}"]`);
                const rad_id = rad_id_input.value.trim();

                const patient = data[index];
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
                        // patientData.splice(index, 1); // Remove from patientData
                        populateTable(patientData); // Refresh table
                    } else {
                        console.error('Error in get_scan:', response.statusText);
                    }
                } catch (error) {
                    console.error('Fetch error:', error);
                }
            }
        });
    }

    // Fetch data and populate table on page load
    fetchData()
        .then(data => {
            patientData = data; // Save the fetched data to patientData
            populateTable(data); // Populate table with fetched data
        })
        .catch(error => {
            console.error('Error fetching and populating data:', error);
        });
});
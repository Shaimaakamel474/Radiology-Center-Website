        // Add event listener for button clicks within the table body
        tableBody.addEventListener('click', async (event) => {
            if (event.target.classList.contains('payment-btn')) {
                const index = event.target.getAttribute('data-index');

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
document.addEventListener('DOMContentLoaded', function() {
    // Event listeners for sidebar links to show relevant tables and search bars
    document.getElementById('doctorLink').addEventListener('click', function() {
        fetchAndPopulateDoctorTable();
        showTableAndSearchBar('doctorTableContainer', 'doctor_bar');
    });

    document.getElementById('radiologistLink').addEventListener('click', function() {
        fetchAndPopulateRadiologistTable();
        showTableAndSearchBar('radiologistTableContainer', 'radiologist_bar');
    });

    document.getElementById('clinicalEngineerLink').addEventListener('click', function() {
        fetchAndPopulateClinicalEngineerTable();
        showTableAndSearchBar('clinicalEngineerTableContainer', 'clinicalEngineer_bar');
    });

    document.getElementById('receptionistLink').addEventListener('click', function() {
        fetchAndPopulateReceptionistTable();
        showTableAndSearchBar('receptionistTableContainer', 'receptionist_bar');
    });

    document.getElementById('patientLink').addEventListener('click', function() {
        fetchAndPopulatePatientTable();
        showTableAndSearchBar('patientTableContainer', 'patient_bar');
    });

    document.getElementById('deviceLink').addEventListener('click', function() {
        fetchAndPopulateDeviceTable();
        showTableAndSearchBar('deviceTableContainer', 'device_bar');
    });

    document.getElementById('branchLink').addEventListener('click', function() {
        fetchAndPopulateBranchTable();
        showTableAndSearchBar('branchTableContainer', 'branch_bar');
    });

    document.getElementById('hrLink').addEventListener('click', function() {
        fetchAndPopulateHRTable();
        showTableAndSearchBar('hrTableContainer', 'hr_bar');
    });

    document.getElementById('managerLink').addEventListener('click', function() {
        fetchAndPopulateManagerTable();
        showTableAndSearchBar('managerTableContainer', 'manager_bar');
    });

    // Function to show the selected table and its associated search bar
    function showTableAndSearchBar(tableId, searchBarClass) {
        hideAllTablesAndSearchBars();

        const tableElement = document.getElementById(tableId);
        if (tableElement) {
            tableElement.style.display = 'block';
        } else {
            console.error(`Table element with ID '${tableId}' not found.`);
        }

        const searchBarElement = document.querySelector(`.${searchBarClass}`);
        if (searchBarElement) {
            searchBarElement.style.display = 'block';
        } else {
            console.error(`Search bar element with class '${searchBarClass}' not found.`);
        }
    }

    // Function to hide all table containers and search bars
    function hideAllTablesAndSearchBars() {
        const tableContainers = document.querySelectorAll('.table-container');
        tableContainers.forEach(container => {
            container.style.display = 'none';
        });

        const searchBars = document.querySelectorAll('.search');
        searchBars.forEach(search => {
            search.style.display = 'none';
        });
    }

    // Fetch functions for each table
    function fetchAndPopulateDoctorTable() {
        fetch('/doctor_table')
            .then(response => response.json())
            .then(data => populateDoctorTable(data))
            .catch(error => console.error('Error fetching doctor data:', error));
    }

    function fetchAndPopulateRadiologistTable() {
        fetch('/radiologist_table')
            .then(response => response.json())
            .then(data => populateRadiologistTable(data))
            .catch(error => console.error('Error fetching radiologist data:', error));
    }

    function fetchAndPopulateClinicalEngineerTable() {
        fetch('/clinical_table')
            .then(response => response.json())
            .then(data => populateClinicalEngineerTable(data))
            .catch(error => console.error('Error fetching clinical engineer data:', error));
    }

    function fetchAndPopulateReceptionistTable() {
        fetch('/receptionist_table')
            .then(response => response.json())
            .then(data => populateReceptionistTable(data))
            .catch(error => console.error('Error fetching receptionist data:', error));
    }

    function fetchAndPopulatePatientTable() {
        fetch('/patient_admin_table')
            .then(response => response.json())
            .then(data => populatePatientTable(data))
            .catch(error => console.error('Error fetching patient data:', error));
    }

    function fetchAndPopulateDeviceTable() {
        fetch('/device_admin_table')
            .then(response => response.json())
            .then(data => populateDeviceTable(data))
            .catch(error => console.error('Error fetching device data:', error));
    }

    function fetchAndPopulateBranchTable() {
        fetch('/branch_admin_table')
            .then(response => response.json())
            .then(data => populateBranchTable(data))
            .catch(error => console.error('Error fetching branch data:', error));
    }

    function fetchAndPopulateHRTable() {
        fetch('/HR_table')
            .then(response => response.json())
            .then(data => populateHRTable(data))
            .catch(error => console.error('Error fetching HR data:', error));
    }

    function fetchAndPopulateManagerTable() {
        fetch('/Manager_table')
            .then(response => response.json())
            .then(data => populateManagerTable(data))
            .catch(error => console.error('Error fetching manager data:', error));
    }

    // Populate functions for each table
    function populateDoctorTable(data) {
        const tableBody = document.getElementById('doctorTableBody');
        populateTable(tableBody, data, 'doctor');
    }

    function populateRadiologistTable(data) {
        const tableBody = document.getElementById('radiologistTableBody');
        populateTable(tableBody, data, 'radiologist');
    }

    function populateClinicalEngineerTable(data) {
        const tableBody = document.getElementById('clinicalEngineerTableBody');
        populateTable(tableBody, data, 'clinicalEngineer');
    }

    function populateReceptionistTable(data) {
        const tableBody = document.getElementById('receptionistTableBody');
        populateTable(tableBody, data, 'receptionist');
    }

    function populateHRTable(data) {
        const tableBody = document.getElementById('hrTableBody');
        populateTable(tableBody, data, 'hr');
    }

    function populateManagerTable(data) {
        const tableBody = document.getElementById('managerTableBody');
        populateTable(tableBody, data, 'manager');
    }

    function populatePatientTable(data) {
        const tableBody = document.getElementById('patientTableBody');
        populatePatientTableBody(tableBody, data);
    }

    function populateDeviceTable(data) {
        const tableBody = document.getElementById('deviceTableBody');
        populateDeviceTableBody(tableBody, data);
    }

    function populateBranchTable(data) {
        const tableBody = document.getElementById('branchTableBody');
        populateBranchTableBody(tableBody, data);
    }

    // Generic function to populate a table body with data
    function populateTable(tableBody, data, type) {
        tableBody.innerHTML = ''; // Clear existing table rows

        data.forEach((item, index) => {
            const row = document.createElement('tr');
            row.id = `${type}-row-${index}`;

            // Adjust fields based on your actual data structure
            row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.employee_id}</td>
                <td>${item.age}</td>
                <td>${item.gender}</td>
                <td>${item.phone_number}</td>
                <td>${item.email}</td>
                <td>${item.password}</td>
                <td>${item.address}</td>
                <td>${item.salary}</td>
                <td>${item.pay_scale}</td>
                <td>${item.start_shift}</td>
                <td>${item.end_shift}</td>
                <td>${item.branch_id}</td>
                ${item.scan_type ? `<td>${item.scan_type}</td>` : ''}
                ${item.technique ? `<td>${item.technique}</td>` : ''}
                <td><button type="button" onclick="editRow('${type}', ${index})">Edit</button></td>
            `;
            tableBody.appendChild(row);
        });
    }

    function populatePatientTableBody(tableBody, data) {
        tableBody.innerHTML = ''; // Clear existing content

        data.forEach((patient, index) => {
            const row = document.createElement('tr');
            row.id = `patient-row-${index}`;
            row.innerHTML = `
                <td>${patient.name}</td>
                <td>${patient.patient_ssn}</td>
                <td>${patient.gender}</td>
                <td>${patient.age}</td>
                <td>${patient.phone_number}</td>
                <td>${patient.email}</td>
                <td>${patient.password}</td>
                <td>${patient.address}</td>
                <td>${patient.booking_technique}</td>
                <td><button type="button" onclick="editRow('patient', ${index})">Edit</button></td>
            `;
            tableBody.appendChild(row);
        });
    }

    function populateDeviceTableBody(tableBody, data) {
        tableBody.innerHTML = ''; // Clear existing content

        data.forEach((device, index) => {
            const row = document.createElement('tr');
            row.id = `device-row-${index}`;
            row.innerHTML = `
                <td>${device.device_name}</td>
                <td>${device.device_sn}</td>
                <td>${device.device_tech}</td>
                <td>${device.bname}</td>
                <td>${device.d_data1}</td>
                <td>${device.d_data2}</td>
                <td>${device.d_data3}</td>
                <td><button type="button" onclick="editRow('device', ${index})">Edit</button></td>
            `;
            tableBody.appendChild(row);
        });
    }

    function populateBranchTableBody(tableBody, data) {
        tableBody.innerHTML = ''; // Clear existing content

        data.forEach((branch, index) => {
            const row = document.createElement('tr');
            row.id = `branch-row-${index}`;
            row.innerHTML = `
                <td>${branch.branch_id}</td>
                <td>${branch.bname}</td>
                <td>${branch.phone_number}</td>
                <td>${branch.email}</td>
                <td>${branch.manager}</td>
                <td><button type="button" onclick="editRow('branch', ${index})">Edit</button></td>
            `;
            tableBody.appendChild(row);
        });
    }

    // Function to convert a table row to input fields for editing
    window.editRow = function(type, index) {
        const row = document.getElementById(`${type}-row-${index}`);
        const cells = row.getElementsByTagName('td');

        // Convert each cell to an input field except the last cell (Edit button)
        for (let i = 0; i < cells.length - 1; i++) {
            const cell = cells[i];
            const originalValue = cell.innerText;
            cell.innerHTML = `<input type="text" value="${originalValue}">`;
        }

        // Change the Edit button to an Update button
        const editButton = cells[cells.length - 1].getElementsByTagName('button')[0];
        editButton.textContent = 'Update';
        editButton.onclick = function() { saveRow(type, index); };
    };

    // Function to save the updated data and convert input fields back to text
    window.saveRow = function(type, index) {
        const row = document.getElementById(`${type}-row-${index}`);
        const cells = row.getElementsByTagName('td');

        // Create an object to hold updated data
        const updatedData = {};

        // Update each cell with the input value and save to the updatedData object
        for (let i = 0; i < cells.length - 1; i++) {
            const inputField = cells[i].getElementsByTagName('input')[0];
            const newValue = inputField.value;
            cells[i].innerText = newValue;
            
            // Assuming the order of the fields matches the order of your data structure
            // Adjust the field mapping as necessary
            switch (i) {
                case 0:
                    updatedData.name = newValue;
                    break;
                case 1:
                    updatedData.id = newValue;
                    break;
                case 2:
                    updatedData.age = newValue;
                    break;
                case 3:
                    updatedData.gender = newValue;
                    break;
                case 4:
                    updatedData.phone_number = newValue;
                    break;
                case 5:
                    updatedData.email = newValue;
                    break;
                case 6:
                    updatedData.password = newValue;
                    break;
                case 7:
                    updatedData.address = newValue;
                    break;
                case 8:
                    updatedData.extraField1 = newValue; // Adjust according to table
                    break;
                case 9:
                    updatedData.extraField2 = newValue; // Adjust according to table
                    break;
                case 10:
                    updatedData.extraField3 = newValue; // Adjust according to table
                    break;
                case 11:
                    updatedData.extraField4 = newValue; // Adjust according to table
                    break;
                case 12:
                    updatedData.extraField5 = newValue; // Adjust according to table
                    break;
                default:
                    break;
            }
        }

        // Change the Update button back to Edit button
        const updateButton = cells[cells.length - 1].getElementsByTagName('button')[0];
        updateButton.textContent = 'Edit';
        updateButton.onclick = function() { editRow(type, index); };

        // Send updated data to the server
        sendUpdatedData(type, updatedData);
    };

    // Function to send updated data to the server
    function sendUpdatedData(type, data) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch("updtae_admin", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': csrfToken // Add CSRF token header
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(result => {
            console.log('Update successful:', result);
            // Optionally refresh the table or provide feedback to the user
        })
        .catch(error => {
            console.error('Error updating data:', error);
            // Optionally handle error and provide feedback to the user
        });
    }
});

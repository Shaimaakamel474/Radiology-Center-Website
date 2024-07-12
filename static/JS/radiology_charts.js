document.addEventListener('DOMContentLoaded', function () {
    fetchAndPopulateRadiologistTable();
});

// Function to fetch radiologist table data
function fetchAndPopulateRadiologistTable() {
    fetch('/radiologist_table')
        .then(response => response.json())
        .then(data => populateRadiologistTable(data))
        .catch(error => console.error('Error fetching radiologist data:', error));
}

// Function to populate radiologist table
function populateRadiologistTable(data) {
    const tableBody = document.getElementById('radiologistTableBody');
    populateTable(tableBody, data, 'radiologist');
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
            <td>${item.technique ? item.technique : ''}</td>
            <td><button type="button" onclick="editRow('${type}', ${index})">Edit</button></td>
        `;
        tableBody.appendChild(row);
    });
}

// Function to convert a table row to input fields for editing
window.editRow = function(type, index) {
    const row = document.getElementById(`${type}-row-${index}`);
    const cells = row.getElementsByTagName('td');

    // Convert each cell to an input field except the last cell (Action button)
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

        // Map updated values to the corresponding fields in updatedData
        switch (i) {
            case 0:
                updatedData.name = newValue;
                break;
            case 1:
                updatedData.employee_id = newValue;
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
                updatedData.salary = newValue;
                break;
            case 9:
                updatedData.pay_scale = newValue;
                break;
            case 10:
                updatedData.start_shift = newValue;
                break;
            case 11:
                updatedData.end_shift = newValue;
                break;
            case 12:
                updatedData.branch_id = newValue;
                break;
            case 13:
                updatedData.technique = newValue;
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
    fetch("/update_radiologists_tablee", {
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

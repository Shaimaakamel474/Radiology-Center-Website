let patientData = [];

// Function to fetch data from the JSON file
function fetchData() {
    return fetch("/pacs_table")
        .then(response => response.json())
        .then(data => {
            patientData = data.map((patient, index) => ({
                name: patient.name,
                patient_ssn: patient.patient_ssn.toString(),
                gender: patient.gender,
                age: patient.age,
                radiology_id: patient.radiologist_id,
                organ: patient.organ,
                modality: patient.modality,
                branch: patient.branch_name,
                datetime: patient.datetime,
                scan: patient.scan_folder,
                status: patient.verified || 'Not Checked',
                report: patient.report || '',
                doctor_id: patient.doctor_id || '',
                index: index // Add an index to identify rows
            }));
            populateTable(patientData);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// Function to populate the table with patient data
function populateTable(data) {
    const tableBody = document.getElementById('patientTableBody');
    tableBody.innerHTML = '';

    if (data.length > 0) {
        data.forEach((patient, index) => {
            const row = document.createElement('tr');
            row.id = `row-${index}`;
            row.innerHTML = `
                <td>${patient.name}</td>
                <td>${patient.patient_ssn}</td>
                <td>${patient.age}</td>
                <td>${patient.gender}</td>
                <td>${patient.radiology_id}</td>
                <td>${patient.organ}</td>
                <td>${patient.modality}</td>
                <td>${patient.branch}</td>
                <td>${patient.datetime}</td>
                <td><button type="button" value="${patient.scan}" onclick="showImagesFunction('${patient.scan}')">${patient.scan}</button></td>
                <td>${patient.status}</td>
                <td>${patient.report}</td>
                <td>${patient.doctor_id}</td>
                <td><button type="button" onclick="editPatientData(${index})">${patient.status === 'Not Checked' || !patient.doctor_id ? 'Add' : 'Edit'}</button></td>
            `;
            tableBody.appendChild(row);
        });
    } else {
        const emptyRow = document.createElement('tr');
        emptyRow.innerHTML = `
            <td><input type="text" id="name" placeholder="Name"></td>
            <td><input type="text" id="patient_ssn" placeholder="Patient SSN"></td>
            <td><input type="text" id="age" placeholder="Age"></td>
            <td><input type="text" id="gender" placeholder="Gender"></td>
            <td><input type="text" id="radiology_id" placeholder="Radiology ID"></td>
            <td><input type="text" id="organ" placeholder="Organ"></td>
            <td><input type="text" id="modality" placeholder="Modality"></td>
            <td><input type="text" id="branch" placeholder="Branch"></td>
            <td><input type="text" id="datetime" placeholder="Datetime"></td>
            <td><input type="text" id="scan" placeholder="Scan"></td>
            ${getInputField('status', 'Not Checked', 0)}
            ${getInputField('report', '', 0)}
            ${getInputField('doctor_id', '', 0)}
            <td><button type="button" onclick="addPatientData()">Add</button></td>
        `;
        tableBody.appendChild(emptyRow);
    }
}

// Function to generate input fields dynamically
function getInputField(key, defaultValue, index) {
    if (patientData.length === 0) {
        return `<td><input type="text" id="${key}-${index}" value="${defaultValue}" placeholder="${key.charAt(0).toUpperCase() + key.slice(1)}"></td>`;
    } else {
        return `<td>${defaultValue}</td>`;
    }
}

// Function to update patient data
function updatePatientData(index) {
    const status = document.getElementById(`status-${index}`).value;
    const report = document.getElementById(`report-${index}`).value;
    const doctorid = document.getElementById(`doctor_id-${index}`).value;

    patientData[index].status = status;
    patientData[index].report = report;
    patientData[index].doctor_id = doctorid;

    const row = document.getElementById(`row-${index}`);
    row.innerHTML = `
        <td>${patientData[index].name}</td>
        <td>${patientData[index].patient_ssn}</td>
        <td>${patientData[index].age}</td>
        <td>${patientData[index].gender}</td>
        <td>${patientData[index].radiology_id}</td>
        <td>${patientData[index].organ}</td>
        <td>${patientData[index].modality}</td>
        <td>${patientData[index].branch}</td>
        <td>${patientData[index].datetime}</td>
        <td><button type="button" value="${patientData[index].scan}" onclick="showImagesFunction('${patientData[index].scan}')">${patientData[index].scan}</button></td>
        <td>${patientData[index].status}</td>
        <td>${patientData[index].report}</td>
        <td>${patientData[index].doctor_id}</td>
        <td><button type="button" onclick="editPatientData(${index})">Edit</button></td>
    `;

    saveUpdatedData(patientData[index]);
}

// Function to save updated patient data to the server
function saveUpdatedData(patient) {
    const formData = new FormData();
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    for (const key in patient) {
        formData.append(key, patient[key]);
    }
    formData.append('csrf_token', csrfToken);

    fetch('/pacs_updated', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to show images based on patient scan
function showImagesFunction(scan) {
    const formData = new FormData();
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    formData.append('scan', scan);
    formData.append('csrf_token', csrfToken);

    fetch('/view_images', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.image_urls)
        const imageUrls = data.image_urls;
        showHidden2()
        updateImageSlider(imageUrls);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}



function showHidden2() {
    const hidden2 = document.getElementById('hidden2');
    if (patientData.length > 0) {
        hidden2.style.display = 'block'; // Show hidden2
    } else {
        hidden2.style.display = 'none'; // Hide hidden2 if no patient data
    }
}




// Function to handle editing patient data
function editPatientData(index) {
    const row = document.getElementById(`row-${index}`);
    row.innerHTML = `
        <td>${patientData[index].name}</td>
        <td>${patientData[index].patient_ssn}</td>
        <td>${patientData[index].age}</td>
        <td>${patientData[index].gender}</td>
        <td>${patientData[index].radiology_id}</td>
        <td>${patientData[index].organ}</td>
        <td>${patientData[index].modality}</td>
        <td>${patientData[index].branch}</td>
        <td>${patientData[index].datetime}</td>
        <td><button type="button" value="${patientData[index].scan}" onclick="showImagesFunction('${patientData[index].scan}')">${patientData[index].scan}</button></td>
        <td>
            <select id="status-${index}" class="status">
                <option value="Not Checked" ${patientData[index].status === 'Not Checked' ? 'selected' : ''}>Not Checked</option>
                <option value="Is Checking" ${patientData[index].status === 'Is Checking' ? 'selected' : ''}>Is Checking</option>
                <option value="Checked" ${patientData[index].status === 'Checked' ? 'selected' : ''}>Checked</option>
            </select>
        </td>
        <td><input type="text" value="${patientData[index].report}" id="report-${index}" class="report"></td>
        <td><input type="text" value="${patientData[index].doctor_id}" id="doctor_id-${index}" class="doctorid"></td>
        <td><button type="button" onclick="updatePatientData(${index})">Done</button></td>
    `;
}

// Event listener when the DOM content is loaded
document.addEventListener('DOMContentLoaded', function() {
    fetchData();

    const searchInputs = document.querySelectorAll('.bars input');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchValue = input.value.toLowerCase();
            const filteredData = patientData.filter(patient => {
                const patient_ssn = patient.patient_ssn.toLowerCase();
                const patientBranch = patient.branch.toLowerCase();
                const patientModality = patient.modality.toLowerCase();
                const patientDatetime = patient.datetime.toLowerCase();
                const patientOrgan = patient.organ.toLowerCase();
                const patientStatus = patient.status.toLowerCase();
                return patient_ssn.includes(searchValue) ||
                       patientBranch.includes(searchValue) ||
                       patientModality.includes(searchValue) ||
                       patientDatetime.includes(searchValue) ||
                       patientStatus.includes(searchValue) ||
                       patientOrgan.includes(searchValue);
            });
            populateTable(filteredData);
        });
    });
});

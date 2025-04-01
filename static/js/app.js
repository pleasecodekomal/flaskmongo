window.onload = function() {
    fetch('/employees')  // Fetch employees from the backend
        .then(response => response.json())
        .then(data => {
            const employeeList = document.getElementById('employee-list');
            data.forEach(employee => {
                const div = document.createElement('div');
                div.textContent = `${employee.name} - ${employee.position}`;
                employeeList.appendChild(div);
            });
        });
};

document.getElementById("loadData").addEventListener("click", async () => {
    const response = await fetch("/api/employees");  // Adjust endpoint as per your backend
    const data = await response.json();
    
    let container = document.getElementById("dataContainer");
    container.innerHTML = "<h2>Employee List</h2>";

    data.forEach(emp => {
        let div = document.createElement("div");
        div.innerHTML = `<strong>${emp.name}</strong> - ${emp.position}`;
        container.appendChild(div);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // File Upload Functionality
    const fileInput = document.getElementById('file-input');
    const fileName = document.getElementById('file-name');
    const uploadBtn = document.getElementById('upload-btn');
    
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            fileName.textContent = this.files[0].name;
        } else {
            fileName.textContent = 'No file selected';
        }
    });
    
    uploadBtn.addEventListener('click', function() {
        if (!fileInput.files.length) {
            alert('Please select a file first!');
            return;
        }
        alert('Dataset uploaded successfully!');
        document.getElementById('update-date').textContent = new Date().toLocaleString();
    });
    
    // Chart Initialization
    const ctx = document.getElementById('trend-chart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'PM2.5 Levels',
                data: [12, 19, 15, 22, 18, 25],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
    
    // Chart Type Toggle
    document.getElementById('chart-type').addEventListener('change', function() {
        chart.config.type = this.value;
        chart.update();
    });
    
    // Export Chart
    document.getElementById('export-chart').addEventListener('click', function() {
        alert('Chart exported!');
    });
    
    // Download Buttons
    document.getElementById('download-excel').addEventListener('click', function() {
        alert('Excel download started!');
    });
    
    document.getElementById('download-pdf').addEventListener('click', function() {
        alert('PDF report generated!');
    });
    
    // Analysis Button
    document.getElementById('analyze-btn').addEventListener('click', function() {
        alert('Analysis completed!');
        document.getElementById('update-date').textContent = new Date().toLocaleString();
    });
});
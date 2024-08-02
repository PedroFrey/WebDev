document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('financialChart').getContext('2d');
    const financialChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June'],
            datasets: [{
                label: 'Revenue',
                data: [12000, 15000, 17000, 14000, 19000, 22000],
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const expensesCtx = document.getElementById('expensesChart').getContext('2d');
    const expensesChart = new Chart(expensesCtx, {
        type: 'pie',
        data: {
            labels: ['Rent', 'Utilities', 'Salaries', 'Marketing', 'Miscellaneous'],
            datasets: [{
                label: 'Expenses',
                data: [5000, 2000, 8000, 3000, 1000],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });

    const financialData = [
        { month: 'January', revenue: 12000 },
        { month: 'February', revenue: 15000 },
        { month: 'March', revenue: 17000 },
        { month: 'April', revenue: 14000 },
        { month: 'May', revenue: 19000 },
        { month: 'June', revenue: 22000 }
    ];

    const financialDataList = document.getElementById('financialData');
    financialData.forEach(data => {
        const listItem = document.createElement('li');
        listItem.textContent = `${data.month}: $${data.revenue}`;
        financialDataList.appendChild(listItem);
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const financialData = [
        { month: 'January', revenue: 12000, expenses: 5000 },
        { month: 'February', revenue: 15000, expenses: 2000 },
        { month: 'March', revenue: 17000, expenses: 8000 },
        { month: 'April', revenue: 14000, expenses: 3000 },
        { month: 'May', revenue: 19000, expenses: 1000 },
        { month: 'June', revenue: 22000, expenses: 7000 }
    ];

    // Extracting revenue and expenses data from the financialData array
    const months = financialData.map(data => data.month);
    const revenueData = financialData.map(data => data.revenue);
    const expensesData = financialData.map(data => data.expenses);

    // Financial chart
    const ctx = document.getElementById('financialChart').getContext('2d');
    const financialChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'Revenue',
                data: revenueData,
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

    // Expenses chart
    const expensesCtx = document.getElementById('expensesChart').getContext('2d');
    const expensesChart = new Chart(expensesCtx, {
        type: 'pie',
        data: {
            labels: ['Rent', 'Utilities', 'Salaries', 'Marketing', 'Miscellaneous'],
            datasets: [{
                label: 'Expenses',
                data: expensesData,
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

    // Display financial data in a list
    const financialDataList = document.getElementById('financialData');
    financialData.forEach(data => {
        const listItem = document.createElement('li');
        listItem.textContent = `${data.month}: Revenue $${data.revenue}, Expenses $${data.expenses}`;
        financialDataList.appendChild(listItem);
    });
});

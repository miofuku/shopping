document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const resultsDiv = document.getElementById('results');

    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const budget = document.getElementById('budget').value;
            const items = document.getElementById('items').value.split(',').map(item => item.trim());

            fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ budget: parseFloat(budget), items: items }),
            })
            .then(response => response.json())
            .then(data => {
                resultsDiv.innerHTML = '<h3>Results:</h3>';
                data.results.forEach(item => {
                    resultsDiv.innerHTML += `
                        <p><strong>${item.name}</strong> - $${item.price.toFixed(2)} (${item.source})</p>
                    `;
                });
                resultsDiv.innerHTML += `
                    <p><strong>Total Cost:</strong> $${data.total_cost.toFixed(2)}</p>
                    <p><strong>Remaining Budget:</strong> $${data.remaining_budget.toFixed(2)}</p>
                `;
            })
            .catch(error => {
                console.error('Error:', error);
                resultsDiv.innerHTML = 'An error occurred while searching for deals.';
            });
        });
    }
});
/**
 * Chart.js Visualizations for Capstone 57
 * Author: Reshma Anandhan
 */

document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            initDashboardCharts(data);
            initComparisonCharts(data);
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
});

function initDashboardCharts(data) {
    // 1. Home Dashboard Bar Chart: Overall Performance Comparison
    const ctxOverall = document.getElementById('dashboardOverallChart');
    if (ctxOverall) {
        new Chart(ctxOverall, {
            type: 'bar',
            data: {
                labels: data.tools,
                datasets: [
                    {
                        label: 'Weighted Score (%)',
                        data: data.weighted_scores,
                        backgroundColor: 'rgba(6, 182, 212, 0.85)',
                        borderColor: '#06b6d4',
                        borderWidth: 1,
                        borderRadius: 6
                    },
                    {
                        label: 'Accuracy Score (%)',
                        data: data.accuracy_scores,
                        backgroundColor: 'rgba(56, 189, 248, 0.4)',
                        borderColor: '#38bdf8',
                        borderWidth: 1,
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#94a3b8', font: { family: 'Inter', size: 12 } }
                    },
                    tooltip: {
                        backgroundColor: '#0f172a',
                        titleColor: '#38bdf8',
                        bodyColor: '#fff',
                        borderColor: '#1e3a63',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#f1f5f9', font: { weight: '600' } }
                    }
                }
            }
        });
    }

    // 2. Modality Breakdown Chart on Dashboard
    const ctxModality = document.getElementById('dashboardModalityChart');
    if (ctxModality) {
        const modalities = ['IMAGE', 'DOCUMENT', 'AUDIO'];
        const datasets = modalities.map((mod, index) => {
            const colors = [
                'rgba(6, 182, 212, 0.85)',  // Cyan for Image
                'rgba(245, 158, 11, 0.85)',  // Amber for Document
                'rgba(239, 68, 68, 0.85)'    // Rose for Audio
            ];
            return {
                label: mod,
                data: data.tools.map(tool => data.modality_breakdown[tool] ? data.modality_breakdown[tool][mod] : 0),
                backgroundColor: colors[index],
                borderRadius: 4
            };
        });

        new Chart(ctxModality, {
            type: 'bar',
            data: {
                labels: data.tools,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#94a3b8', font: { family: 'Inter', size: 12 } }
                    }
                },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#f1f5f9' }
                    }
                }
            }
        });
    }
}

function initComparisonCharts(data) {
    // 3. Comparison Radar Chart
    const ctxRadar = document.getElementById('comparisonRadarChart');
    if (ctxRadar) {
        new Chart(ctxRadar, {
            type: 'radar',
            data: {
                labels: data.radar_labels,
                datasets: data.radar_datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#94a3b8', font: { family: 'Inter', size: 12 } }
                    }
                },
                scales: {
                    r: {
                        min: 0,
                        max: 100,
                        angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                        grid: { color: 'rgba(255, 255, 255, 0.08)' },
                        pointLabels: { color: '#38bdf8', font: { size: 11, weight: '600' } },
                        ticks: { backdropColor: 'transparent', color: '#94a3b8', stepSize: 20 }
                    }
                }
            }
        });
    }

    // 4. Failure Analysis Chart (Hallucinations & Outdated Info)
    const ctxFailure = document.getElementById('failureAnalysisChart');
    if (ctxFailure) {
        new Chart(ctxFailure, {
            type: 'bar',
            data: {
                labels: data.failure_data.labels,
                datasets: [
                    {
                        label: 'Hallucinations Caught',
                        data: data.failure_data.hallucinations,
                        backgroundColor: '#ef4444',
                        borderRadius: 4
                    },
                    {
                        label: 'Unsafe / Outdated Statements',
                        data: data.failure_data.unsafe_outdated,
                        backgroundColor: '#f59e0b',
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#94a3b8' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1, color: '#94a3b8' },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    },
                    x: {
                        ticks: { color: '#f1f5f9' },
                        grid: { display: false }
                    }
                }
            }
        });
    }
}

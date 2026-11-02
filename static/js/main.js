/**
 * Main Application JavaScript for Capstone 57
 * Author: Reshma Anandhan
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Initialize Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 2. Mobile Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('open');
        });
    }

    // 3. Real-Time Dynamic Evaluation Score Calculator
    const accInput = document.getElementById('accuracy_score');
    const compInput = document.getElementById('completeness_score');
    const relInput = document.getElementById('relevance_score');
    const easeInput = document.getElementById('ease_of_use_score');
    const liveScoreDisplay = document.getElementById('liveWeightedScore');
    const liveFormulaDisplay = document.getElementById('liveFormulaBreakdown');

    function updateLiveScore() {
        if (!accInput || !compInput || !relInput || !easeInput || !liveScoreDisplay) return;

        const acc = parseFloat(accInput.value) || 0;
        const comp = parseFloat(compInput.value) || 0;
        const rel = parseFloat(relInput.value) || 0;
        const ease = parseFloat(easeInput.value) || 0;

        // Formula: 40% Accuracy, 25% Completeness, 20% Relevance, 15% Ease of Use
        const weighted = (acc * 0.40) + (comp * 0.25) + (rel * 0.20) + (ease * 0.15);
        const rounded = weighted.toFixed(1);

        liveScoreDisplay.textContent = rounded + '%';

        if (liveFormulaDisplay) {
            liveFormulaDisplay.textContent = `(${acc}×0.40) + (${comp}×0.25) + (${rel}×0.20) + (${ease}×0.15) = ${rounded}%`;
        }

        // Color shift based on score
        if (weighted >= 85) {
            liveScoreDisplay.className = 'kpi-value text-success';
        } else if (weighted >= 70) {
            liveScoreDisplay.className = 'kpi-value text-info';
        } else if (weighted >= 50) {
            liveScoreDisplay.className = 'kpi-value text-warning';
        } else {
            liveScoreDisplay.className = 'kpi-value text-danger';
        }
    }

    if (accInput) {
        [accInput, compInput, relInput, easeInput].forEach(inp => {
            inp.addEventListener('input', updateLiveScore);
        });
        updateLiveScore(); // Initial run
    }

    // 4. Checklist Live Reliability & Risk Level Calculator
    const checklistForm = document.getElementById('checklistAuditForm');
    if (checklistForm) {
        const checkboxes = checklistForm.querySelectorAll('.check-risk-item');
        const liveScoreBadge = document.getElementById('liveReliabilityScore');
        const liveRiskBadge = document.getElementById('liveRiskLevel');

        function updateChecklistStats() {
            let issueCount = 0;
            checkboxes.forEach(cb => {
                if (cb.checked) issueCount++;
            });

            // Reliability = 100 - (issueCount * 14.28)
            const reliability = Math.max(0, (100 - (issueCount * 14.28))).toFixed(1);
            let risk = 'Low';
            let riskClass = 'bg-success';

            if (issueCount === 0) {
                risk = 'Low';
                riskClass = 'bg-success';
            } else if (issueCount <= 2) {
                risk = 'Moderate';
                riskClass = 'bg-warning text-dark';
            } else if (issueCount <= 4) {
                risk = 'High';
                riskClass = 'bg-danger';
            } else {
                risk = 'Critical';
                riskClass = 'bg-danger animate-pulse';
            }

            if (liveScoreBadge) liveScoreBadge.textContent = reliability + '%';
            if (liveRiskBadge) {
                liveRiskBadge.textContent = risk + ' Risk';
                liveRiskBadge.className = 'badge ' + riskClass;
            }
        }

        checkboxes.forEach(cb => cb.addEventListener('change', updateChecklistStats));
        updateChecklistStats();
    }
});

/**
 * Copy Text to Clipboard Utility
 */
function copyToClipboard(elementId, btnElement) {
    const textElement = document.getElementById(elementId);
    if (!textElement) return;

    const textToCopy = textElement.textContent || textElement.value;
    navigator.clipboard.writeText(textToCopy).then(() => {
        const originalHtml = btnElement.innerHTML;
        btnElement.innerHTML = '<i class="bi bi-check2"></i> Copied!';
        btnElement.classList.add('btn-success');
        btnElement.classList.remove('btn-outline-cyan');

        setTimeout(() => {
            btnElement.innerHTML = originalHtml;
            btnElement.classList.remove('btn-success');
            btnElement.classList.add('btn-outline-cyan');
        }, 2000);
    }).catch(err => {
        alert("Failed to copy text: " + err);
    });
}

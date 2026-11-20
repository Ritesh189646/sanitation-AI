/* =========================================================
   SANITATION AI DASHBOARD - FRONTEND JAVASCRIPT
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

    // ---------------------------------------------------------
    // TAB SWITCHING
    // ---------------------------------------------------------
    const navBtns = document.querySelectorAll('.nav-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            navBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.add('hidden'));

            btn.classList.add('active');
            const targetTab = btn.getAttribute('data-tab');
            document.getElementById(targetTab).classList.remove('hidden');
        });
    });

    // ---------------------------------------------------------
    // INITIALIZE SAMPLE SELECTOR
    // ---------------------------------------------------------
    const sampleSelect = document.getElementById('sample-select');

    async function loadTestImagesList() {
        try {
            const res = await fetch('/api/test_images');
            const files = await res.json();
            if (Array.isArray(files)) {
                files.forEach(file => {
                    const opt = document.createElement('option');
                    opt.value = file;
                    opt.textContent = file;
                    sampleSelect.appendChild(opt);
                });
            }
        } catch (err) {
            console.error('Failed to load test images:', err);
        }
    }
    loadTestImagesList();

    // ---------------------------------------------------------
    // SLIDER REAL-TIME DISPLAY
    // ---------------------------------------------------------
    const confSlider = document.getElementById('conf-slider');
    const confVal = document.getElementById('conf-val');
    confSlider.addEventListener('input', (e) => {
        confVal.textContent = parseFloat(e.target.value).toFixed(2);
    });

    const padSlider = document.getElementById('pad-slider');
    const padVal = document.getElementById('pad-val');
    padSlider.addEventListener('input', (e) => {
        padVal.textContent = `${e.target.value}px`;
    });

    // ---------------------------------------------------------
    // DRAG AND DROP FILE UPLOAD
    // ---------------------------------------------------------
    const dropzone = document.getElementById('image-dropzone');
    const fileInput = document.getElementById('file-input');
    let selectedFile = null;

    dropzone.addEventListener('click', () => fileInput.click());

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            selectedFile = e.dataTransfer.files[0];
            updateDropzoneFileName(selectedFile.name);
            sampleSelect.value = ''; // clear sample dropdown
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            selectedFile = e.target.files[0];
            updateDropzoneFileName(selectedFile.name);
            sampleSelect.value = '';
        }
    });

    sampleSelect.addEventListener('change', () => {
        if (sampleSelect.value) {
            selectedFile = null;
            resetDropzoneText();
        }
    });

    function updateDropzoneFileName(name) {
        dropzone.querySelector('.drop-title').textContent = name;
        dropzone.querySelector('.drop-sub').textContent = 'File selected ready for inspection';
    }

    function resetDropzoneText() {
        dropzone.querySelector('.drop-title').textContent = 'Drag & Drop Image Here';
        dropzone.querySelector('.drop-sub').textContent = 'or click to browse local files';
    }

    // ---------------------------------------------------------
    // IMAGE VIEW TOGGLE (ANNOTATED VS ORIGINAL)
    // ---------------------------------------------------------
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    const imgAnnotated = document.getElementById('img-annotated');
    const imgOriginal = document.getElementById('img-original');

    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            toggleBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const view = btn.getAttribute('data-view');
            if (view === 'annotated') {
                imgAnnotated.classList.remove('hidden');
                imgOriginal.classList.add('hidden');
            } else {
                imgAnnotated.classList.add('hidden');
                imgOriginal.classList.remove('hidden');
            }
        });
    });

    // ---------------------------------------------------------
    // RUN SINGLE INSPECTION
    // ---------------------------------------------------------
    const btnRunInspect = document.getElementById('btn-run-inspect');
    const inspectEmpty = document.getElementById('inspect-empty');
    const inspectLoading = document.getElementById('inspect-loading');
    const inspectResults = document.getElementById('inspect-results');

    btnRunInspect.addEventListener('click', async () => {
        const conf = confSlider.value;
        const pad = padSlider.value;

        if (!selectedFile && !sampleSelect.value) {
            alert('Please upload an image or select a sample image first.');
            return;
        }

        // Show loading state
        inspectEmpty.classList.add('hidden');
        inspectResults.classList.add('hidden');
        inspectLoading.classList.remove('hidden');

        try {
            let response;
            if (selectedFile) {
                const formData = new FormData();
                formData.append('image', selectedFile);
                formData.append('conf_thresh', conf);
                formData.append('pad', pad);

                response = await fetch('/api/predict', {
                    method: 'POST',
                    body: formData
                });
            } else {
                response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        test_filename: sampleSelect.value,
                        conf_thresh: conf,
                        pad: pad
                    })
                });
            }

            const data = await response.json();

            if (data.error) {
                alert(`Error: ${data.error}`);
                inspectLoading.classList.add('hidden');
                inspectEmpty.classList.remove('hidden');
                return;
            }

            renderInspectionData(data);
        } catch (err) {
            console.error(err);
            alert('Failed to execute model inspection');
            inspectLoading.classList.add('hidden');
            inspectEmpty.classList.remove('hidden');
        }
    });

    function renderInspectionData(data) {
        // Hide loader, show results
        inspectLoading.classList.add('hidden');
        inspectResults.classList.remove('hidden');

        // Header info
        document.getElementById('res-filename').textContent = data.filename;
        document.getElementById('res-dims').textContent = `${data.width} × ${data.height} px`;

        // Overall status badge
        const badgeEl = document.getElementById('res-overall-status');
        badgeEl.className = 'status-badge';

        const st = data.overall_status.toUpperCase();
        let iconHtml = '<i class="fa-solid fa-circle-check"></i>';

        if (st === 'GOOD') {
            badgeEl.classList.add('status-good');
            iconHtml = '<i class="fa-solid fa-circle-check"></i>';
        } else if (st === 'AVERAGE') {
            badgeEl.classList.add('status-avg');
            iconHtml = '<i class="fa-solid fa-triangle-exclamation"></i>';
        } else {
            badgeEl.classList.add('status-bad');
            iconHtml = '<i class="fa-solid fa-circle-exclamation"></i>';
        }

        badgeEl.innerHTML = `${iconHtml} <span>${st}</span>`;

        // Images
        imgAnnotated.src = data.annotated_b64;
        imgOriginal.src = data.original_b64;

        // Counts
        document.getElementById('res-obj-count').textContent = data.total_objects;
        document.getElementById('cnt-good').textContent = data.status_counts.good || 0;
        document.getElementById('cnt-avg').textContent = data.status_counts.average || 0;
        document.getElementById('cnt-bad').textContent = data.status_counts.bad || 0;

        // Dynamic Crops Grid
        const cropsGrid = document.getElementById('crops-grid');
        cropsGrid.innerHTML = '';

        if (data.objects.length === 0) {
            cropsGrid.innerHTML = '<p style="color:var(--text-muted); font-size:13px;">No sanitation objects met the confidence threshold.</p>';
            return;
        }

        data.objects.forEach(obj => {
            const card = document.createElement('div');
            card.className = 'crop-card';

            let rClass = 'count-good';
            if (obj.rating === 'average') rClass = 'count-avg';
            if (obj.rating === 'bad') rClass = 'count-bad';

            card.innerHTML = `
                <div class="crop-img-wrap">
                    <img src="${obj.crop_b64}" alt="${obj.class_name}">
                </div>
                <div class="crop-details">
                    <div class="crop-title">
                        <span>${obj.class_name.replace(/_/g, ' ')}</span>
                        <span class="crop-rating-badge ${rClass}">${obj.rating}</span>
                    </div>
                    <div class="crop-meta">
                        <span>Class Conf: ${(obj.rating_confidence * 100).toFixed(0)}%</span>
                        <span>Det Conf: ${(obj.det_confidence * 100).toFixed(0)}%</span>
                    </div>
                </div>
            `;
            cropsGrid.appendChild(card);
        });
    }

    // ---------------------------------------------------------
    // RUN BATCH TEST SUITE
    // ---------------------------------------------------------
    const btnRunBatch = document.getElementById('btn-run-batch');
    const batchProgress = document.getElementById('batch-progress');
    const batchSummaryCard = document.getElementById('batch-summary-card');
    const batchResultsWrap = document.getElementById('batch-results-wrap');
    const batchGrid = document.getElementById('batch-grid');
    let cachedBatchResults = [];

    btnRunBatch.addEventListener('click', async () => {
        batchProgress.classList.remove('hidden');
        batchSummaryCard.classList.add('hidden');
        batchResultsWrap.classList.add('hidden');

        try {
            const res = await fetch('/api/batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    conf_thresh: confSlider.value,
                    pad: padSlider.value
                })
            });

            const data = await res.json();
            batchProgress.classList.add('hidden');

            if (data.error) {
                alert(`Batch Error: ${data.error}`);
                return;
            }

            renderBatchData(data);
        } catch (err) {
            console.error(err);
            batchProgress.classList.add('hidden');
            alert('Failed to execute batch test suite');
        }
    });

    function renderBatchData(data) {
        batchSummaryCard.classList.remove('hidden');
        batchResultsWrap.classList.remove('hidden');

        const s = data.summary;
        document.getElementById('bstat-total').textContent = s.total_images;
        document.getElementById('bstat-good').textContent = s.good;
        document.getElementById('bstat-avg').textContent = s.average;
        document.getElementById('bstat-bad').textContent = s.bad;
        document.getElementById('bstat-objects').textContent = s.total_objects;

        cachedBatchResults = data.results;
        filterAndRenderBatchGrid('all');
    }

    // Filter Buttons
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterAndRenderBatchGrid(btn.getAttribute('data-filter'));
        });
    });

    function filterAndRenderBatchGrid(filter) {
        batchGrid.innerHTML = '';
        const items = cachedBatchResults.filter(item => {
            if (filter === 'all') return true;
            return item.overall_status.toLowerCase() === filter;
        });

        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'batch-item-card';

            let stClass = 'status-good';
            if (item.overall_status.toLowerCase() === 'average') stClass = 'status-avg';
            if (item.overall_status.toLowerCase() === 'bad') stClass = 'status-bad';

            card.innerHTML = `
                <img src="${item.annotated_b64}" class="batch-thumb" alt="${item.filename}">
                <div class="batch-info">
                    <span class="batch-filename" title="${item.filename}">${item.filename}</span>
                    <div style="display:flex; justify-between; align-items:center; margin-top:4px;">
                        <span class="status-badge ${stClass}" style="font-size:10px; padding:2px 8px;">${item.overall_status}</span>
                        <span style="font-size:11px; color:var(--text-dim);">${item.total_objects} objects</span>
                    </div>
                </div>
            `;
            batchGrid.appendChild(card);
        });
    }

});

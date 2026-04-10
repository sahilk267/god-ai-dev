let currentProjectId = null;
let ws = null;
let currentTrainingMode = 'text';

async function startBuild() {
    const prompt = document.getElementById('prompt').value;
    if (!prompt.trim()) {
        showToast('Please describe your application!', 'error');
        return;
    }

    document.getElementById('buildBtn').disabled = true;
    document.getElementById('buildBtn').textContent = '🔄 Building...';

    try {
        const response = await fetch('/api/build', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-API-Key': 'god_mode_secret_key'
            },
            body: JSON.stringify({ prompt: prompt })
        });

        const data = await response.json();
        currentProjectId = data.project_id;

        // Show logs panel
        document.getElementById('logsPanel').style.display = 'block';
        document.getElementById('logs').innerHTML = '';

        // Connect WebSocket
        connectWebSocket(currentProjectId);

        // Refresh projects list
        refreshProjects();

    } catch (error) {
        console.error('Error:', error);
        showToast('Failed to start build', 'error');
    } finally {
        document.getElementById('buildBtn').disabled = false;
        document.getElementById('buildBtn').textContent = '🚀 Build Application';
    }
}

let wsReconnectDelay = 1000;
let wsGeneration = 0;

function connectWebSocket(projectId) {
    wsGeneration += 1;
    const gen = wsGeneration;

    if (ws) {
        const old = ws;
        ws = null;
        old.onclose = null;
        old.close();
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const socket = new WebSocket(`${protocol}//${window.location.host}/ws/${projectId}`);
    ws = socket;

    socket.onmessage = (event) => {
        if (gen !== wsGeneration) return;
        const data = JSON.parse(event.data);
        if (data.type === 'log') {
            addLog(data.message);
        }
    };

    socket.onerror = (error) => {
        if (gen === wsGeneration) console.error('WebSocket error:', error);
    };

    socket.onclose = (event) => {
        if (gen !== wsGeneration) return;
        ws = null;
        if (currentProjectId !== projectId) return;
        console.log('WebSocket closed. Reconnecting...', event);
        const delay = wsReconnectDelay;
        wsReconnectDelay = Math.min(wsReconnectDelay * 2, 30000);
        setTimeout(() => {
            if (gen !== wsGeneration) return;
            if (currentProjectId !== projectId) return;
            connectWebSocket(projectId);
        }, delay);
    };

    socket.onopen = () => {
        if (gen !== wsGeneration) return;
        wsReconnectDelay = 1000;
    };
}

function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.position = 'fixed';
        container.style.bottom = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.background = type === 'error' ? '#f44336' : '#2196F3';
    toast.style.color = 'white';
    toast.style.padding = '12px 20px';
    toast.style.marginTop = '10px';
    toast.style.borderRadius = '4px';
    toast.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
    toast.style.transition = 'opacity 0.3s';
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function addLog(message) {
    const logsDiv = document.getElementById('logs');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.textContent = message;
    logsDiv.appendChild(logEntry);
    logEntry.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function refreshProjects() {
    try {
        const response = await fetch('/api/projects');
        if (!response.ok) {
            console.warn('refreshProjects: HTTP', response.status, response.statusText);
            return;
        }
        const ct = response.headers.get('content-type') || '';
        if (!ct.includes('application/json')) {
            console.warn('refreshProjects: expected JSON, got', ct);
            return;
        }
        const projects = await response.json();

        const projectsDiv = document.getElementById('projectsList');
        if (projects.length === 0) {
            projectsDiv.innerHTML = '<p>No active projects</p>';
            return;
        }

        projectsDiv.innerHTML = '';
        projects.forEach(id => {
            const card = document.createElement('div');
            card.className = 'project-card';
            card.onclick = () => viewProject(id);
            
            const strong = document.createElement('strong');
            strong.textContent = 'Project: ';
            
            const text = document.createTextNode(id.substring(0, 8) + '...');
            const br = document.createElement('br');
            
            const small = document.createElement('small');
            small.textContent = 'Click to view logs';
            
            const downloadBtn = document.createElement('button');
            downloadBtn.textContent = '📥 Download';
            downloadBtn.className = 'primary-button';
            downloadBtn.style.marginTop = '10px';
            downloadBtn.onclick = (e) => {
                e.stopPropagation();
                window.location.href = `/api/projects/${id}/download`;
            };
            
            card.appendChild(strong);
            card.appendChild(text);
            card.appendChild(br);
            card.appendChild(small);
            card.appendChild(document.createElement('br'));
            card.appendChild(downloadBtn);
            
            projectsDiv.appendChild(card);
        });

    } catch (error) {
        console.error('Error fetching projects:', error);
    }
}

function viewProject(projectId) {
    currentProjectId = projectId;
    document.getElementById('logsPanel').style.display = 'block';
    document.getElementById('logs').innerHTML = '';
    connectWebSocket(projectId);

    // Also fetch status
    fetch(`/api/status/${projectId}`)
        .then(res => res.json())
        .then(status => {
            if (status.logs) {
                status.logs.forEach(log => addLog(log));
            }
        });
}

function toggleTraining() {
    const section = document.getElementById('trainingSection');
    section.style.display = section.style.display === 'none' ? 'block' : 'none';
}

function setTrainingMode(mode) {
    currentTrainingMode = mode;
    document.getElementById('textMode').style.display = mode === 'text' ? 'block' : 'none';
    document.getElementById('urlMode').style.display = mode === 'url' ? 'block' : 'none';
    
    // Toggle active tab class
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.toLowerCase().includes(mode)) btn.classList.add('active');
    });
}

async function trainMasterAgent() {
    let payload = {};
    if (currentTrainingMode === 'text') {
        const logs = document.getElementById('chatLogs').value;
        if (!logs.trim()) {
            showToast('Please paste some chat logs!', 'error');
            return;
        }
        payload.logs = logs;
    } else {
        const url = document.getElementById('chatUrl').value;
        if (!url.trim()) {
            showToast('Please provide a chat link!', 'error');
            return;
        }
        payload.url = url;
    }

    const btn = document.getElementById('startTrainingBtn');
    btn.disabled = true;
    btn.textContent = '🧠 Extracting Patterns...';

    try {
        const response = await fetch('/api/learn', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-API-Key': 'god_mode_secret_key'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (data.success) {
            showToast(`Training complete! Extracted ${data.patterns_extracted} patterns.`, 'info');
            document.getElementById('trainingStats').style.display = 'block';
            document.getElementById('patternCount').textContent = data.patterns_extracted;
            if (currentTrainingMode === 'text') document.getElementById('chatLogs').value = '';
            else document.getElementById('chatUrl').value = '';
        } else {
            showToast(data.detail || 'Training failed', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Failed to train', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = '🔥 Extract Knowledge & Train';
    }
}

// Auto-refresh projects every 5 seconds
setInterval(refreshProjects, 5000);
refreshProjects();
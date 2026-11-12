const API_BASE = 'http://localhost:8000/api';

function getToken() {
  return localStorage.getItem('lab_monitor_token');
}

function setAuthHeader(headers = {}) {
  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: setAuthHeader(options.headers || {}),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Request failed');
  }

  return response.json();
}

async function login(username, password) {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    throw new Error('Invalid credentials');
  }

  const data = await response.json();
  localStorage.setItem('lab_monitor_token', data.access_token);
  localStorage.setItem('lab_monitor_user', JSON.stringify(data.user));
  return data;
}

function renderTable(rows, columns, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  if (!rows.length) {
    target.innerHTML = '<p>No data available.</p>';
    return;
  }

  const table = document.createElement('table');
  const headerRow = document.createElement('tr');
  columns.forEach((column) => {
    const th = document.createElement('th');
    th.textContent = column.label;
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  rows.forEach((row) => {
    const tr = document.createElement('tr');
    columns.forEach((column) => {
      const td = document.createElement('td');
      const value = row[column.key];
      td.textContent = value ?? '—';
      tr.appendChild(td);
    });
    table.appendChild(tr);
  });

  target.innerHTML = '';
  target.appendChild(table);
}

async function loadDashboard() {
  try {
    const data = await apiRequest('/dashboard/summary');
    const summary = data.summary;
    const cards = [
      { label: 'Total computers', value: summary.total_computers },
      { label: 'Active sessions', value: summary.active_sessions },
      { label: 'Online computers', value: summary.online_computers },
      { label: 'Website domains', value: summary.total_web_domains },
    ];

    const container = document.getElementById('summaryCards');
    if (container) {
      container.innerHTML = cards.map((card) => `
        <div class="stat-card">
          <h4>${card.label}</h4>
          <div class="stat-value">${card.value}</div>
        </div>
      `).join('');
    }

    const userBadge = document.getElementById('userBadge');
    if (userBadge) {
      userBadge.textContent = `${data.role} • ${data.username}`;
    }

    const sessionTable = document.getElementById('sessionTable');
    if (sessionTable) {
      try {
        const sessions = await apiRequest('/sessions');
        sessionTable.innerHTML = `
          <table>
            <tr><th>Student</th><th>Computer</th><th>Status</th><th>Login</th><th>Duration</th></tr>
            ${sessions.map((row) => `
              <tr>
                <td>${row.username}</td>
                <td>${row.computer_name ?? 'Unknown'}</td>
                <td>${row.status}</td>
                <td>${row.login_time}</td>
                <td>${row.duration}</td>
              </tr>
            `).join('')}
          </table>
        `;
      } catch (error) {
        sessionTable.innerHTML = '<p>Unable to load sessions.</p>';
      }
    }
  } catch (error) {
    console.error(error);
    window.location.href = 'login.html';
  }
}

async function loadPageData() {
  const route = location.pathname.split('/').pop();
  if (route === 'login.html') {
    attachLoginForm();
    return;
  }

  const token = getToken();
  if (!token) {
    window.location.href = 'login.html';
    return;
  }

  if (route === 'dashboard.html') {
    await loadDashboard();
    return;
  }

  try {
    const sessions = await apiRequest('/sessions');
    const computers = await apiRequest('/computers');
    const applications = await apiRequest('/applications');
    const websites = await apiRequest('/website-activity');

    const renderMap = {
      'students.html': () => renderTable(sessions, [{ label: 'Student', key: 'username' }, { label: 'Status', key: 'status' }, { label: 'Login', key: 'login_time' }], 'studentTable'),
      'computers.html': () => renderTable(computers, [{ label: 'Computer', key: 'computer_name' }, { label: 'Location', key: 'location' }, { label: 'Status', key: 'is_online' }], 'computerTable'),
      'activity-logs.html': () => renderTable(sessions, [{ label: 'Username', key: 'username' }, { label: 'Computer', key: 'computer_name' }, { label: 'Duration', key: 'duration' }], 'activityTable'),
      'application-usage.html': () => renderTable(applications, [{ label: 'App', key: 'app_name' }, { label: 'Start', key: 'start_time' }, { label: 'Duration', key: 'duration' }], 'applicationTable'),
      'website-activity.html': () => renderTable(websites, [{ label: 'Domain', key: 'domain' }, { label: 'Accessed', key: 'accessed_at' }], 'websiteTable'),
      'users.html': () => {
        const userInfo = [{ username: 'admin', role: 'admin' }, { username: 'viewer', role: 'viewer' }];
        renderTable(userInfo, [{ label: 'User', key: 'username' }, { label: 'Role', key: 'role' }], 'userTable');
      },
      'reports.html': () => {
        const reportSummary = document.getElementById('reportSummary');
        if (reportSummary) {
          reportSummary.innerHTML = '<p>CSV export is available for authorized staff users.</p>';
        }
        const exportButton = document.getElementById('exportCsvButton');
        if (exportButton) {
          exportButton.addEventListener('click', () => {
            window.open(`${API_BASE}/reports/export.csv`, '_blank');
          });
        }
      },
    };

    if (renderMap[route]) {
      renderMap[route]();
    }
  } catch (error) {
    console.error(error);
  }
}

function attachLoginForm() {
  const form = document.getElementById('loginForm');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const message = document.getElementById('loginMessage');

    try {
      await login(username, password);
      window.location.href = 'dashboard.html';
    } catch (error) {
      message.textContent = 'Login failed. Check your credentials.';
      message.style.color = '#b91c1c';
    }
  });
}

function attachLogout() {
  const logoutButton = document.getElementById('logoutButton');
  if (!logoutButton) return;
  logoutButton.addEventListener('click', () => {
    localStorage.removeItem('lab_monitor_token');
    window.location.href = 'login.html';
  });
}

attachLogout();
loadPageData();

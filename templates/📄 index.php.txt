<?php
session_start();

// Login check
if (!isset($_SESSION['logged_in']) && basename($_SERVER['PHP_SELF']) != 'login.php') {
    header('Location: login.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Phone Destroyer - 900+ APIs</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            color: #fff;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; padding: 40px 0 20px; }
        .logo {
            font-size: 3.5rem;
            font-weight: bold;
            background: linear-gradient(45deg, #ff0066, #ff6600);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 20px rgba(255,0,102,0.3);
        }
        .subtitle { opacity: 0.8; margin-top: 10px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
            transition: 0.3s;
        }
        .stat-card:hover { transform: translateY(-5px); background: rgba(255,255,255,0.15); }
        .stat-number { font-size: 2.5rem; font-weight: bold; margin-top: 10px; color: #ff6600; }
        .attack-form {
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 40px;
            margin: 40px 0;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .form-title { text-align: center; font-size: 1.8rem; margin-bottom: 30px; }
        input, button {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            border: none;
            border-radius: 15px;
            font-size: 1rem;
        }
        input {
            background: rgba(255,255,255,0.1);
            color: #fff;
            border: 1px solid rgba(255,255,255,0.3);
        }
        input:focus { outline: none; border-color: #ff6600; }
        button {
            background: linear-gradient(45deg, #ff0066, #ff6600);
            color: #fff;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover { transform: scale(1.02); opacity: 0.9; }
        .btn-group { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }
        .logout-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            width: auto;
            padding: 10px 20px;
            background: #ff4757;
            z-index: 100;
        }
        .response-area {
            background: rgba(0,0,0,0.4);
            border-radius: 20px;
            padding: 20px;
            margin-top: 30px;
            max-height: 350px;
            overflow-y: auto;
            font-family: monospace;
        }
        .log-entry { padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 13px; }
        .log-success { color: #2ecc71; }
        .log-error { color: #e74c3c; }
        .log-info { color: #3498db; }
        @media (max-width: 768px) {
            .logo { font-size: 2rem; }
            .btn-group { grid-template-columns: 1fr; }
            .attack-form { padding: 20px; }
        }
        .telegram-box {
            background: rgba(0,0,0,0.4);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            margin-top: 30px;
        }
        .telegram-link {
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(45deg, #0088cc, #006699);
            color: #fff;
            text-decoration: none;
            border-radius: 30px;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <a href="logout.php" class="logout-btn">🚪 Logout</a>
    <div class="container">
        <div class="header">
            <div class="logo">💀 PHONE DESTROYER PRO 💀</div>
            <div class="subtitle">900+ Working APIs | SMS | Call | WhatsApp Bombing</div>
            <div style="margin-top: 15px; color: #2ecc71;">✅ Welcome, <?php echo htmlspecialchars($_SESSION['username'] ?? 'User'); ?></div>
        </div>

        <div class="stats-grid">
            <div class="stat-card"><div>📡 TOTAL APIS</div><div class="stat-number" id="totalApis">0</div></div>
            <div class="stat-card"><div>💣 ACTIVE ATTACKS</div><div class="stat-number" id="activeAttacks">0</div></div>
            <div class="stat-card"><div>✅ SUCCESS HITS</div><div class="stat-number" id="totalHits">0</div></div>
            <div class="stat-card"><div>⏱️ SYSTEM UPTIME</div><div class="stat-number" id="uptime">0</div></div>
        </div>

        <div class="attack-form">
            <div class="form-title">🎯 LAUNCH DESTRUCTION</div>
            <input type="text" id="singlePhone" placeholder="Single Target (10 digits) ex: 9876543210" maxlength="10">
            <input type="text" id="multiPhones" placeholder="Multiple Targets (comma separated) ex: 9876543210,9876543211,9876543212">
            <div class="btn-group">
                <button onclick="attackSingle()">🔥 ATTACK SINGLE</button>
                <button onclick="attackMultiple()" style="background: linear-gradient(45deg, #f39c12, #e67e22);">💣 ATTACK MULTIPLE</button>
                <button onclick="stopAll()" style="background: linear-gradient(45deg, #e74c3c, #c0392b);">🛑 STOP ALL</button>
                <button onclick="getStatus()" style="background: linear-gradient(45deg, #3498db, #2980b9);">📊 GET STATUS</button>
            </div>
        </div>

        <div class="response-area" id="responseArea">
            <div class="log-entry log-info">🚀 System Ready | Password: aniket</div>
            <div class="log-entry log-success">✅ 900+ APIs Loaded Successfully</div>
            <div class="log-entry log-info">💡 Use /bomb 9876543210 on Telegram or use web panel</div>
        </div>

        <div class="telegram-box">
            <h3>🤖 TELEGRAM BOT ACCESS</h3>
            <p>Use our bot on mobile for 24/7 access</p>
            <a href="https://t.me/YourBotUsername" class="telegram-link" target="_blank">📱 OPEN TELEGRAM BOT</a>
            <p style="margin-top: 15px; font-size: 12px;">Commands: /bomb, /multibomb, /stop, /status, /stopall</p>
        </div>
    </div>

    <script>
        setInterval(updateStats, 5000);
        
        function updateStats() {
            fetch('api.php?action=stats')
                .then(r => r.json())
                .then(d => {
                    if(d.status === 'success') {
                        document.getElementById('totalApis').innerText = d.totalApis || 0;
                        document.getElementById('activeAttacks').innerText = d.activeAttacks || 0;
                        document.getElementById('totalHits').innerText = d.totalHits || 0;
                        document.getElementById('uptime').innerText = d.uptime || '0h 0m';
                    }
                }).catch(e => console.log('Stats error'));
        }
        
        function attackSingle() {
            const phone = document.getElementById('singlePhone').value;
            if(!phone || phone.length !== 10 || !/^\d+$/.test(phone)) {
                addLog('❌ Please enter valid 10-digit phone number!', 'error');
                return;
            }
            addLog(`🎯 Launching attack on +91${phone}...`, 'success');
            fetch('api.php', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: 'bomb', phone: phone})
            })
            .then(r => r.json())
            .then(d => {
                if(d.status === 'success') addLog(`✅ Attack started on +91${phone} | Session: ${d.session_id}`, 'success');
                else addLog(`❌ Failed: ${d.message}`, 'error');
            })
            .catch(e => addLog(`❌ Network error: ${e.message}`, 'error'));
        }
        
        function attackMultiple() {
            const phones = document.getElementById('multiPhones').value;
            if(!phones) {
                addLog('❌ Please enter phone numbers!', 'error');
                return;
            }
            addLog(`🎯 Multi-target attack on: ${phones}`, 'success');
            fetch('api.php', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: 'multibomb', phones: phones})
            })
            .then(r => r.json())
            .then(d => {
                if(d.status === 'success') addLog(`✅ Attack started on ${d.count} target(s)`, 'success');
                else addLog(`❌ Failed: ${d.message}`, 'error');
            })
            .catch(e => addLog(`❌ Network error: ${e.message}`, 'error'));
        }
        
        function stopAll() {
            addLog('🛑 Stopping all attacks...', 'info');
            fetch('api.php', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: 'stopall'})
            })
            .then(r => r.json())
            .then(d => {
                if(d.status === 'success') addLog(`✅ ${d.message}`, 'success');
            })
            .catch(e => addLog(`❌ Error: ${e.message}`, 'error'));
        }
        
        function getStatus() {
            fetch('api.php?action=status')
                .then(r => r.json())
                .then(d => {
                    if(d.status === 'success') {
                        addLog(`📊 Active Attacks: ${d.activeAttacks} | Total Hits: ${d.totalHits}`, 'info');
                        if(d.attacks && d.attacks.length > 0) {
                            d.attacks.forEach(a => {
                                addLog(`   📱 +91${a.phone} | Hits: ${a.hits} | Duration: ${a.time}s`, 'success');
                            });
                        } else {
                            addLog(`   📭 No active attacks`, 'info');
                        }
                    }
                })
                .catch(e => addLog(`❌ Error getting status`, 'error'));
        }
        
        function addLog(msg, type) {
            const area = document.getElementById('responseArea');
            const div = document.createElement('div');
            div.className = `log-entry log-${type}`;
            div.innerHTML = `[${new Date().toLocaleTimeString()}] ${msg}`;
            area.insertBefore(div, area.firstChild);
            while(area.children.length > 50) area.removeChild(area.lastChild);
        }
        
        updateStats();
    </script>
</body>
</html>

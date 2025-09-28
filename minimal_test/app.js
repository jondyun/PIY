const logs = document.getElementById('logs');
document.getElementById('sliceBtn').addEventListener('click', async () => {
    const stl = document.getElementById('stl').files[0];
    const layer = document.getElementById('layer').value;
    const infill = document.getElementById('infill').value;
    if (!stl) { logs.textContent = "Choose an STL file"; return; }

    const fd = new FormData();
    fd.append('stlFile', stl);
    fd.append('layerHeight', layer);
    fd.append('infill', infill);

    logs.textContent = "Slicing...";
    try {
        const res = await fetch('/slice', { method:'POST', body: fd });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);
        logs.textContent = `✅ ${data.message}\nDownload: ${data.download_url}`;
    } catch(e) {
        logs.textContent = `❌ ${e.message}`;
    }
});
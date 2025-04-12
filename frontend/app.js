async function callBackend() {
    const res = await fetch("http://127.0.0.1:8000/");
    const data = await res.json();
    document.getElementById("output").textContent = data.message;
  }

  
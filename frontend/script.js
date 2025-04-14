async function sendQuery() {
    const query = document.getElementById("query").value;
    const res = await fetch(`http://localhost:8000/query?q=${query}`);
    const data = await res.json();

    const responseArea = document.getElementById("responseArea");
    if (data.type === "link") {
        responseArea.innerHTML = `🔗 <a href="${data.content}" target="_blank">${data.message}</a>`;
    } else if (data.type === "stats") {
        responseArea.innerHTML = `📊 ${data.content}`;
    } else {
        responseArea.innerHTML = data.content;
    }
}

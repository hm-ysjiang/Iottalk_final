//使用 WebSocket 的網址向 Server 開啟連結
let ws = new WebSocket('ws://140.113.123.205:3000')

ws.onopen = () => {
    console.log('open connection')
}

ws.onclose = () => {
    console.log('close connection')
    document.getElementById('server-msg').textContent = 'Connection closed by remote server'
}

ws.onmessage = evt => {
    data = JSON.parse(evt.data)
    if (data['type'] == "msg")
        document.getElementById('server-msg').textContent = data["msg"]
    else if (data['type'] == "sql-windspeed")
        document.getElementById('sql-wind').textContent = data["value"]
    else if (data['type'] == "sql-winddirection") {
        document.getElementById('sql-windir').style.transform = 'rotate(' + data["value"] + 'deg)'
        console.log('rotate(' + data["value"] + ')deg')
    }
    else if (data['type'] == "sql-visibility")
        document.getElementById('sql-visibility').textContent = data["value"]
}

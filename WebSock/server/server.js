const express = require('express')
const SocketServer = require('ws').Server
const stdio = require('console-read-write')
const mysql = require('mysql')
const fs = require('fs')

const PORT = 3000
const server = express().listen(PORT, () => console.log(`Listening on ${PORT}`))
const wss = new SocketServer({ server })
const db = mysql.createConnection({
    host: 'localhost',
    user: 'iotf',
    password: 'iotthefuck',
    database: 'iotf_final'
})
db.connect()

async function pendAndSendMsg(ws) {
    while (true)
        ws.send(JSON.stringify({ 'type': "msg", 'msg': await stdio.read() }))
}

wss.on('connection', ws => {
    ws.send(JSON.stringify({ 'type': "msg", 'msg': "Connected to the server" }))

    sql_updater = setInterval(() => {
        db.query('select value from windspeed where timestamp = (select MAX(timestamp) from windspeed);',
            (err, res, fields) => {
                if (err)
                    throw err
                ws.send(JSON.stringify({ 'type': "sql-windspeed", 'value': res[0].value }))
            })
        db.query('select value from winddirection where timestamp = (select MAX(timestamp) from winddirection);',
            (err, res, fields) => {
                if (err)
                    throw err
                ws.send(JSON.stringify({ 'type': "sql-winddirection", 'value': res[0].value }))
            })
        db.query('select value from visibility where timestamp = (select MAX(timestamp) from visibility);',
            (err, res, fields) => {
                if (err)
                    throw err
                ws.send(JSON.stringify({ 'type': "sql-visibility", 'value': res[0].value }))
            })
    }, 2000)

    msg_updater = setInterval(() => {
        fs.readFile(__dirname + '/msg', 'utf-8', (err, data) => {
            if (err)
                console.log(err)
            else
                ws.send(JSON.stringify({ 'type': "msg", 'msg': data }))
        })
    }, 5000)

    ws.on('close', () => {
        console.log('Connection closed')
        clearInterval(sql_updater)
    })
})

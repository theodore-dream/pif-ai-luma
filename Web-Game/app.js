const http = require('http');
const express = require('express');
const axios = require('axios');
const ejs = require('ejs');
const path = require('path');

const util = require('util');
console.log = function () {
  process.stdout.write(`${new Date().toISOString()} - `);
  process.stdout.write(util.format.apply(null, arguments) + '\n');
};


const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: true }));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.get('/', async (req, res) => {
  try {
    const choice = 'start'; 
    const session_id = ''; 
    const response = await axios.post(
      'http://app:5000/api/game',
      { choice: choice, session_id: session_id },
      { headers: { 'Content-Type': 'application/json' } }
    );
    res.render('index', { gametext: response.data.gametext, session_id: response.data.session_id });
  } catch (error) {
    console.error('Error occurred while sending request to Flask API:', error);
    res.status(500).send('Something went wrong.');
  }
});


app.post('/api/game', async (req, res) => {
  console.log('Received request to /api/game');
  console.log(req.body);
  const { choice, session_id } = req.body; // Add session_id here
  try {
    console.log('Sending request to Flask API');
    const response = await axios.post(
      'http://app:5000/api/game',
      { choice: choice, session_id: session_id }, // Update this line
      { headers: { 'Content-Type': 'application/json' } }
    );
    console.log('Received response from Flask API');
    res.send(response.data);
  } catch (error) {
    console.error('Error occurred while sending request to Flask API:', error);
    res.status(500).send('Something went wrong.');
  }
});


const server = http.createServer(app);
const port = process.env.PORT || 3000;
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

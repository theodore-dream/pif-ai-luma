const http = require('http');
const express = require('express');
const axios = require('axios');
const ejs = require('ejs');
const path = require('path');

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: true }));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.get('/', (req, res) => {
  res.render('index', { poem: '' });
});

app.post('/submit', async (req, res) => {
  console.log('Received request to /submit');
  console.log(req.body);
  const { input_text, prompt_id } = req.body;
  try {
    console.log('Sending request to Flask API');
    const response = await axios.post(
      'http://app:5000/api/submit-text',
      { input_text: input_text, prompt_id: prompt_id },
      { headers: { 'Content-Type': 'application/json' } }
    );
    console.log('Received response from Flask API');
    res.send(response.data.poem);
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

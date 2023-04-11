const express = require('express');
const { json, urlencoded } = require('body-parser');
const { Remix } = require('@remix-run/express');
const axios = require('axios');

const app = express();
app.use(json());
app.use(urlencoded({ extended: true }));

const remix = new Remix({ build: { manifestDirectory: '/app/build' } });
app.use(remix.middleware());

app.get('/', (req, res) => {
  res.send(
    `
      <!DOCTYPE html>
      <html>
        <head>
          <title>Node.js Docker Example</title>
          <style>
            body {
              font-family: 'Courier New', monospace;
            }
          </style>
        </head>
        <body>
          <h1>Enter some text:</h1>
          <form action="/submit" method="POST">
            <input type="text" name="input_text" />
            <button type="submit">Submit</button>
          </form>
        </body>
      </html>
    `
  );
});

app.post('/submit', async (req, res) => {
  console.log(req.body);
  const { input_text } = req.body;
  try {
    const response = await axios.post(
      'http://app:5000/api/submit-text', 
      { input_text: input_text },
      { headers: { 'Content-Type': 'application/json' } }
    );
    const formattedText = response.data.poem.replace(/\n/g, '<br>');
    res.send(
      `
        <!DOCTYPE html>
        <html>
          <head>
            <title>Formatted Output</title>
            <style>
              body {
                font-family: 'Courier New', monospace;
              }
            </style>
          </head>
          <body>
            ${formattedText}
          </body>
        </html>
      `
    );
  } catch (error) {
    console.error(error);
    res.status(500).send('Something went wrong!');
  }
});

remix.serve();

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
const express = require('express');
const { json, urlencoded } = require('body-parser');
const { Remix } = require('@remix-run/express');
const axios = require('axios');

const app = express();
app.use(json());
app.use(urlencoded({ extended: true }));

const remix = new Remix({ build: { manifestDirectory: '/app/build' } });
app.use(remix.middleware());

app.get('/', (req, res) => {
  res.send(
    `
      <!DOCTYPE html>
      <html>
        <head>
          <title>Node.js Docker Example</title>
          <style>
            body {
              font-family: 'Courier New', monospace;
            }
          </style>
        </head>
        <body>
          <h1>Enter some text:</h1>
          <form action="/submit" method="POST">
            <input type="text" name="input_text" />
            <button type="submit">Submit</button>
          </form>
        </body>
      </html>
    `
  );
});

app.post('/submit', async (req, res) => {
  console.log(req.body);
  const { input_text } = req.body;
  try {
    const response = await axios.post(
      'http://app:5000/api/submit-text', 
      { input_text: input_text },
      { headers: { 'Content-Type': 'application/json' } }
    );
    const formattedText = response.data.poem.replace(/\n/g, '<br>');
    res.send(
      `
        <!DOCTYPE html>
        <html>
          <head>
            <title>Formatted Output</title>
            <style>
              body {
                font-family: 'Courier New', monospace;
              }
            </style>
          </head>
          <body>
            ${formattedText}
          </body>
        </html>
      `
    );
  } catch (error) {
    console.error(error);
    res.status(500).send('Something went wrong!');
  }
});

remix.serve();

app.listen(3000, () => {
  console.log('Server running on port 3000');
});

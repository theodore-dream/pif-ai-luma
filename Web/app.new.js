const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
  <head>
      <title>Node.js Docker Example</title>
      <style>
        body {
          font-family: 'Courier New', monospace;
      }
     </style>
     <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  </head>  
      <body>
        <h1>Enter some text:</h1>
        <form id="submit-form" method="POST" action="/submit">
          <input type="text" name="input_text" />
          <button type="submit">Submit</button>
        </form>
        <div id="result"></div>
        <button onclick="selectPrompt(1)">Poetical Alchemist</button>
        <button onclick="selectPrompt(2)">Talia</button>
        <button onclick="selectPrompt(3)">Prompt 3</button>
        <script>
          let selectedPromptId = 1;

          function selectPrompt(promptId) {
            selectedPromptId = promptId;
          }

          document.getElementById('submit-form').addEventListener('submit', async (event) => {
            event.preventDefault();
            const inputText = document.querySelector('input[name="input_text"]').value;

            try {
              const response = await axios.post(
                'http://app:5000/api/submit-text',
                { input_text: inputText, prompt_id: selectedPromptId },
                { headers: { 'Content-Type': 'application/json' } }
              );

              const formattedText = response.data.poem;
              document.getElementById('result').innerHTML = formattedText.replace(/\\n/g, '<br>');
            } catch (error) {
              console.error(error);
              alert('Something went wrong!');
            }
          });
        </script>
      </body>
    </html>
  `);
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});

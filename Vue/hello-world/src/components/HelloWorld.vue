<template>
  <div class="hello">
    <h1>PIF</h1>
    <div class="input-section">
      <input type="text" v-model="inputText" placeholder="Insert text" />
      <button @click="submitText">Submit</button>
      <div class="display-box">
        <p>{{ displayText }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HelloWorld',
  data() {
    return {
      inputText: '',
      displayText: 'Example',
    };
  },
  methods: {
    async submitText() {
      try {
        const response = await axios.post('http://app:5000/api/submit-text', { input_text: this.inputText });
        this.displayText = response.data.poem;
      } catch (error) {
        console.error('Error submitting text:', error);
      }
    },
  },
};
</script>

<style scoped>
.hello {
  text-align: center;
}

.input-section {
  display: inline-block;
  text-align: left;
}

.display-box {
  width: 300px;
  height: 100px;
  border: 1px solid #000;
  padding: 10px;
  margin-top: 20px;
}
</style>




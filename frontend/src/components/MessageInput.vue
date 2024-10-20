<template>
    <div class="w-full max-w-lg mx-auto mt-4">
      <TextArea
        v-model="message"
        rows="5"
        placeholder="Type your message..."
        class="w-full p-2"
      />
      <button @click="sendMessage" class="btn mt-2">Send</button>
  
      <!-- Display the response from the backend -->
      <div v-if="response" class="mt-4 p-4 rounded">
        <p><strong>Lucian:</strong> {{ response }}</p>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  import TextArea from 'primevue/textarea';
  
  // Register the PrimeVue component
  const message = ref('');
  const response = ref('');
  
  const sendMessage = () => {
    if (!message.value.trim()) {
      return; // Do not send empty messages
    }
  
    // Send the message to the backend
    fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_message: message.value })
    })
      .then(response => response.json())
      .then(data => {
        console.log('Response from backend:', data);
        response.value = data.response;
        message.value = ''; // Clear the input field
      })
      .catch(error => {
        console.error('Error sending message:', error);
      });
  };
  </script>
  
  <style>
  /* Tailwind CSS styles for the send button */
  .btn {
    @apply px-4 py-2 bg-green-500 text-white rounded-lg transition-transform duration-300 hover:scale-110;
  }
  </style>
  
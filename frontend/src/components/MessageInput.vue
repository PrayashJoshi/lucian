<template>
  <div class="flex flex-col items-center">
    <!-- <button @click="startListening" class="btn">Start Listening</button>
    <audio ref="audioPlayer" controls class="mt-4"></audio> -->
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const websocket = new WebSocket("ws://localhost:8000/ws/audio");
const audioPlayer = ref<HTMLAudioElement | null>(null);

websocket.onmessage = (event) => {
  const blob = new Blob([event.data], { type: 'audio/wav' });
  const url = URL.createObjectURL(blob);
  if (audioPlayer.value) {
    audioPlayer.value.src = url;
    audioPlayer.value.play();
  }
};

function startListening() {
  navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    mediaRecorder.ondataavailable = (event) => {
      websocket.send(event.data); // Send audio chunks to the server
    };
  });
}
</script>

<style>
.btn {
  @apply px-4 py-2 bg-green-500 text-white rounded-lg transition-transform duration-300 hover:scale-110;
}
</style>

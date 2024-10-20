<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="flex justify-between items-center p-4">
      <div></div>
      <span class="text-4xl pr-4 pt-2 pacifico-regular">Lucian</span>
    </header>

    <main class="flex-1 flex flex-col items-center justify-center gap-4">
      <LucianFace
        :listening="isListening"
        :talking="isTalking"
        :waiting="isWaiting"
        :hasContent="hasContent"
        @start-listening="startListening"
      >
        <transition name="fade" mode="out-in">
          <component :is="currentContent" :key="currentContentKey" v-if="hasContent" />
        </transition>
      </LucianFace>

      <MessageInput />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import LucianFace from './components/LucianFace.vue';
import MessageInput from './components/MessageInput.vue';

// State Variables
const isListening = ref(false);
const isTalking = ref(false);
const isWaiting = ref(false);
const content = ref(null);

const startListening = () => {
  console.log("Listening started"); // Confirm listening in console
  isListening.value = true;

  // Trigger the backend WebSocket connection or speech-to-text logic
  startSpeechRecognition();
};

// Placeholder function to connect with WebSocket or Deepgram
const startSpeechRecognition = async () => {
  console.log("Connecting to Deepgram...");
  // Connect to backend here and log events
};
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

.pacifico-regular {
  font-family: 'Pacifico', cursive;
  font-weight: 400;
  font-style: normal;
}

.btn {
  @apply px-4 py-2 bg-blue-500 text-white rounded-lg transition-transform duration-300 hover:scale-110;
}

/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="flex justify-between items-center p-4">
      <div></div>
      <span class="text-4xl pr-4 pt-2 pacifico-regular">Lucian</span>
    </header>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col items-center justify-center gap-4">
      <LucianFace
        :listening="isListening"
        :talking="isTalking"
        :waiting="isWaiting"
        :hasContent="hasContent"
      >
        <transition name="fade" mode="out-in">
          <component :is="currentContent" :key="currentContentKey" v-if="hasContent" />
        </transition>
      </LucianFace>

      <!-- Include the MessageInput component -->
      <MessageInput />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import LucianFace from './components/LucianFace.vue';
import ContentOne from './components/tests/content1.vue';
import ContentTwo from './components/tests/content2.vue';
import { ContentTypes, ContentType } from './constants/contentTypes';
import MessageInput from './components/MessageInput.vue'; // Import the new component

// State Variables
const isListening = ref(false);
const isTalking = ref(false);
const isWaiting = ref(false);
const content = ref<ContentType>(ContentTypes.NONE);

// Computed Property for Content Presence
const hasContent = computed(() => content.value !== ContentTypes.NONE);

// Helper Function to Get the Correct Component
const getComponent = (type: ContentType) => {
  switch (type) {
    case ContentTypes.ONE:
      return ContentOne;
    case ContentTypes.TWO:
      return ContentTwo;
    default:
      return null;
  }
};

// Dynamic Content Management
const currentContent = computed(() => getComponent(content.value));
const currentContentKey = ref(0);

// Toggle Functions
const toggleListening = () => (isListening.value = !isListening.value);
const toggleTalking = () => (isTalking.value = !isTalking.value);
const toggleWaiting = () => (isWaiting.value = !isWaiting.value);

const setContent = (type: ContentType) => {
  content.value = type;
  currentContentKey.value++;
};

const clearContent = () => {
  content.value = ContentTypes.NONE;
  currentContentKey.value++;
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

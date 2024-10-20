<template>
  <div
    @click="handleClick"
    :class="[
      'circle-container',
      listening ? 'listening' : '',
      talking ? 'talking' : '',
      waiting ? 'waiting' : '',
      hasContent ? 'adjusting' : ''
    ]"
  >
    <slot></slot>
    <div v-if="waiting" class="spinner"></div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  listening: boolean;
  talking: boolean;
  waiting: boolean;
  hasContent: boolean;
}>();

const emit = defineEmits(['start-listening']);

const handleClick = () => {
  emit('start-listening'); // Trigger the listening event
};
</script>

<style scoped>
/* Circle Animation Styles */
.circle-container {
  width: 90vw;
  max-width: 500px;
  height: 90vw;
  max-height: 500px;
  border-radius: 50%;
  transition: all 0.5s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* Glow Animation When Listening */
.listening {
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.6);
}

/* Spinner Animation */
.spinner {
  width: 20%;
  height: 20%;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top-color: #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

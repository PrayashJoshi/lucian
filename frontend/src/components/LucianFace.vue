<!-- src/components/LucianFace.vue -->
<template>
  <div
    :class="[
      'circle-container',
      listening ? 'listening' : '',
      talking ? 'talking' : '',
      waiting ? 'waiting' : '',
      hasContent ? 'adjusting' : ''
    ]"
  >
    <slot></slot>
    <!-- Spinner for Waiting State -->
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
</script>

<style scoped>
.circle-container {
  width: 90vw;
  max-width: 500px;
  height: 90vw;
  max-height: 500px;
  border-radius: 50%;
  border: 5px solid #555;
  transition: 
    width 0.5s ease-in-out, 
    height 0.5s ease-in-out, 
    border-radius 0.5s ease-in-out, 
    box-shadow 0.5s ease-in-out, 
    border-color 0.5s ease-in-out;
  box-shadow: 0 0 0 rgba(0, 0, 0, 0);
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Glow when listening */
.listening {
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.6);
  border-color: rgb(89, 161, 223);
}

/* Wave animation when talking using pseudo-elements */
.talking::before,
.talking::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 200%;
  height: 200%;
  border-radius: 50%;
  border: 12px solid rgba(215, 123, 251, 0.6);
  transform: translate(-50%, -50%) scale(1);
  animation: wave 1s ease-out infinite;
}

.talking::after {
  animation-delay: 0.1s;
}

@keyframes wave {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.6;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.3);
    opacity: 0.3;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.6);
    opacity: 0;
  }
}

/* Spinner for waiting state */
.spinner {
  position: absolute;
  width: 20%;
  height: 20%;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top-color: #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Spin keyframes */
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Adjust shape for content display */
.adjusting {
  width: 80vw;
  max-width: 600px;
  height: auto;
  max-height: 80vh;
  border-radius: 20px;
  padding: 20px;
  box-sizing: border-box;
}

/* Hide wave animations when adjusting */
.adjusting.talking::before,
.adjusting.talking::after {
  display: none;
}
</style>

<template>
  <div class="star-rating-container">
    <div class="stars" @mouseleave="mouseLeave">
      <div 
        v-for="i in 5" 
        :key="i" 
        class="star-wrapper"
      >
        <span class="star-base">★</span>
        
        <span 
          class="star-filled" 
          :style="{ width: getStarWidth(i) }"
        >★</span>

        <div class="detect-left" @mouseover="mouseOver(i - 0.5)" @click="setRank(i - 0.5)"></div>
        <div class="detect-right" @mouseover="mouseOver(i)" @click="setRank(i)"></div>
      </div>
    </div>
    
    <span class="rank-text">{{ (hoverRank || modelValue || 0).toFixed(1) }} / 5.0</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const hoverRank = ref(0)

// 별 하나당 채워질 너비 계산
const getStarWidth = (i) => {
  const currentRank = hoverRank.value || props.modelValue || 0
  if (currentRank >= i) return '100%'
  if (currentRank === i - 0.5) return '50%'
  return '0%'
}

const setRank = (rank) => {
  emit('update:modelValue', rank)
}

const mouseOver = (rank) => {
  hoverRank.value = rank
}

const mouseLeave = () => {
  hoverRank.value = 0
}
</script>

<style scoped>
.star-rating-container {
  display: flex;
  align-items: center;
  gap: 15px;
  user-select: none;
}

.stars {
  display: flex;
  position: relative;
}

.star-wrapper {
  position: relative;
  font-size: 2.5rem; /* 별 크기 조정 */
  width: 2.5rem;
  height: 2.5rem;
  line-height: 1;
}

/* 기본 회색 별 */
.star-base {
  color: #dee2e6;
  position: absolute;
  top: 0;
  left: 0;
}

/* 채워지는 노란색 별 */
.star-filled {
  color: #ffc107;
  position: absolute;
  top: 0;
  left: 0;
  overflow: hidden;
  white-space: nowrap;
  width: 0;
  transition: width 0.1s;
}

/* 감지 구역 (투명) */
.detect-left, .detect-right {
  position: absolute;
  top: 0;
  width: 50%;
  height: 100%;
  z-index: 2;
  cursor: pointer;
}
.detect-left { left: 0; }
.detect-right { left: 50%; }

.rank-text {
  font-size: 1.3rem;
  font-weight: bold;
  color: #ffc107;
  min-width: 80px;
}
</style>
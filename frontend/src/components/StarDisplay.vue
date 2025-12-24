<template>
  <div class="star-display">
    <div v-for="i in 5" :key="i" class="star-wrapper">
      <span class="star-base">★</span>
      <span 
        class="star-filled" 
        :style="{ width: getStarWidth(i) }"
      >★</span>
    </div>
    <span v-if="showScore" class="score-text ms-1">{{ rating.toFixed(1) }}</span>
  </div>
</template>

<script setup>
const props = defineProps({
  rating: { type: Number, default: 0 }, // 5점 만점 기준 점수
  showScore: { type: Boolean, default: true } // 옆에 숫자 점수도 보여줄지 여부
})

const getStarWidth = (i) => {
  const diff = props.rating - (i - 1)
  if (diff >= 1) return '100%'
  if (diff >= 0.5) return '50%'
  return '0%'
}
</script>

<style scoped>
.star-display {
  display: flex;
  align-items: center;
}
.star-wrapper {
  position: relative;
  font-size: 1.2rem; /* 카드 크기에 맞춰 조절 가능 */
  width: 1.2rem;
  height: 1.2rem;
  line-height: 1;
}
.star-base {
  color: #dee2e6;
  position: absolute;
  top: 0; left: 0;
}
.star-filled {
  color: #ffc107;
  position: absolute;
  top: 0; left: 0;
  overflow: hidden;
  white-space: nowrap;
  width: 0;
}
.score-text {
  font-size: 0.9rem;
  color: #ffc107;
  font-weight: bold;
}
</style>
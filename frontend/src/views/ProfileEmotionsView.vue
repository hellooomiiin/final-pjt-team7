<template>
  <div class="profile-emotions-container">
    <div class="container">
      <div class="mb-4">
        <button @click="$router.push('/profile')" class="btn btn-outline-secondary">
          ← 뒤로가기
        </button>
      </div>
      <div class="alert alert-info">
        <h2>감정 분석 기록</h2>
        <p>이 페이지는 준비 중입니다.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileEmotionsView'
}
</script>

<style scoped>
.profile-emotions-container {
  min-height: calc(100vh - 80px);
  padding: 3rem 0;
}

.alert-info {
  background-color: #ffffff;
  border: 1px solid #000000;
  color: #000000;
  padding: 2rem;
  text-align: center;
}

.btn-outline-secondary {
  border: 1px solid #000000;
  color: #000000;
  background-color: #ffffff;
}

.btn-outline-secondary:hover {
  background-color: #000000;
  color: #ffffff;
}
</style>


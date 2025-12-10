<template>
  <div class="container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="!student" class="empty-state">
      <h3>学生不存在</h3>
    </div>
    <div v-else>
      <div class="card">
        <h1>为 {{ student.name }} 评分</h1>
        
        <div class="student-info-card">
          <p><strong>学校：</strong>{{ student.school_name }}</p>
          <p><strong>年级：</strong>{{ student.grade }}</p>
        </div>

        <form @submit.prevent="handleSubmit">
          <div class="input-group">
            <label>评分等级</label>
            <div class="rating-options">
              <label 
                v-for="(label, score) in ratingLabels" 
                :key="score"
                :class="['rating-option', { active: form.score === parseInt(score) }]"
                @click="form.score = parseInt(score)"
              >
                <input 
                  type="radio" 
                  :value="parseInt(score)" 
                  v-model="form.score" 
                  required
                />
                <span :class="['rating-badge', `rating-${score}`]">{{ label }}</span>
              </label>
            </div>
          </div>

          <div class="input-group">
            <label>评论（可选）</label>
            <textarea 
              v-model="form.comment" 
              placeholder="写下你的评价..."
              rows="5"
            ></textarea>
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>
          <div v-if="success" class="success-message">{{ success }}</div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary">提交评分</button>
            <router-link :to="`/student/${student.id}`" class="btn btn-secondary">取消</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const dataStore = useDataStore()
const authStore = useAuthStore()

const student = ref(null)
const loading = ref(true)
const error = ref('')
const success = ref('')

const form = ref({
  score: null,
  comment: ''
})

const ratingLabels = {
  5: '夯',
  4: '顶级',
  3: '人上人',
  2: 'NPC',
  1: '拉完了'
}

onMounted(() => {
  loadStudent()
})

function loadStudent() {
  const studentId = route.params.id
  student.value = dataStore.students.find(s => s.id === studentId)
  loading.value = false
}

function handleSubmit() {
  error.value = ''
  success.value = ''
  
  if (!form.value.score) {
    error.value = '请选择评分等级'
    return
  }

  // 检查是否已经评分过
  const existingRating = dataStore.ratings.find(
    r => r.rater_id === authStore.currentUser.id && r.target_id === student.value.id
  )
  
  if (existingRating) {
    error.value = '您已经为该同学评分过了'
    return
  }

  const rating = {
    rater_id: authStore.currentUser.id,
    rater_name: authStore.currentUser.name,
    target_id: student.value.id,
    target_name: student.value.name,
    score: form.value.score,
    comment: form.value.comment
  }

  dataStore.addRating(rating)
  success.value = '评分提交成功！'
  
  setTimeout(() => {
    router.push(`/student/${student.value.id}`)
  }, 1500)
}
</script>

<style scoped>
.student-info-card {
  background: rgba(0, 0, 0, 0.3);
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
}

.student-info-card p {
  margin: 8px 0;
  color: #fff;
}

.rating-options {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
}

.rating-option {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  color: #fff;
  position: relative;
}

.rating-option:hover {
  border-color: rgba(255, 255, 255, 0.7);
  background: rgba(255, 255, 255, 0.1);
}

.rating-option.active {
  border-color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.15);
}

.rating-option input[type="radio"] {
  margin-right: 8px;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  background: transparent;
  position: relative;
  outline: none;
  flex-shrink: 0;
}

.rating-option input[type="radio"]:focus {
  outline: none;
  box-shadow: none;
}

.rating-option input[type="radio"]:checked {
  border-color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.2);
}

.rating-option input[type="radio"]:checked::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #fff;
}

.rating-badge {
  display: inline-flex;
  align-items: center;
  line-height: 1;
  white-space: nowrap;
}

.error-message {
  color: #fff;
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(220, 53, 69, 0.25);
  border-radius: 6px;
}

.success-message {
  color: #fff;
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(40, 167, 69, 0.25);
  border-radius: 6px;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.form-actions .btn {
  flex: 1;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}
</style>


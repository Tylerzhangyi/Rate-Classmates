<template>
  <div class="container">
    <div :class="['card', { 'card--compact': !filtersExpanded }]">
      <div class="card-header">
        <div>
          <h1>{{ schoolName || '学生列表' }}</h1>
          <router-link to="/schools" class="back-link" v-if="schoolId">
            <i class="fas fa-arrow-left"></i> 返回评分大厅
          </router-link>
        </div>
        <button @click="toggleFilters" class="filter-toggle-btn">
          <i :class="['fas', filtersExpanded ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
          <span>{{ filtersExpanded ? '收起筛选' : '展开筛选' }}</span>
        </button>
      </div>
      
      <!-- 搜索和筛选 -->
      <div v-show="filtersExpanded" class="filters">
        <div class="filter-row">
          <div class="input-group" style="flex: 1;">
            <label>年级</label>
            <input v-model.number="filters.grade" type="number" placeholder="如：2021" />
          </div>
          <div class="input-group" style="flex: 1;">
            <label>姓名搜索</label>
            <input v-model="filters.name" type="text" placeholder="输入姓名搜索" />
          </div>
          <div class="input-group" style="flex: 1;">
            <label>平均分区间</label>
            <div style="display: flex; gap: 10px;">
              <input v-model.number="filters.min_score" type="number" placeholder="最低分" step="0.1" />
              <span style="line-height: 40px;">-</span>
              <input v-model.number="filters.max_score" type="number" placeholder="最高分" step="0.1" />
            </div>
          </div>
        </div>
        <div class="filter-row">
          <div class="input-group">
            <label>排序方式</label>
            <select v-model="sortBy">
              <option value="avg_score">按平均分</option>
              <option value="rating_count">按评分数量</option>
              <option value="name">按姓名</option>
              <option value="score">按评分</option>
            </select>
          </div>
          <div class="input-group">
            <label>排序顺序</label>
            <select v-model="sortOrder">
              <option value="desc">降序</option>
              <option value="asc">升序</option>
            </select>
          </div>
          <div class="input-group input-group--action">
            <label>&nbsp;</label>
            <button @click="resetFilters" class="btn btn-secondary action-button">重置</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 学生列表 -->
    <div class="students-list">
      <div 
        v-for="(student, index) in filteredStudents" 
        :key="student.id" 
        :class="['student-item', 'fade-in-item', { top3: index < 3 }]"
        :style="{ animationDelay: `${index * 0.05}s` }"
      >
        <div class="rank">
          <i v-if="index === 0" class="fas fa-medal rank-icon rank-gold"></i>
          <i v-else-if="index === 1" class="fas fa-medal rank-icon rank-silver"></i>
          <i v-else-if="index === 2" class="fas fa-medal rank-icon rank-bronze"></i>
          <span v-else class="rank-number">{{ index + 1 }}</span>
        </div>
        <div class="entry-info">
          <div class="entry-name">{{ student.name }}</div>
          <div class="entry-details">
            <span>{{ student.school_name }}</span>
            <span>{{ student.grade }}级</span>
          </div>
        </div>
        <div class="entry-stats">
          <div class="stat-item">
            <span class="stat-label">平均分</span>
            <span class="stat-value">{{ student.avg_score || '0' }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">评分数</span>
            <span class="stat-value">{{ student.rating_count }}</span>
          </div>
          <div class="rating-badge-container">
            <span :class="['rating-badge', `rating-${student.dominant_rating}`]">
              {{ getRatingLabel(student.dominant_rating) }}
            </span>
          </div>
        </div>
        <div class="entry-actions">
          <button class="btn btn-secondary btn-sm" @click="goStudent(student.id)">查看</button>
          <button class="btn btn-primary btn-sm" @click="goRate(student.id)">评分</button>
        </div>
      </div>
    </div>

    <div v-if="filteredStudents.length === 0" class="empty-state">
      <h3>暂无学生数据</h3>
      <p>请调整筛选条件或添加新学生</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'

const route = useRoute()
const router = useRouter()
const dataStore = useDataStore()

const schoolId = computed(() => route.params.schoolId || null)
const schools = ref([])
const filtersExpanded = ref(false)
const filters = ref({
  grade: null,
  name: '',
  min_score: null,
  max_score: null
})

const sortBy = ref('avg_score')
const sortOrder = ref('desc')

const schoolName = computed(() => {
  if (!schoolId.value) return null
  const school = dataStore.schools.find(s => s.id === schoolId.value)
  return school ? school.school_name : null
})

onMounted(async () => {
  await dataStore.loadInitial()
  schools.value = dataStore.schools
})

function toggleFilters() {
  filtersExpanded.value = !filtersExpanded.value
}

const filteredStudents = computed(() => {
  let result = [...dataStore.students]
  
  // 如果指定了学校ID，只显示该学校的学生
  if (schoolId.value) {
    result = result.filter(s => s.school_id === schoolId.value)
  }
  
  // 应用筛选
  if (filters.value.grade) {
    result = result.filter(s => s.grade === filters.value.grade)
  }
  if (filters.value.name) {
    result = result.filter(s => 
      s.name.toLowerCase().includes(filters.value.name.toLowerCase())
    )
  }
  if (filters.value.min_score !== null) {
    result = result.filter(s => parseFloat(s.avg_score) >= filters.value.min_score)
  }
  if (filters.value.max_score !== null) {
    result = result.filter(s => parseFloat(s.avg_score) <= filters.value.max_score)
  }
  
  // 排序
  result.sort((a, b) => {
    let aVal, bVal
    if (sortBy.value === 'avg_score') {
      aVal = parseFloat(a.avg_score) || 0
      bVal = parseFloat(b.avg_score) || 0
    } else if (sortBy.value === 'rating_count') {
      aVal = a.rating_count || 0
      bVal = b.rating_count || 0
    } else if (sortBy.value === 'score') {
      aVal = a.dominant_rating || 0
      bVal = b.dominant_rating || 0
    } else {
      aVal = a.name
      bVal = b.name
    }
    
    if (sortOrder.value === 'desc') {
      return typeof aVal === 'string' ? bVal.localeCompare(aVal) : bVal - aVal
    } else {
      return typeof aVal === 'string' ? aVal.localeCompare(bVal) : aVal - bVal
    }
  })
  
  return result
})

function getRatingLabel(score) {
  const labels = {
    5: '夯',
    4: '顶级',
    3: '人上人',
    2: 'NPC',
    1: '拉完了'
  }
  return labels[score] || '暂无'
}

function getStudentBadges(studentId) {
  return dataStore.studentBadges.filter(b => b.student_id === studentId)
}

function goStudent(studentId) {
  router.push(`/student/${studentId}`)
}

function goRate(studentId) {
  router.push(`/rate/${studentId}`)
}

function resetFilters() {
  filters.value = {
    grade: null,
    name: '',
    min_score: null,
    max_score: null
  }
  sortBy.value = 'avg_score'
  sortOrder.value = 'desc'
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h1 {
  margin: 0;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s;
}

.back-link:hover {
  color: #fff;
  transform: translateX(-4px);
}

.filter-toggle-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 1);
  border-radius: 8px;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.filter-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2);
}

.card--compact {
  margin-bottom: 12px;
  padding-bottom: 12px;
}

.filters {
  margin-top: 20px;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.filter-row .input-group {
  flex: 1;
}

.input-group--action {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.input-group--action label {
  visibility: hidden;
  margin-bottom: 8px;
}

.action-button {
  width: auto;
  align-self: flex-start;
  padding: 8px 20px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.8);
  color: #fff;
}

.students-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 20px;
}

.student-item {
  display: grid;
  grid-template-columns: 60px 1fr auto auto;
  gap: 20px;
  align-items: center;
  padding: 20px;
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  transition: all 0.3s;
}

.student-item:hover {
  border-color: rgba(255, 255, 255, 0.7);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
}

.student-item.top3 {
  background: transparent;
}

.students-list .student-item:first-child {
  border-color: #FFD700;
  border-width: 3px;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
}

.students-list .student-item:nth-child(2) {
  border-color: #C0C0C0;
  border-width: 3px;
  box-shadow: 0 0 15px rgba(192, 192, 192, 0.4);
}

.students-list .student-item:nth-child(3) {
  border-color: #CD7F32;
  border-width: 3px;
  box-shadow: 0 0 15px rgba(205, 127, 50, 0.4);
}

.rank {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #fff;
}

.rank-icon {
  font-size: 32px;
  display: inline-block;
}

.rank-gold {
  color: #FFD700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
}

.rank-silver {
  color: #C0C0C0;
  text-shadow: 0 0 10px rgba(192, 192, 192, 0.6);
}

.rank-bronze {
  color: #CD7F32;
  text-shadow: 0 0 10px rgba(205, 127, 50, 0.6);
}

.rank-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  color: #fff;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.8);
  margin: 0 auto;
  font-size: 18px;
  font-weight: bold;
}

.entry-info {
  flex: 1;
}

.entry-name {
  font-size: 18px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 8px;
}

.entry-details {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #fff;
}

.entry-stats {
  display: flex;
  gap: 24px;
  align-items: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 12px;
  color: #fff;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
}

.rating-badge-container {
  margin-left: 16px;
}

.entry-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  align-items: center;
}

.entry-actions .btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.8);
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 38px;
  padding: 0 18px;
  cursor: pointer;
}

.btn-sm {
  padding: 0 18px;
  font-size: 12px;
}
</style>


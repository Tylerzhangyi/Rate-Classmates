<template>
  <div class="container">
    <div :class="['card', { 'card--compact': !filtersExpanded }]">
      <div class="card-header">
        <h1>学生列表</h1>
        <button @click="toggleFilters" class="filter-toggle-btn">
          <i :class="['fas', filtersExpanded ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
          <span>{{ filtersExpanded ? '收起筛选' : '展开筛选' }}</span>
        </button>
      </div>
      
      <!-- 搜索和筛选 -->
      <div v-show="filtersExpanded" class="filters">
        <div class="filter-row">
          <div class="input-group" style="flex: 1;">
            <label>学校</label>
            <select v-model="filters.school_id">
              <option value="">全部学校</option>
              <option v-for="school in schools" :key="school.id" :value="school.id">
                {{ school.school_name }}
              </option>
            </select>
          </div>
          <div class="input-group" style="flex: 1;">
            <label>年级</label>
            <input v-model.number="filters.grade" type="number" placeholder="如：2021" />
          </div>
        </div>
        <div class="filter-row">
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
    <div class="students-grid">
      <div v-for="student in filteredStudents" :key="student.id" class="student-card">
        <div class="student-header">
          <h3>{{ student.name }}</h3>
          <span :class="['rating-badge', `rating-${student.dominant_rating}`]">
            {{ getRatingLabel(student.dominant_rating) }}
          </span>
        </div>
        <div class="student-info">
          <p><strong>学校：</strong>{{ student.school_name }}</p>
          <p><strong>年级：</strong>{{ student.grade }}</p>
          <p><strong>平均分：</strong>{{ student.avg_score || '暂无' }}</p>
          <p><strong>评分数量：</strong>{{ student.rating_count }}</p>
          <p>
            <strong>徽章：</strong>
            <template v-if="getStudentBadges(student.id).length">
              <span class="badge-chip" v-for="badge in getStudentBadges(student.id)" :key="badge.id">
                {{ badge.badge_name || badge.name }}
              </span>
            </template>
            <span v-else class="badge-chip badge-chip--empty">暂无徽章</span>
          </p>
        </div>
        <div class="student-actions">
          <router-link :to="`/student/${student.id}`" class="btn btn-secondary">查看详情</router-link>
          <router-link :to="`/rate/${student.id}`" class="btn btn-primary">评分</router-link>
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
import { ref, computed, onMounted } from 'vue'
import { useDataStore } from '../stores/data'

const dataStore = useDataStore()

const schools = ref([])
const filtersExpanded = ref(false)
const filters = ref({
  school_id: '',
  grade: null,
  name: '',
  min_score: null,
  max_score: null
})

const sortBy = ref('avg_score')
const sortOrder = ref('desc')

onMounted(async () => {
  await dataStore.loadInitial()
  schools.value = dataStore.schools
})

function toggleFilters() {
  filtersExpanded.value = !filtersExpanded.value
}

const filteredStudents = computed(() => {
  let result = [...dataStore.students]
  
  // 应用筛选
  if (filters.value.school_id) {
    result = result.filter(s => s.school_id === filters.value.school_id)
  }
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

function resetFilters() {
  filters.value = {
    school_id: '',
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

.students-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.student-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s, box-shadow 0.3s;
}

.student-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

.student-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.student-header h3 {
  margin: 0;
  color: #fff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.student-info {
  margin-bottom: 16px;
}

.student-info p {
  margin: 8px 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.badge-chip {
  display: inline-block;
  padding: 4px 8px;
  margin-right: 6px;
  margin-bottom: 4px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  font-size: 12px;
}

.badge-chip--empty {
  opacity: 0.7;
}

.student-actions {
  display: flex;
  gap: 10px;
}

.student-actions .btn {
  flex: 1;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.8);
  color: #fff;
}
</style>


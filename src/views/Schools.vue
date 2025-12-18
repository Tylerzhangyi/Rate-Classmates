<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <h1>评分大厅</h1>
        <p class="description">选择学校查看该学校的学生</p>
      </div>
      
      <!-- 搜索和排序 -->
      <div class="search-sort-bar">
        <div class="search-box">
          <i class="fas fa-search search-icon"></i>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="搜索学校名称..."
            class="search-input"
          />
        </div>
        <div class="sort-options">
          <label>排序：</label>
          <select v-model="sortBy">
            <option value="name">按首字母</option>
            <option value="count">按学生数量</option>
            <option value="score">按平均分</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 学校列表 -->
    <div v-if="dataStore.loading" class="loading-state">
      <p>加载中...</p>
    </div>
    <div v-else class="schools-list">
      <div 
        v-for="(school, index) in filteredAndSortedSchools" 
        :key="school.id" 
        class="school-item fade-in-item"
        :style="{ animationDelay: `${index * 0.05}s` }"
        @click="goToSchool(school.id)"
      >
        <div class="school-icon">
          <i class="fas fa-school"></i>
        </div>
        <div class="school-info">
          <div class="school-name">{{ school.school_name }}</div>
          <div class="school-stats">
            <span class="stat-item">
              <i class="fas fa-users"></i>
              {{ getSchoolStudentCount(school.id) }} 名学生
            </span>
          </div>
        </div>
        <div class="school-score">
          <div class="score-label">平均分</div>
          <div class="score-value">{{ getSchoolAvgScore(school.id) }}</div>
        </div>
        <div class="school-arrow">
          <i class="fas fa-chevron-right"></i>
        </div>
      </div>
    </div>

    <div v-if="filteredAndSortedSchools.length === 0" class="empty-state">
      <h3>暂无学校数据</h3>
      <p>请先添加学校</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'

const router = useRouter()
const dataStore = useDataStore()

const schools = ref([])
const searchQuery = ref('')
const sortBy = ref('name')

onMounted(async () => {
  try {
    await dataStore.loadInitial()
    schools.value = dataStore.schools || []
  } catch (error) {
    console.error('Failed to load schools:', error)
    schools.value = []
  }
})

function getSchoolStudentCount(schoolId) {
  return dataStore.students.filter(s => s.school_id === schoolId).length
}

function getSchoolAvgScore(schoolId) {
  // 只统计有评分的学生（rating_count > 0）
  const schoolStudents = dataStore.students.filter(s => 
    s.school_id === schoolId && (s.rating_count > 0 || parseFloat(s.avg_score) > 0)
  )
  if (schoolStudents.length === 0) return '0.00'
  const totalScore = schoolStudents.reduce((sum, s) => sum + (parseFloat(s.avg_score) || 0), 0)
  const avg = totalScore / schoolStudents.length
  return avg.toFixed(2)
}

function getFirstLetter(str) {
  const firstChar = str.charAt(0).toUpperCase()
  if (/[A-Z]/.test(firstChar)) {
    return firstChar
  }
  if (/[0-9]/.test(firstChar)) {
    return '#'
  }
  // 中文字符，返回拼音首字母（简化处理，实际可以使用拼音库）
  return firstChar
}

const filteredAndSortedSchools = computed(() => {
  let result = [...schools.value]
  
  // 搜索过滤
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    result = result.filter(school => 
      school.school_name.toLowerCase().includes(query)
    )
  }
  
  // 排序
  if (sortBy.value === 'name') {
    result.sort((a, b) => {
      const aLetter = getFirstLetter(a.school_name)
      const bLetter = getFirstLetter(b.school_name)
      if (aLetter === bLetter) {
        return a.school_name.localeCompare(b.school_name, 'zh-CN')
      }
      return aLetter.localeCompare(bLetter)
    })
  } else if (sortBy.value === 'count') {
    result.sort((a, b) => {
      const aCount = getSchoolStudentCount(a.id)
      const bCount = getSchoolStudentCount(b.id)
      return bCount - aCount
    })
  } else if (sortBy.value === 'score') {
    result.sort((a, b) => {
      const aScore = parseFloat(getSchoolAvgScore(a.id))
      const bScore = parseFloat(getSchoolAvgScore(b.id))
      return bScore - aScore
    })
  }
  
  return result
})

function goToSchool(schoolId) {
  router.push(`/school/${schoolId}/students`)
}
</script>

<style scoped>
.description {
  color: rgba(255, 255, 255, 0.8);
  margin-top: 8px;
  font-size: 14px;
}

.card-header {
  margin-bottom: 20px;
}

.search-sort-bar {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.search-box {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 12px 10px 36px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: #fff;
  font-size: 14px;
  transition: all 0.3s;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.8);
  background: rgba(0, 0, 0, 0.4);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2);
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-options label {
  color: #fff;
  font-size: 14px;
}

.sort-options select {
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.3);
  color: #fff;
  font-size: 14px;
  cursor: pointer;
}

.schools-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 20px;
}

.school-item {
  display: grid;
  grid-template-columns: 60px 1fr auto auto;
  gap: 20px;
  align-items: center;
  padding: 20px;
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  transition: all 0.3s;
  cursor: pointer;
}

.school-item:hover {
  border-color: rgba(255, 255, 255, 0.7);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
  transform: translateX(4px);
}

.school-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  background: rgba(102, 126, 234, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
  flex-shrink: 0;
}

.school-info {
  flex: 1;
}

.school-name {
  font-size: 18px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 8px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.school-stats {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-item i {
  font-size: 12px;
}

.school-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
}

.score-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 4px;
}

.score-value {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
}

.school-arrow {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s;
  flex-shrink: 0;
}

.school-item:hover .school-arrow {
  color: #fff;
  transform: translateX(4px);
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.8);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.8);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.empty-state h3 {
  margin-bottom: 10px;
  color: #fff;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}
</style>


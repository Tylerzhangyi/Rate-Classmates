<template>
  <div class="container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="!student" class="empty-state">
      <h3>学生不存在</h3>
    </div>
    <div v-else>
      <!-- 学生信息卡片 -->
      <div class="card">
        <div class="student-profile">
          <div class="profile-header">
            <h1>{{ student.name }}</h1>
            <span :class="['rating-badge', `rating-${student.dominant_rating}`]">
              {{ getRatingLabel(student.dominant_rating) }}
            </span>
          </div>
          <div class="profile-info">
            <div class="info-item">
              <strong>学校：</strong>{{ student.school_name }}
            </div>
            <div class="info-item">
              <strong>年级：</strong>{{ student.grade }}
            </div>
            <div class="info-item">
              <strong>平均分：</strong>{{ student.avg_score || '暂无' }}
            </div>
            <div class="info-item">
              <strong>评分数量：</strong>{{ student.rating_count }}
            </div>
          <div class="info-item">
            <strong>徽章：</strong>
            <template v-if="badges.length">
              <span class="badge-chip" v-for="badge in badges" :key="badge.id">
                {{ badge.badge_name || badge.name }}
              </span>
            </template>
            <span v-else class="badge-chip badge-chip--empty">暂无徽章</span>
          </div>
          </div>
          <div class="profile-actions">
            <router-link :to="`/rate/${student.id}`" class="btn btn-primary">评分</router-link>
            <router-link to="/schools" class="btn btn-secondary">返回评分大厅</router-link>
          </div>
        </div>
      </div>

      <!-- 评分趋势图 -->
      <div class="card" v-if="comments.length > 0">
        <h2>评分趋势</h2>
        <div class="chart-container">
          <Line :data="chartData" :options="chartOptions" />
        </div>
      </div>

      <!-- 评论列表 -->
      <div class="card">
        <h2>评论列表</h2>
        <div class="comments-header">
          <div class="sort-options">
            <label>排序方式：</label>
            <select v-model="commentSortBy">
              <option value="time">按时间</option>
              <option value="score">按评分</option>
            </select>
            <select v-model="commentSortOrder">
              <option value="desc">降序</option>
              <option value="asc">升序</option>
            </select>
          </div>
        </div>
        <div v-if="comments.length === 0" class="empty-state">
          <p>暂无评论</p>
        </div>
        <div v-else class="comments-list">
          <div v-for="(comment, index) in sortedComments" :key="comment.id" class="comment-item fade-in-item" :style="{ animationDelay: `${index * 0.1}s` }">
            <div class="comment-header">
              <div class="comment-author">
                <strong>匿名用户</strong>
                <span :class="['rating-badge', `rating-${comment.score}`]" style="margin-left: 8px;">
                  {{ getRatingLabel(comment.score) }}
                </span>
              </div>
              <div class="comment-time">
                {{ formatTime(comment.created_at) }}
              </div>
            </div>
            <div class="comment-content">
              {{ comment.comment || '（无评论内容）' }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDataStore } from '../stores/data'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const route = useRoute()
const dataStore = useDataStore()

const student = ref(null)
const comments = ref([])
const loading = ref(true)
const commentSortBy = ref('time')
const commentSortOrder = ref('desc')

const badges = computed(() => {
  if (!student.value) return []
  return dataStore.studentBadges.filter(b => b.student_id === student.value.id)
})

// 图表数据
const chartData = computed(() => {
  if (!comments.value || comments.value.length === 0) {
    return {
      labels: [],
      datasets: []
    }
  }

  // 按时间排序（从早到晚）
  const sortedRatings = [...comments.value].sort((a, b) => {
    return new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
  })

  // 准备图表数据
  const labels = sortedRatings.map(rating => {
    const date = new Date(rating.created_at)
    return `${date.getMonth() + 1}/${date.getDate()}`
  })

  const scores = sortedRatings.map(rating => rating.score)

  return {
    labels,
    datasets: [
      {
        label: '评分',
        data: scores,
        borderColor: 'rgba(102, 126, 234, 1)',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        borderWidth: 2,
        pointRadius: 4,
        pointBackgroundColor: 'rgba(102, 126, 234, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        tension: 0.4,
        fill: true
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: 'rgba(255, 255, 255, 0.2)',
      borderWidth: 1,
      padding: 12,
      displayColors: true,
      callbacks: {
        label: function(context) {
          const score = context.parsed.y
          const labels = {
            5: '夯',
            4: '顶级',
            3: '人上人',
            2: 'NPC',
            1: '拉完了'
          }
          return `${context.dataset.label}: ${score} (${labels[score] || '未知'})`
        }
      }
    }
  },
  scales: {
    x: {
      grid: {
        color: 'rgba(255, 255, 255, 0.1)',
        drawBorder: false
      },
      ticks: {
        color: '#fff',
        font: {
          size: 11
        }
      }
    },
    y: {
      min: 0,
      max: 5,
      grid: {
        color: 'rgba(255, 255, 255, 0.1)',
        drawBorder: false
      },
      ticks: {
        color: '#fff',
        font: {
          size: 11
        },
        stepSize: 1,
        callback: function(value) {
          const labels = {
            5: '夯',
            4: '顶级',
            3: '人上人',
            2: 'NPC',
            1: '拉完了'
          }
          return labels[value] || value
        }
      }
    }
  }
}

onMounted(async () => {
  await dataStore.loadInitial()
  await loadStudent()
})

async function loadStudent() {
  const studentId = route.params.id
  student.value = await dataStore.fetchStudentById(studentId)
  await Promise.all([
    dataStore.fetchStudentRatings(studentId),
    dataStore.fetchStudentBadges(studentId)
  ])
  comments.value = dataStore.getStudentRatings(studentId)
  loading.value = false
}

const sortedComments = computed(() => {
  const sorted = [...comments.value]
  sorted.sort((a, b) => {
    if (commentSortBy.value === 'time') {
      const aTime = new Date(a.created_at).getTime()
      const bTime = new Date(b.created_at).getTime()
      return commentSortOrder.value === 'desc' ? bTime - aTime : aTime - bTime
    } else {
      return commentSortOrder.value === 'desc' 
        ? b.score - a.score 
        : a.score - b.score
    }
  })
  return sorted
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

function formatTime(timeString) {
  const date = new Date(timeString)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.student-profile {
  max-width: 800px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
}

.profile-header h1 {
  margin: 0;
  color: #fff;
}

.profile-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.info-item {
  padding: 12px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  color: #fff;
}

.badge-chip {
  display: inline-block;
  padding: 4px 8px;
  margin-right: 6px;
  margin-top: 6px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  font-size: 12px;
}

.badge-chip--empty {
  opacity: 0.7;
}

.profile-actions {
  display: flex;
  gap: 12px;
}

.profile-actions .btn {
  text-decoration: none;
  display: inline-block;
}

.comments-header {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.sort-options {
  display: flex;
  gap: 12px;
  align-items: center;
}

.sort-options select {
  padding: 6px 12px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.3);
  color: #fff;
}

.comments-list {
  margin-top: 20px;
}

.comment-item {
  padding: 16px;
  margin-bottom: 16px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border-left: 4px solid #667eea;
  transition: all 0.3s ease;
}

.comment-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  border-left-width: 6px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.comment-author {
  display: flex;
  align-items: center;
}

.comment-time {
  color: #fff;
  font-size: 12px;
}

.comment-content {
  color: #fff;
  line-height: 1.6;
}

.chart-container {
  height: 300px;
  margin-top: 20px;
  position: relative;
}
</style>


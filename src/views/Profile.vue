<template>
  <div class="container">
    <div class="card">
      <h1>个人中心</h1>
      
      <!-- 个人信息 -->
      <div class="profile-section">
        <h2>个人信息</h2>
        <div class="profile-info">
          <div class="info-item">
            <strong>姓名：</strong>{{ currentUser.name }}
          </div>
          <div class="info-item">
            <strong>账号：</strong>{{ currentUser.account }}
          </div>
          <div class="info-item">
            <strong>学校：</strong>{{ currentUser.school_name }}
          </div>
          <div class="info-item">
            <strong>年级：</strong>{{ currentUser.grade }}
          </div>
          <div class="info-item">
            <strong>班级：</strong>{{ currentUser.class_no }}
          </div>
        </div>
      </div>

      <!-- 我的统计 -->
      <div class="profile-section">
        <h2>我的统计</h2>
        <div v-if="myStats" class="stats-grid">
          <div class="stat-card">
            <div class="stat-value">{{ myStats.avg_score || '暂无' }}</div>
            <div class="stat-label">平均分</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ myStats.rating_count || 0 }}</div>
            <div class="stat-label">收到评分</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ myStats.dominant_rating_label || '暂无' }}</div>
            <div class="stat-label">主要等级</div>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>暂无统计数据</p>
        </div>
      </div>

      <!-- 我的徽章 -->
      <div class="profile-section">
        <h2>我的徽章</h2>
        <div v-if="myBadges.length === 0" class="empty-state">
          <p>暂无徽章</p>
        </div>
        <div v-else class="badges-grid">
          <div v-for="badge in myBadges" :key="badge.id" class="badge-card">
            <div class="badge-icon">🏆</div>
            <div class="badge-info">
              <div class="badge-name">{{ badge.badge_name }}</div>
              <div class="badge-period">{{ badge.period }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 我给出的评分 -->
      <div class="profile-section">
        <h2>我给出的评分</h2>
        <div v-if="myRatings.length === 0" class="empty-state">
          <p>暂无评分记录</p>
        </div>
        <div v-else class="ratings-list">
          <div v-for="rating in myRatings" :key="rating.id" class="rating-item">
            <div class="rating-header">
              <div class="rating-target">
                <strong>{{ rating.target_name }}</strong>
                <span :class="['rating-badge', `rating-${rating.score}`]">
                  {{ getRatingLabel(rating.score) }}
                </span>
              </div>
              <div class="rating-time">
                {{ formatTime(rating.created_at) }}
              </div>
            </div>
            <div class="rating-comment" v-if="rating.comment">
              {{ rating.comment }}
            </div>
            <div class="rating-actions">
              <router-link :to="`/student/${rating.target_id}`" class="btn-link">查看详情</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useDataStore } from '../stores/data'

const authStore = useAuthStore()
const dataStore = useDataStore()

const currentUser = computed(() => authStore.currentUser)

const myStats = computed(() => {
  const student = dataStore.students.find(s => s.id === currentUser.value.id)
  if (!student) return null
  
  return {
    ...student,
    dominant_rating_label: getRatingLabel(student.dominant_rating)
  }
})

const myBadges = computed(() => {
  return dataStore.studentBadges.filter(b => b.student_id === currentUser.value.id)
})

const myRatings = computed(() => {
  return dataStore.ratings.filter(r => r.rater_id === currentUser.value.id)
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
.profile-section {
  margin-bottom: 40px;
  padding-bottom: 40px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.profile-section:last-child {
  border-bottom: none;
}

.profile-section h2 {
  margin-bottom: 20px;
  color: #fff;
}

.profile-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.info-item {
  padding: 16px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  color: #fff;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
}

.stat-card {
  background: transparent;
  color: #fff;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.6);
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.badge-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border-left: 4px solid #ffa94d;
}

.badge-icon {
  font-size: 32px;
}

.badge-name {
  font-weight: bold;
  color: #fff;
  margin-bottom: 4px;
}

.badge-period {
  font-size: 12px;
  color: #fff;
}

.ratings-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.rating-item {
  padding: 16px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.rating-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.rating-target {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rating-time {
  font-size: 12px;
  color: #fff;
}

.rating-comment {
  color: #fff;
  line-height: 1.6;
  margin-bottom: 12px;
}

.rating-actions {
  margin-top: 8px;
}

.btn-link {
  color: #fff;
  text-decoration: underline;
  font-size: 14px;
  font-weight: 500;
}
</style>


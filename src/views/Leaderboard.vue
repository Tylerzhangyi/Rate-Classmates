<template>
  <div class="container">
    <div class="card">
      <h1>排行榜</h1>
      
      <div class="leaderboard-tabs">
        <button 
          :class="['tab-btn', { active: activeTab === 'all' }]"
          @click="activeTab = 'all'"
        >
          综合榜
        </button>
        <button 
          :class="['tab-btn', { active: activeTab === 'school' }]"
          @click="activeTab = 'school'"
        >
          学校榜
        </button>
      </div>

      <div class="period-selector">
        <label>周期：</label>
        <select v-model="period">
          <option value="all">全部</option>
          <option value="week">本周</option>
          <option value="month">本月</option>
          <option value="quarter">本季度</option>
        </select>
      </div>

      <!-- 综合榜 -->
      <div v-if="activeTab === 'all'" class="leaderboard-content">
        <h2>Top 10 综合排行榜</h2>
        <div v-if="allLeaderboard.length === 0" class="empty-state">
          <p>暂无数据</p>
        </div>
        <div v-else class="leaderboard-list">
          <div 
            v-for="(entry, index) in allLeaderboard" 
            :key="entry.id"
            :class="['leaderboard-item', { top3: index < 3 }]"
          >
            <div class="rank">
              <i v-if="index === 0" class="fas fa-medal rank-icon rank-gold"></i>
              <i v-else-if="index === 1" class="fas fa-medal rank-icon rank-silver"></i>
              <i v-else-if="index === 2" class="fas fa-medal rank-icon rank-bronze"></i>
              <span v-else class="rank-number">{{ index + 1 }}</span>
            </div>
            <div class="entry-info">
              <div class="entry-name">{{ entry.name }}</div>
              <div class="entry-details">
                <span>{{ entry.school_name }}</span>
                <span>{{ entry.grade }}级</span>
              </div>
            </div>
            <div class="entry-stats">
              <div class="stat-item">
                <span class="stat-label">平均分</span>
                <span class="stat-value">{{ entry.avg_score }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">评分数</span>
                <span class="stat-value">{{ entry.rating_count }}</span>
              </div>
              <div class="rating-badge-container">
                <span :class="['rating-badge', `rating-${entry.dominant_rating}`]">
                  {{ getRatingLabel(entry.dominant_rating) }}
                </span>
              </div>
            </div>
            <div class="entry-actions">
              <router-link :to="`/student/${entry.id}`" class="btn btn-secondary btn-sm">查看</router-link>
              <router-link :to="`/rate/${entry.id}`" class="btn btn-primary btn-sm">评分</router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- 学校榜 -->
      <div v-if="activeTab === 'school'" class="leaderboard-content">
        <h2>Top 10 学校排行榜</h2>
        <div v-if="schoolLeaderboard.length === 0" class="empty-state">
          <p>暂无数据</p>
        </div>
        <div v-else class="leaderboard-list">
          <div 
            v-for="(entry, index) in schoolLeaderboard" 
            :key="entry.school_id"
            :class="['leaderboard-item', { top3: index < 3 }]"
          >
            <div class="rank">
              <i v-if="index === 0" class="fas fa-medal rank-icon rank-gold"></i>
              <i v-else-if="index === 1" class="fas fa-medal rank-icon rank-silver"></i>
              <i v-else-if="index === 2" class="fas fa-medal rank-icon rank-bronze"></i>
              <span v-else class="rank-number">{{ index + 1 }}</span>
            </div>
            <div class="entry-info">
              <div class="entry-name">{{ entry.school_name }}</div>
              <div class="entry-details">
                <span>{{ entry.students.length }} 名学生</span>
              </div>
            </div>
            <div class="entry-stats">
              <div class="stat-item">
                <span class="stat-label">学校平均分</span>
                <span class="stat-value">{{ entry.avg_score }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useDataStore } from '../stores/data'

const dataStore = useDataStore()

const activeTab = ref('all')
const period = ref('all')

const allLeaderboard = computed(() => {
  return dataStore.getLeaderboard('all', period.value)
})

const schoolLeaderboard = computed(() => {
  return dataStore.getLeaderboard('school', period.value)
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
</script>

<style scoped>
.leaderboard-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  color: #fff;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

.tab-btn:hover {
  border-bottom-color: rgba(255, 255, 255, 0.5);
}

.tab-btn.active {
  color: #fff;
  border-bottom-color: rgba(255, 255, 255, 0.8);
}

.period-selector {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.period-selector select {
  padding: 8px 16px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.3);
  color: #fff;
}

.leaderboard-content h2 {
  margin-bottom: 20px;
  color: #fff;
}

.leaderboard-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.leaderboard-item {
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

.leaderboard-item:hover {
  border-color: rgba(255, 255, 255, 0.7);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
}

.leaderboard-item.top3 {
  background: transparent;
}

.leaderboard-list .leaderboard-item:first-child {
  border-color: #FFD700;
  border-width: 3px;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
}

.leaderboard-list .leaderboard-item:nth-child(2) {
  border-color: #C0C0C0;
  border-width: 3px;
  box-shadow: 0 0 15px rgba(192, 192, 192, 0.4);
}

.leaderboard-list .leaderboard-item:nth-child(3) {
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
}

.btn-sm {
  padding: 0 18px;
  font-size: 12px;
}
</style>


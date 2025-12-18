<template>
  <div class="container">
    <div class="card">
      <!-- 管理员审核页面 -->
      <template v-if="authStore.isAdmin">
        <h1>审核学校申请</h1>
        <p class="description">审核待处理的学校申请，可以选择批准或拒绝。</p>
        
        <div v-if="pendingApplications.length === 0" class="empty-state">
          <p>暂无待审核的申请</p>
        </div>
        
        <div v-else class="applications-list">
          <div 
            v-for="application in pendingApplications" 
            :key="application.id"
            class="application-item"
          >
            <div class="application-header">
              <h3>{{ application.school_name }}</h3>
              <span :class="['status-badge', `status-${application.status}`]">
                {{ getStatusText(application.status) }}
              </span>
            </div>
            
            <div class="application-details">
              <div class="detail-row">
                <span class="detail-label">申请人ID：</span>
                <span class="detail-value">{{ application.applicant_id }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">联系方式：</span>
                <span class="detail-value">{{ application.contact }}</span>
              </div>
              <div class="detail-row" v-if="application.reason">
                <span class="detail-label">申请理由：</span>
                <span class="detail-value">{{ application.reason }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">申请时间：</span>
                <span class="detail-value">{{ formatDate(application.created_at) }}</span>
              </div>
            </div>
            
            <div class="application-actions">
              <button 
                @click="handleApprove(application.id)" 
                class="btn btn-success"
                :disabled="processing"
              >
                <i class="fas fa-check"></i> 批准
              </button>
              <button 
                @click="handleReject(application.id)" 
                class="btn btn-danger"
                :disabled="processing"
              >
                <i class="fas fa-times"></i> 拒绝
              </button>
            </div>
          </div>
        </div>
        
        <!-- 已处理的申请 -->
        <div v-if="processedApplications.length > 0" class="processed-section">
          <h2>已处理的申请</h2>
          <div class="applications-list">
            <div 
              v-for="application in processedApplications" 
              :key="application.id"
              class="application-item processed"
            >
              <div class="application-header">
                <h3>{{ application.school_name }}</h3>
                <span :class="['status-badge', `status-${application.status}`]">
                  {{ getStatusText(application.status) }}
                </span>
              </div>
              <div class="application-details">
                <div class="detail-row">
                  <span class="detail-label">申请人ID：</span>
                  <span class="detail-value">{{ application.applicant_id }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">处理时间：</span>
                  <span class="detail-value">{{ formatDate(application.updated_at || application.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
      
      <!-- 普通用户申请页面 -->
      <template v-else>
        <h1>申请添加学校</h1>
        <p class="description">如果您所在的学校不在列表中，可以提交申请添加新学校。我们会在审核后添加您的学校。</p>
        
        <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label>学校名称 <span class="required">*</span></label>
          <input 
            type="text" 
            v-model="form.school_name" 
            placeholder="请输入学校全称"
            required
          />
        </div>

        <div class="input-group">
          <label>联系方式 <span class="required">*</span></label>
          <input 
            type="text" 
            v-model="form.contact" 
            placeholder="请输入邮箱或手机号"
            required
          />
        </div>

        <div class="input-group">
          <label>申请理由</label>
          <textarea 
            v-model="form.reason" 
            placeholder="请简要说明申请添加该学校的理由（可选）"
            rows="5"
          ></textarea>
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="success" class="success-message">{{ success }}</div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? '提交中...' : '提交申请' }}
          </button>
          <router-link to="/schools" class="btn btn-secondary">取消</router-link>
        </div>
      </form>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const dataStore = useDataStore()
const authStore = useAuthStore()

const form = ref({
  school_name: '',
  contact: '',
  reason: ''
})

const error = ref('')
const success = ref('')
const submitting = ref(false)
const processing = ref(false)

// 获取待审核的申请
const pendingApplications = computed(() => {
  return dataStore.getSchoolApplications('pending')
})

// 获取已处理的申请
const processedApplications = computed(() => {
  const all = dataStore.getSchoolApplications()
  return all.filter(app => app.status !== 'pending').slice(0, 10)
})

onMounted(async () => {
  await dataStore.loadInitial()
  await dataStore.fetchSchoolApplications()
})

function handleSubmit() {
  error.value = ''
  success.value = ''
  submitting.value = true

  // 验证学校名称是否已存在
  const existingSchool = dataStore.schools.find(
    s => s.school_name.toLowerCase() === form.value.school_name.toLowerCase().trim()
  )

  if (existingSchool) {
    error.value = '该学校已存在于系统中'
    submitting.value = false
    return
  }

  // 检查是否已经提交过相同学校的申请
  const existingApplication = dataStore.schoolApplications.find(
    app => app.school_name.toLowerCase() === form.value.school_name.toLowerCase().trim() &&
           app.status === 'pending'
  )

  if (existingApplication) {
    error.value = '您已经提交过该学校的申请，请等待审核'
    submitting.value = false
    return
  }

  const application = {
    school_name: form.value.school_name.trim(),
    contact: form.value.contact,
    reason: form.value.reason || '',
    status: 'pending'
  }

  dataStore.createSchoolApplication(application)
  success.value = '申请提交成功！我们会在审核后通知您。'
  
  // 重置表单
  form.value = {
    school_name: '',
    contact: '',
    reason: ''
  }

  submitting.value = false

  setTimeout(() => {
    router.push('/schools')
  }, 2000)
}

// 管理员审核功能
function handleApprove(applicationId) {
  processing.value = true
  dataStore.updateSchoolApplicationStatus(applicationId, 'approved').then(() => {
    success.value = '申请已批准，学校已添加到系统中'
    return dataStore.fetchSchoolApplications()
  }).finally(() => {
    processing.value = false
    setTimeout(() => { success.value = '' }, 3000)
  })
}

function handleReject(applicationId) {
  processing.value = true
  dataStore.updateSchoolApplicationStatus(applicationId, 'rejected').then(() => {
    success.value = '申请已拒绝'
    return dataStore.fetchSchoolApplications()
  }).finally(() => {
    processing.value = false
    setTimeout(() => { success.value = '' }, 3000)
  })
}

function getStatusText(status) {
  const statusMap = {
    pending: '待审核',
    approved: '已批准',
    rejected: '已拒绝'
  }
  return statusMap[status] || status
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.description {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 24px;
  line-height: 1.6;
}

.required {
  color: #ff6b6b;
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

.form-actions .btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 审核页面样式 */
.applications-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 24px;
}

.application-item {
  background: rgba(0, 0, 0, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s;
}

.application-item:hover {
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.application-item.processed {
  opacity: 0.7;
}

.application-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.application-header h3 {
  margin: 0;
  color: #fff;
  font-size: 20px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-pending {
  background: rgba(255, 193, 7, 0.3);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.5);
}

.status-approved {
  background: rgba(40, 167, 69, 0.3);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.5);
}

.status-rejected {
  background: rgba(220, 53, 69, 0.3);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.5);
}

.application-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.detail-row {
  display: flex;
  align-items: flex-start;
}

.detail-label {
  color: rgba(255, 255, 255, 0.7);
  min-width: 100px;
  font-weight: 500;
}

.detail-value {
  color: #fff;
  flex: 1;
}

.application-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.btn-success {
  background: #28a745;
  color: white;
  border: 1px solid #28a745;
}

.btn-success:hover {
  background: #218838;
  border-color: #1e7e34;
}

.btn-danger {
  background: #dc3545;
  color: white;
  border: 1px solid #dc3545;
}

.btn-danger:hover {
  background: #c82333;
  border-color: #bd2130;
}

.processed-section {
  margin-top: 40px;
  padding-top: 24px;
  border-top: 2px solid rgba(255, 255, 255, 0.2);
}

.processed-section h2 {
  margin-bottom: 20px;
  color: #fff;
  font-size: 20px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: rgba(255, 255, 255, 0.7);
}
</style>


<template>
  <div class="container">
    <div class="card">
      <!-- 管理员审核页面 -->
      <template v-if="authStore.isAdmin">
        <h1>审核学生申请</h1>
        <p class="description">审核待处理的学生档案申请，可以选择批准或拒绝。</p>

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
              <h3>{{ application.student_name }}（{{ application.school_name }}）</h3>
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
                <span class="detail-label">学校：</span>
                <span class="detail-value">{{ application.school_name }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">年级：</span>
                <span class="detail-value">{{ application.grade }}</span>
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
                <h3>{{ application.student_name }}（{{ application.school_name }}）</h3>
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
        <h1>申请添加学生档案</h1>
        <p class="description">若列表中没有你想评价的同学，可提交申请添加学生档案。</p>

        <form @submit.prevent="handleSubmit">
          <div class="input-group">
            <label>学生姓名 <span class="required">*</span></label>
            <input
              type="text"
              v-model="form.student_name"
              placeholder="请输入学生姓名"
              required
            />
          </div>

          <div class="input-group">
            <label>学校 <span class="required">*</span></label>
            <select v-model="form.school_id" required>
              <option value="">请选择学校</option>
              <option v-for="school in schools" :key="school.id" :value="school.id">
                {{ school.school_name }}
              </option>
            </select>
          </div>

          <div class="input-group">
            <label>年级 <span class="required">*</span></label>
            <input
              type="number"
              v-model.number="form.grade"
              placeholder="如：2023"
              required
            />
          </div>

          <div class="input-group">
            <label>申请理由</label>
            <textarea
              v-model="form.reason"
              placeholder="请简要说明申请原因（可选）"
              rows="4"
            ></textarea>
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>
          <div v-if="success" class="success-message">{{ success }}</div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? '提交中...' : '提交申请' }}
            </button>
            <router-link to="/students" class="btn btn-secondary">取消</router-link>
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
  student_name: '',
  school_id: '',
  grade: null,
  reason: ''
})

const error = ref('')
const success = ref('')
const submitting = ref(false)
const processing = ref(false)
const schools = ref([])

const pendingApplications = computed(() => dataStore.getStudentApplications('pending'))
const processedApplications = computed(() => {
  const all = dataStore.getStudentApplications()
  return all.filter(app => app.status !== 'pending').slice(0, 10)
})

onMounted(async () => {
  await dataStore.loadInitial()
  schools.value = dataStore.schools
  await dataStore.fetchStudentApplications()
})

function handleSubmit() {
  error.value = ''
  success.value = ''
  submitting.value = true

  const selectedSchool = dataStore.schools.find(s => s.id === form.value.school_id)
  if (!selectedSchool) {
    error.value = '请选择学校'
    submitting.value = false
    return
  }

  // 检查重复申请
  const existingApplication = dataStore.getStudentApplications('pending').find(
    app =>
      app.student_name === form.value.student_name &&
      app.school_id === form.value.school_id &&
      app.grade === form.value.grade
  )
  if (existingApplication) {
    error.value = '已提交过该学生档案的申请，请等待审核'
    submitting.value = false
    return
  }

  // 检查学生是否已存在
  const exists = dataStore.students.find(
    s =>
      s.name === form.value.student_name &&
      s.school_id === form.value.school_id &&
      s.grade === form.value.grade
  )
  if (exists) {
    error.value = '该学生档案已存在'
    submitting.value = false
    return
  }

  const application = {
    applicant_id: authStore.currentUser.id,
    student_name: form.value.student_name,
    school_id: form.value.school_id,
    school_name: selectedSchool.school_name,
    grade: form.value.grade,
    reason: form.value.reason || '',
    status: 'pending'
  }

  dataStore.createStudentApplication(application)
  success.value = '申请提交成功！审核通过后会添加该学生档案。'
  form.value = {
    student_name: '',
    school_id: '',
    grade: null,
    reason: ''
  }
  submitting.value = false
}

function handleApprove(id) {
  processing.value = true
  dataStore.updateStudentApplicationStatus(id, 'approved').then(() => {
    return dataStore.fetchStudentApplications()
  }).finally(() => {
    processing.value = false
  })
}

function handleReject(id) {
  processing.value = true
  dataStore.updateStudentApplicationStatus(id, 'rejected').then(() => {
    return dataStore.fetchStudentApplications()
  }).finally(() => {
    processing.value = false
  })
}

function getStatusText(status) {
  const map = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return map[status] || status
}

function formatDate(time) {
  return new Date(time).toLocaleString('zh-CN')
}
</script>

<style scoped>
.description {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 16px;
}

.input-group,
.input-row {
  margin-bottom: 16px;
}

.input-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #fff;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.3);
  color: #fff;
}

.form-actions {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-top: 12px;
}

.applications-list {
  display: grid;
  gap: 16px;
}

.application-item {
  background: rgba(0, 0, 0, 0.3);
  padding: 16px;
  border-radius: 10px;
  border-left: 4px solid #667eea;
}

.application-item.processed {
  border-left-color: #6c757d;
}

.application-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.application-details {
  display: grid;
  gap: 8px;
  margin-bottom: 12px;
}

.detail-row {
  display: flex;
  gap: 6px;
  color: #fff;
}

.detail-label {
  color: rgba(255, 255, 255, 0.8);
}

.status-badge {
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  color: #fff;
}

.status-pending {
  background: #ffc107;
}

.status-approved {
  background: #28a745;
}

.status-rejected {
  background: #dc3545;
}

.btn {
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary {
  background: #667eea;
  color: #fff;
}

.btn-secondary {
  background: transparent;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.5);
  text-decoration: none;
  text-align: center;
  padding: 10px 16px;
  border-radius: 8px;
}

.btn-success {
  background: #28a745;
  color: #fff;
}

.btn-danger {
  background: #dc3545;
  color: #fff;
}

.error-message {
  padding: 12px;
  background: rgba(220, 53, 69, 0.25);
  border-radius: 6px;
  color: #fff;
  margin-bottom: 10px;
}

.success-message {
  padding: 12px;
  background: rgba(40, 167, 69, 0.25);
  border-radius: 6px;
  color: #fff;
  margin-bottom: 10px;
}

.required {
  color: #ff6b6b;
}
</style>


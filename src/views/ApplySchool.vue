<template>
  <div class="container">
    <div class="card">
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
          <label>申请人姓名 <span class="required">*</span></label>
          <input 
            type="text" 
            v-model="form.applicant_name" 
            placeholder="请输入您的姓名"
            required
          />
        </div>

        <div class="input-group">
          <label>申请人学号/账号 <span class="required">*</span></label>
          <input 
            type="text" 
            v-model="form.applicant_account" 
            placeholder="请输入您的学号或账号"
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
          <router-link to="/students" class="btn btn-secondary">取消</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const dataStore = useDataStore()
const authStore = useAuthStore()

const form = ref({
  school_name: '',
  applicant_name: '',
  applicant_account: '',
  contact: '',
  reason: ''
})

const error = ref('')
const success = ref('')
const submitting = ref(false)

onMounted(() => {
  // 自动填充当前用户信息
  if (authStore.currentUser) {
    form.value.applicant_name = authStore.currentUser.name || ''
    form.value.applicant_account = authStore.currentUser.account || ''
  }
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
    applicant_id: authStore.currentUser.id,
    applicant_name: form.value.applicant_name,
    applicant_account: form.value.applicant_account,
    school_name: form.value.school_name.trim(),
    contact: form.value.contact,
    reason: form.value.reason || '',
    status: 'pending'
  }

  dataStore.addSchoolApplication(application)
  success.value = '申请提交成功！我们会在审核后通知您。'
  
  // 重置表单
  form.value = {
    school_name: '',
    applicant_name: authStore.currentUser.name || '',
    applicant_account: authStore.currentUser.account || '',
    contact: '',
    reason: ''
  }

  submitting.value = false

  setTimeout(() => {
    router.push('/students')
  }, 2000)
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
</style>


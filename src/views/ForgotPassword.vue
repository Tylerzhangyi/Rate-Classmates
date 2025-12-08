<template>
  <section class="forgot-password section">
    <div class="forgot-password__container container grid">
      <div class="forgot-password__content grid">
        <div class="forgot-password__data">
          <h1 class="forgot-password__title">忘记密码</h1>
          <p class="forgot-password__description">请输入您的账号，我们将帮您重置密码</p>
        </div>

        <form @submit.prevent="handleForgotPassword" class="forgot-password__form">
          <div class="forgot-password__inputs">
            <div class="forgot-password__box">
              <input 
                v-model="form.account" 
                type="text" 
                required 
                placeholder="账号（学号或邮箱）"
                class="forgot-password__input forgot-password__input-with-icon"
              />
              <i class="fas fa-user forgot-password__input-icon"></i>
            </div>
          </div>

          <div v-if="error" class="forgot-password__error">
            {{ error }}
          </div>

          <div v-if="success" class="forgot-password__success">
            {{ success }}
          </div>

          <button type="submit" class="forgot-password__button button" :disabled="loading">
            {{ loading ? '处理中...' : '发送重置链接' }}
          </button>

          <div class="forgot-password__back">
            <router-link to="/login" class="forgot-password__link">
              <i class="fas fa-arrow-left"></i> 返回登录
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  account: ''
})

const error = ref('')
const success = ref('')
const loading = ref(false)

function handleForgotPassword() {
  error.value = ''
  success.value = ''
  loading.value = true

  // 模拟发送重置密码链接
  setTimeout(() => {
    const user = authStore.users.find(u => 
      u.account === form.value.account || u.account.includes(form.value.account)
    )
    
    if (user) {
      success.value = '重置密码链接已发送到您的邮箱，请查收！'
      loading.value = false
      // 3秒后返回登录页
      setTimeout(() => {
        router.push('/login')
      }, 3000)
    } else {
      error.value = '未找到该账号，请检查账号是否正确'
      loading.value = false
    }
  }, 1500)
}
</script>

<style scoped>
/*=============== FORGOT PASSWORD ===============*/
.forgot-password {
  position: relative;
  height: 100vh;
  display: grid;
  align-items: center;
}

.forgot-password__container {
  position: relative;
  height: 100vh;
  display: grid;
  align-items: center;
}

.forgot-password__content {
  row-gap: 3rem;
}

.forgot-password__data {
  text-align: center;
}

.forgot-password__title {
  font-size: 2.5rem;
  color: #fff;
  margin-bottom: 1rem;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.forgot-password__description {
  margin-bottom: 2.5rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.forgot-password__form {
  display: grid;
  row-gap: 1.5rem;
}

.forgot-password__inputs {
  display: grid;
  row-gap: 1.5rem;
  margin-bottom: 1rem;
}

.forgot-password__box {
  position: relative;
  display: flex;
  align-items: center;
}

.forgot-password__input {
  width: 100%;
  background: transparent;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 1);
  border-radius: 1rem;
  padding: 1.25rem 1.875rem;
  color: #fff;
  font-weight: 500;
  transition: border-color 0.4s, background-color 0.4s;
  outline: none;
}

.forgot-password__input-with-icon {
  padding-right: 3.5rem;
}

.forgot-password__input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.forgot-password__input:focus {
  border-color: rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 0.05);
}

.forgot-password__input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.forgot-password__input-icon {
  position: absolute;
  right: 1.25rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  pointer-events: none;
  transition: color 0.4s;
}

.forgot-password__input:focus + .forgot-password__input-icon {
  color: rgba(255, 255, 255, 1);
}

.forgot-password__error {
  padding: 0.875rem 1.25rem;
  background: rgba(220, 53, 69, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(220, 53, 69, 0.4);
  border-radius: 0.75rem;
  color: #fff;
  font-size: 0.875rem;
  text-align: center;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.forgot-password__success {
  padding: 0.875rem 1.25rem;
  background: rgba(40, 167, 69, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(40, 167, 69, 0.4);
  border-radius: 0.75rem;
  color: #fff;
  font-size: 0.875rem;
  text-align: center;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.forgot-password__button {
  width: 100%;
  padding: 1.25rem;
  border-radius: 1rem;
  background: transparent;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 1);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s;
  font-size: 1rem;
}

.forgot-password__button:hover:not(:disabled) {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
}

.forgot-password__button:active:not(:disabled) {
  transform: translateY(0);
}

.forgot-password__button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.forgot-password__back {
  text-align: center;
  margin-top: 1.5rem;
}

.forgot-password__link {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.forgot-password__link:hover {
  color: #fff;
  text-shadow: 0 1px 3px rgba(255, 255, 255, 0.5);
}

.forgot-password__link i {
  font-size: 0.875rem;
}

/*=============== BREAKPOINTS ===============*/
/* For small devices */
@media screen and (max-width: 340px) {
  .forgot-password__container {
    padding-inline: 1rem;
  }

  .forgot-password__title {
    font-size: 2rem;
  }
}

/* For medium devices */
@media screen and (min-width: 576px) {
  .forgot-password__form {
    width: 400px;
    justify-self: center;
  }
}

/* For large devices */
@media screen and (min-width: 1024px) {
  .forgot-password__content {
    grid-template-columns: 1fr 1fr;
    align-items: center;
    column-gap: 4rem;
  }

  .forgot-password__data {
    text-align: initial;
  }

  .forgot-password__title {
    margin-inline: 0 5rem;
  }

  .forgot-password__description {
    margin-inline: 0 5rem;
  }
}
</style>


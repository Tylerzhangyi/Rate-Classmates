<template>
  <section class="register section">
    <div class="register__container container grid">
      <div class="register__content grid">
        <div class="register__data">
          <h1 class="register__title">注册</h1>
          <p class="register__description">创建新账号，加入我们</p>
        </div>

        <form @submit.prevent="handleRegister" class="register__form">
          <div class="register__inputs">
            <div class="register__box">
              <input 
                v-model="form.account" 
                type="text" 
                required 
                placeholder="账号（邮箱或学号）"
                class="register__input register__input-with-icon"
              />
              <i class="fas fa-user register__input-icon"></i>
            </div>

            <div class="register__box">
              <input 
                v-model="form.password" 
                type="password" 
                required 
                placeholder="密码"
                class="register__input register__input-with-icon"
              />
              <i class="fas fa-lock register__input-icon"></i>
            </div>
          </div>

          <!-- 用户协议复选框 -->
          <div class="register__agreement">
            <label class="register__checkbox-label">
              <input 
                v-model="form.agreedToTerms" 
                type="checkbox" 
                class="register__checkbox"
                required
              />
              <span class="register__checkbox-text">
                我已阅读并同意
                <a href="#" class="register__terms-link" @click.prevent="showTerms">《用户协议》</a>
                和
                <a href="#" class="register__terms-link" @click.prevent="showPrivacy">《隐私政策》</a>
              </span>
            </label>
          </div>

          <div v-if="error" class="register__error">
            {{ error }}
          </div>

          <div v-if="success" class="register__success">
            {{ success }}
          </div>

          <button 
            type="submit" 
            class="register__button button"
            :disabled="!form.agreedToTerms"
            :class="{ 'register__button--disabled': !form.agreedToTerms }"
          >
            注册
          </button>

          <div class="register__login">
            已有账号？ <router-link to="/login" class="register__link">立即登录</router-link>
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
  account: '',
  password: '',
  agreedToTerms: false
})

const error = ref('')
const success = ref('')

async function handleRegister() {
  error.value = ''
  success.value = ''

  // 检查是否同意用户协议
  if (!form.value.agreedToTerms) {
    error.value = '请先阅读并同意用户协议和隐私政策'
    return
  }

  const result = await authStore.register(form.value.account, form.value.password)
  if (result.success) {
    success.value = result.message
    setTimeout(() => {
      router.push('/login')
    }, 1000)
  } else {
    error.value = result.message
  }
}

function showTerms() {
  alert('用户协议\n\n1. 用户应遵守平台规则，不得发布不当内容\n2. 评分应客观公正，不得恶意评分\n3. 平台有权对违规行为进行处理\n4. 用户应保护账号安全，不得将账号转借他人')
}

function showPrivacy() {
  alert('隐私政策\n\n1. 我们重视您的隐私保护\n2. 您的个人信息仅用于平台功能实现\n3. 我们不会向第三方泄露您的个人信息\n4. 您有权随时查看和修改您的个人信息')
}
</script>

<style scoped>
/*=============== REGISTER ===============*/
.register {
  position: relative;
  height: 100vh;
  display: grid;
  align-items: center;
}

.register__container {
  position: relative;
  height: 100vh;
  display: grid;
  align-items: center;
}

.register__content {
  row-gap: 3rem;
}

.register__data {
  text-align: center;
}

.register__title {
  font-size: 2.5rem;
  color: #fff;
  margin-bottom: 1rem;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.register__description {
  margin-bottom: 2.5rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.register__form {
  display: grid;
  row-gap: 1.5rem;
}

.register__inputs {
  display: grid;
  row-gap: 1.25rem;
  margin-bottom: 1rem;
}

.register__box {
  position: relative;
  display: flex;
  align-items: center;
}

.register__input {
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

.register__input-with-icon {
  padding-right: 3.5rem;
}

.register__input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.register__input:focus {
  border-color: rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 0.05);
}

.register__input-icon {
  position: absolute;
  right: 1.25rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  pointer-events: none;
  transition: color 0.4s;
}

.register__input:focus + .register__input-icon {
  color: rgba(255, 255, 255, 1);
}

.register__select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23fff' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1.25rem center;
  padding-right: 3rem;
  cursor: pointer;
}

.register__select option {
  background: rgba(44, 62, 80, 0.95);
  color: #fff;
}

.register__row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.register__error {
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

.register__success {
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

.register__button {
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

.register__button:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
}

.register__button:active {
  transform: translateY(0);
}

.register__login {
  text-align: center;
  margin-top: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.register__link {
  color: #fff;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  text-shadow: 0 1px 3px rgba(102, 126, 234, 0.5);
}

.register__link:hover {
  text-shadow: 0 2px 8px rgba(102, 126, 234, 0.8);
}

.register__agreement {
  margin: 1rem 0;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.register__checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  line-height: 1.5;
}

.register__checkbox {
  width: 18px;
  height: 18px;
  margin-top: 2px;
  cursor: pointer;
  flex-shrink: 0;
  accent-color: rgba(255, 255, 255, 0.9);
}

.register__checkbox-text {
  flex: 1;
  user-select: none;
}

.register__terms-link {
  color: #fff;
  text-decoration: underline;
  font-weight: 600;
  transition: all 0.3s;
}

.register__terms-link:hover {
  text-shadow: 0 1px 3px rgba(102, 126, 234, 0.8);
}

.register__button--disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.register__button--disabled:hover {
  transform: none;
  background: transparent;
  box-shadow: none;
}

/*=============== BREAKPOINTS ===============*/
/* For small devices */
@media screen and (max-width: 340px) {
  .register__container {
    padding-inline: 1rem;
  }

  .register__title {
    font-size: 2rem;
  }

  .register__row {
    grid-template-columns: 1fr;
  }
}

/* For medium devices */
@media screen and (min-width: 576px) {
  .register__form {
    width: 400px;
    justify-self: center;
  }
}

/* For large devices */
@media screen and (min-width: 1024px) {
  .register__content {
    grid-template-columns: 1fr 1fr;
    align-items: center;
    column-gap: 4rem;
  }

  .register__data {
    text-align: initial;
  }

  .register__title {
    margin-inline: 0 5rem;
  }

  .register__description {
    margin-inline: 0 5rem;
  }
}
</style>

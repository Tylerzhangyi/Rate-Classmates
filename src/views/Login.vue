<template>
  <section class="login section">
    <div class="login__container container grid">
      <div class="login__content grid">
        <div class="login__data">
          <h1 class="login__title">Rate My Classmates</h1>
          <p class="login__description">欢迎回来，请登录您的账号</p>
        </div>

        <form @submit.prevent="handleLogin" class="login__form">
          <div class="login__inputs">
            <div class="login__box">
              <input 
                v-model="form.account" 
                type="text" 
                required 
                placeholder="账号（学号或邮箱）"
                class="login__input login__input-with-icon"
              />
              <i class="fas fa-user login__input-icon"></i>
            </div>

            <div class="login__box">
              <input 
                v-model="form.password" 
                type="password" 
                required 
                placeholder="密码"
                class="login__input login__input-with-icon"
              />
              <i class="fas fa-lock login__input-icon"></i>
            </div>
          </div>

          <div class="login__options">
            <label class="login__remember">
              <input 
                v-model="rememberMe" 
                type="checkbox" 
                class="login__checkbox"
              />
              <span class="login__remember-text">记住我</span>
            </label>
            <router-link to="/forgot-password" class="login__forgot-link">忘记密码？</router-link>
          </div>

          <div v-if="error" class="login__error">
            {{ error }}
          </div>

          <button type="submit" class="login__button button">
            登录
          </button>

          <div class="login__register">
            还没有账号？ <router-link to="/register" class="login__link">立即注册</router-link>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  account: '',
  password: ''
})

const rememberMe = ref(false)
const error = ref('')

onMounted(() => {
  // 检查是否有保存的账号
  const savedAccount = localStorage.getItem('rememberedAccount')
  if (savedAccount) {
    form.value.account = savedAccount
    rememberMe.value = true
  }
})

function handleLogin() {
  error.value = ''
  const result = authStore.login(form.value.account, form.value.password)
  if (result.success) {
    // 如果勾选了记住我，保存账号
    if (rememberMe.value) {
      localStorage.setItem('rememberedAccount', form.value.account)
    } else {
      localStorage.removeItem('rememberedAccount')
    }
    router.push('/students')
  } else {
    error.value = result.message
  }
}
</script>

<style scoped>
/*=============== LOGIN ===============*/
.login {
  position: relative;
  height: 100vh;
  display: grid;
  align-items: center;
}

.login__container {
  position: relative;
  height: 100vh;
  display: grid;
  align-items: center;
}

.login__content {
  row-gap: 2rem;
}

.login__data {
  text-align: center;
}

.login__title {
  font-size: 2rem;
  color: #fff;
  margin-bottom: 0.75rem;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.login__description {
  margin-bottom: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.login__form {
  display: grid;
  row-gap: 1.25rem;
}

.login__inputs {
  display: grid;
  row-gap: 1rem;
  margin-bottom: 0.75rem;
}

.login__box {
  position: relative;
  display: flex;
  align-items: center;
}

.login__input {
  width: 100%;
  background: transparent;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 1);
  border-radius: 0.875rem;
  padding: 1rem 1.5rem;
  color: #fff;
  font-weight: 500;
  font-size: 0.95rem;
  transition: border-color 0.4s, background-color 0.4s;
  outline: none;
}

.login__input-with-icon {
  padding-right: 3rem;
}

.login__input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.login__input:focus {
  border-color: rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 0.05);
}

.login__input-icon {
  position: absolute;
  right: 1rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  pointer-events: none;
  transition: color 0.4s;
}

.login__input:focus + .login__input-icon {
  color: rgba(255, 255, 255, 1);
}

.login__error {
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

.login__button {
  width: 100%;
  padding: 1rem;
  border-radius: 0.875rem;
  background: transparent;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 1);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s;
  font-size: 0.95rem;
}

.login__button:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
}

.login__button:active {
  transform: translateY(0);
}

.login__options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -0.25rem;
  margin-bottom: 0.5rem;
}

.login__remember {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.login__checkbox {
  width: 18px;
  height: 18px;
  margin-right: 0.5rem;
  cursor: pointer;
  accent-color: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 4px;
  background: transparent;
}

.login__checkbox:checked {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 1);
}

.login__remember-text {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.login__forgot-link {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.3s;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.login__forgot-link:hover {
  color: #fff;
  text-shadow: 0 1px 3px rgba(255, 255, 255, 0.5);
}

.login__register {
  text-align: center;
  margin-top: 1rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.login__link {
  color: #fff;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  text-shadow: 0 1px 3px rgba(102, 126, 234, 0.5);
}

.login__link:hover {
  text-shadow: 0 2px 8px rgba(102, 126, 234, 0.8);
}

/*=============== BREAKPOINTS ===============*/
/* For small devices */
@media screen and (max-width: 340px) {
  .login__container {
    padding-inline: 1rem;
  }

  .login__title {
    font-size: 2rem;
  }
}

/* For medium devices */
@media screen and (min-width: 576px) {
  .login__form {
    width: 360px;
    justify-self: center;
  }
}

/* For large devices */
@media screen and (min-width: 1024px) {
  .login__content {
    grid-template-columns: 1fr 1fr;
    align-items: center;
    column-gap: 4rem;
  }

  .login__data {
    text-align: initial;
  }

  .login__title {
    margin-inline: 0 5rem;
  }

  .login__description {
    margin-inline: 0 5rem;
  }
}
</style>

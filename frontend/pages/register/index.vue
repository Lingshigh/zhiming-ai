<template>
	<view class="app-container flex-center">
		<view class="auth-card">
			<view class="header">
				<text class="title">账号注册</text>
				<text class="sub-title">加入智名 AI，开启您的旅程</text>
			</view>
			
			<view class="form-group">
				<input class="input-dark" v-model="form.username" placeholder="请输入用户名" placeholder-class="ph-style"/>
				<input class="input-dark" v-model="form.email" placeholder="请输入邮箱地址" placeholder-class="ph-style"/>
				
				<view class="code-row">
					<input class="input-dark code-input" v-model="form.code" placeholder="验证码" placeholder-class="ph-style"/>
					<button class="btn-code" :disabled="counting" @tap="handleGetCode">
						{{ counting ? `${count}s后重发` : '获取验证码' }}
					</button>
				</view>
				
				<input class="input-dark" v-model="form.password" password placeholder="设置密码" placeholder-class="ph-style"/>
				<input class="input-dark" v-model="form.confirm_password" password placeholder="确认密码" placeholder-class="ph-style"/>
			</view>
			
			<button class="btn-gold" hover-class="btn-hover" @tap="handleRegister">立即注册</button>
			
			<view class="footer-link">
				<text @tap="goLogin">已有账号？去登录</text>
			</view>
		</view>
	</view>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { request } from '@/utils/request';

const form = reactive({
	username: '',
	email: '',
	code: '',
	password: '',
	confirm_password: ''
});

// 验证码倒计时逻辑
const counting = ref(false);
const count = ref(60);
let timer = null;

const handleGetCode = async () => {
	if(!form.email) return uni.showToast({title:'请先填写邮箱', icon:'none'});
	if(!/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(form.email)){
		return uni.showToast({title:'邮箱格式不正确', icon:'none'});
	}
	
	try {
		uni.showLoading({ title: '发送中...' });
		await request({
			url: '/auth/code',
			method: 'GET',
			data: { email: form.email }
		});
		uni.hideLoading();
		uni.showToast({ title: '验证码已发送' });
		
		// 开始倒计时
		counting.value = true;
		count.value = 60;
		timer = setInterval(() => {
			if(count.value > 0) {
				count.value--;
			} else {
				clearInterval(timer);
				counting.value = false;
			}
		}, 1000);
		
	} catch(e) {
		uni.hideLoading();
		console.error(e);
	}
};

const handleRegister = async () => {
	// 1. 前端校验
	if(!form.username || !form.email || !form.code || !form.password) {
		return uni.showToast({title:'请填写完整信息', icon:'none'});
	}
	if(form.password !== form.confirm_password) {
		return uni.showToast({title:'两次密码不一致', icon:'none'});
	}

	try {
		uni.showLoading({ title: '注册并登录中...' });
		
		// 2. 发送请求给后端
		const res = await request({
			url: '/auth/register',
			method: 'POST',
			data: {
				username: form.username,
				email: form.email,
				code: form.code,
				password: form.password,
				confirm_password: form.confirm_password
			}
		});
		
		uni.hideLoading();

		// ✅【核心功能】自动登录逻辑
		// 检查后端是否返回了 token (因为我们修改了后端，注册成功也会发 token)
		const token = res.token || res.access_token;
		
		if (token) {
			// A. 成功拿到 Token：存起来，直接去首页
			uni.setStorageSync('access_token', token);
			uni.showToast({ title: '注册成功，欢迎！' });
			
			// 延迟 1.5秒 跳转，让用户看清提示
			setTimeout(() => {
				uni.switchTab({ url: '/pages/index/index' });
			}, 1500);
			
		} else {
			// B. 兜底逻辑：如果后端没给 Token，还是跳回登录页
			uni.showToast({ title: '注册成功' });
			setTimeout(() => {
				uni.navigateTo({ url: '/pages/login/index' });
			}, 1500);
		}

	} catch(e) {
		uni.hideLoading();
		console.error("注册失败:", e);
		// request.js 通常会自动弹出错误提示，如果没弹可以在这里补一个
	}
};

const goLogin = () => uni.navigateTo({ url: '/pages/login/index' });
</script>

<style scoped>
/* 样式复用你登录页的风格 */
.flex-center { display: flex; align-items: center; justify-content: center; padding: 40rpx; min-height: 100vh; background-color: #1a1a1a; }
.auth-card { width: 100%; padding: 60rpx 40rpx; background: rgba(255,255,255,0.05); border-radius: 20rpx; border: 1px solid rgba(212, 175, 55, 0.3); backdrop-filter: blur(10px); }
.header { margin-bottom: 50rpx; text-align: center; }
.title { font-size: 48rpx; color: #d4af37; font-weight: bold; display: block; margin-bottom: 15rpx; }
.sub-title { font-size: 26rpx; color: #aaa; letter-spacing: 2rpx; }

.input-dark { height: 90rpx; background: rgba(0,0,0,0.3); border-radius: 10rpx; margin-bottom: 30rpx; padding: 0 30rpx; color: #fff; border: 1px solid #333; font-size: 28rpx; width: 100%; box-sizing: border-box; }
.code-row { display: flex; justify-content: space-between; gap: 20rpx; margin-bottom: 30rpx; }
.code-input { margin-bottom: 0; flex: 1; }
.btn-code { width: 220rpx; height: 90rpx; line-height: 90rpx; font-size: 26rpx; background: rgba(212, 175, 55, 0.2); color: #d4af37; border: 1px solid #d4af37; border-radius: 10rpx; padding: 0; }
.btn-code[disabled] { opacity: 0.5; background: #333; color: #999; border-color: #555; }

.btn-gold { background: linear-gradient(90deg, #d4af37, #c5a028); color: #000; font-weight: bold; border-radius: 50rpx; margin-top: 20rpx; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3); }
.btn-hover { opacity: 0.9; transform: scale(0.98); }
.footer-link { margin-top: 40rpx; text-align: center; font-size: 26rpx; color: #8e2de2; text-decoration: underline; }
.ph-style { color: #666; }
</style>
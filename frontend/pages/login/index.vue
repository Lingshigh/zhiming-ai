<template>
	<view class="app-container flex-center">
		<view class="auth-card">
			<view class="header">
				<text class="title">智名 AI</text>
				<text class="sub-title">登录开启智慧之旅</text>
			</view>
			
			<view class="form-group">
				<input class="input-dark" v-model="form.username" placeholder="请输入邮箱" placeholder-class="ph-style"/>
				<input class="input-dark" v-model="form.password" password placeholder="请输入密码" placeholder-class="ph-style"/>
			</view>
			
			<button class="btn-gold" hover-class="btn-hover" @tap="handleLogin">登 录</button>
			
			<view class="footer-link">
				<text @tap="goRegister">还没有账号？立即注册</text>
			</view>
		</view>
	</view>
</template>

<script setup>
import { reactive } from 'vue';
import { request } from '@/utils/request';

const form = reactive({
	username: '', // 这里继续用 username 变量存输入框的值没问题
	password: ''
});

const handleLogin = async () => {
	if (!form.username || !form.password) return uni.showToast({title:'请填写完整', icon:'none'});
	
	try {
		uni.showLoading({ title: '登录中...' });

		// index.vue 的 handleLogin 函数里
		
		const res = await request({
		    url: '/auth/login', 
		    method: 'POST',
		    data: {
		        // 👇 必须左边写 email，右边取输入框的值
		        email: form.username, 
		        password: form.password
		    }
		});
		
		uni.hideLoading();

		// ✅ 修改点 3: Token 兼容处理
		// 你的后端 user_router.py 返回的是 { "token": "...", "user": ... }
		// 所以这里优先取 res.token
		const token = res.token || res.access_token;

		if(token){
			// 存储 Token (注意 key 要和 request.js 里的拦截器一致，通常是 access_token)
			uni.setStorageSync('access_token', token);
			
			uni.showToast({title: '登录成功'});
			
			// 延迟跳转，让用户看清提示
			setTimeout(() => {
				uni.switchTab({ url: '/pages/index/index' });
			}, 1000);
		} else {
			// 如果没拿到 token，提示异常
			console.log("登录返回结果:", res);
			// request.js 可能已经处理了错误，这里只做兜底
		}

	} catch (e) {
		uni.hideLoading();
		console.error("登录报错:", e);
		// 如果 request.js 没有自动弹窗，这里可以补一个
		// uni.showToast({ title: '登录失败', icon: 'none' });
	}
};

const goRegister = () => uni.navigateTo({ url: '/pages/register/index' });
</script>

<style scoped>
/* 保持你原来的样式不变 */
.flex-center { display: flex; align-items: center; justify-content: center; padding: 40rpx; }
.auth-card { width: 100%; padding: 60rpx 40rpx; background: rgba(255,255,255,0.05); border-radius: 20rpx; border: 1px solid rgba(212, 175, 55, 0.3); backdrop-filter: blur(10px); }
.header { margin-bottom: 60rpx; text-align: center; }
.title { font-size: 56rpx; color: #d4af37; font-weight: bold; display: block; margin-bottom: 10rpx; }
.sub-title { font-size: 28rpx; color: #aaa; letter-spacing: 4rpx; }
.input-dark { height: 90rpx; background: rgba(0,0,0,0.3); border-radius: 10rpx; margin-bottom: 30rpx; padding: 0 30rpx; color: #fff; border: 1px solid #333; font-size: 28rpx; width: 100%; box-sizing: border-box; }
.btn-gold { background: linear-gradient(90deg, #d4af37, #c5a028); color: #000; font-weight: bold; border-radius: 50rpx; margin-top: 40rpx; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3); }
.btn-hover { opacity: 0.9; transform: scale(0.98); }
.footer-link { margin-top: 40rpx; text-align: center; font-size: 26rpx; color: #8e2de2; text-decoration: underline; }
.ph-style { color: #666; }
</style>
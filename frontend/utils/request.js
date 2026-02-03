// 这里换成你 FastAPI main.py 运行的真实 IP 地址
// 如果是真机调试，不能用 127.0.0.1，请用电脑的局域网 IP (如 192.168.x.x)
const BASE_URL = 'http://127.0.0.1:8000'; 

export const request = (options) => {
	const token = uni.getStorageSync('access_token');
	
	return new Promise((resolve, reject) => {
		// 显示加载动画（除非显式关闭）
		if (!options.hideLoading) {
			uni.showLoading({ title: '加载中...', mask: true });
		}

		uni.request({
			url: BASE_URL + options.url,
			method: options.method || 'GET',
			data: options.data || {},
			header: {
				'Content-Type': 'application/json',
				// 自动携带 Bearer Token
				'Authorization': token ? `Bearer ${token}` : ''
			},
			success: (res) => {
				// FastAPI 成功通常返回 200
				if (res.statusCode >= 200 && res.statusCode < 300) {
					resolve(res.data);
				} 
				// 401/403 代表 Token 失效
				else if (res.statusCode === 401 || res.statusCode === 403) {
					uni.showToast({ title: '登录已过期', icon: 'none' });
					uni.removeStorageSync('access_token');
					setTimeout(() => {
						uni.reLaunch({ url: '/pages/login/index' });
					}, 1500);
					reject(res);
				} else {
					uni.showToast({ 
						title: res.data.detail || '请求失败', 
						icon: 'none',
						duration: 3000
					});
					reject(res);
				}
			},
			fail: (err) => {
				uni.showToast({ title: '网络连接失败', icon: 'none' });
				reject(err);
			},
			complete: () => {
				if (!options.hideLoading) uni.hideLoading();
			}
		});
	});
};
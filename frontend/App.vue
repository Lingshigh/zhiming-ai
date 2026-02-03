<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		}
	}
</script>

<style>
	/* 全局样式 - 黑金紫调性 */
	page {
		background: #0f0c29;  /* 兜底背景色 */
		font-family: 'Helvetica Neue', Helvetica, sans-serif;
	}
	
	/* 通用容器，用于页面根节点 */
	.app-container {
		min-height: 100vh;
		background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
		color: #e0e0e0;
		box-sizing: border-box;
	}
	
	/* 金色文字高亮 */
	.text-gold { color: #d4af37; }
	/* 紫色主色调 */
	.text-purple { color: #8e2de2; }
</style>
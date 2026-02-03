<template>
  <view class="page-container">
    
    <view class="navbar glass-effect">
      <view class="nav-content">
        <view class="logo-area">
          <view class="logo-box">AI</view>
          <text class="logo-text">ZHIMING</text>
        </view>

        <view class="nav-links">
          <view class="nav-item active">首页</view>
          <view class="nav-item">案例</view>
          <view class="nav-item">关于</view>
        </view>
      </view>
    </view>

    <view class="hero-section">
      <view class="hero-content">
        <h1 class="hero-title">
          融汇东西方智慧<br />赋予名字灵魂
        </h1>
        <p class="hero-subtitle">
          ZhiMing AI 不仅仅是起名工具，而是您的文化咨询顾问。
          我们将《诗经》的典雅与希腊神话的博雅深度融合，为您寻找那个能穿越时间的文字符号。
        </p>
      </view>
    </view>

    <view class="content-section">
      <view class="section-header">选择您的命名类型</view>
      
      <view class="card-grid">
        <view 
          class="card card-life" 
          @click="openForm('婴儿')"
        >
          <view class="card-overlay">
            <view class="card-tag">Personal</view>
            <text class="card-title">婴儿起名</text>
            <text class="card-desc">承载家族血脉，寄托一生希冀。融合生辰与诗词的独家定制。</text>
            <view class="card-arrow">→</view>
          </view>
        </view>

        <view 
          class="card card-business" 
          @click="openForm('公司')"
        >
          <view class="card-overlay">
            <view class="card-tag">Business</view>
            <text class="card-title">公司起名</text>
            <text class="card-desc">商业逻辑与运势的结合，打造具备上市潜力的商业名片。</text>
            <view class="card-arrow">→</view>
          </view>
        </view>

        <view 
          class="card card-brand" 
          @click="openForm('品牌')"
        >
          <view class="card-overlay">
            <view class="card-tag">Global</view>
            <text class="card-title">品牌起名</text>
            <text class="card-desc">面向国际市场的品牌构建，兼顾跨文化传播与商标保护。</text>
            <view class="card-arrow">→</view>
          </view>
        </view>
      </view>
    </view>

    <view v-if="showModal" class="modal-mask" @click="closeForm">
      <view class="modal-content" @click.stop>
        <view class="modal-header">
          <text class="modal-title">创建{{ currentType }}名字</text>
          <text class="close-btn" @click="closeForm">×</text>
        </view>
        
        <view class="form-body">
          <view class="input-group">
            <text class="input-label">核心愿景</text>
            <input class="input-field" v-model="formData.vision" placeholder="例如: 智慧、长青、国际化" placeholder-class="input-placeholder"/>
          </view>

          <view v-if="currentType === '婴儿'" class="row-inputs">
            <view class="input-group half">
              <text class="input-label">姓氏</text>
              <input class="input-field" v-model="formData.surname" placeholder="姓"/>
            </view>
            <view class="input-group half">
              <text class="input-label">性别</text>
              <picker :range="['不限','男','女']" @change="e => formData.gender = ['不限','男','女'][e.detail.value]">
                <view class="picker-val">{{ formData.gender }}</view>
              </picker>
            </view>
          </view>

          <view class="input-group">
            <text class="input-label">其他要求</text>
            <input class="input-field" v-model="formData.other" placeholder="五行、忌讳等..." placeholder-class="input-placeholder"/>
          </view>

          <button class="btn-submit" :loading="loading" @tap="startGenerate">
            {{ loading ? 'AI 构思中...' : '开始生成' }}
          </button>
        </view>
      </view>
    </view>

    <view v-if="resultList.length" class="result-section">
      <view class="result-header">— 推荐方案 —</view>
      <view v-for="(item, idx) in resultList" :key="idx" class="result-card">
        <view class="res-top">
          <text class="res-name">{{ item.name }}</text>
          <text class="res-tag">精选</text>
        </view>
        <view class="res-body">
          <view class="res-ref">📖 {{ item.reference }}</view>
          <view class="res-moral">{{ item.moral }}</view>
        </view>
      </view>
    </view>
    
    <view class="footer">
      <text>© 2026 ZhiMing AI. Design by Minimalist.</text>
    </view>

  </view>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { request } from '@/utils/request';
import { onShow } from '@dcloudio/uni-app';

// 状态管理
const showModal = ref(false);
const currentType = ref('');
const loading = ref(false);
const resultList = ref([]);

// 表单数据
const formData = reactive({
  vision: '',
  surname: '',
  gender: '不限',
  length: '两字',
  other: ''
});

// 生命周期：检查登录
onShow(() => {
  const token = uni.getStorageSync('access_token');
  if (!token) {
    uni.reLaunch({ url: '/pages/login/index' });
  }
});

// 打开表单
const openForm = (type) => {
  currentType.value = type;
  showModal.value = true;
};

// 关闭表单
const closeForm = () => {
  showModal.value = false;
};

// 开始生成
const startGenerate = async () => {
  if(!formData.vision) return uni.showToast({title:'请输入核心愿景', icon:'none'});
  
  loading.value = true;
  resultList.value = []; // 清空旧结果
  
  try {
    const postData = {
      category: currentType.value,
      vision: formData.vision,
      surname: currentType.value === '婴儿' ? formData.surname : null,
      gender: currentType.value === '婴儿' ? formData.gender : '不限',
      length: formData.length,
      other: formData.other || "",
      exclude: []
    };

    const res = await request({
      url: '/name', 
      method: 'POST',
      data: postData,
      timeout: 60000 
    });
    
    if (res.names) {
      resultList.value = res.names;
      showModal.value = false; // 成功后关闭弹窗
      
      // 滚动到底部查看结果
      setTimeout(() => {
        uni.pageScrollTo({ scrollTop: 9999, duration: 300 });
      }, 200);
    }
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* ================= 1. 全局基调 ================= */
.page-container {
  min-height: 100vh;
  background-color: #F0F0F0; /* 浅灰底色 */
  font-family: 'Inter', -apple-system, Helvetica, sans-serif;
  color: #333;
  padding-bottom: 60px;
}

/* ================= 2. 导航栏 ================= */
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  height: 70px;
  background: rgba(240, 240, 240, 0.95);
  backdrop-filter: blur(10px);
  z-index: 100;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40rpx;
}

.logo-area { display: flex; align-items: center; gap: 10px; }
.logo-box { 
  width: 32px; height: 32px; background: #000; color: #fff; 
  font-weight: 900; display: flex; align-items: center; justify-content: center; 
  font-size: 14px; border-radius: 4px; 
}
.logo-text { font-weight: 700; font-size: 18px; letter-spacing: 1px; }

.nav-links { display: flex; gap: 20px; }
.nav-item { font-size: 14px; color: #666; cursor: pointer; }
.nav-item.active { color: #000; font-weight: 600; }

/* ================= 3. Hero 区域 ================= */
.hero-section {
  padding-top: 150px;
  padding-bottom: 80px;
  text-align: center;
}

.hero-title {
  font-size: 56px;
  font-weight: 900;
  color: #111;
  line-height: 1.1;
  margin-bottom: 24px;
  letter-spacing: -2px;
}

.hero-subtitle {
  font-size: 16px;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* ================= 4. 卡片区域 ================= */
.content-section { padding: 0 40rpx; max-width: 1200px; margin: 0 auto; }
.section-header { font-size: 14px; color: #999; margin-bottom: 20px; letter-spacing: 1px; text-transform: uppercase; }

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.card {
  height: 400px;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease;
}
.card:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }

/* --- 艺术纹理背景 --- */
.card-life { background: linear-gradient(135deg, #2b0a0a, #521111); } /* 婴儿: 红黑 */
.card-business { background: radial-gradient(circle at top right, #333, #000); } /* 公司: 几何黑 */
.card-brand { background: linear-gradient(to top, #132822, #24463d); } /* 品牌: 绿烟雾 */

.card-overlay {
  position: absolute; bottom: 0; left: 0; width: 100%;
  padding: 30px;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  box-sizing: border-box;
}

.card-tag { 
  font-size: 10px; color: rgba(255,255,255,0.6); 
  border: 1px solid rgba(255,255,255,0.2); 
  display: inline-block; padding: 2px 8px; border-radius: 10px; margin-bottom: 10px;
}
.card-title { display: block; font-size: 24px; color: #fff; font-weight: 700; margin-bottom: 8px; }
.card-desc { font-size: 13px; color: rgba(255,255,255,0.8); line-height: 1.5; }
.card-arrow { color: #fff; margin-top: 15px; font-size: 20px; opacity: 0.5; }

/* ================= 5. 弹窗表单 (极简白) ================= */
.modal-mask {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(4px);
  z-index: 999;
  display: flex; justify-content: center; align-items: center;
}

.modal-content {
  background: #fff;
  width: 90%; max-width: 500px;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}

.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.modal-title { font-size: 20px; font-weight: 700; color: #000; }
.close-btn { font-size: 24px; color: #999; cursor: pointer; }

.input-group { margin-bottom: 20px; }
.input-label { display: block; font-size: 12px; font-weight: 600; color: #000; margin-bottom: 8px; text-transform: uppercase; }
.input-field, .picker-val {
  background: #F7F7F7;
  height: 50px; line-height: 50px;
  padding: 0 16px;
  border-radius: 8px;
  font-size: 16px; color: #333;
  width: 100%; box-sizing: border-box;
}
.input-placeholder { color: #ccc; }

.row-inputs { display: flex; gap: 15px; }
.half { flex: 1; }

.btn-submit {
  background: #000; color: #fff;
  height: 54px; line-height: 54px;
  border-radius: 8px; font-weight: 600; font-size: 16px;
  margin-top: 10px;
}

/* ================= 6. 结果展示 ================= */
.result-section { max-width: 800px; margin: 60px auto; padding: 0 40rpx; }
.result-header { text-align: center; color: #ccc; margin-bottom: 30px; font-size: 12px; letter-spacing: 2px; }

.result-card {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  border-left: 4px solid #000;
}
.res-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.res-name { font-size: 32px; font-weight: 900; color: #000; }
.res-tag { background: #f0f0f0; color: #666; font-size: 12px; padding: 4px 10px; border-radius: 4px; }
.res-ref { color: #666; font-style: italic; font-size: 14px; margin-bottom: 10px; }
.res-moral { color: #333; line-height: 1.6; text-align: justify; }

.footer { text-align: center; color: #bbb; padding: 40px; font-size: 12px; }

/* 响应式 */
@media screen and (max-width: 768px) {
  .hero-title { font-size: 36px; }
  .card-grid { grid-template-columns: 1fr; }
}
</style>
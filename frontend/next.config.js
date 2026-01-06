/** @type {import('next').NextConfig} */
const path = require('path');

const nextConfig = {
  reactStrictMode: true,
  // 静态导出配置 - 用于部署到 space.ai_builder
  output: 'export',
  // 禁用图片优化（静态导出不支持）
  images: {
    unoptimized: true,
  },
  // 静态导出时不需要 rewrites（API 调用使用相对路径）
  // 确保路径别名在构建时正确解析
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname, '.'),
    };
    return config;
  },
};

module.exports = nextConfig;


/** @type {import('next').NextConfig} */
const path = require('path');

// 检查是否是生产构建（用于部署）
const isProductionBuild = process.env.NODE_ENV === 'production' && process.env.NEXT_PUBLIC_BUILD_STATIC === 'true';

const nextConfig = {
  reactStrictMode: true,
  // 只在生产构建时使用静态导出（用于部署到 space.ai_builder）
  // 开发模式下不使用静态导出，以提高开发体验
  ...(isProductionBuild && {
    output: 'export',
    images: {
      unoptimized: true,
    },
  }),
  // 确保路径别名在构建时正确解析
  webpack: (config, { isServer }) => {
    // 确保路径别名在客户端和服务器端都正确配置
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname, '.'),
    };
    
    // 确保模块解析顺序正确
    config.resolve.modules = [
      path.resolve(__dirname, '.'),
      'node_modules',
    ];
    
    return config;
  },
};

module.exports = nextConfig;


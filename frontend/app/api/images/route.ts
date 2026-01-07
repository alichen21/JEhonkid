/**
 * API 路由：获取图片列表和 OCR 结果
 * 这个路由会调用 FastAPI 后端获取数据
 */

import { NextResponse } from 'next/server';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export async function GET() {
  try {
    // 注意：这里需要从后端获取图片列表
    // 由于原 Flask 应用是在服务端扫描文件夹，我们需要创建一个后端 API
    // 暂时返回空数组，实际应该调用后端 API
    return NextResponse.json({
      results: [],
      total_count: 0,
      success_count: 0,
      fail_count: 0,
    });
  } catch (error) {
    return NextResponse.json(
      { error: '获取图片列表失败' },
      { status: 500 }
    );
  }
}





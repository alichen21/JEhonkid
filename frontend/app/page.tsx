'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { getOCRResult, getImageUrl } from '@/lib/api';
import ResultCard from '@/components/ResultCard';
import StatsCards from '@/components/StatsCards';

interface OCRResult {
  success: boolean;
  filename: string;
  full_text: string;
  text_blocks: Array<{
    text: string;
    confidence?: number;
  }>;
  language?: Array<{
    languageCode: string;
    confidence: number;
  }>;
  error?: string;
  processed_text?: any;
}

export default function Home() {
  const [results, setResults] = useState<OCRResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 从 API 获取图片列表
  useEffect(() => {
    const fetchImages = async () => {
      try {
        // 注意：需要后端提供获取图片列表的 API
        // 暂时显示空状态，用户可以上传新图片
        setLoading(false);
      } catch (err) {
        setError(err instanceof Error ? err.message : '加载失败');
        setLoading(false);
      }
    };
    fetchImages();
  }, []);

  const totalCount = results.length;
  const successCount = results.filter((r) => r.success).length;
  const failCount = results.filter((r) => !r.success).length;

  return (
    <div className="container">
      <header>
        <h1>📚 日语绘本OCR识别结果</h1>
        <p className="subtitle">亲子日语可理解输入助手 - Picture to Text</p>
        <div style={{ marginTop: '20px' }}>
          <Link
            href="/upload"
            style={{
              display: 'inline-block',
              backgroundColor: '#4CAF50',
              color: 'white',
              padding: '12px 24px',
              textDecoration: 'none',
              borderRadius: '6px',
              fontSize: '16px',
            }}
          >
            📸 上传新图片
          </Link>
        </div>
      </header>

      <StatsCards
        totalCount={totalCount}
        successCount={successCount}
        failCount={failCount}
      />

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'white' }}>
          加载中...
        </div>
      ) : error ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'white' }}>
          错误: {error}
        </div>
      ) : results.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'white' }}>
          <p>暂无图片数据</p>
          <p style={{ marginTop: '10px' }}>
            <Link
              href="/upload"
              style={{
                color: 'white',
                textDecoration: 'underline',
              }}
            >
              点击上传图片
            </Link>
          </p>
        </div>
      ) : (
        <div className="results-grid">
          {results.map((result, index) => (
            <ResultCard key={index} result={result} imageIndex={index} />
          ))}
        </div>
      )}

      <footer>
        <p>
          使用 Google Cloud Vision API 进行OCR识别 | Google Cloud
          Text-to-Speech API 进行语音合成
        </p>
      </footer>
    </div>
  );
}


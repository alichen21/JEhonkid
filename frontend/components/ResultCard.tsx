'use client';

import { useState } from 'react';
import { getImageUrl } from '@/lib/api';
import { useTTS } from '@/lib/hooks/useTTS';
import ProcessedTextSection from './ProcessedTextSection';

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

interface ResultCardProps {
  result: OCRResult;
  imageIndex: number;
}

export default function ResultCard({ result, imageIndex }: ResultCardProps) {
  const [speakingRate, setSpeakingRate] = useState(0.75);
  const [sentencesPerSegment, setSentencesPerSegment] = useState(2);
  const { playAudio, loading: ttsLoading, error: ttsError } = useTTS();

  const handlePlaySegment = async (
    text: string,
    type: 'instruction' | 'main' | number
  ) => {
    await playAudio(text, speakingRate);
  };

  return (
    <div
      className={`result-card ${!result.success ? 'error-card' : ''}`}
    >
      <div className="card-header">
        <h2 className="filename">
          <span className="file-icon">📄</span>
          {result.filename}
        </h2>
        {result.success ? (
          <span className="badge success-badge">✓ 成功</span>
        ) : (
          <span className="badge error-badge">✗ 失败</span>
        )}
      </div>

      <div className="card-content">
        <div className="image-section">
          <img
            src={getImageUrl(result.filename)}
            alt={result.filename}
            className="preview-image"
            loading="lazy"
          />
        </div>

        {result.success ? (
          <div className="text-section">
            <div className="section-title">
              <span className="icon">📝</span>
              识别文本
            </div>

            {result.full_text && (
              <div className="full-text">
                <div className="text-label">完整文本：</div>
                <div className="text-content">{result.full_text}</div>
              </div>
            )}

            {result.text_blocks && result.text_blocks.length > 0 && (
              <div className="text-blocks">
                <div className="text-label">
                  文本块 ({result.text_blocks.length}个)：
                </div>
                <div className="blocks-container">
                  {result.text_blocks.map((block, idx) => (
                    <div key={idx} className="text-block">
                      <span className="block-number">{idx + 1}</span>
                      <span className="block-text">{block.text}</span>
                      {block.confidence && (
                        <span className="confidence">
                          置信度: {(block.confidence * 100).toFixed(1)}%
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.language && result.language.length > 0 && (
              <div className="language-info">
                <div className="text-label">检测语言：</div>
                <div className="languages">
                  {result.language.map((lang, idx) => (
                    <span key={idx} className="language-tag">
                      {lang.languageCode.toUpperCase()}
                      <span className="confidence-small">
                        {Math.round(lang.confidence * 100)}%
                      </span>
                    </span>
                  ))}
                </div>
              </div>
            )}

            {result.processed_text && !result.processed_text.error && (
              <ProcessedTextSection
                processedText={result.processed_text}
                imageIndex={imageIndex}
                speakingRate={speakingRate}
                onSpeakingRateChange={setSpeakingRate}
                sentencesPerSegment={sentencesPerSegment}
                onSentencesPerSegmentChange={setSentencesPerSegment}
                onPlaySegment={handlePlaySegment}
                ttsLoading={ttsLoading}
                ttsError={ttsError}
              />
            )}

            {result.processed_text && result.processed_text.error && (
              <div className="processed-section error-section">
                <div className="error-message">
                  <span className="error-icon">⚠️</span>
                  <div>
                    <strong>LLM处理失败</strong>
                    <p>{result.processed_text.error}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="error-section">
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              <div>
                <strong>识别失败</strong>
                <p>{result.error}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}


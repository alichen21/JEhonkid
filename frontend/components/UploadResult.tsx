import { getStaticUrl } from '@/lib/api';

interface UploadResultProps {
  result: {
    ocr?: {
      full_text?: string;
    };
    processed_text?: {
      instruction?: string;
      main_text?: string;
      japanese_text?: string;
      segments?: string[];
      chinese_translation?: string;
    };
    audio_urls?: Record<string, string>;
  };
  onReset: () => void;
}

export default function UploadResult({ result, onReset }: UploadResultProps) {
  const processedText = result.processed_text;
  const audioUrls = result.audio_urls || {};

  return (
    <div className="result-section">
      <h3>处理结果</h3>
      <div className="result-card">
        {processedText && (
          <>
            {/* 指导语 */}
            {processedText.instruction && (
              <div style={{ marginBottom: '20px' }}>
                <h4>📋 指导语</h4>
                <p>{processedText.instruction}</p>
                {audioUrls.instruction && (
                  <audio controls src={getStaticUrl(audioUrls.instruction.replace('/static/', ''))} />
                )}
              </div>
            )}

            {/* 正文 */}
            {(processedText.main_text || processedText.japanese_text) && (
              <div style={{ marginBottom: '20px' }}>
                <h4>📝 正文</h4>
                <p style={{ fontSize: '18px', lineHeight: '1.8' }}>
                  {processedText.main_text || processedText.japanese_text}
                </p>
                {audioUrls.main && (
                  <audio controls src={getStaticUrl(audioUrls.main.replace('/static/', ''))} />
                )}
              </div>
            )}

            {/* 分段 */}
            {processedText.segments && processedText.segments.length > 0 && (
              <div style={{ marginBottom: '20px' }}>
                <h4>📖 分段朗读</h4>
                {processedText.segments.map((segment, idx) => (
                  <div
                    key={idx}
                    style={{
                      marginBottom: '15px',
                      padding: '10px',
                      backgroundColor: '#f9f9f9',
                      borderRadius: '6px',
                    }}
                  >
                    <p style={{ fontSize: '16px', marginBottom: '8px' }}>{segment}</p>
                    {audioUrls[`segment_${idx}`] && (
                      <audio
                        controls
                        src={getStaticUrl(
                          audioUrls[`segment_${idx}`].replace('/static/', '')
                        )}
                      />
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* 中文翻译 */}
            {processedText.chinese_translation && (
              <div style={{ marginBottom: '20px' }}>
                <h4>🇨🇳 中文翻译</h4>
                <p>{processedText.chinese_translation}</p>
              </div>
            )}
          </>
        )}

        {/* OCR原始文本 */}
        {result.ocr?.full_text && (
          <div
            style={{
              marginTop: '20px',
              paddingTop: '20px',
              borderTop: '1px solid #eee',
            }}
          >
            <h4>📄 OCR原始文本</h4>
            <p style={{ color: '#666', fontSize: '14px' }}>{result.ocr.full_text}</p>
          </div>
        )}

        <div style={{ marginTop: '20px' }}>
          <button className="btn" onClick={onReset}>
            处理新图片
          </button>
        </div>
      </div>
    </div>
  );
}


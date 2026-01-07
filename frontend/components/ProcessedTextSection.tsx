'use client';

interface ProcessedTextSectionProps {
  processedText: {
    instruction?: string;
    main_text?: string;
    japanese_text?: string;
    segments?: string[];
    chinese_translation?: string;
  };
  imageIndex: number;
  speakingRate: number;
  onSpeakingRateChange: (rate: number) => void;
  sentencesPerSegment: number;
  onSentencesPerSegmentChange: (count: number) => void;
  onPlaySegment: (text: string, type: 'instruction' | 'main' | number) => void;
  ttsLoading: boolean;
  ttsError: string | null;
}

export default function ProcessedTextSection({
  processedText,
  imageIndex,
  speakingRate,
  onSpeakingRateChange,
  sentencesPerSegment,
  onSentencesPerSegmentChange,
  onPlaySegment,
  ttsLoading,
  ttsError,
}: ProcessedTextSectionProps) {
  const mainText = processedText.main_text || processedText.japanese_text || '';
  const segments = processedText.segments || [];

  const handlePlaySegment = (type: 'instruction' | 'main' | number) => {
    let text = '';
    if (type === 'instruction') {
      text = processedText.instruction || '';
    } else if (type === 'main') {
      text = mainText;
    } else {
      text = segments[type] || '';
    }
    if (text) {
      onPlaySegment(text, type);
    }
  };

  return (
    <div className="processed-section">
      <div className="section-title">
        <span className="icon">✨</span>
        LLM处理结果
      </div>

      {/* 难度控制面板 */}
      <div className="difficulty-controls" id={`difficulty-controls-${imageIndex}`}>
        <div className="control-group">
          <label>每段句子数：</label>
          <select
            id={`sentences-per-segment-${imageIndex}`}
            value={sentencesPerSegment}
            onChange={(e) => onSentencesPerSegmentChange(Number(e.target.value))}
          >
            <option value={1}>1句</option>
            <option value={2}>2句</option>
            <option value={3}>3句</option>
            <option value={4}>4句</option>
          </select>
        </div>
        <div className="control-group">
          <label>语速：</label>
          <input
            type="range"
            id={`speaking-rate-${imageIndex}`}
            min="0.5"
            max="1.5"
            step="0.1"
            value={speakingRate}
            onChange={(e) => onSpeakingRateChange(Number(e.target.value))}
          />
          <span id={`rate-display-${imageIndex}`}>
            {speakingRate.toFixed(1)}x
          </span>
        </div>
      </div>

      {/* 指导语 */}
      {processedText.instruction && (
        <div className="processed-text instruction-text">
          <div className="text-label-with-action">
            <span>📋 指导语：</span>
            <button
              className="play-button"
              onClick={() => handlePlaySegment('instruction')}
              disabled={ttsLoading}
              title="播放指导语"
            >
              <span className="play-icon">
                {ttsLoading ? '⏳' : '🔊'}
              </span>
              <span className="play-text">
                {ttsLoading ? '生成中...' : '播放'}
              </span>
            </button>
          </div>
          <div
            className="text-content instruction-content"
            id={`instruction-text-${imageIndex}`}
          >
            {processedText.instruction}
          </div>
        </div>
      )}

      {/* 正文（完整） */}
      {mainText && (
        <div className="processed-text main-text">
          <div className="text-label-with-action">
            <span>📝 正文（完整）：</span>
            <button
              className="play-button"
              onClick={() => handlePlaySegment('main')}
              disabled={ttsLoading}
              title="播放完整正文"
            >
              <span className="play-icon">
                {ttsLoading ? '⏳' : '🔊'}
              </span>
              <span className="play-text">
                {ttsLoading ? '生成中...' : '播放'}
              </span>
            </button>
          </div>
          <div
            className="text-content japanese-content"
            id={`main-text-${imageIndex}`}
          >
            {mainText}
          </div>
        </div>
      )}

      {/* 分段朗读 */}
      {segments.length > 0 && (
        <div className="segments-section">
          <div className="text-label">📖 分段朗读：</div>
          <div className="segments-container" id={`segments-container-${imageIndex}`}>
            {segments.map((segment, idx) => (
              <div key={idx} className="segment-item">
                <div className="segment-header">
                  <span className="segment-number">段落 {idx + 1}</span>
                  <button
                    className="play-button segment-play-btn"
                    onClick={() => handlePlaySegment(idx)}
                    disabled={ttsLoading}
                    title="播放此段落"
                  >
                    <span className="play-icon">
                      {ttsLoading ? '⏳' : '🔊'}
                    </span>
                    <span className="play-text">
                      {ttsLoading ? '生成中...' : '播放'}
                    </span>
                  </button>
                </div>
                <div
                  className="segment-content"
                  id={`segment-text-${imageIndex}-${idx}`}
                >
                  {segment}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 中文翻译 */}
      {processedText.chinese_translation && (
        <div className="processed-text">
          <div className="text-label">🇨🇳 中文翻译：</div>
          <div className="text-content chinese-content">
            {processedText.chinese_translation}
          </div>
        </div>
      )}

      {ttsError && (
        <div className="error-message" style={{ marginTop: '10px' }}>
          ⚠️ {ttsError}
        </div>
      )}
    </div>
  );
}





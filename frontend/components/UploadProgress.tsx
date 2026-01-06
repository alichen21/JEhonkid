import { TaskResult } from '../lib/api';

interface UploadProgressProps {
  task: TaskResult | null;
  loading: boolean;
}

export default function UploadProgress({ task, loading }: UploadProgressProps) {
  if (!task) {
    return null;
  }

  const progress = task.progress || {};
  const completedSteps = [
    progress.ocr === 'completed',
    progress.text_processing === 'completed',
    progress.tts === 'completed',
  ].filter(Boolean).length;

  const totalProgress = (completedSteps / 3) * 100;

  const getStepStatus = (status: string) => {
    if (status === 'completed') return 'completed';
    if (status === 'processing') return 'processing';
    return 'pending';
  };

  return (
    <div className="progress-section">
      <h3>处理进度</h3>
      <div className="progress-bar-container">
        <div
          className="progress-bar"
          style={{ width: `${totalProgress}%` }}
        >
          {Math.round(totalProgress)}%
        </div>
      </div>
      <div className="progress-steps">
        <div className={`progress-step ${getStepStatus(progress.ocr || 'pending')}`}>
          📝 OCR识别
        </div>
        <div
          className={`progress-step ${getStepStatus(progress.text_processing || 'pending')}`}
        >
          ✨ 文本处理
        </div>
        <div className={`progress-step ${getStepStatus(progress.tts || 'pending')}`}>
          🔊 语音生成
        </div>
      </div>
    </div>
  );
}


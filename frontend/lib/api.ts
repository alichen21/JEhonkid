/**
 * API 客户端 - 与 FastAPI 后端通信
 * 
 * 部署模式：使用相对路径（前后端在同一域名）
 * 开发模式：使用环境变量或默认本地地址
 */

// 在浏览器环境中，如果 NEXT_PUBLIC_API_URL 未设置，使用相对路径
// 这样部署后前后端在同一域名下，API 调用会自动使用当前域名
const API_BASE_URL = typeof window !== 'undefined' 
  ? (process.env.NEXT_PUBLIC_API_URL || '')  // 浏览器环境：空字符串表示相对路径
  : (process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000');  // SSR 环境（虽然静态导出不使用）

export interface OCRResult {
  success: boolean;
  filename: string;
  full_text: string;
  text_blocks: Array<{
    text: string;
    confidence?: number;
    bounding_box?: any;
  }>;
  language?: Array<{
    languageCode: string;
    confidence: number;
  }>;
  error?: string;
}

export interface ProcessedText {
  japanese_text?: string;
  chinese_translation?: string;
  instruction?: string;
  main_text?: string;
  segments?: string[];
  error?: string;
}

export interface TaskResult {
  success: boolean;
  task_id: string;
  filename: string;
  status: string;
  progress: {
    ocr: string;
    text_processing: string;
    tts: string;
  };
  created_at: string;
  updated_at: string;
  result?: {
    ocr: OCRResult;
    processed_text?: ProcessedText;
    audio_urls?: Record<string, string>;
  };
  error?: string;
}

export interface UploadResponse {
  success: boolean;
  task_id: string;
  filename: string;
  message: string;
  error?: string;
}

export interface TTSResponse {
  success: boolean;
  audio_data?: string;
  audio_format?: string;
  voice_name?: string;
  model?: string;
  error?: string;
}

/**
 * 上传图片文件
 */
export async function uploadImage(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  console.log('上传到:', `${API_BASE_URL}/api/upload`);
  console.log('文件信息:', {
    name: file.name,
    size: file.size,
    type: file.type
  });

  try {
    const response = await fetch(`${API_BASE_URL}/api/upload`, {
      method: 'POST',
      body: formData,
    });

    console.log('响应状态:', response.status, response.statusText);

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
        console.error('错误响应:', errorData);
      } catch (e) {
        const text = await response.text();
        console.error('错误响应文本:', text);
        throw new Error(`上传失败 (${response.status}): ${text || response.statusText}`);
      }
      throw new Error(errorData.detail || errorData.error || `上传失败 (${response.status})`);
    }

    const result = await response.json();
    console.log('上传成功:', result);
    return result;
  } catch (error) {
    console.error('上传请求失败:', error);
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否运行');
    }
    throw error;
  }
}

/**
 * 查询任务状态
 */
export async function getTaskStatus(taskId: string): Promise<TaskResult> {
  const response = await fetch(`${API_BASE_URL}/api/task/${taskId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || error.error || '查询失败');
  }

  return response.json();
}

/**
 * 获取 OCR 结果
 */
export async function getOCRResult(filename: string): Promise<OCRResult> {
  const response = await fetch(`${API_BASE_URL}/api/ocr/${filename}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || error.error || '获取 OCR 结果失败');
  }

  return response.json();
}

/**
 * 生成 TTS 音频（返回 base64）
 */
export async function generateTTS(
  text: string,
  voiceName: string = 'ja-JP-Neural2-B',
  speakingRate: number = 0.75,
  model?: string
): Promise<TTSResponse> {
  const response = await fetch(`${API_BASE_URL}/api/tts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text,
      voice_name: voiceName,
      speaking_rate: speakingRate,
      model,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || error.error || 'TTS 生成失败');
  }

  return response.json();
}

/**
 * 生成 TTS 音频（返回音频文件）
 */
export async function generateTTSAudio(
  text: string,
  speakingRate: number = 0.75
): Promise<Blob> {
  const response = await fetch(`${API_BASE_URL}/api/tts/audio`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text,
      speaking_rate: speakingRate,
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || 'TTS 生成失败');
  }

  return response.blob();
}

/**
 * 获取图片 URL
 */
export function getImageUrl(filename: string): string {
  return `${API_BASE_URL}/images/${filename}`;
}

/**
 * 获取静态资源 URL
 */
export function getStaticUrl(path: string): string {
  return `${API_BASE_URL}/static/${path}`;
}


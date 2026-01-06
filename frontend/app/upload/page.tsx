'use client';

import { useState, useRef } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { uploadImage } from '../lib/api';
import { useTaskPolling } from '../lib/hooks/useTaskPolling';
import UploadProgress from '../components/UploadProgress';
import UploadResult from '../components/UploadResult';
import CameraCapture from '../components/CameraCapture';

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [showCamera, setShowCamera] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);

  const { task, loading: pollingLoading } = useTaskPolling(taskId);

  const handleFileSelect = (selectedFile: File) => {
    // 验证文件类型
    const allowedTypes = [
      'image/png',
      'image/jpeg',
      'image/jpg',
      'image/heic',
      'image/heif',
    ];
    if (
      !allowedTypes.includes(selectedFile.type) &&
      !selectedFile.name.match(/\.(png|jpg|jpeg|heic|heif)$/i)
    ) {
      setError('不支持的文件格式。请选择 PNG, JPG 或 HEIC 格式的图片。');
      return;
    }

    // 验证文件大小
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('文件大小不能超过 10MB。');
      return;
    }

    setFile(selectedFile);
    setError(null);

    // 显示预览
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target?.result as string);
    };
    reader.readAsDataURL(selectedFile);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      handleFileSelect(selectedFile);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const handleUpload = async (filesToUpload?: File | File[]) => {
    // 确保 files 总是一个数组
    let files: File[] = [];
    
    console.log('handleUpload 调用:', {
      filesToUpload,
      filesToUploadType: typeof filesToUpload,
      isFile: filesToUpload instanceof File,
      isArray: Array.isArray(filesToUpload),
      currentFile: file,
      fileType: file ? typeof file : 'null'
    });
    
    // 确定要处理的文件列表
    if (filesToUpload !== undefined && filesToUpload !== null) {
      // 如果传入了参数
      if (filesToUpload instanceof File) {
        files = [filesToUpload];
      } else if (Array.isArray(filesToUpload)) {
        // 确保数组中的每个元素都是 File
        files = filesToUpload.filter(f => f instanceof File);
        if (files.length === 0) {
          console.error('数组中没有有效的 File 对象');
          setError('文件格式错误: 没有有效的文件');
          return;
        }
        if (files.length !== filesToUpload.length) {
          console.warn('过滤掉了非 File 对象:', filesToUpload.length - files.length);
        }
      } else {
        console.error('无效的文件格式:', filesToUpload, typeof filesToUpload);
        setError('无效的文件格式: 参数必须是 File 或 File[]');
        return;
      }
    } else {
      // 如果没有传入参数，使用当前选择的文件
      if (!file) {
        setError('请先选择文件');
        return;
      }
      if (!(file instanceof File)) {
        console.error('当前 file 不是 File 对象:', file, typeof file);
        setError('文件格式错误: 当前文件不是有效的 File 对象');
        return;
      }
      files = [file];
    }
    
    console.log('处理后的 files:', files);
    
    if (files.length === 0) {
      setError('请先选择文件');
      return;
    }

    // 确保所有元素都是 File 对象
    const invalidFiles = files.filter(f => !(f instanceof File));
    if (invalidFiles.length > 0) {
      console.error('文件格式错误:', invalidFiles);
      setError(`文件格式错误: ${invalidFiles.length} 个文件不是有效的 File 对象`);
      return;
    }

    setUploading(true);
    setError(null);

    try {
      // 如果有多张图片，合并为一张（垂直拼接）
      let fileToUpload: File;
      
      if (files.length === 1) {
        fileToUpload = files[0];
      } else {
        // 合并多张图片
        fileToUpload = await mergeImages(files);
      }
      
      console.log('准备上传文件:', {
        name: fileToUpload.name,
        size: fileToUpload.size,
        type: fileToUpload.type
      });
      
      const result = await uploadImage(fileToUpload);
      console.log('上传成功:', result);
      setTaskId(result.task_id);
      setUploading(false); // 上传成功，重置上传状态
    } catch (err) {
      console.error('上传错误:', err);
      const errorMessage = err instanceof Error ? err.message : '上传失败';
      console.error('错误详情:', {
        message: errorMessage,
        error: err
      });
      setError(`上传失败: ${errorMessage}`);
      setUploading(false);
    }
  };

  // 合并多张图片为一张（垂直拼接）
  const mergeImages = async (files: File[]): Promise<File> => {
    // 确保 files 是数组
    if (!Array.isArray(files)) {
      throw new Error('files 必须是数组');
    }
    
    if (files.length === 0) {
      throw new Error('没有文件需要合并');
    }
    
    return new Promise((resolve, reject) => {
      const images: HTMLImageElement[] = [];
      let loadedCount = 0;
      const totalImages = files.length;

      files.forEach((file) => {
        const img = new Image();
        img.onload = () => {
          loadedCount++;
          if (loadedCount === totalImages) {
            // 所有图片加载完成，开始合并
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            if (!ctx) {
              reject(new Error('无法创建canvas上下文'));
              return;
            }

            // 计算总高度和最大宽度
            let totalHeight = 0;
            let maxWidth = 0;
            images.forEach((img) => {
              totalHeight += img.height;
              maxWidth = Math.max(maxWidth, img.width);
            });

            canvas.width = maxWidth;
            canvas.height = totalHeight;

            // 绘制所有图片
            let currentY = 0;
            images.forEach((img) => {
              ctx.drawImage(img, 0, currentY);
              currentY += img.height;
            });

            // 转换为File
            canvas.toBlob((blob) => {
              if (!blob) {
                reject(new Error('图片合并失败'));
                return;
              }
              const mergedFile = new File(
                [blob],
                `merged_${Date.now()}.jpg`,
                { type: 'image/jpeg' }
              );
              resolve(mergedFile);
            }, 'image/jpeg', 0.9);
          }
        };
        img.onerror = () => reject(new Error('图片加载失败'));
        
        const reader = new FileReader();
        reader.onload = (e) => {
          img.src = e.target?.result as string;
          images.push(img);
        };
        reader.onerror = () => reject(new Error('文件读取失败'));
        reader.readAsDataURL(file);
      });
    });
  };

  // 处理相机拍照结果
  const handleCameraCapture = async (files: File[]) => {
    setShowCamera(false);
    
    // 确保 files 是数组
    if (!Array.isArray(files) || files.length === 0) {
      console.error('无效的文件列表:', files);
      setError('没有拍摄到图片');
      return;
    }
    
    // 如果只有一张，直接设置预览
    if (files.length === 1) {
      setFile(files[0]);
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target?.result as string);
      };
      reader.readAsDataURL(files[0]);
    } else {
      // 多张图片，直接上传（会自动合并）
      await handleUpload(files);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreview(null);
    setTaskId(null);
    setUploading(false);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    if (cameraInputRef.current) {
      cameraInputRef.current.value = '';
    }
  };

  const isMobile = typeof window !== 'undefined' &&
    /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

  return (
    <div className="upload-container">
      <Link href="/" className="back-link">
        ← 返回主页
      </Link>

      <h1>📸 上传图片</h1>
      <p className="subtitle">拍照或选择图片进行OCR识别和语音生成</p>

      {!taskId && !uploading && (
        <>
          <div
            className={`upload-area ${dragOver ? 'dragover' : ''}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => {
              if (isMobile) {
                const choice = confirm(
                  '选择操作：\n确定 = 拍照\n取消 = 选择图片'
                );
                if (choice) {
                  cameraInputRef.current?.click();
                } else {
                  fileInputRef.current?.click();
                }
              } else {
                fileInputRef.current?.click();
              }
            }}
          >
            <div className="upload-icon">📷</div>
            <div className="upload-text">点击或拖拽图片到这里</div>
            <div className="upload-hint">支持 PNG, JPG, HEIC 格式，最大 10MB</div>
            <input
              ref={fileInputRef}
              type="file"
              id="file-input"
              accept="image/*"
              onChange={handleFileInputChange}
              style={{ display: 'none' }}
            />
            <input
              ref={cameraInputRef}
              type="file"
              id="camera-input"
              accept="image/*"
              capture="environment"
              onChange={handleFileInputChange}
              style={{ display: 'none' }}
            />
          </div>

          <div className="button-group">
            <button
              className="btn"
              style={{ backgroundColor: '#2196F3' }}
              onClick={() => setShowCamera(true)}
            >
              📸 拍照（支持连拍）
            </button>
            <button
              className="btn"
              style={{ backgroundColor: '#4CAF50' }}
              onClick={() => fileInputRef.current?.click()}
            >
              🖼️ 选择图片
            </button>
          </div>

          {preview && file && (
            <div className="preview-section">
              <h3>预览</h3>
              <img src={preview} alt="预览" className="preview-image" />
              <button 
                className="btn" 
                onClick={() => {
                  console.log('点击开始处理，当前 file:', file);
                  handleUpload();
                }}
                disabled={!file}
              >
                开始处理
              </button>
            </div>
          )}

          {error && (
            <div className="error-message" style={{ marginTop: '20px' }}>
              <strong>❌ 错误</strong>
              <p>{error}</p>
              <button 
                className="btn" 
                onClick={() => setError(null)} 
                style={{ marginTop: '10px', backgroundColor: '#666' }}
              >
                关闭
              </button>
            </div>
          )}
        </>
      )}

      {taskId && (
        <>
          <UploadProgress task={task} loading={pollingLoading} />
          {task?.status === 'completed' && task.result && (
            <UploadResult result={task.result} onReset={handleReset} />
          )}
          {task?.status === 'failed' && (
            <div className="error-message" style={{ marginTop: '20px' }}>
              <strong>处理失败</strong>
              <p>{task.error || '未知错误'}</p>
              <button className="btn" onClick={handleReset} style={{ marginTop: '10px' }}>
                重试
              </button>
            </div>
          )}
        </>
      )}

      {showCamera && (
        <CameraCapture
          onCapture={handleCameraCapture}
          onClose={() => setShowCamera(false)}
          maxPages={10}
        />
      )}
    </div>
  );
}


'use client';

import { useState, useRef, useEffect, useCallback } from 'react';

interface CameraCaptureProps {
  onCapture: (files: File[]) => void;
  onClose: () => void;
  maxPages?: number;
}

interface CapturedImage {
  id: string;
  dataUrl: string;
  file: File;
}

// 检测是否为 iOS 设备
const isIOS = () => {
  if (typeof window === 'undefined') return false;
  return /iPad|iPhone|iPod/.test(navigator.userAgent) || 
         (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
};

export default function CameraCapture({ onCapture, onClose, maxPages = 10 }: CameraCaptureProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  
  const [isStreaming, setIsStreaming] = useState(false);
  const [capturedImages, setCapturedImages] = useState<CapturedImage[]>([]);
  const [showReflectionTip, setShowReflectionTip] = useState(true);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [isInitializing, setIsInitializing] = useState(false);

  // 启动摄像头
  const startCamera = useCallback(async () => {
    // 如果已经在运行，不重复启动
    if (streamRef.current) {
      setIsStreaming(true);
      return;
    }
    
    // 如果正在初始化，不重复启动
    setIsInitializing((prev) => {
      if (prev) return prev;
      return true;
    });
    
    setCameraError(null);
    
    try {
      // iOS 需要更宽松的配置
      const constraints: MediaStreamConstraints = {
        video: isIOS() ? {
          facingMode: 'environment',
          // iOS 上不指定具体分辨率，让系统自动选择
        } : {
          facingMode: 'environment',
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      };
      
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsStreaming(true);
        setIsInitializing(false);
      }
    } catch (error: any) {
      console.error('无法访问摄像头:', error);
      setIsInitializing(false);
      
      let errorMessage = '无法访问摄像头';
      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        errorMessage = '摄像头权限被拒绝，请在浏览器设置中允许摄像头访问';
      } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
        errorMessage = '未找到摄像头设备';
      } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
        errorMessage = '摄像头被其他应用占用，请关闭其他应用后重试';
      }
      
      setCameraError(errorMessage);
    }
  }, []); // 移除依赖，避免循环

  // 停止摄像头
  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsStreaming(false);
    setIsInitializing(false);
  }, []);

  // 初始化摄像头 - iOS 上延迟启动，等待用户交互
  useEffect(() => {
    // iOS 上不在 useEffect 中自动启动，等待用户点击按钮
    // 非 iOS 设备自动启动
    if (!isIOS()) {
      startCamera();
    }
    
    return () => {
      stopCamera();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // 只在组件挂载时运行一次

  // 计算对齐框位置（居中，占屏幕80%）
  const getAlignmentFrame = () => {
    if (!videoRef.current) return null;
    const video = videoRef.current;
    const videoWidth = video.videoWidth || video.clientWidth;
    const videoHeight = video.videoHeight || video.clientHeight;
    
    const frameWidth = videoWidth * 0.8;
    const frameHeight = videoHeight * 0.8;
    const frameX = (videoWidth - frameWidth) / 2;
    const frameY = (videoHeight - frameHeight) / 2;
    
    return { x: frameX, y: frameY, width: frameWidth, height: frameHeight };
  };

  // 拍照 - 改进 iOS 支持
  const capturePhoto = useCallback(async () => {
    // iOS 上如果还没有启动摄像头，先启动
    if (isIOS() && !streamRef.current) {
      await startCamera();
      // 等待视频流就绪
      if (videoRef.current) {
        await new Promise<void>((resolve) => {
          const video = videoRef.current;
          if (!video) {
            resolve();
            return;
          }
          
          const onLoadedMetadata = () => {
            video.removeEventListener('loadedmetadata', onLoadedMetadata);
            resolve();
          };
          
          if (video.readyState >= 2) {
            resolve();
          } else {
            video.addEventListener('loadedmetadata', onLoadedMetadata);
            // 超时保护
            setTimeout(() => {
              video.removeEventListener('loadedmetadata', onLoadedMetadata);
              resolve();
            }, 3000);
          }
        });
      }
    }
    
    if (!videoRef.current || !canvasRef.current || !streamRef.current) {
      setCameraError('摄像头未启动，请点击"启动摄像头"按钮');
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d', { 
      willReadFrequently: false, // iOS 优化
      alpha: false 
    });
    
    if (!ctx) {
      setCameraError('无法创建画布上下文');
      return;
    }

    try {
      // 设置canvas尺寸为视频实际尺寸
      const videoWidth = video.videoWidth || video.clientWidth;
      const videoHeight = video.videoHeight || video.clientHeight;
      
      if (videoWidth === 0 || videoHeight === 0) {
        setCameraError('视频尺寸无效，请稍候再试');
        return;
      }
      
      canvas.width = videoWidth;
      canvas.height = videoHeight;
      
      // 绘制当前视频帧
      ctx.drawImage(video, 0, 0, videoWidth, videoHeight);
      
      // 转换为data URL（用于预览）
      const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
      
      // 转换为File对象 - 使用新的 Blob 确保不被锁定
      canvas.toBlob((blob) => {
        if (!blob) {
          setCameraError('图片转换失败');
          return;
        }
        
        // 创建新的 File 对象，确保是全新的 Blob
        const file = new File([blob], `photo_${Date.now()}_${Math.random().toString(36).substr(2, 9)}.jpg`, { 
          type: 'image/jpeg',
          lastModified: Date.now()
        });
        
        const capturedImage: CapturedImage = {
          id: `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          dataUrl,
          file
        };
        
        // 直接添加到已拍摄列表
        setCapturedImages(prev => {
          const newImages = [...prev, capturedImage];
          // 如果还没达到最大页数，显示反光提示
          if (newImages.length < maxPages) {
            setShowReflectionTip(true);
          }
          return newImages;
        });
      }, 'image/jpeg', 0.9);
    } catch (error: any) {
      console.error('拍照失败:', error);
      setCameraError(`拍照失败: ${error.message || '未知错误'}`);
    }
  }, [maxPages, isStreaming, isInitializing, startCamera]);

  // 删除已拍摄的图片
  const removeImage = (id: string) => {
    setCapturedImages(prev => prev.filter(img => img.id !== id));
  };

  // 完成并上传
  const handleFinish = () => {
    if (capturedImages.length === 0) {
      alert('请至少拍摄一张图片');
      return;
    }
    
    const files = capturedImages.map(img => img.file);
    stopCamera();
    onCapture(files);
  };

  const alignmentFrame = getAlignmentFrame();

  return (
    <div className="camera-capture-overlay">
      <div className="camera-capture-container">
        <div className="camera-header">
          <h2>📸 拍照模式</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        {showReflectionTip && (
          <div className="reflection-tip">
            <span>💡 提示：避免反光，请稍微移动角度、远离直射灯</span>
            <button onClick={() => setShowReflectionTip(false)}>×</button>
          </div>
        )}

        <div className="camera-view">
          <div className="video-wrapper">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="camera-video"
            />
            
            {/* 对齐框 */}
            {alignmentFrame && (
              <div
                className="alignment-frame"
                style={{
                  left: `${(alignmentFrame.x / (videoRef.current?.videoWidth || videoRef.current?.clientWidth || 1)) * 100}%`,
                  top: `${(alignmentFrame.y / (videoRef.current?.videoHeight || videoRef.current?.clientHeight || 1)) * 100}%`,
                  width: `${(alignmentFrame.width / (videoRef.current?.videoWidth || videoRef.current?.clientWidth || 1)) * 100}%`,
                  height: `${(alignmentFrame.height / (videoRef.current?.videoHeight || videoRef.current?.clientHeight || 1)) * 100}%`,
                }}
              >
                <div className="alignment-corner tl"></div>
                <div className="alignment-corner tr"></div>
                <div className="alignment-corner bl"></div>
                <div className="alignment-corner br"></div>
                <div className="alignment-hint">把页面四角放进框里</div>
              </div>
            )}
          </div>

          <canvas ref={canvasRef} style={{ display: 'none' }} />

          <div className="camera-controls">
            {cameraError && (
              <div className="error-message" style={{ 
                padding: '10px', 
                backgroundColor: '#ffebee', 
                color: '#c62828',
                borderRadius: '4px',
                marginBottom: '10px'
              }}>
                <strong>⚠️ {cameraError}</strong>
                {!isStreaming && isIOS() && (
                  <div style={{ marginTop: '5px', fontSize: '0.9em' }}>
                    请点击下方按钮启动摄像头
                  </div>
                )}
              </div>
            )}
            
            {!isStreaming && isIOS() && (
              <button
                className="btn btn-capture"
                onClick={startCamera}
                disabled={isInitializing}
                style={{ marginBottom: '10px' }}
              >
                {isInitializing ? '正在启动摄像头...' : '📷 启动摄像头'}
              </button>
            )}
            
            <button
              className="btn btn-capture"
              onClick={capturePhoto}
              disabled={!isStreaming && !isIOS()}
            >
              📷 拍照
            </button>
            
            {capturedImages.length > 0 && (
              <>
                <div className="captured-preview">
                  <p>已拍摄 ({capturedImages.length}/{maxPages})：</p>
                  <div className="preview-thumbnails">
                    {capturedImages.map((img) => (
                      <div key={img.id} className="thumbnail-wrapper">
                        <img src={img.dataUrl} alt="预览" />
                        <button
                          className="remove-thumbnail"
                          onClick={() => removeImage(img.id)}
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
                
                <button
                  className="btn btn-finish"
                  onClick={handleFinish}
                >
                  ✅ 完成并上传 ({capturedImages.length} 张)
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

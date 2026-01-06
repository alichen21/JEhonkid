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

export default function CameraCapture({ onCapture, onClose, maxPages = 10 }: CameraCaptureProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  
  const [isStreaming, setIsStreaming] = useState(false);
  const [capturedImages, setCapturedImages] = useState<CapturedImage[]>([]);
  const [showReflectionTip, setShowReflectionTip] = useState(true);

  // 启动摄像头
  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment', // 后置摄像头
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsStreaming(true);
      }
    } catch (error) {
      console.error('无法访问摄像头:', error);
      alert('无法访问摄像头，请检查权限设置');
    }
  }, []);

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
  }, []);

  // 初始化摄像头
  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
    };
  }, [startCamera, stopCamera]);

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

  // 拍照
  const capturePhoto = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    if (!ctx) return;

    // 设置canvas尺寸为视频实际尺寸
    const videoWidth = video.videoWidth || video.clientWidth;
    const videoHeight = video.videoHeight || video.clientHeight;
    
    canvas.width = videoWidth;
    canvas.height = videoHeight;
    
    // 绘制当前视频帧
    ctx.drawImage(video, 0, 0);
    
    // 转换为data URL
    const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
    
    // 转换为File对象
    canvas.toBlob((blob) => {
      if (!blob) return;
      
      const file = new File([blob], `photo_${Date.now()}.jpg`, { type: 'image/jpeg' });
      const capturedImage: CapturedImage = {
        id: Date.now().toString(),
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
  }, [maxPages]);

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
            <button
              className="btn btn-capture"
              onClick={capturePhoto}
              disabled={!isStreaming}
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

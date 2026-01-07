/**
 * TTS 音频播放 Hook
 */

import { useState, useRef } from 'react';
import { generateTTSAudio } from '../api';

export function useTTS() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const playAudio = async (text: string, speakingRate: number = 0.75) => {
    if (!text.trim()) {
      setError('文本内容为空');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 生成音频
      const audioBlob = await generateTTSAudio(text, speakingRate);
      const audioUrl = URL.createObjectURL(audioBlob);

      // 创建或更新音频元素
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.src = '';
      }

      const audio = new Audio(audioUrl);
      audioRef.current = audio;

      // 播放音频
      await audio.play();

      // 清理 URL 对象
      audio.addEventListener('ended', () => {
        URL.revokeObjectURL(audioUrl);
      });

      audio.addEventListener('error', () => {
        setError('音频播放失败');
        URL.revokeObjectURL(audioUrl);
      });

      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : '生成音频失败');
      setLoading(false);
    }
  };

  const stopAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
  };

  return {
    playAudio,
    stopAudio,
    loading,
    error,
  };
}





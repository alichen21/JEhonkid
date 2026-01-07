/**
 * 任务轮询 Hook
 */

import { useState, useEffect, useRef } from 'react';
import { getTaskStatus, TaskResult } from '../api';

export function useTaskPolling(taskId: string | null, interval: number = 1000) {
  const [task, setTask] = useState<TaskResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!taskId) {
      return;
    }

    setLoading(true);
    setError(null);

    const poll = async () => {
      try {
        const result = await getTaskStatus(taskId);
        setTask(result);
        setLoading(false);

        // 如果任务完成或失败，停止轮询
        if (result.status === 'completed' || result.status === 'failed') {
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : '查询失败');
        setLoading(false);
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
      }
    };

    // 立即执行一次
    poll();

    // 设置轮询
    intervalRef.current = setInterval(poll, interval);

    // 清理函数
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [taskId, interval]);

  return { task, loading, error };
}





"""
任务管理器 - 使用内存存储任务状态
支持后台线程处理图片OCR、文本处理和TTS生成
"""

import uuid
import threading
import time
from datetime import datetime
from typing import Dict, Optional
from enum import Enum


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"          # 等待处理
    PROCESSING = "processing"    # 处理中
    OCR_COMPLETED = "ocr_completed"  # OCR完成
    TEXT_PROCESSING = "text_processing"  # 文本处理中
    TTS_GENERATING = "tts_generating"  # TTS生成中
    COMPLETED = "completed"     # 完成
    FAILED = "failed"           # 失败


class TaskManager:
    """任务管理器 - 内存存储"""
    
    def __init__(self):
        """初始化任务管理器"""
        self.tasks: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        # 任务过期时间（秒），默认1小时
        self.task_ttl = 3600
    
    def create_task(self, filename: str, filepath: str) -> str:
        """
        创建新任务
        
        Args:
            filename: 文件名
            filepath: 文件路径
            
        Returns:
            任务ID
        """
        task_id = str(uuid.uuid4())
        
        task = {
            'task_id': task_id,
            'filename': filename,
            'filepath': filepath,
            'status': TaskStatus.PENDING.value,
            'progress': {
                'ocr': 'pending',
                'text_processing': 'pending',
                'tts': 'pending'
            },
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'result': None,
            'error': None
        }
        
        with self.lock:
            self.tasks[task_id] = task
        
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """
        获取任务信息
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务信息字典，如果不存在返回None
        """
        with self.lock:
            return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: TaskStatus, 
                          progress: Optional[Dict] = None, 
                          result: Optional[Dict] = None,
                          error: Optional[str] = None):
        """
        更新任务状态
        
        Args:
            task_id: 任务ID
            status: 任务状态
            progress: 进度信息（可选）
            result: 结果数据（可选）
            error: 错误信息（可选）
        """
        with self.lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task['status'] = status.value
                task['updated_at'] = datetime.now().isoformat()
                
                if progress:
                    task['progress'].update(progress)
                
                if result is not None:
                    task['result'] = result
                
                if error:
                    task['error'] = error
                    task['status'] = TaskStatus.FAILED.value
    
    def cleanup_old_tasks(self):
        """清理过期任务"""
        current_time = time.time()
        with self.lock:
            expired_tasks = []
            for task_id, task in self.tasks.items():
                created_time = datetime.fromisoformat(task['created_at']).timestamp()
                if current_time - created_time > self.task_ttl:
                    expired_tasks.append(task_id)
            
            for task_id in expired_tasks:
                del self.tasks[task_id]
            
            if expired_tasks:
                print(f"清理了 {len(expired_tasks)} 个过期任务")
    
    def get_all_tasks(self) -> Dict[str, Dict]:
        """获取所有任务（用于调试）"""
        with self.lock:
            return self.tasks.copy()


# 全局任务管理器实例
task_manager = TaskManager()


interface StatsCardsProps {
  totalCount: number;
  successCount: number;
  failCount: number;
}

export default function StatsCards({
  totalCount,
  successCount,
  failCount,
}: StatsCardsProps) {
  return (
    <div className="stats">
      <div className="stat-card">
        <span className="stat-number">{totalCount}</span>
        <span className="stat-label">总图片数</span>
      </div>
      <div className="stat-card success">
        <span className="stat-number">{successCount}</span>
        <span className="stat-label">识别成功</span>
      </div>
      <div className="stat-card error">
        <span className="stat-number">{failCount}</span>
        <span className="stat-label">识别失败</span>
      </div>
    </div>
  );
}


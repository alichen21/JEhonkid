import type { Metadata } from 'next';
import '../styles/globals.css';

export const metadata: Metadata = {
  title: '日语绘本OCR识别结果',
  description: '亲子日语可理解输入助手 - Picture to Text',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}


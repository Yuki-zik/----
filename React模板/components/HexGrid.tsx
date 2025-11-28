import React from 'react';

interface HexGridProps {
  className?: string;
  style?: React.CSSProperties;
}

export const HexGrid: React.FC<HexGridProps> = ({ className, style }) => {
  return (
    <svg 
      width="100%" 
      height="100%" 
      className={`absolute inset-0 pointer-events-none ${className || 'opacity-40'}`}
      style={style}
    >
      <defs>
        <pattern id="hex-grid" width="20" height="34" patternUnits="userSpaceOnUse" patternTransform="scale(0.8)">
          <path
            d="M10 0 L20 5 L20 15 L10 20 L0 15 L0 5 Z"
            fill="none"
            stroke="currentColor"
            strokeWidth="0.5"
            className="text-cyan-600"
          />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#hex-grid)" />
    </svg>
  );
};
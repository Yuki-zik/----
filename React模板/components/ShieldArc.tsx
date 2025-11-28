import React from 'react';

interface ShieldArcProps {
  percentage: number; // 0 to 100
  side: 'left' | 'right';
  isCritical: boolean;
}

export const ShieldArc: React.FC<ShieldArcProps> = ({ percentage, side, isCritical }) => {
  // SVG Configuration for a 260x260 canvas
  const size = 260;
  const strokeWidth = 8; // Thinner: 12 -> 8
  const radius = (size - strokeWidth) / 2 - 4; // Adjusted padding slightly for new width
  const center = size / 2;

  // Arc math
  // Left shield: extends roughly from 135deg to 225deg (normalized)
  // Right shield: extends roughly from -45deg to 45deg
  
  // We'll use strokeDasharray to simulate progress.
  // Circumference = 2 * PI * r
  const circumference = 2 * Math.PI * radius;
  
  // Define arc length in degrees. Let's say each shield covers 100 degrees vertical.
  const arcDegrees = 80; 
  const arcLength = (arcDegrees / 360) * circumference;
  
  // Calculate filled amount based on percentage
  const filledLength = (percentage / 100) * arcLength;
  
  // Rotation for placement
  // Left side: centered at 180deg (left). 
  // Right side: centered at 0deg (right).
  const rotation = side === 'left' ? 140 : -40; // Starting angles roughly

  // Color logic
  const colorClass = isCritical ? 'stroke-red-500 drop-shadow-[0_0_8px_rgba(239,68,68,0.8)]' : 'stroke-cyan-400 drop-shadow-[0_0_5px_rgba(34,211,238,0.5)]';
  // Made track more obvious (opacity 30 -> 60)
  const trackClass = 'stroke-cyan-900/60';

  return (
    <svg width="100%" height="100%" className="absolute inset-0 pointer-events-none rotate-90" viewBox={`0 0 ${size} ${size}`}>
      {/* Background Track */}
      <circle
        cx={center}
        cy={center}
        r={radius}
        fill="none"
        strokeWidth={strokeWidth}
        className={trackClass}
        strokeLinecap="round" 
        strokeDasharray={`${arcLength} ${circumference - arcLength}`}
        strokeDashoffset={0}
        transform={`rotate(${rotation} ${center} ${center})`}
      />
      
      {/* Active Value */}
      <circle
        cx={center}
        cy={center}
        r={radius}
        fill="none"
        strokeWidth={strokeWidth}
        className={`${colorClass} transition-all duration-500 ease-out`}
        strokeLinecap="round"
        strokeDasharray={`${filledLength} ${circumference - filledLength}`}
        strokeDashoffset={0}
        transform={`rotate(${rotation} ${center} ${center})`}
      />
    </svg>
  );
};
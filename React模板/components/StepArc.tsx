import React from 'react';

interface StepArcProps {
  steps: number;
  goal?: number;
}

export const StepArc: React.FC<StepArcProps> = ({ steps, goal = 10000 }) => {
  const size = 260;
  const strokeWidth = 4; // Thinner: 6 -> 4
  const radius = (size - strokeWidth) / 2 - 2; 
  const center = size / 2;

  // Mirror of DaylightArc: 100 degrees total at the BOTTOM
  // Top center is -90deg. Bottom center is 90deg.
  // Start: 90 - 50 = 40deg
  // End: 90 + 50 = 140deg
  const startAngle = 40;
  const totalDegrees = 100;
  const endAngle = startAngle + totalDegrees;

  const percentage = Math.min(steps / goal, 1);
  const activeDegrees = totalDegrees * percentage;
  const activeEndAngle = startAngle + activeDegrees;

  const getPoint = (angle: number, r: number = radius) => {
    const rad = angle * Math.PI / 180;
    return {
      x: center + r * Math.cos(rad),
      y: center + r * Math.sin(rad)
    };
  };

  const makePath = (start: number, end: number) => {
    const p1 = getPoint(start);
    const p2 = getPoint(end);
    const largeArc = Math.abs(end - start) > 180 ? 1 : 0;
    return `M ${p1.x} ${p1.y} A ${radius} ${radius} 0 ${largeArc} 1 ${p2.x} ${p2.y}`;
  };

  return (
    <svg width="100%" height="100%" className="absolute inset-0 pointer-events-none" viewBox={`0 0 ${size} ${size}`}>
      {/* Background Track */}
      <path
        d={makePath(startAngle, endAngle)}
        fill="none"
        stroke="#1e293b" // Slate-800
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        className="opacity-60"
      />

      {/* Active Progress */}
      {percentage > 0 && (
        <path
          d={makePath(startAngle, activeEndAngle)}
          fill="none"
          stroke="#0891b2" // Cyan-600 (Darker Cyan)
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          className="drop-shadow-[0_0_2px_rgba(8,145,178,0.6)] transition-all duration-1000 ease-out"
        />
      )}
      
      {/* Goal Label */}
      <text
        x={center}
        y={size - 12}
        textAnchor="middle"
        className="text-[10px] fill-slate-600 font-mono tracking-widest font-bold"
      >
        GOAL {goal/1000}K
      </text>
    </svg>
  );
};
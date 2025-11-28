
import React from 'react';

interface SedentarySidebarProps {
  level: number; // 1 to 5
}

export const SedentarySidebar: React.FC<SedentarySidebarProps> = ({ level }) => {
  // Config for the curved layout
  const cx = 130;
  const cy = 130;
  // Adjusted for perfect right-edge fit (260x260 canvas)
  const rOuter = 128; 
  const rInner = 120; // 8px thickness
  
  // Angle coverage: Right side, centered at 0 deg.
  // We want 5 blocks stacking UP.
  const startAngle = 32; 
  const totalSpan = 64;
  const gap = 1; // Tight gap for nesting look
  const blockSpan = (totalSpan - (4 * gap)) / 5; 

  // Heatmap Colors
  const colors = [
    '#22c55e', // Lv1: Green
    '#84cc16', // Lv2: Lime
    '#f59e0b', // Lv3: Amber
    '#f97316', // Lv4: Orange
    '#ef4444', // Lv5: Red
  ];

  // Current active color determines the color of ALL active blocks
  const activeColor = colors[Math.min(Math.max(0, level - 1), 4)];

  // Helper to get coordinates
  const getPoint = (angleDeg: number, radius: number) => {
    const rad = (angleDeg * Math.PI) / 180;
    return `${cx + radius * Math.cos(rad)} ${cy + radius * Math.sin(rad)}`;
  };

  // Generate the "Nested Arrow/Chevron" path for a curved segment
  const makeChevronPath = (index: number) => {
    const currentStart = startAngle - (index * (blockSpan + gap));
    const currentEnd = currentStart - blockSpan;
    
    // Indentation amount (degrees) to create the chevron "interlock"
    const indent = 3; 

    const rMid = (rOuter + rInner) / 2;

    // Points:
    // Bottom Edge (Start Angle) -> The "Notch" (indent UP/Counter-Clockwise)
    const p1_Inner = getPoint(currentStart, rInner);
    const p2_Mid   = getPoint(currentStart - indent, rMid); 
    const p3_Outer = getPoint(currentStart, rOuter);
    
    // Top Edge (End Angle) -> The "Point" (point UP/Counter-Clockwise)
    const p4_Outer = getPoint(currentEnd, rOuter);
    const p5_Mid   = getPoint(currentEnd - indent, rMid); 
    const p6_Inner = getPoint(currentEnd, rInner);

    return `
      M ${p1_Inner}
      L ${p2_Mid}
      L ${p3_Outer}
      A ${rOuter} ${rOuter} 0 0 0 ${p4_Outer}
      L ${p5_Mid}
      L ${p6_Inner}
      A ${rInner} ${rInner} 0 0 1 ${p1_Inner}
      Z
    `;
  };

  return (
    <svg width="100%" height="100%" className="absolute inset-0 pointer-events-none" viewBox="0 0 260 260">
      <defs>
        <filter id="glow-sedentary">
          <feGaussianBlur stdDeviation="2" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Render Blocks */}
      {[0, 1, 2, 3, 4].map((i) => {
        const isActive = (i + 1) <= level;
        
        return (
          <path
            key={i}
            d={makeChevronPath(i)}
            fill={isActive ? activeColor : '#0f172a'} 
            stroke={isActive ? activeColor : '#334155'}
            strokeWidth={isActive ? 0 : 1}
            strokeLinejoin="round"
            className="transition-all duration-500 ease-out"
            filter={isActive && level >= 3 ? 'url(#glow-sedentary)' : undefined}
            opacity={isActive ? 1 : 0.5}
          />
        );
      })}
    </svg>
  );
};

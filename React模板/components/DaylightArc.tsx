import React from 'react';

interface DaylightArcProps {
  currentTime: Date;
}

export const DaylightArc: React.FC<DaylightArcProps> = ({ currentTime }) => {
  // Config
  const size = 260;
  const strokeWidth = 6;
  const radius = (size - strokeWidth) / 2 - 2; // Pushed to very edge
  const center = size / 2;
  
  // Arc spans 100 degrees at the top
  const startAngle = -140;
  const totalDegrees = 100;
  const endAngle = startAngle + totalDegrees;
  
  // Time calculations
  const totalMinutes = 24 * 60;
  const currentMinutes = currentTime.getHours() * 60 + currentTime.getMinutes();
  const currentPercent = currentMinutes / totalMinutes;
  
  // Daylight assumptions (06:00 to 18:00)
  const sunrisePercent = 0.25; // 06:00
  const sunsetPercent = 0.75; // 18:00
  
  // Angles for segments
  const dayStartAngle = startAngle + (totalDegrees * sunrisePercent);
  const dayEndAngle = startAngle + (totalDegrees * sunsetPercent);
  const currentIndicatorAngle = startAngle + (totalDegrees * currentPercent);

  // Helper to get coordinates
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

  // Marker Component with distinct types
  const HorizonMarker = ({ angle, type }: { angle: number, type: 'sunrise' | 'sunset' }) => {
      const pos = getPoint(angle);
      // Rotation: Tangent to the circle.
      const rotation = angle + 90;
      
      return (
        <g transform={`translate(${pos.x}, ${pos.y}) rotate(${rotation})`}>
            {/* Horizon Line */}
            <path 
                d="M -4 0 L 4 0" 
                stroke="#94a3b8" 
                strokeWidth="1.5" 
                strokeLinecap="round" 
            />
            
            {/* Sun Icon */}
            {type === 'sunrise' ? (
                // Sun Rising (Above line)
                 <path 
                    d="M -2.5 0 A 2.5 2.5 0 0 1 2.5 0" 
                    fill="#fbbf24" 
                />
            ) : (
                // Sun Setting (Below line)
                <path 
                    d="M -2.5 0 A 2.5 2.5 0 0 0 2.5 0" 
                    fill="#fbbf24" 
                />
            )}
        </g>
      );
  };

  // Label Positions (Closer: radius - 13)
  const labelRadius = radius - 13;
  const sunriseLabelPos = getPoint(dayStartAngle, labelRadius);
  const sunsetLabelPos = getPoint(dayEndAngle, labelRadius);

  return (
    <svg width="100%" height="100%" className="absolute inset-0 pointer-events-none" viewBox={`0 0 ${size} ${size}`}>
      <defs>
          <linearGradient id="dayGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#0891b2" /> 
              <stop offset="50%" stopColor="#fbbf24" /> 
              <stop offset="100%" stopColor="#0891b2" /> 
          </linearGradient>
      </defs>

      {/* Night Segment 1 (00-06) */}
      <path
        d={makePath(startAngle, dayStartAngle)}
        fill="none"
        stroke="#1e293b"
        strokeWidth={strokeWidth}
        strokeLinecap="round" // Round start
      />
      {/* Fix round cap overlap: butt end */}
       <path
        d={makePath(dayStartAngle - 1, dayStartAngle)}
        fill="none"
        stroke="#1e293b"
        strokeWidth={strokeWidth}
        strokeLinecap="butt" 
      />
      
      {/* Day Segment (06-18) */}
      <path
        d={makePath(dayStartAngle, dayEndAngle)}
        fill="none"
        stroke="url(#dayGradient)"
        strokeWidth={strokeWidth}
        strokeLinecap="butt" // Butt ends for seamless join
        className="drop-shadow-[0_0_2px_rgba(251,191,36,0.5)]"
      />
      
      {/* Night Segment 2 (18-24) */}
      <path
        d={makePath(dayEndAngle, endAngle)}
        fill="none"
        stroke="#1e293b"
        strokeWidth={strokeWidth}
        strokeLinecap="round" // Round end
      />
       {/* Fix round cap overlap: butt start */}
       <path
        d={makePath(dayEndAngle, dayEndAngle + 1)}
        fill="none"
        stroke="#1e293b"
        strokeWidth={strokeWidth}
        strokeLinecap="butt"
      />

      {/* Markers directly on track */}
      <HorizonMarker angle={dayStartAngle} type="sunrise" />
      <HorizonMarker angle={dayEndAngle} type="sunset" />

      {/* Current Time Indicator */}
      <circle 
        cx={getPoint(currentIndicatorAngle).x} 
        cy={getPoint(currentIndicatorAngle).y}
        r={2.5}
        className="fill-white drop-shadow-[0_0_4px_white]"
      />
      
      {/* Labels */}
      <text 
        x={sunriseLabelPos.x} 
        y={sunriseLabelPos.y} 
        textAnchor="middle" 
        dominantBaseline="middle" 
        className="text-[10px] fill-slate-500 font-mono font-bold tracking-tighter"
        style={{ transform: `rotate(${(dayStartAngle + 90)}deg)`, transformBox: 'fill-box', transformOrigin: 'center' }} 
      >
        06:00
      </text>
      <text 
        x={sunsetLabelPos.x} 
        y={sunsetLabelPos.y} 
        textAnchor="middle" 
        dominantBaseline="middle" 
        className="text-[10px] fill-slate-500 font-mono font-bold tracking-tighter"
        style={{ transform: `rotate(${(dayEndAngle + 90)}deg)`, transformBox: 'fill-box', transformOrigin: 'center' }} 
      >
        18:00
      </text>

      {/* 12 (Noon) marker */}
      <rect x={center - 0.5} y={4} width={1} height={4} fill="#475569" />
    </svg>
  );
};

import React, { useState, useEffect } from 'react';
import { HexGrid } from './HexGrid';
import { DaylightArc } from './DaylightArc';
import { StepArc } from './StepArc';
import { SedentarySidebar } from './SedentarySidebar';
import { SensorData, WidgetType } from '../types';

interface WatchFaceProps {
  sensorData: SensorData;
  sedentaryLevel: number; // Added prop
  onOpenChat: () => void;
  onOpenSettings: () => void;
  widgetConfig: {
    topWidgets: WidgetType[];
    btmWidgets: WidgetType[];
    leftWidgets: WidgetType[];
  };
  onWidgetCycle: (section: 'top' | 'btm' | 'left', index: number) => void;
}

// Inline SVGs to guarantee rendering without layout shift or font dependency issues
const Icons = {
  Bluetooth: ({ active }: { active: boolean }) => (
    <svg className={`w-3 h-3 ${active ? 'text-blue-400' : 'text-slate-800'}`} viewBox="0 0 24 24" fill="currentColor">
      <path d="M17.71 7.71L12 2h-1v7.58L7.38 5.97 5.97 7.38 10.59 12l-4.62 4.62 1.41 1.41L12 14.42V22h1l5.71-5.71-4.3-4.29 4.3-4.29zM13 5.83l1.88 1.88L13 9.59V5.83zm0 12.34v-3.76l1.88 1.88L13 18.17z"/>
    </svg>
  ),
  Smartphone: ({ active }: { active: boolean }) => (
    <svg className={`w-3 h-3 ${active ? 'text-green-400 animate-pulse' : 'text-slate-800'}`} viewBox="0 0 24 24" fill="currentColor">
      <path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/>
    </svg>
  ),
  Alarm: ({ active }: { active: boolean }) => (
    <svg className={`w-3 h-3 ${active ? 'text-yellow-500' : 'text-slate-800'}`} viewBox="0 0 24 24" fill="currentColor">
      <path d="M22 5.72l-4.6-3.86-1.29 1.53 4.6 3.86L22 5.72zM7.88 3.39L6.6 1.86 2 5.71l1.29 1.53 4.59-3.85zM12.5 8H11v6l4.75 2.85.75-1.23-4-2.37V8zM12 4c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9z"/>
    </svg>
  ),
  Moon: ({ active }: { active: boolean }) => (
    <svg className={`w-3 h-3 ${active ? 'text-purple-400' : 'text-slate-800'}`} viewBox="0 0 24 24" fill="currentColor">
      <path d="M9 2c-1.05 0-2.05.16-3 .46 2.81.92 4.85 3.57 4.85 6.74 0 3.98-3.22 7.2-7.2 7.2-.63 0-1.23-.09-1.8-.24 1.05 3.43 3.44 4.84 6.15 4.84 4.42 0 8-3.58 8-8s-3.58-8-8-8z"/>
    </svg>
  ),
  SmartToy: () => (
    <svg className="w-5 h-5 group-hover:drop-shadow-[0_0_5px_cyan]" viewBox="0 0 24 24" fill="currentColor">
      <path d="M20 9V7c0-1.1-.9-2-2-2h-3c0-1.66-1.34-3-3-3S9 3.34 9 5H6c-1.1 0-2 .9-2 2v2c-1.66 0-3 1.34-3 3s1.34 3 3 3v4c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-4c1.66 0 3-1.34 3-3s-1.34-3-3-3zm-5 10H9v-6h6v6zM9 9V7h6v2H9z"/>
    </svg>
  )
};

// Mini bar chart component for step history
const MiniStepChart = ({ data, compact = false }: { data: number[], compact?: boolean }) => {
    // Normalize data: Goal is 10k
    const goal = 10000;
    
    return (
        <div className={`flex items-end ${compact ? 'gap-[1px] h-2 w-6' : 'gap-[2px] h-3 w-10'}`}>
            {data.map((steps, i) => {
                const height = Math.min(steps / goal, 1);
                const isToday = i === data.length - 1;
                const isMet = steps >= goal;
                
                let barColor = 'bg-slate-700';
                if (isMet) barColor = 'bg-cyan-500 shadow-[0_0_2px_cyan]';
                else if (isToday) barColor = 'bg-white animate-pulse';

                return (
                    <div 
                        key={i} 
                        style={{ height: `${Math.max(10, height * 100)}%` }} 
                        className={`flex-1 ${barColor} rounded-[1px] transition-all duration-500`} 
                    />
                );
            })}
        </div>
    );
};

export const WatchFace: React.FC<WatchFaceProps> = ({ 
    sensorData, 
    sedentaryLevel,
    onOpenChat, 
    widgetConfig,
    onWidgetCycle 
}) => {
  const [time, setTime] = useState(new Date());

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (date: Date) => {
    const h = date.getHours().toString().padStart(2, '0');
    const m = date.getMinutes().toString().padStart(2, '0');
    return { h, m };
  };

  const { h, m } = formatTime(time);
  const isCritical = sensorData.heartRate > 150;
  const accentColor = isCritical ? 'text-red-500' : 'text-cyan-400';
  const glowClass = isCritical ? 'drop-shadow-[0_0_10px_rgba(239,68,68,0.8)]' : 'drop-shadow-[0_0_5px_rgba(34,211,238,0.6)]';

  // Helper to extract uniform data structure for any widget type
  const getWidgetData = (type: WidgetType) => {
    switch(type) {
        case WidgetType.BATTERY:
            return {
                icon: 'battery_std',
                value: `${sensorData.battery}%`,
                percent: sensorData.battery,
                color: sensorData.battery < 20 ? 'text-red-500' : 'text-cyan-400',
                barColor: sensorData.battery < 20 ? 'bg-red-500' : 'bg-cyan-400'
            };
        case WidgetType.HEART_RATE:
            return {
                icon: 'favorite',
                value: sensorData.heartRate,
                percent: Math.min((sensorData.heartRate / 200) * 100, 100),
                color: sensorData.heartRate > 150 ? 'text-red-500 animate-pulse' : 'text-red-400',
                barColor: sensorData.heartRate > 150 ? 'bg-red-500' : 'bg-red-400'
            };
        case WidgetType.STEPS:
            return {
                icon: 'directions_walk',
                value: sensorData.steps > 9999 ? '9.9k' : sensorData.steps,
                percent: Math.min((sensorData.steps / 10000) * 100, 100),
                color: 'text-slate-200',
                barColor: 'bg-cyan-400'
            };
        case WidgetType.CALORIES:
            return {
                icon: 'local_fire_department',
                value: sensorData.calories,
                percent: Math.min((sensorData.calories / 3000) * 100, 100),
                color: 'text-orange-400',
                barColor: 'bg-orange-400'
            };
        case WidgetType.HUMIDITY:
            return {
                icon: 'water_drop',
                value: `${sensorData.humidity}%`,
                percent: sensorData.humidity,
                color: 'text-blue-400',
                barColor: 'bg-blue-400'
            };
        case WidgetType.MESSAGES:
            return {
                icon: 'chat',
                value: sensorData.notifications,
                percent: sensorData.notifications > 0 ? 100 : 0,
                color: 'text-green-400',
                barColor: 'bg-green-400'
            };
        case WidgetType.WEATHER:
            return {
                icon: 'cloud',
                value: `${sensorData.temperature}°`,
                percent: 0, 
                color: 'text-yellow-400',
                barColor: 'bg-yellow-400'
            };
        case WidgetType.DATE:
            return {
                icon: 'calendar_today',
                value: `${time.getDate()}/${time.getMonth() + 1}`,
                percent: (time.getDate() / 31) * 100,
                color: 'text-slate-300',
                barColor: 'bg-slate-500'
            };
        case WidgetType.STEP_CHART:
            return {
                icon: 'bar_chart',
                value: 'CHART',
                percent: 0,
                color: 'text-cyan-400',
                barColor: 'bg-cyan-400',
                isChart: true
            };
        default:
            return {
                icon: 'check_box_outline_blank',
                value: '--',
                percent: 0,
                color: 'text-slate-600',
                barColor: 'bg-slate-800'
            };
    }
  };

  // Generalized Widget Renderer
  const renderVisualWidget = (type: WidgetType, size: 'small' | 'medium') => {
     if (type === WidgetType.EMPTY) return <div className={`w-8 ${size === 'small' ? 'h-6' : 'h-8'}`} />;

     const data = getWidgetData(type);
     const isSmall = size === 'small';

     // Special case for Chart
     if (data.isChart) {
         return (
            <div className={`flex flex-col items-center justify-end ${isSmall ? 'h-6 w-8' : 'h-8 w-12'} group-hover:scale-110 transition-transform`}>
                <div className="flex items-center gap-1 mb-0.5">
                    <span className={`material-icons ${isSmall ? 'text-[8px]' : 'text-[10px]'} text-slate-500`}>{data.icon}</span>
                </div>
                <MiniStepChart data={sensorData.stepHistory || []} compact={isSmall} />
            </div>
         );
     }

     return (
         <div className={`flex flex-col items-center justify-end ${isSmall ? 'h-6' : 'h-8'} group-hover:scale-110 transition-transform cursor-pointer`}>
             <div className="flex items-center gap-1 mb-0.5">
                <span className={`material-icons ${isSmall ? 'text-[8px]' : 'text-[10px]'} ${data.color}`}>{data.icon}</span>
                <span className={`${isSmall ? 'text-[9px]' : 'text-[10px]'} font-bold leading-none font-mono tracking-tighter ${data.color}`}>{data.value}</span>
             </div>
             
             {/* Progress Bar */}
             <div className={`${isSmall ? 'w-6 h-[3px]' : 'w-10 h-[4px]'} bg-slate-800/80 rounded-sm overflow-hidden`}>
                 <div className={`h-full ${data.barColor} transition-all duration-1000`} style={{ width: `${data.percent}%` }} />
             </div>
         </div>
     )
  }

  // Helper to render large left wing widget
  const renderLeftWidgetContent = (type: WidgetType) => {
    switch(type) {
        case WidgetType.WEATHER:
            return {
                label: 'ENV.DATA',
                value: (
                    <div className="flex items-center gap-1 justify-end whitespace-nowrap overflow-hidden">
                        <span className="text-lg">{sensorData.weatherIcon}</span>
                        <span className={`text-[22px] leading-none font-bold ${accentColor} ${glowClass} font-[Rajdhani]`}>{sensorData.temperature}°</span>
                    </div>
                )
            };
        case WidgetType.STEPS:
            return {
                label: 'PEDOMETER',
                value: <div className={`text-[18px] leading-none font-bold ${isCritical ? 'text-red-500' : 'text-slate-200'} font-[Rajdhani] whitespace-nowrap`}>{sensorData.steps}</div>
            };
        case WidgetType.STEP_CHART:
             return {
                 label: 'ACTIVITY',
                 value: (
                     <div className="flex justify-end pt-1">
                         <div className="flex items-end h-5 w-12">
                            <MiniStepChart data={sensorData.stepHistory || []} compact={true} />
                         </div>
                     </div>
                 )
             };
        case WidgetType.HEART_RATE:
            return {
                label: 'BIO.READ',
                value: <div className={`text-[20px] leading-none font-bold ${isCritical ? 'text-red-500 animate-pulse' : 'text-red-400'} font-[Rajdhani] whitespace-nowrap`}>{sensorData.heartRate}<span className="text-[10px] ml-1 text-slate-500 font-mono align-middle">BPM</span></div>
            };
        case WidgetType.BATTERY:
            return {
                label: 'PWR.LVL',
                value: <div className={`text-[20px] leading-none font-bold ${sensorData.battery < 20 ? 'text-red-500' : 'text-cyan-300'} font-[Rajdhani] whitespace-nowrap`}>{sensorData.battery}<span className="text-[10px] ml-1 text-slate-500 font-mono align-middle">%</span></div>
            };
        case WidgetType.CALORIES:
            return {
                label: 'KCAL.BURN',
                value: <div className="text-[18px] leading-none font-bold text-orange-400 font-[Rajdhani] whitespace-nowrap">{sensorData.calories}</div>
            };
        case WidgetType.DATE:
             return {
                label: 'SYS.DATE',
                value: <div className="text-[18px] leading-none font-bold text-slate-200 font-[Rajdhani] whitespace-nowrap">{time.getDate()}/{time.getMonth() + 1}</div>
            };
        case WidgetType.HUMIDITY:
             return {
                label: 'HUMIDITY',
                value: <div className="text-[18px] leading-none font-bold text-blue-300 font-[Rajdhani] whitespace-nowrap">{sensorData.humidity}%</div>
             };
        case WidgetType.MESSAGES:
             return {
                label: 'NOTIFS',
                value: <div className="text-[18px] leading-none font-bold text-green-400 font-[Rajdhani] whitespace-nowrap">{sensorData.notifications}</div>
             };
        default:
            return { label: 'EMPTY', value: <span>--</span> };
    }
  };

  const leftTopContent = renderLeftWidgetContent(widgetConfig.leftWidgets[0]);
  const leftBtmContent = renderLeftWidgetContent(widgetConfig.leftWidgets[1]);

  return (
    <div className="relative w-[260px] h-[260px] rounded-full bg-black overflow-hidden border-4 border-slate-800 shadow-[0_0_50px_rgba(0,0,0,0.8)] select-none">
      {/* 1. Background System */}
      <HexGrid 
        className="opacity-40" 
        style={{ 
          maskImage: 'radial-gradient(circle at 80% 50%, black 30%, transparent 70%)',
          WebkitMaskImage: 'radial-gradient(circle at 80% 50%, black 30%, transparent 70%)'
        }} 
      />
      
      {/* Golden Spiral Overlay */}
      <svg viewBox="0 0 260 260" className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[150%] h-[150%] pointer-events-none z-0">
        <path
          d="M 120 130 
             A 10 10 0 0 1 130 140
             A 20 20 0 0 1 110 160
             A 30 30 0 0 1 80 130
             A 50 50 0 0 1 130 80
             A 80 80 0 0 1 210 160"
          fill="none"
          stroke="#22d3ee"
          strokeWidth="1.5"
          className="opacity-50 drop-shadow-[0_0_3px_cyan]"
        />
      </svg>
      
      {/* 2. Arcs Layer */}
      {/* Top: Daylight 24h Arc */}
      <DaylightArc currentTime={time} />
      
      {/* Bottom: Step Progress Arc */}
      <StepArc steps={sensorData.steps} />
      
      {/* Right Edge: Sedentary Sidebar (Curved SVG Overlay) */}
      <SedentarySidebar level={sedentaryLevel} />

      {/* 3. The Left Wing: Data Stack */}
      <div className="absolute left-[30px] top-[70px] w-[70px] h-[120px] flex flex-col justify-center border-r border-slate-700/50 pr-2 overflow-hidden z-30">
        <button 
          onClick={() => onWidgetCycle('left', 0)} 
          className="h-1/2 flex flex-col justify-end items-end mb-2 hover:bg-white/5 transition-colors rounded-l px-1 cursor-pointer group outline-none active:scale-95 w-full"
        >
           <span className={`text-[10px] font-mono tracking-widest text-slate-500 group-hover:text-cyan-300 truncate w-full text-right`}>{leftTopContent.label}</span>
           {leftTopContent.value}
        </button>
        
        <div className="w-full h-[1px] bg-slate-700/50" />

        <button 
          onClick={() => onWidgetCycle('left', 1)} 
          className="h-1/2 flex flex-col justify-start items-end mt-2 hover:bg-white/5 transition-colors rounded-l px-1 cursor-pointer group outline-none active:scale-95 w-full"
        >
            {leftBtmContent.value}
            <span className="text-[10px] font-mono tracking-widest text-slate-500 group-hover:text-cyan-300 truncate w-full text-right">{leftTopContent.label === 'PEDOMETER' && leftBtmContent.label === 'PEDOMETER' ? 'STEPS' : leftBtmContent.label}</span>
        </button>
      </div>

      {/* 4. The Spine: Central Icons */}
      <div className="absolute left-[108px] top-[92px] w-[14px] flex flex-col gap-[10px] items-center opacity-80 z-20">
        <Icons.Bluetooth active={sensorData.bluetoothConnected} />
        <Icons.Smartphone active={sensorData.notifications > 0} />
        <Icons.Alarm active={sensorData.alarmSet} />
        <Icons.Moon active={sensorData.doNotDisturb} />
        
        <div className="flex flex-col gap-1 mt-1">
            <button 
                onClick={onOpenChat} 
                className="text-cyan-500 hover:text-white transition-colors cursor-pointer group active:scale-90"
            >
                <Icons.SmartToy />
            </button>
        </div>
      </div>

      {/* 5. The Right Wing: Velocity Time */}
      <div className="absolute right-[45px] top-[50%] -translate-y-[50%] flex flex-col items-end pointer-events-none z-10">
        <div className={`text-[80px] leading-[0.8] font-black italic -skew-x-[10deg] ${accentColor} ${glowClass} font-[Rajdhani]`}>
          {h}
        </div>
        <div className={`text-[80px] leading-[0.8] font-black italic -skew-x-[10deg] text-white ${glowClass} font-[Rajdhani]`}>
          {m}
        </div>
      </div>

      {/* 6. Top Data Slots (Stacked into 2 Rows) */}
      
      {/* Upper Row (2 Small Widgets) - RAISED to 10px */}
      <div className="absolute top-[10px] left-1/2 -translate-x-1/2 flex justify-center gap-2 z-20 w-full pointer-events-none">
        {/* Indices 0 and 4 are the 'small' outer widgets */}
        {[0, 4].map((idx) => (
             <button 
                key={`top-upper-${idx}`} 
                onClick={() => onWidgetCycle('top', idx)} 
                className="active:scale-95 outline-none flex items-center justify-center min-w-[28px] pointer-events-auto"
                title="Click to change widget"
             >
                 {renderVisualWidget(widgetConfig.topWidgets[idx], 'small')}
             </button>
        ))}
      </div>

      {/* Main Row (3 Medium Widgets) - RAISED to 32px */}
      <div className="absolute top-[32px] left-1/2 -translate-x-1/2 flex justify-center gap-4 z-20 w-full pointer-events-none">
        {/* Indices 1, 2, 3 are the 'medium' central widgets */}
        {[1, 2, 3].map((idx) => (
             <button 
                key={`top-main-${idx}`} 
                onClick={() => onWidgetCycle('top', idx)} 
                className="active:scale-95 outline-none flex items-center justify-center min-w-[28px] pointer-events-auto"
                title="Click to change widget"
             >
                 {renderVisualWidget(widgetConfig.topWidgets[idx], 'medium')}
             </button>
        ))}
      </div>

      {/* 7. Bottom Data Slots */}
      <div className="absolute bottom-[40px] left-1/2 -translate-x-1/2 flex justify-center gap-6 z-20 items-end w-full">
         {widgetConfig.btmWidgets.map((w, i) => (
             <button 
                key={`btm-${i}`} 
                onClick={() => onWidgetCycle('btm', i)} 
                className="active:scale-95 outline-none"
                title="Click to change widget"
             >
                 {renderVisualWidget(w, 'medium')}
             </button>
         ))}
      </div>
      
      {/* Decorative Overlays */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none mix-blend-overlay opacity-30 bg-gradient-to-br from-white/10 to-black/50 z-10" />
      <div className="absolute inset-0 rounded-full border border-white/5 pointer-events-none z-30" />
    </div>
  );
};

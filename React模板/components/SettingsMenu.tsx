
import React from 'react';
import { WidgetType } from '../types';

interface SettingsMenuProps {
  isOpen: boolean;
  onClose: () => void;
  config: {
    topWidgets: WidgetType[];
    btmWidgets: WidgetType[];
    leftWidgets: WidgetType[];
  };
  onUpdate: (section: 'top' | 'btm' | 'left', index: number, type: WidgetType) => void;
}

const WIDGET_LABELS: Record<WidgetType, string> = {
  [WidgetType.EMPTY]: '空 (EMPTY)',
  [WidgetType.DATE]: '日期 (DATE)',
  [WidgetType.BATTERY]: '电量 (BATTERY)',
  [WidgetType.CALORIES]: '卡路里 (CALORIES)',
  [WidgetType.HEART_RATE]: '心率 (HEART RATE)',
  [WidgetType.MESSAGES]: '消息 (MESSAGES)',
  [WidgetType.HUMIDITY]: '湿度 (HUMIDITY)',
  [WidgetType.WEATHER]: '天气 (WEATHER)',
  [WidgetType.STEPS]: '步数 (STEPS)',
  [WidgetType.STEP_CHART]: '历史趋势 (HISTORY)',
};

export const SettingsMenu: React.FC<SettingsMenuProps> = ({ isOpen, onClose, config, onUpdate }) => {
  const widgetOptions = Object.values(WidgetType);

  const renderSelect = (section: 'top' | 'btm' | 'left', index: number, current: WidgetType, label: string) => (
    <div className="flex flex-col gap-1 mb-4">
      <label className="text-[12px] text-cyan-500 font-mono tracking-widest">{label}</label>
      <div className="relative">
        <select 
          value={current}
          onChange={(e) => onUpdate(section, index, e.target.value as WidgetType)}
          className="w-full bg-slate-900 border border-slate-700 text-slate-300 text-xs p-2 pr-8 rounded focus:border-cyan-500 outline-none font-mono appearance-none"
        >
          {widgetOptions.map(t => (
            <option key={t} value={t}>{WIDGET_LABELS[t]}</option>
          ))}
        </select>
        <div className="absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500">
          <span className="material-icons text-sm">expand_more</span>
        </div>
      </div>
    </div>
  );

  return (
    <div className={`absolute top-0 left-0 h-full w-full md:w-80 bg-[#050505]/95 backdrop-blur-xl border-r border-cyan-500/30 flex flex-col z-50 transition-transform duration-300 ease-out ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
       <div className="p-4 border-b border-cyan-500/30 flex justify-between items-center bg-cyan-950/20">
        <div className="flex items-center gap-2">
            <span className="material-icons text-cyan-400 text-sm">settings</span>
            <h2 className="text-cyan-400 font-bold tracking-widest text-sm font-[Rajdhani]">系统配置 (SYSTEM CONFIG)</h2>
        </div>
        <button onClick={onClose} className="text-cyan-600 hover:text-cyan-400 transition-colors">
          <span className="material-icons">close</span>
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-6 scrollbar-thin scrollbar-thumb-cyan-900 scrollbar-track-transparent">
        <div className="mb-8">
            <h3 className="text-white font-bold mb-4 text-xs tracking-widest border-b border-slate-800 pb-2 flex items-center gap-2">
                <span className="w-1 h-3 bg-cyan-500"></span>左侧数据区 (LEFT STACK)
            </h3>
            {renderSelect('left', 0, config.leftWidgets[0], '上方插槽 (Top Slot)')}
            {renderSelect('left', 1, config.leftWidgets[1], '下方插槽 (Bottom Slot)')}
        </div>

        <div className="mb-8">
            <h3 className="text-white font-bold mb-4 text-xs tracking-widest border-b border-slate-800 pb-2 flex items-center gap-2">
                <span className="w-1 h-3 bg-cyan-500"></span>顶部阵列 (TOP ARRAY)
            </h3>
            <div className="grid grid-cols-2 gap-2 mb-2">
                 {/* Row 1: Leftmost / Rightmost are now Upper Left / Upper Right */}
                 {renderSelect('top', 0, config.topWidgets[0], '上层-左 (Upper L)')}
                 {renderSelect('top', 4, config.topWidgets[4], '上层-右 (Upper R)')}
            </div>
            <div className="grid grid-cols-3 gap-2">
                {/* Row 2: Center 3 */}
                {renderSelect('top', 1, config.topWidgets[1], '主层-左 (Main L)')}
                {renderSelect('top', 2, config.topWidgets[2], '主层-中 (Main C)')}
                {renderSelect('top', 3, config.topWidgets[3], '主层-右 (Main R)')}
            </div>
        </div>

        <div className="mb-8">
            <h3 className="text-white font-bold mb-4 text-xs tracking-widest border-b border-slate-800 pb-2 flex items-center gap-2">
                <span className="w-1 h-3 bg-cyan-500"></span>底部阵列 (BOTTOM ARRAY)
            </h3>
            <div className="grid grid-cols-3 gap-2">
                {renderSelect('btm', 0, config.btmWidgets[0], '左 (L)')}
                {renderSelect('btm', 1, config.btmWidgets[1], '中 (C)')}
                {renderSelect('btm', 2, config.btmWidgets[2], '右 (R)')}
            </div>
        </div>
        
        <div className="p-3 bg-cyan-900/20 border border-cyan-500/20 rounded text-[10px] text-cyan-300 font-mono leading-relaxed">
            <p>注意：更改将立即反映在终端界面上。</p>
        </div>
      </div>
    </div>
  );
};
